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
import java.time.LocalDateTime;
import java.util.List;
import java.util.Map;

/**
 * 动态需求卡片（多规格）
 *
 * 关键设计：
 * - items 是多条规格的数组（钢贸 80%+ 询价为多规格）
 * - 单条规格只是 items.size() == 1 的退化情况
 * - 整单级字段（如 defaultDeliveryCity）可被行级覆盖
 *
 * @see docs/07-产品PRD-v2/02-采购会话核心模块.md  第 5.2 节
 */
@Data
@EqualsAndHashCode(callSuper = true)
@TableName(value = "demand_cards", autoResultMap = true)
public class DemandCard extends BaseEntity {

    @TableId(type = IdType.INPUT)
    private String cardId;

    private String sessionId;

    private Integer version;

    /** 多条规格明细（1-100 行） */
    @TableField(typeHandler = JacksonTypeHandler.class)
    private List<DemandItem> items;

    /** 整单全局默认值（每行可覆盖） */
    @TableField(typeHandler = JacksonTypeHandler.class)
    private Map<String, Object> defaults;

    /** 整单备注 */
    private String note;

    /**
     * 拆单策略：auto（智能拆单）/ bundle（整单打包）/ manual（手动拆）
     */
    private String splitStrategy;

    @TableField(typeHandler = JacksonTypeHandler.class)
    private Map<String, Object> deliveryInfo;

    @TableField(typeHandler = JacksonTypeHandler.class)
    private Map<String, Object> paymentTerms;

    @TableField(typeHandler = JacksonTypeHandler.class)
    private Map<String, Object> qualityRequirements;

    private String parentCardId;

    /** 本次变更引用（含行号） */
    @TableField(typeHandler = JacksonTypeHandler.class)
    private List<ChangeRef> changedFields;

    private String changedBy;

    private String changeReason;

    private String createdBy;

    /**
     * 单条规格明细
     */
    @Data
    public static class DemandItem {
        /** 行号（1-N），增删后已有行号不变 */
        private Integer itemNo;

        /** 客户端临时 ID（用于幂等） */
        private String clientTempId;

        // 商品规格
        private String productType;        // plate / rebar / hbeam / coil / pipe / stainless
        private String materialGrade;      // Q235B / HRB400E / 304 等
        private Map<String, Object> spec;  // {thickness, width, length, diameter, ...}
        private BigDecimal quantity;
        private String quantityUnit;       // ton / kg / piece / meter
        private String packaging;

        // 行级到货地（可覆盖 defaults.deliveryCity）
        private String deliveryCity;
        private String deliveryDistrict;
        private LocalDateTime deliveryDeadline;

        // 价格期望
        private BigDecimal targetPriceRangeMin;
        private BigDecimal targetPriceRangeMax;
        private String priceUnit;           // per_ton / per_piece

        // 质量
        private Boolean requireQualityCertificate;
        private String requireProcessing;   // 探伤 / 定尺 / ...

        // 行级备注
        private String note;

        // 运行时状态（非存储字段）
        @TableField(exist = false)
        private String status;  // pending / dispatching / quoted / locked / deal / no_supply

        @TableField(exist = false)
        private Integer matchedQuoteCount;
    }

    /**
     * 变更引用（行级或整单级）
     */
    @Data
    public static class ChangeRef {
        private Integer itemNo;  // null 表示整单变更
        private String field;    // 如 "quantity" / "deliveryCity" / "items[2].quantity"
        private Object oldValue;
        private Object newValue;
    }
}
