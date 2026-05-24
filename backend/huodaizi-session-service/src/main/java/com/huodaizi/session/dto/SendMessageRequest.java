package com.huodaizi.session.dto;

import jakarta.validation.constraints.NotBlank;
import lombok.Data;

import java.util.List;
import java.util.Map;

@Data
public class SendMessageRequest {

    @NotBlank
    private String type = "text";

    @NotBlank
    private String content;

    /** 附件 URL（语音/图片/文件） */
    private List<String> attachments;

    /** 引用消息 ID */
    private String quoteMessageId;

    /** 客户端临时 ID（用于幂等） */
    private String clientTempId;

    /** 元数据 */
    private Map<String, Object> metadata;
}
