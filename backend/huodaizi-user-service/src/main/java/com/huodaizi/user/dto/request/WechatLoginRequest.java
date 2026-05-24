package com.huodaizi.user.dto.request;

import jakarta.validation.constraints.NotBlank;
import lombok.Data;

import java.io.Serializable;

@Data
public class WechatLoginRequest implements Serializable {

    @NotBlank(message = "code 不能为空")
    private String code;

    private WechatUserInfo userInfo;

    @Data
    public static class WechatUserInfo {
        private String nickname;
        private String avatarUrl;
    }
}
