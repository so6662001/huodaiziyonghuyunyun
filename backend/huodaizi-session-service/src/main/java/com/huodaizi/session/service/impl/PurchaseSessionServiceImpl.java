package com.huodaizi.session.service.impl;

import cn.hutool.core.bean.BeanUtil;
import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.huodaizi.common.api.ErrorCode;
import com.huodaizi.common.exception.BusinessException;
import com.huodaizi.common.util.IdGenerator;
import com.huodaizi.domain.enums.SessionStatus;
import com.huodaizi.session.dto.CreateSessionRequest;
import com.huodaizi.session.dto.SendMessageRequest;
import com.huodaizi.session.entity.DemandCard;
import com.huodaizi.session.entity.PurchaseSession;
import com.huodaizi.session.mapper.DemandCardMapper;
import com.huodaizi.session.mapper.PurchaseSessionMapper;
import com.huodaizi.session.service.AIIntentService;
import com.huodaizi.session.service.PurchaseSessionService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * 采购会话核心服务实现
 *
 * 设计要点：
 *  - 创建会话时同步创建初始 DemandCard v1
 *  - 发消息时调用 AIIntentService 识别需求变更
 *  - 检测到变更则生成新的 DemandCard v2/v3...（parent_card_id 链式追溯）
 *  - 变更超过 5 次拒绝（避免恶意 SPAM 卖家）
 *  - 调用 dispatch-service 触发派单（通过 Feign）
 */
@Slf4j
@Service
@RequiredArgsConstructor
public class PurchaseSessionServiceImpl implements PurchaseSessionService {

    private final PurchaseSessionMapper sessionMapper;
    private final DemandCardMapper cardMapper;
    private final AIIntentService aiIntentService;
    // private final DispatchClient dispatchClient;   // Feign 调用派单服务

    private static final int MAX_CHANGE_COUNT = 5;

    @Override
    @Transactional(rollbackFor = Exception.class)
    public PurchaseSession createSession(String buyerId, CreateSessionRequest request) {
        // 1. 创建会话
        PurchaseSession session = new PurchaseSession();
        session.setSessionId(IdGenerator.sessionId());
        session.setBuyerId(buyerId);
        session.setStatus(SessionStatus.ACTIVE);
        session.setPriority(request.getPriority());
        session.setBountyAmount(request.getBountyAmount());
        session.setDeliveryDeadline(request.getDeliveryDeadline());
        session.setSessionExpireAt(LocalDateTime.now().plusDays(7));
        session.setChangeCount(0);
        session.setQuoteCount(0);
        sessionMapper.insert(session);

        // 2. 创建初始需求卡片 v1
        DemandCard card = new DemandCard();
        card.setCardId(IdGenerator.cardId());
        card.setSessionId(session.getSessionId());
        card.setVersion(1);
        card.setItems(request.getItems());
        card.setDeliveryInfo(request.getDeliveryInfo());
        card.setPaymentTerms(request.getPaymentTerms());
        card.setCreatedBy(buyerId);
        cardMapper.insert(card);

        // 3. 更新会话的 currentCardId
        session.setCurrentCardId(card.getCardId());
        sessionMapper.updateById(session);

        // 4. 异步触发派单（通过 MQ 或 Feign）
        // dispatchClient.dispatchSession(session.getSessionId());
        log.info("会话创建成功: sessionId={}, buyer={}, items={}",
                session.getSessionId(), buyerId, request.getItems().size());

        return session;
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public Object sendMessage(String sessionId, String userId, SendMessageRequest request) {
        PurchaseSession session = sessionMapper.selectById(sessionId);
        if (session == null) {
            throw new BusinessException(ErrorCode.SESSION_NOT_FOUND);
        }
        if (session.getStatus() == SessionStatus.CLOSED || session.getStatus() == SessionStatus.CANCELLED) {
            throw new BusinessException(ErrorCode.SESSION_CLOSED);
        }

        Map<String, Object> result = new HashMap<>();
        result.put("messageId", IdGenerator.snowflakeStr());
        result.put("timestamp", LocalDateTime.now());

        // AI 意图识别（仅对文字消息）
        if ("text".equals(request.getType())) {
            DemandCard currentCard = cardMapper.selectById(session.getCurrentCardId());
            AIIntentService.IntentDetectionResult intent =
                    aiIntentService.detectIntent(request.getContent(), currentCard);

            if (!"none".equals(intent.intent) && intent.confidence >= 0.7) {
                if (session.getChangeCount() >= MAX_CHANGE_COUNT) {
                    log.warn("会话变更次数超限: sessionId={}", sessionId);
                    result.put("aiDetected", false);
                    result.put("warning", "变更次数已达上限，请直接创建新会话");
                    return result;
                }
                result.put("aiDetected", true);
                result.put("intent", intent);
                result.put("requireConfirmation", true);
            }
        }

        return result;
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public void closeSession(String sessionId, String userId, String reason) {
        PurchaseSession session = sessionMapper.selectById(sessionId);
        if (session == null) {
            throw new BusinessException(ErrorCode.SESSION_NOT_FOUND);
        }
        if (!session.getBuyerId().equals(userId)) {
            throw new BusinessException(ErrorCode.FORBIDDEN, "仅会话发起人可关闭");
        }
        session.setStatus(SessionStatus.CLOSED);
        session.setClosedAt(LocalDateTime.now());
        sessionMapper.updateById(session);
        log.info("会话关闭: sessionId={}, reason={}", sessionId, reason);
    }

    @Override
    public Object getSessionDetail(String sessionId, String userId) {
        PurchaseSession session = sessionMapper.selectById(sessionId);
        if (session == null) {
            throw new BusinessException(ErrorCode.SESSION_NOT_FOUND);
        }
        DemandCard currentCard = cardMapper.selectById(session.getCurrentCardId());
        List<DemandCard> history = cardMapper.selectList(
                new LambdaQueryWrapper<DemandCard>()
                        .eq(DemandCard::getSessionId, sessionId)
                        .orderByAsc(DemandCard::getVersion)
        );

        Map<String, Object> result = new HashMap<>();
        result.put("session", session);
        result.put("currentCard", currentCard);
        result.put("cardHistory", history);
        return result;
    }
}
