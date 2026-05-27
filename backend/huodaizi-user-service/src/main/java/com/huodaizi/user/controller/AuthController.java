package com.huodaizi.user.controller;

import com.huodaizi.common.api.Result;
import com.huodaizi.user.dto.AuthResponse;
import com.huodaizi.user.dto.request.SmsLoginRequest;
import com.huodaizi.user.dto.request.SmsSendRequest;
import com.huodaizi.user.dto.request.WechatLoginRequest;
import com.huodaizi.user.service.AuthService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@Tag(name = "Auth", description = "鉴权与登录")
@RestController
@RequestMapping("/api/v1/auth")
@RequiredArgsConstructor
public class AuthController {

    private final AuthService authService;

    @Operation(summary = "微信小程序登录")
    @PostMapping("/wechat-login")
    public Result<AuthResponse> wechatLogin(@Valid @RequestBody WechatLoginRequest request) {
        return Result.success(authService.wechatLogin(request));
    }

    @Operation(summary = "发送短信验证码")
    @PostMapping("/sms-send")
    public Result<Void> sendSmsCode(@Valid @RequestBody SmsSendRequest request) {
        authService.sendSmsCode(request.getPhone(), request.getScenario());
        return Result.success();
    }

    @Operation(summary = "短信验证码登录")
    @PostMapping("/sms-login")
    public Result<AuthResponse> smsLogin(@Valid @RequestBody SmsLoginRequest request) {
        return Result.success(authService.smsLogin(request));
    }

    @Operation(summary = "登出")
    @PostMapping("/logout")
    public Result<Void> logout() {
        authService.logout();
        return Result.success();
    }
}
