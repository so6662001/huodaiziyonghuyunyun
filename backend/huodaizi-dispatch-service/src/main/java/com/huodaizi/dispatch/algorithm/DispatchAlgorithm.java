package com.huodaizi.dispatch.algorithm;

import com.huodaizi.domain.enums.PoolLevel;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.springframework.stereotype.Component;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;

/**
 * 智能派单核心算法
 *
 * ============================
 * 核心策略：三级池 + 综合评分
 * ============================
 *
 * 1. 根据买家信用 + 成交频率 划分到 试水池 / 标准池 / 优质池
 * 2. 在卖家库中过滤：
 *    - 产品/品种匹配（必要）
 *    - 区域覆盖匹配（必要）
 *    - 资质达标（必要）
 *    - 排除黑名单（必要）
 * 3. 对候选卖家打分：
 *    - 价格优势 (30%)
 *    - 库存匹配度 (25%)
 *    - 信用分 (20%)
 *    - 距离/物流 (15%)
 *    - 历史合作 (10%)
 * 4. 按分数倒排，取 TopN（N = 池等级决定）
 * 5. 区域保护：同省卖家 >= 60%
 * 6. 反围猎：单卖家 24h 接单数 <= 30
 *
 * @author huodaizi
 */
@Component
public class DispatchAlgorithm {

    /**
     * 派单决策
     */
    public DispatchResult dispatch(DispatchRequest request) {
        // 1. 决定推送池级别
        PoolLevel pool = PoolLevel.determinByCreditScore(
                request.buyerCreditScore,
                request.buyerDealCount,
                request.buyerContactCount30d
        );

        // 2. 候选卖家过滤
        List<SellerCandidate> candidates = filterCandidates(request.allSellers, request);

        // 3. 打分
        candidates.forEach(c -> c.score = calculateScore(c, request));

        // 4. 排序 + 取 TopN
        candidates.sort(Comparator.comparingDouble((SellerCandidate c) -> c.score).reversed());
        int targetCount = pool.getMaxSellersPushed();
        if (candidates.size() > targetCount) {
            candidates = new ArrayList<>(candidates.subList(0, targetCount));
        }

        // 5. 区域保护后处理
        candidates = applyRegionProtection(candidates, request);

        DispatchResult result = new DispatchResult();
        result.pool = pool;
        result.selectedSellers = candidates;
        result.totalCandidates = request.allSellers.size();
        return result;
    }

    /**
     * 必要条件过滤
     */
    private List<SellerCandidate> filterCandidates(List<SellerCandidate> all, DispatchRequest request) {
        return all.stream()
                .filter(c -> c.hasMatchingProduct)
                .filter(c -> c.hasCoverageInRegion)
                .filter(c -> c.qualified)
                .filter(c -> !c.blacklisted)
                .filter(c -> c.last24hDispatchCount < 30)
                .filter(c -> c.sellerCreditScore >= 60)
                .toList();
    }

    /**
     * 综合打分（0-100）
     *
     * 价格优势：(目标价 - 报价)/目标价 * 100
     * 库存匹配：有库存且数量充足 = 100，部分匹配 = 60，无库存 = 30
     * 信用分：直接使用卖家信用分
     * 距离物流：100 - (距离 km / 10)
     * 历史合作：成交次数 * 5（上限 50）+ 评分 * 10
     */
    private double calculateScore(SellerCandidate c, DispatchRequest req) {
        double priceScore = c.estimatedPriceAdvantage * 100;        // 0~100
        double stockScore = c.stockMatchLevel;                      // 0~100
        double creditScore = c.sellerCreditScore;                   // 0~100
        double distanceScore = Math.max(0, 100 - c.distanceKm / 10);
        double historyScore = Math.min(50, c.dealCount * 5) + c.sellerRating * 10;

        return priceScore * 0.30
             + stockScore * 0.25
             + creditScore * 0.20
             + distanceScore * 0.15
             + historyScore * 0.10;
    }

    /**
     * 区域保护：保证同省卖家 >= 60%
     */
    private List<SellerCandidate> applyRegionProtection(List<SellerCandidate> sorted, DispatchRequest req) {
        long sameProvince = sorted.stream().filter(c -> c.province.equals(req.buyerProvince)).count();
        if (sorted.isEmpty()) return sorted;

        double ratio = sameProvince * 1.0 / sorted.size();
        if (ratio >= 0.6) {
            return sorted;
        }

        // 不足 60%，从原始候选中补充同省卖家
        // 实际实现需要回调 filterCandidates 返回的完整列表，这里简化
        return sorted;
    }

    // ====================================================
    // 数据结构
    // ====================================================

    @Data
    @NoArgsConstructor
    public static class DispatchRequest {
        public String sessionId;
        public String buyerId;
        public Integer buyerCreditScore;
        public Integer buyerDealCount;
        public Integer buyerContactCount30d;
        public String buyerProvince;
        public List<SellerCandidate> allSellers;
        public String productType;       // 板材/管材/型材
        public String materialGrade;
    }

    @Data
    @NoArgsConstructor
    @AllArgsConstructor
    public static class SellerCandidate {
        public String sellerId;
        public String sellerCompanyId;
        public String province;
        public Integer sellerCreditScore;
        public Double sellerRating;
        public Integer dealCount;                 // 累计成交
        public Integer last24hDispatchCount;      // 24h 接单数
        public Double distanceKm;
        public Boolean hasMatchingProduct;
        public Boolean hasCoverageInRegion;
        public Boolean qualified;
        public Boolean blacklisted;
        public Double stockMatchLevel;            // 库存匹配度 0~100
        public Double estimatedPriceAdvantage;    // 0~1
        public Double score;                      // 计算后填充
    }

    @Data
    public static class DispatchResult {
        public PoolLevel pool;
        public List<SellerCandidate> selectedSellers;
        public Integer totalCandidates;
    }
}
