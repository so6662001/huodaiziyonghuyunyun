package com.huodaizi.domain.enums;

import lombok.AllArgsConstructor;
import lombok.Getter;

@Getter
@AllArgsConstructor
public enum UserRole {

    BUYER("buyer", "买家"),
    SELLER("seller", "卖家"),
    BOTH("both", "双重身份"),
    ADMIN("admin", "管理员");

    private final String code;
    private final String label;
}
