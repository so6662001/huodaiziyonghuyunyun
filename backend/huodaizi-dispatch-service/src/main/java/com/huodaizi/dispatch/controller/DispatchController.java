package com.huodaizi.dispatch.controller;

import com.huodaizi.common.api.Result;
import com.huodaizi.dispatch.algorithm.DispatchAlgorithm;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/v1/dispatch")
@RequiredArgsConstructor
public class DispatchController {

    private final DispatchAlgorithm dispatchAlgorithm;

    /**
     * 派单接口（被 session-service 异步调用）
     */
    @PostMapping("/sessions/{sessionId}")
    public Result<DispatchAlgorithm.DispatchResult> dispatchSession(
            @PathVariable String sessionId,
            @RequestBody DispatchAlgorithm.DispatchRequest request) {
        request.sessionId = sessionId;
        return Result.success(dispatchAlgorithm.dispatch(request));
    }

    /**
     * 算法调试接口（仅 admin 可访问）
     */
    @PostMapping("/debug")
    public Result<DispatchAlgorithm.DispatchResult> debug(@RequestBody DispatchAlgorithm.DispatchRequest request) {
        return Result.success(dispatchAlgorithm.dispatch(request));
    }
}
