package com.huodaizi.domain.enums;

import lombok.AllArgsConstructor;
import lombok.Getter;

@Getter
@AllArgsConstructor
public enum QuoteStatus {

    ACTIVE("active", "有效"),
    UPDATED("updated", "已更新"),
    EXPIRED("expired", "已过期"),
    WITHDRAWN("withdrawn", "已撤回"),
    WON("won", "已成交"),
    LOST("lost", "未中标"),
    SUPERSEDED("superseded", "被替换");

    private final String code;
    private final String label;
}
