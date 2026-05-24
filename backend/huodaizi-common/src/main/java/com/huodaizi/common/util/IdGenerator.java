package com.huodaizi.common.util;

import cn.hutool.core.lang.Snowflake;
import cn.hutool.core.util.IdUtil;

import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.util.concurrent.ThreadLocalRandom;

/**
 * 业务 ID 生成器
 *
 * 业务 ID 格式：{前缀}_{日期}{随机}
 *  示例：
 *    u_20260523001234   用户
 *    c_20260523001234   公司
 *    ps_20260523001234  采购会话
 *    pl_20260523001234  采购清单
 *    q_20260523001234   报价
 *    d_20260523001234   派单
 */
public class IdGenerator {

    private static final Snowflake SNOWFLAKE = IdUtil.getSnowflake(1, 1);
    private static final DateTimeFormatter DATE_FORMAT = DateTimeFormatter.ofPattern("yyMMdd");

    /**
     * 生成基于雪花算法的 long ID
     */
    public static long snowflake() {
        return SNOWFLAKE.nextId();
    }

    /**
     * 生成基于雪花算法的 String ID
     */
    public static String snowflakeStr() {
        return String.valueOf(SNOWFLAKE.nextId());
    }

    /**
     * 生成带业务前缀的 ID
     * @param prefix 前缀（如 "u", "ps", "q"）
     * @return 完整 ID（如 "u_240523123456"）
     */
    public static String prefixed(String prefix) {
        String date = LocalDate.now().format(DATE_FORMAT);
        int random = ThreadLocalRandom.current().nextInt(100000, 1000000);
        return prefix + "_" + date + random;
    }

    public static String userId() { return prefixed("u"); }
    public static String companyId() { return prefixed("c"); }
    public static String sessionId() { return prefixed("ps"); }
    public static String listId() { return prefixed("pl"); }
    public static String quoteId() { return prefixed("q"); }
    public static String dispatchId() { return prefixed("d"); }
    public static String cardId() { return prefixed("card"); }
    public static String requestId() { return "req_" + IdUtil.fastSimpleUUID(); }
}
