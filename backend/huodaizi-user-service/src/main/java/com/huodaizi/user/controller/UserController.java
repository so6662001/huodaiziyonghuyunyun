package com.huodaizi.user.controller;

import cn.dev33.satoken.annotation.SaCheckLogin;
import com.huodaizi.common.api.ErrorCode;
import com.huodaizi.common.api.Result;
import com.huodaizi.common.exception.BusinessException;
import com.huodaizi.common.util.SecurityUtils;
import com.huodaizi.user.dto.UserDTO;
import com.huodaizi.user.entity.User;
import com.huodaizi.user.mapper.UserConverter;
import com.huodaizi.user.mapper.UserMapper;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.Data;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

@Tag(name = "Users", description = "用户管理")
@RestController
@RequestMapping("/api/v1/users")
@RequiredArgsConstructor
public class UserController {

    private final UserMapper userMapper;
    private final UserConverter userConverter;

    @Operation(summary = "获取当前用户")
    @SaCheckLogin
    @GetMapping("/me")
    public Result<UserDTO> me() {
        String userId = SecurityUtils.currentUserId();
        User user = userMapper.selectById(userId);
        if (user == null) {
            throw new BusinessException(ErrorCode.USER_NOT_FOUND);
        }
        return Result.success(userConverter.toDTO(user));
    }

    @Operation(summary = "更新当前用户信息")
    @SaCheckLogin
    @PatchMapping("/me")
    public Result<UserDTO> updateMe(@RequestBody UpdateUserRequest request) {
        String userId = SecurityUtils.currentUserId();
        User user = userMapper.selectById(userId);
        if (user == null) {
            throw new BusinessException(ErrorCode.USER_NOT_FOUND);
        }
        if (request.getName() != null) user.setName(request.getName());
        if (request.getAvatar() != null) user.setAvatar(request.getAvatar());
        if (request.getCurrentView() != null) user.setCurrentView(request.getCurrentView());
        userMapper.updateById(user);
        return Result.success(userConverter.toDTO(user));
    }

    @Operation(summary = "切换买家/卖家视角")
    @SaCheckLogin
    @PostMapping("/me/switch-view")
    public Result<UserDTO> switchView(@RequestBody SwitchViewRequest request) {
        String userId = SecurityUtils.currentUserId();
        User user = userMapper.selectById(userId);
        if (user == null) throw new BusinessException(ErrorCode.USER_NOT_FOUND);

        if (!"buyer".equals(request.getTargetView()) && !"seller".equals(request.getTargetView())) {
            throw new BusinessException(ErrorCode.INVALID_PARAM, "targetView 必须是 buyer 或 seller");
        }
        user.setCurrentView(request.getTargetView());
        userMapper.updateById(user);
        return Result.success(userConverter.toDTO(user));
    }

    @Operation(summary = "根据 ID 查询用户（内部接口）")
    @GetMapping("/{id}")
    public Result<UserDTO> getUser(@PathVariable("id") String userId) {
        User user = userMapper.selectById(userId);
        if (user == null) throw new BusinessException(ErrorCode.USER_NOT_FOUND);
        return Result.success(userConverter.toDTO(user));
    }

    @Data
    public static class UpdateUserRequest {
        private String name;
        private String avatar;
        private String currentView;
    }

    @Data
    public static class SwitchViewRequest {
        private String targetView;
    }
}
