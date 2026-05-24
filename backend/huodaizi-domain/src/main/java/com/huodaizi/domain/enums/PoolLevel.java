package com.huodaizi.domain.enums;

import lombok.AllArgsConstructor;
import lombok.Getter;

/**
 * 买家匹配池级别（M5 智能匹配引擎核心枚举）
 */
@Getter
@AllArgsConstructor
public enum PoolLevel {

    PILOT("pilot", "试水池", 5, 3),
    STANDARD("standard", "标准池", 15, 12),
    PREMIUM("premium", "优质池", 20, 17);

    private final String code;
    private final String label;
    /** 最大推送卖家数 */
    private final Integer maxSellersPushed;
    /** 最小预期报价数 */
    private final Integer minExpectedQuotes;

    public static PoolLevel determinByCreditScore(Integer score, Integer dealCount, Integer contactCount30d) {
        if (score == null) score = 60;
        if (dealCount == null) dealCount = 0;
        if (contactCount30d == null) contactCount30d = 0;

        if (score >= 80 || (dealCount >= 2 && contactCount30d >= 3)) {
            return PREMIUM;
        }
        if (score < 60 || dealCount == 0) {
            return PILOT;
        }
        return STANDARD;
    }
}
