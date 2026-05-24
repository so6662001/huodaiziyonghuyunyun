package com.huodaizi.session.dto;

import com.huodaizi.domain.enums.PriorityLevel;
import com.huodaizi.session.entity.DemandCard;
import jakarta.validation.constraints.NotEmpty;
import lombok.Data;

import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.util.List;
import java.util.Map;

@Data
public class CreateSessionRequest {

    @NotEmpty(message = "需求明细不能为空")
    private List<DemandCard.DemandItem> items;

    private Map<String, Object> deliveryInfo;

    private Map<String, Object> paymentTerms;

    private PriorityLevel priority = PriorityLevel.STANDARD;

    private BigDecimal bountyAmount;

    private LocalDateTime deliveryDeadline;

    /** 来源：app / wechat_chat / list_upload */
    private String source = "app";
}
