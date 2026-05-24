package com.huodaizi.session.entity;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import com.baomidou.mybatisplus.extension.handlers.JacksonTypeHandler;
import com.huodaizi.domain.entity.BaseEntity;
import lombok.Data;
import lombok.EqualsAndHashCode;

import java.math.BigDecimal;
import java.util.List;
import java.util.Map;

@Data
@EqualsAndHashCode(callSuper = true)
@TableName(value = "demand_cards", autoResultMap = true)
public class DemandCard extends BaseEntity {

    @TableId(type = IdType.INPUT)
    private String cardId;

    private String sessionId;

    private Integer version;

    @TableField(typeHandler = JacksonTypeHandler.class)
    private List<DemandItem> items;

    @TableField(typeHandler = JacksonTypeHandler.class)
    private Map<String, Object> deliveryInfo;

    @TableField(typeHandler = JacksonTypeHandler.class)
    private Map<String, Object> paymentTerms;

    @TableField(typeHandler = JacksonTypeHandler.class)
    private Map<String, Object> qualityRequirements;

    private String parentCardId;

    @TableField(typeHandler = JacksonTypeHandler.class)
    private List<String> changeReason;

    private String createdBy;

    @Data
    public static class DemandItem {
        private String productType;
        private String materialGrade;
        private Map<String, Object> spec;
        private BigDecimal quantity;
        private String quantityUnit;
        private String packaging;
        private BigDecimal targetPriceRangeMin;
        private BigDecimal targetPriceRangeMax;
        private String priceUnit;
    }
}
