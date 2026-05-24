package com.huodaizi.user.service.impl;

import cn.dev33.satoken.stp.SaTokenInfo;
import cn.dev33.satoken.stp.StpUtil;
import cn.hutool.core.util.RandomUtil;
import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.huodaizi.common.api.ErrorCode;
import com.huodaizi.common.exception.BusinessException;
import com.huodaizi.common.util.IdGenerator;
import com.huodaizi.domain.enums.UserRole;
import com.huodaizi.user.dto.AuthResponse;
import com.huodaizi.user.dto.request.SmsLoginRequest;
import com.huodaizi.user.dto.request.WechatLoginRequest;
import com.huodaizi.user.entity.User;
import com.huodaizi.user.mapper.UserConverter;
import com.huodaizi.user.mapper.UserMapper;
import com.huodaizi.user.service.AuthService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.stereotype.Service;

import java.time.Duration;
import java.time.LocalDateTime;

@Slf4j
@Service
@RequiredArgsConstructor
public class AuthServiceImpl implements AuthService {

    private final UserMapper userMapper;
    private final UserConverter userConverter;
    private final StringRedisTemplate redisTemplate;

    private static final String SMS_KEY_PREFIX = "sms:code:";
    private static final String SMS_RATE_LIMIT_PREFIX = "sms:limit:";

    @Override
    public AuthResponse wechatLogin(WechatLoginRequest request) {
        // TODO: 调用微信 API 获取 openid / unionid
        // 此处简化为 mock
        String openId = "mock_open_" + request.getCode();
        String unionId = "mock_union_" + request.getCode();

        // 查询用户
        User user = userMapper.selectOne(
                new LambdaQueryWrapper<User>().eq(User::getWechatUnionId, unionId)
        );

        if (user == null) {
            // 自动注册
            user = new User();
            user.setUserId(IdGenerator.userId());
            user.setWechatOpenId(openId);
            user.setWechatUnionId(unionId);
            user.setName(request.getUserInfo() != null ? request.getUserInfo().getNickname() : "微信用户");
            user.setAvatar(request.getUserInfo() != null ? request.getUserInfo().getAvatarUrl() : null);
            user.setPrimaryRole(UserRole.BOTH);
            user.setCurrentView("buyer");
            user.setStatus("active");
            user.setLastActiveAt(LocalDateTime.now());
            userMapper.insert(user);
            log.info("微信新用户注册: userId={}", user.getUserId());
        } else {
            user.setLastActiveAt(LocalDateTime.now());
            userMapper.updateById(user);
        }

        return buildAuthResponse(user);
    }

    @Override
    public void sendSmsCode(String phone, String scenario) {
        // 频率限制：60 秒内只能发一次
        String rateKey = SMS_RATE_LIMIT_PREFIX + phone;
        Boolean set = redisTemplate.opsForValue().setIfAbsent(rateKey, "1", Duration.ofSeconds(60));
        if (Boolean.FALSE.equals(set)) {
            throw new BusinessException(ErrorCode.RATE_LIMITED, "60 秒内只能发送一次");
        }

        // 生成 6 位验证码
        String code = RandomUtil.randomNumbers(6);
        String codeKey = SMS_KEY_PREFIX + scenario + ":" + phone;
        redisTemplate.opsForValue().set(codeKey, code, Duration.ofMinutes(5));

        // TODO: 调用阿里云短信发送
        log.info("发送短信验证码: phone={}, code={}", phone, code);
    }

    @Override
    public AuthResponse smsLogin(SmsLoginRequest request) {
        String codeKey = SMS_KEY_PREFIX + "login:" + request.getPhone();
        String storedCode = redisTemplate.opsForValue().get(codeKey);

        if (storedCode == null || !storedCode.equals(request.getCode())) {
            throw new BusinessException(ErrorCode.SMS_CODE_INVALID);
        }
        redisTemplate.delete(codeKey);

        // 查询/创建用户
        User user = userMapper.selectOne(
                new LambdaQueryWrapper<User>().eq(User::getPhone, request.getPhone())
        );
        if (user == null) {
            user = new User();
            user.setUserId(IdGenerator.userId());
            user.setPhone(request.getPhone());
            user.setName("用户" + request.getPhone().substring(7));
            user.setPrimaryRole(UserRole.BOTH);
            user.setCurrentView("buyer");
            user.setStatus("active");
            user.setLastActiveAt(LocalDateTime.now());
            userMapper.insert(user);
            log.info("短信新用户注册: userId={}", user.getUserId());
        } else {
            user.setLastActiveAt(LocalDateTime.now());
            userMapper.updateById(user);
        }

        return buildAuthResponse(user);
    }

    @Override
    public AuthResponse refreshToken(String refreshToken) {
        // TODO: 验证 refresh token 并刷新
        throw new BusinessException(ErrorCode.UNAUTHORIZED, "暂未实现");
    }

    @Override
    public void logout() {
        StpUtil.logout();
    }

    private AuthResponse buildAuthResponse(User user) {
        StpUtil.login(user.getUserId());
        StpUtil.getSession().set("role", user.getPrimaryRole().getCode());

        SaTokenInfo tokenInfo = StpUtil.getTokenInfo();

        return AuthResponse.builder()
                .accessToken(tokenInfo.getTokenValue())
                .refreshToken(null) // 简化版无 refresh token
                .expiresIn(tokenInfo.getTokenTimeout())
                .user(userConverter.toDTO(user))
                .build();
    }
}
