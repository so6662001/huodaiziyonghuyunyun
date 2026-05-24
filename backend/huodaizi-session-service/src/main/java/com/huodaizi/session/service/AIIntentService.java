package com.huodaizi.session.service;

import com.huodaizi.session.entity.DemandCard;

import java.util.List;

/**
 * AI 意图识别服务（核心：从用户消息中检测需求变更）
 *
 * 这是采购会话模型的灵魂：
 *   用户在群里随口说"明天前要"，
 *   AI 识别为 delivery_deadline 变更，
 *   生成新需求卡片 v2，
 *   推送给已报价卖家发起补报。
 */
public interface AIIntentService {

    /**
     * 检测消息中的需求变更意图
     */
    IntentDetectionResult detectIntent(String message, DemandCard currentCard);

    /**
     * 检测结果
     */
    class IntentDetectionResult {
        public String intent;             // none / quantity_change / price_negotiate / delivery_change ...
        public Double confidence;          // 0~1
        public List<DemandCardChange> changes;
        public String summary;

        public static IntentDetectionResult none() {
            IntentDetectionResult r = new IntentDetectionResult();
            r.intent = "none";
            r.confidence = 0.0;
            return r;
        }
    }

    class DemandCardChange {
        public String field;
        public Object oldValue;
        public Object newValue;
    }
}
