package com.huodaizi.common.api;

import lombok.AllArgsConstructor;
import lombok.Getter;

/**
 * 业务错误码
 * 规则：模块前缀（3 位）+ 4 位编号
 */
@Getter
@AllArgsConstructor
public enum ErrorCode {

    // 通用错误（10x）
    SUCCESS("0", "success"),
    SYSTEM_ERROR("1001", "系统异常"),
    INVALID_PARAM("1002", "参数错误"),
    UNAUTHORIZED("1003", "未授权"),
    FORBIDDEN("1004", "无权限"),
    NOT_FOUND("1005", "资源不存在"),
    RATE_LIMITED("1006", "请求过于频繁"),

    // 用户模块（10x）
    USER_NOT_FOUND("10101", "用户不存在"),
    USER_ALREADY_EXISTS("10102", "用户已存在"),
    PHONE_INVALID("10103", "手机号格式错误"),
    SMS_CODE_INVALID("10104", "验证码错误"),
    SMS_SEND_FAILED("10105", "短信发送失败"),

    // 企业模块
    COMPANY_NOT_FOUND("10201", "企业不存在"),
    COMPANY_ALREADY_EXISTS("10202", "该企业已注册"),
    BUSINESS_LICENSE_INVALID("10203", "营业执照无效"),
    OCR_FAILED("10204", "OCR 识别失败"),

    // 会话模块（11x）
    SESSION_NOT_FOUND("11001", "会话不存在"),
    SESSION_CLOSED("11002", "会话已关闭"),
    DEMAND_CARD_NOT_FOUND("11003", "需求卡片不存在"),
    CHANGE_LIMIT_EXCEEDED("11004", "变更次数超过上限"),

    // 报价模块（12x）
    QUOTE_NOT_FOUND("12001", "报价不存在"),
    QUOTE_EXPIRED("12002", "报价已过期"),
    NEGOTIATION_LIMIT_EXCEEDED("12003", "议价次数已达上限"),

    // 清单模块（13x）
    LIST_NOT_FOUND("13001", "清单不存在"),
    PARSING_FAILED("13002", "清单解析失败"),
    AI_SERVICE_ERROR("13003", "AI 服务异常"),

    // 派单模块（14x）
    DISPATCH_NO_CANDIDATES("14001", "无匹配卖家"),

    // 信用模块（15x）
    APPEAL_NOT_FOUND("15001", "申诉不存在"),

    // 商业化模块（16x）
    INSUFFICIENT_BALANCE("16001", "余额不足"),
    MEMBERSHIP_EXPIRED("16002", "会员已过期"),

    // 风控模块（17x）
    RISK_BLOCKED("17001", "命中风控规则"),
    DEVICE_BLACKLISTED("17002", "设备已被禁用");

    private final String code;
    private final String message;
}
