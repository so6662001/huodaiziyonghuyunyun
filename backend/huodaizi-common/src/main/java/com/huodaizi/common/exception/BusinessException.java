package com.huodaizi.common.exception;

import com.huodaizi.common.api.ErrorCode;
import lombok.Getter;

/**
 * 业务异常
 * 用于表示已知的业务错误，会被全局异常处理器捕获并转换为标准响应。
 */
@Getter
public class BusinessException extends RuntimeException {

    private final String code;
    private final String message;
    private Object details;

    public BusinessException(String code, String message) {
        super(message);
        this.code = code;
        this.message = message;
    }

    public BusinessException(ErrorCode errorCode) {
        this(errorCode.getCode(), errorCode.getMessage());
    }

    public BusinessException(ErrorCode errorCode, Object details) {
        this(errorCode.getCode(), errorCode.getMessage());
        this.details = details;
    }

    public BusinessException(ErrorCode errorCode, String customMessage) {
        super(customMessage);
        this.code = errorCode.getCode();
        this.message = customMessage;
    }
}
