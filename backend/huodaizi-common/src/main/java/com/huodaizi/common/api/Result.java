package com.huodaizi.common.api;

import com.fasterxml.jackson.annotation.JsonInclude;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.slf4j.MDC;

import java.io.Serializable;

/**
 * 统一响应包装
 *
 * @param <T> 数据类型
 * @author huodaizi
 */
@Data
@NoArgsConstructor
@JsonInclude(JsonInclude.Include.NON_NULL)
public class Result<T> implements Serializable {

    /** 业务码：0 = 成功 */
    private String code;

    /** 提示信息 */
    private String message;

    /** 业务数据 */
    private T data;

    /** 错误详情（仅失败时） */
    private Object details;

    /** 请求追踪 ID */
    private String requestId;

    /** 时间戳 */
    private Long timestamp;

    public static <T> Result<T> success() {
        return success(null, "success");
    }

    public static <T> Result<T> success(T data) {
        return success(data, "success");
    }

    public static <T> Result<T> success(T data, String message) {
        Result<T> result = new Result<>();
        result.setCode("0");
        result.setMessage(message);
        result.setData(data);
        result.setRequestId(MDC.get("requestId"));
        result.setTimestamp(System.currentTimeMillis());
        return result;
    }

    public static <T> Result<T> fail(String code, String message) {
        return fail(code, message, null);
    }

    public static <T> Result<T> fail(String code, String message, Object details) {
        Result<T> result = new Result<>();
        result.setCode(code);
        result.setMessage(message);
        result.setDetails(details);
        result.setRequestId(MDC.get("requestId"));
        result.setTimestamp(System.currentTimeMillis());
        return result;
    }

    public static <T> Result<T> fail(ErrorCode errorCode) {
        return fail(errorCode.getCode(), errorCode.getMessage());
    }

    public boolean isSuccess() {
        return "0".equals(this.code);
    }
}
