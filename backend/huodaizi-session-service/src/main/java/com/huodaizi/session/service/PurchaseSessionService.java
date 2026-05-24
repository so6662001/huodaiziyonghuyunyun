package com.huodaizi.session.service;

import com.huodaizi.session.dto.CreateSessionRequest;
import com.huodaizi.session.dto.SendMessageRequest;
import com.huodaizi.session.entity.PurchaseSession;

public interface PurchaseSessionService {

    /**
     * 创建采购会话（同时创建初始需求卡片 v1）
     */
    PurchaseSession createSession(String buyerId, CreateSessionRequest request);

    /**
     * 在会话中发送消息（AI 自动识别意图，可能触发需求卡片变更）
     */
    Object sendMessage(String sessionId, String userId, SendMessageRequest request);

    /**
     * 关闭会话
     */
    void closeSession(String sessionId, String userId, String reason);

    /**
     * 获取会话聚合视图（含当前需求卡片 + 报价 + 时间线）
     */
    Object getSessionDetail(String sessionId, String userId);
}
