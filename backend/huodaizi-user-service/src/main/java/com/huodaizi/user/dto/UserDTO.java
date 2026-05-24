package com.huodaizi.user.dto;

import com.huodaizi.domain.enums.UserRole;
import lombok.Data;

import java.io.Serializable;
import java.time.LocalDateTime;

@Data
public class UserDTO implements Serializable {

    private String userId;
    private String phone;
    private String name;
    private String avatar;
    private UserRole primaryRole;
    private String currentView;
    private String status;
    private LocalDateTime createdAt;
    private LocalDateTime lastActiveAt;
}
