package com.huodaizi.session.service.impl;

import com.huodaizi.session.entity.DemandCard;
import com.huodaizi.session.service.AIIntentService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * AI 意图识别实现
 *
 * v1 实现：基于规则 + 关键词匹配（保证可运行）
 * v2 实现：接入 LLM（通义千问/GPT），调用 ai-service
 *
 * 识别能力：
 *   1. 数量变更：「再加 5 吨」「降到 80 吨」
 *   2. 交期变更：「明天就要」「下周二前」
 *   3. 价格协商：「3950 能下吗」「降 50 行不」
 *   4. 规格变更：「改成 Q355B」「16mm 换成 14mm」
 *   5. 地址变更：「送到唐山仓库」
 */
@Slf4j
@Service
public class AIIntentServiceImpl implements AIIntentService {

    // 数量变更：「再加 X 吨」「降到 X 吨」
    private static final Pattern QUANTITY_PATTERN = Pattern.compile(
            "(再加|新增|增加|降到|减到|改成|变成)(\\d+(?:\\.\\d+)?)(吨|t|公斤|kg|根|件)"
    );

    // 交期变更：「明天前」「下周二」「3 天内」
    private static final Pattern DELIVERY_PATTERN = Pattern.compile(
            "(明天|后天|今天|本周|下周|大后天|\\d+月\\d+日|\\d+天内|\\d+小时内)"
    );

    // 价格协商：「X 块」「X 元」
    private static final Pattern PRICE_PATTERN = Pattern.compile(
            "(\\d{4})\\s*(块|元|元/吨)?(能下|下吗|可以|行不|行)"
    );

    @Override
    public IntentDetectionResult detectIntent(String message, DemandCard currentCard) {
        if (message == null || message.isBlank()) {
            return IntentDetectionResult.none();
        }

        IntentDetectionResult result = new IntentDetectionResult();
        result.changes = new ArrayList<>();

        // 数量变更检测
        Matcher quantityMatcher = QUANTITY_PATTERN.matcher(message);
        if (quantityMatcher.find()) {
            String op = quantityMatcher.group(1);
            double value = Double.parseDouble(quantityMatcher.group(2));
            String unit = quantityMatcher.group(3);

            DemandCardChange change = new DemandCardChange();
            change.field = "items[0].quantity";
            // 简化：取第一行
            if (currentCard != null && currentCard.getItems() != null && !currentCard.getItems().isEmpty()) {
                change.oldValue = currentCard.getItems().get(0).getQuantity();
            }
            if (op.matches("再加|新增|增加")) {
                change.newValue = "+" + value + unit;
                result.intent = "quantity_add";
            } else {
                change.newValue = value + unit;
                result.intent = "quantity_change";
            }
            result.changes.add(change);
            result.confidence = 0.85;
            result.summary = "买家要求修改采购数量";
            log.info("识别到数量变更意图: {}", change.newValue);
            return result;
        }

        // 交期变更检测
        Matcher deliveryMatcher = DELIVERY_PATTERN.matcher(message);
        if (deliveryMatcher.find() && (message.contains("要") || message.contains("交") || message.contains("前"))) {
            DemandCardChange change = new DemandCardChange();
            change.field = "deliveryDeadline";
            change.newValue = deliveryMatcher.group(1);
            result.intent = "delivery_change";
            result.confidence = 0.80;
            result.changes.add(change);
            result.summary = "买家要求调整交期";
            log.info("识别到交期变更意图: {}", change.newValue);
            return result;
        }

        // 价格协商检测
        Matcher priceMatcher = PRICE_PATTERN.matcher(message);
        if (priceMatcher.find()) {
            DemandCardChange change = new DemandCardChange();
            change.field = "items[0].targetPrice";
            change.newValue = Double.parseDouble(priceMatcher.group(1));
            result.intent = "price_negotiate";
            result.confidence = 0.75;
            result.changes.add(change);
            result.summary = "买家发起价格协商";
            log.info("识别到价格协商意图: {}", change.newValue);
            return result;
        }

        return IntentDetectionResult.none();
    }
}
