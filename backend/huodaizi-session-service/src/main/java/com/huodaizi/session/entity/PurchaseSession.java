package com.huodaizi.session.entity;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import com.huodaizi.domain.entity.BaseEntity;
import com.huodaizi.domain.enums.PoolLevel;
import com.huodaizi.domain.enums.PriorityLevel;
import com.huodaizi.domain.enums.SessionStatus;
import lombok.Data;
import lombok.EqualsAndHashCode;

import java.math.BigDecimal;
import java.time.LocalDateTime;

@Data
@EqualsAndHashCode(callSuper = true)
@TableName("purchase_sessions")
public class PurchaseSession extends BaseEntity {

    @TableId(type = IdType.INPUT)
    private String sessionId;

    private String buyerId;

    private String buyerCompanyId;

    private String currentCardId;

    private SessionStatus status;

    private PriorityLevel priority;

    private BigDecimal bountyAmount;

    private PoolLevel matchPoolLevel;

    private LocalDateTime deliveryDeadline;

    private LocalDateTime sessionExpireAt;

    private Integer changeCount;

    private Integer quoteCount;

    private LocalDateTime closedAt;
}
