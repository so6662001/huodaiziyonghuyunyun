package com.huodaizi.session.controller;

import cn.dev33.satoken.annotation.SaCheckLogin;
import com.huodaizi.common.api.Result;
import com.huodaizi.common.util.SecurityUtils;
import com.huodaizi.session.dto.CreateSessionRequest;
import com.huodaizi.session.dto.SendMessageRequest;
import com.huodaizi.session.entity.PurchaseSession;
import com.huodaizi.session.service.PurchaseSessionService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import lombok.Data;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

@Tag(name = "Sessions", description = "采购会话")
@RestController
@RequestMapping("/api/v1/sessions")
@RequiredArgsConstructor
public class PurchaseSessionController {

    private final PurchaseSessionService sessionService;

    @Operation(summary = "创建采购会话")
    @SaCheckLogin
    @PostMapping
    public Result<PurchaseSession> create(@Valid @RequestBody CreateSessionRequest request) {
        String buyerId = SecurityUtils.currentUserId();
        return Result.success(sessionService.createSession(buyerId, request));
    }

    @Operation(summary = "获取会话详情（聚合视图）")
    @SaCheckLogin
    @GetMapping("/{sessionId}")
    public Result<Object> get(@PathVariable String sessionId) {
        return Result.success(sessionService.getSessionDetail(sessionId, SecurityUtils.currentUserId()));
    }

    @Operation(summary = "在会话中发送消息（AI 自动识变）")
    @SaCheckLogin
    @PostMapping("/{sessionId}/messages")
    public Result<Object> sendMessage(@PathVariable String sessionId,
                                      @Valid @RequestBody SendMessageRequest request) {
        return Result.success(sessionService.sendMessage(sessionId, SecurityUtils.currentUserId(), request));
    }

    @Operation(summary = "关闭会话")
    @SaCheckLogin
    @PostMapping("/{sessionId}/close")
    public Result<Void> close(@PathVariable String sessionId,
                              @RequestBody CloseSessionRequest request) {
        sessionService.closeSession(sessionId, SecurityUtils.currentUserId(), request.getReason());
        return Result.success();
    }

    @Data
    public static class CloseSessionRequest {
        private String reason;
    }
}
