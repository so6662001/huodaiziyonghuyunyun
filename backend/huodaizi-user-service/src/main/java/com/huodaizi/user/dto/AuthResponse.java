package com.huodaizi.user.dto;

import lombok.Builder;
import lombok.Data;

import java.io.Serializable;

@Data
@Builder
public class AuthResponse implements Serializable {

    private String accessToken;
    private String refreshToken;
    private Long expiresIn;
    private UserDTO user;
}
