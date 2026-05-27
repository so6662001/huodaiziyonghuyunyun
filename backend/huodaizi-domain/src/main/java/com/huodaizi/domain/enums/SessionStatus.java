package com.huodaizi.domain.enums;

import lombok.AllArgsConstructor;
import lombok.Getter;

@Getter
@AllArgsConstructor
public enum SessionStatus {

    ACTIVE("active", "进行中"),
    MATCHING("matching", "匹配中"),
    QUOTING("quoting", "报价中"),
    NEGOTIATING("negotiating", "议价中"),
    DEAL("deal", "已成交"),
    EXPIRED("expired", "已过期"),
    CLOSED("closed", "已关闭"),
    CANCELLED("cancelled", "已取消");

    private final String code;
    private final String label;
}
