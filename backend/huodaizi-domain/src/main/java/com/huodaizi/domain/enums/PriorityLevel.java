package com.huodaizi.domain.enums;

import lombok.AllArgsConstructor;
import lombok.Getter;

@Getter
@AllArgsConstructor
public enum PriorityLevel {

    STANDARD("standard", "标准"),
    URGENT("urgent", "加急"),
    BOUNTY("bounty", "悬赏");

    private final String code;
    private final String label;
}
