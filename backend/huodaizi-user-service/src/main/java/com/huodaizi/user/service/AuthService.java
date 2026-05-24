package com.huodaizi.user.service;

import com.huodaizi.user.dto.AuthResponse;
import com.huodaizi.user.dto.request.SmsLoginRequest;
import com.huodaizi.user.dto.request.WechatLoginRequest;

public interface AuthService {

    /** 微信小程序登录 */
    AuthResponse wechatLogin(WechatLoginRequest request);

    /** 发送短信验证码 */
    void sendSmsCode(String phone, String scenario);

    /** 短信验证码登录 */
    AuthResponse smsLogin(SmsLoginRequest request);

    /** 刷新 token */
    AuthResponse refreshToken(String refreshToken);

    /** 登出 */
    void logout();
}
