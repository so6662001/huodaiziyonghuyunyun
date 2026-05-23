-- ============================================================
-- 货袋子平台初始数据
-- 包含：风控规则、品类字典、市场参考价示例
-- ============================================================

-- ============================================================
-- 风控规则初始数据（36 条核心规则节选）
-- ============================================================

INSERT INTO `risk_rules` (`rule_id`, `name`, `category`, `severity`, `enabled`, `conditions`, `disposition`, `version`) VALUES
('R001', '设备同源注册检测', 'register', 'L1', 1,
  JSON_OBJECT('time_window_hours', 24, 'max_accounts_per_device', 2),
  JSON_OBJECT('action', 'manual_review', 'blacklist_device_hours', 48), 1),

('R002', '营业执照唯一性', 'register', 'L2', 1,
  JSON_OBJECT('check_field', 'business_license_no', 'check_relations', JSON_ARRAY('legal_person', 'id_card_hash')),
  JSON_OBJECT('action', 'reject', 'message', '该企业已注册'), 1),

('R003', '注册资料完整度', 'register', 'L0', 1,
  JSON_OBJECT('min_score', 50),
  JSON_OBJECT('action', 'restrict_features', 'allowed', JSON_ARRAY('browse')), 1),

('R004', '批量注册识别', 'register', 'L1', 1,
  JSON_OBJECT('time_window_minutes', 10, 'max_accounts_per_ip_segment', 3, 'similarity_threshold', 0.5),
  JSON_OBJECT('action', 'manual_review'), 1),

('R005', '黑名单关联', 'register', 'L4', 1,
  JSON_OBJECT('check_against', 'blacklist_db'),
  JSON_OBJECT('action', 'reject'), 1),

('R006', '自邀自闭环检测', 'invitation', 'L2', 1,
  JSON_OBJECT('check_relations', JSON_ARRAY('legal_person', 'id_card_hash', 'bank_account', 'address_building')),
  JSON_OBJECT('action', 'invalidate_invitation', 'freeze_rewards', true), 1),

('R007', '设备同源邀请', 'invitation', 'L2', 1,
  JSON_OBJECT('same_device_post_register_days', 7, 'activity_ratio_threshold', 0.5),
  JSON_OBJECT('action', 'invalidate_invitation'), 1),

('R008', '邀请关系链异常', 'invitation', 'L2', 1,
  JSON_OBJECT('max_circular_depth', 3, 'same_ip_segment_check', true),
  JSON_OBJECT('action', 'manual_review', 'freeze_chain', true), 1),

('R009', '被邀请人行为异常', 'invitation', 'L1', 1,
  JSON_OBJECT('days_after_register', 7, 'check_autonomous_actions', true),
  JSON_OBJECT('action', 'invalidate_activation'), 1),

('R010', '高速激活异常', 'invitation', 'L2', 1,
  JSON_OBJECT('register_to_deal_minutes', 60, 'same_inviter_deal', true),
  JSON_OBJECT('action', 'invalidate_full_chain'), 1),

('R013', '询价党识别', 'demand', 'L0', 1,
  JSON_OBJECT('time_window_days', 30, 'min_demands', 30, 'max_deals', 0, 'max_contact_ratio', 0.3),
  JSON_OBJECT('action', 'tag_inquirer', 'pool_downgrade', 'pilot'), 1),

('R014', '探价行为识别', 'demand', 'L1', 1,
  JSON_OBJECT('time_window_hours', 24, 'same_demand_count', 5, 'zero_contact', true),
  JSON_OBJECT('action', 'suspend_demand_publish_hours', 24), 1),

('R015', '竞品探价识别', 'demand', 'L0', 1,
  JSON_OBJECT('industry_keywords', JSON_ARRAY('钢贸', '钢材', '贸易'), 'never_purchased', true, 'high_frequency', true),
  JSON_OBJECT('action', 'manual_review'), 1),

('R016', '异常字段填写', 'demand', 'L0', 1,
  JSON_OBJECT('rules', JSON_ARRAY('quantity_payment_mismatch', 'price_deviation_20pct', 'sensitive_keywords')),
  JSON_OBJECT('action', 'tag_and_downweight'), 1),

('R018', '需求重复推送防控', 'demand', 'L0', 1,
  JSON_OBJECT('time_window_hours', 72, 'similarity_threshold', 0.95),
  JSON_OBJECT('action', 'merge_with_existing'), 1),

('R019', '异常报价检测', 'quote', 'L1', 1,
  JSON_OBJECT('deviation_threshold_pct', 15, 'consecutive_violations', 3),
  JSON_OBJECT('action', 'restrict_pool_hours', 72), 1),

('R020', '同质化报价检测', 'quote', 'L0', 1,
  JSON_OBJECT('min_quotes', 3, 'max_variance', 0.005),
  JSON_OBJECT('action', 'manual_review', 'watchlist', 'collusion'), 1),

('R021', '机器报价识别', 'quote', 'L1', 1,
  JSON_OBJECT('avg_response_sec', 5, 'integer_price_pattern', true, 'concurrent_quotes_per_hour', 20),
  JSON_OBJECT('action', 'captcha_challenge'), 1),

('R022', '报价撤回滥用', 'quote', 'L1', 1,
  JSON_OBJECT('daily_withdraw_count', 5, 'withdraw_rate_pct', 30),
  JSON_OBJECT('action', 'reduce_daily_quota', 'multiplier', 0.5), 1),

('R023', '恶意低价扰乱', 'quote', 'L2', 1,
  JSON_OBJECT('below_market_pct', 15, 'no_inventory', true, 'no_recent_deals_days', 90),
  JSON_OBJECT('action', 'warn_first', 'suspend_after_3', 30), 1),

('R024', '跳单识别', 'contact', 'L0', 1,
  JSON_OBJECT('signals', JSON_ARRAY('contact_info_in_im', 'stop_platform_im', 'demand_not_closed')),
  JSON_OBJECT('action', 'promote_platform_services'), 1),

('R025', '骚扰识别', 'contact', 'L1', 1,
  JSON_OBJECT('contacts_per_day', 10, 'negative_reply_ratio', 0.5),
  JSON_OBJECT('action', 'restrict_contact_target', 'tag_count', 5), 1),

('R026', '黑话灰产识别', 'contact', 'L3', 1,
  JSON_OBJECT('keywords', JSON_ARRAY('票货分离', '虚开', '代缴'), 'instant_block', true),
  JSON_OBJECT('action', 'block_message_and_review'), 1),

('R028', '虚假成交检测', 'deal', 'L2', 1,
  JSON_OBJECT('min_im_rounds', 5, 'check_relations', true),
  JSON_OBJECT('action', 'reject_unless_evidence'), 1),

('R029', '成交金额异常', 'deal', 'L0', 1,
  JSON_OBJECT('amount_ratio_high', 2.0, 'amount_ratio_low', 0.5),
  JSON_OBJECT('action', 'manual_review'), 1),

('R030', '单方面成交回填', 'deal', 'L0', 1,
  JSON_OBJECT('confirm_window_hours', 72),
  JSON_OBJECT('action', 'auto_expire'), 1),

('R032', '自买自卖刷线索', 'traffic_fee', 'L2', 1,
  JSON_OBJECT('check_relations', JSON_ARRAY('device', 'business_license', 'fund_chain')),
  JSON_OBJECT('action', 'no_charge_and_freeze'), 1),

('R033', '申诉滥用', 'traffic_fee', 'L1', 1,
  JSON_OBJECT('appeal_rate_pct', 25, 'success_rate_pct', 20, 'monthly_threshold_months', 3),
  JSON_OBJECT('action', 'restrict_appeals'), 1),

('R034', '线索质量异常', 'traffic_fee', 'L0', 1,
  JSON_OBJECT('contact_success_rate_pct', 30, 'consecutive_days', 7),
  JSON_OBJECT('action', 'pause_cpl_billing'), 1),

('R036', '扣费幂等', 'traffic_fee', 'L0', 1,
  JSON_OBJECT('idempotent_required', true),
  JSON_OBJECT('action', 'duplicate_prevention'), 1);

-- ============================================================
-- 品类字典（示意：实际钢贸品类约 100+）
-- 注意：此处用于演示，实际可用单独的品类表
-- ============================================================

-- 通过 JSON 配置初始化常用品类（示例数据）
-- 实际项目中应该单独建品类表 categories

-- ============================================================
-- 市场参考价示例（M5 风控用）
-- ============================================================

INSERT INTO `market_references`
  (`reference_id`, `product_category`, `material_grade`, `spec_pattern`, `region`,
   `median_price`, `p25`, `p75`, `sample_count`, `timeframe_days`, `computed_at`)
VALUES
('mr_001', '热轧卷板', 'Q235B', '5.5×1500×C', '唐山', 4280.00, 4250.00, 4320.00, 156, 7, NOW()),
('mr_002', '热轧卷板', 'Q235B', '5.5×1500×C', '天津', 4300.00, 4270.00, 4340.00, 142, 7, NOW()),
('mr_003', '热轧卷板', 'Q355B', '10×2000×6000', '唐山', 4380.00, 4350.00, 4420.00, 89, 7, NOW()),
('mr_004', '螺纹钢', 'HRB400', 'Φ18', '唐山', 3920.00, 3890.00, 3960.00, 234, 7, NOW()),
('mr_005', '螺纹钢', 'HRB400', 'Φ20', '唐山', 3900.00, 3870.00, 3940.00, 198, 7, NOW()),
('mr_006', '镀锌板', 'SGCC', '0.5mm', '聊城', 4720.00, 4680.00, 4780.00, 87, 7, NOW()),
('mr_007', 'H 型钢', 'Q345B', 'HM350×175', '唐山', 4520.00, 4480.00, 4570.00, 64, 7, NOW()),
('mr_008', '角钢', 'Q235B', 'L100×100×8', '聊城', 4180.00, 4150.00, 4220.00, 76, 7, NOW()),
('mr_009', '无缝钢管', '20#', 'φ60×3', '聊城', 5680.00, 5620.00, 5750.00, 45, 7, NOW()),
('mr_010', '中厚板', 'Q235B', '20mm', '唐山', 4280.00, 4250.00, 4320.00, 112, 7, NOW());

-- ============================================================
-- 测试用户与企业（开发环境用）
-- ============================================================

-- 测试买家
INSERT INTO `users` (`user_id`, `phone`, `name`, `primary_role`, `current_view`, `status`) VALUES
('u_test_buyer_001', '13800000001', '测试买家张总', 'buyer', 'buyer', 'active'),
('u_test_buyer_002', '13800000002', '测试买家李总', 'buyer', 'buyer', 'active');

INSERT INTO `companies` (`company_id`, `business_license_no`, `name`, `city`, `industry`, `verified`, `verification_level`) VALUES
('c_test_001', '91120100000000001', '测试天津钢结构有限公司', '天津', '钢结构', 1, 'L2'),
('c_test_002', '91120100000000002', '测试唐山机械加工有限公司', '唐山', '机械加工', 1, 'L2');

INSERT INTO `user_company_mappings` (`user_id`, `company_id`, `role`) VALUES
('u_test_buyer_001', 'c_test_001', 'purchaser'),
('u_test_buyer_002', 'c_test_002', 'owner');

-- 测试卖家
INSERT INTO `users` (`user_id`, `phone`, `name`, `primary_role`, `current_view`, `status`) VALUES
('u_test_seller_001', '13900000001', '测试卖家王总', 'seller', 'seller', 'active'),
('u_test_seller_002', '13900000002', '测试卖家赵总', 'seller', 'seller', 'active');

INSERT INTO `companies` (`company_id`, `business_license_no`, `name`, `city`, `industry`, `verified`, `verification_level`) VALUES
('c_test_seller_001', '91130200000000001', '测试唐山华泰钢贸有限公司', '唐山', '钢贸', 1, 'L3'),
('c_test_seller_002', '91120100000000003', '测试天津兴隆钢铁有限公司', '天津', '钢贸', 1, 'L3');

INSERT INTO `user_company_mappings` (`user_id`, `company_id`, `role`) VALUES
('u_test_seller_001', 'c_test_seller_001', 'owner'),
('u_test_seller_002', 'c_test_seller_002', 'owner');

-- 信用分初始
INSERT INTO `credit_scores` (`user_id`, `role`, `current_score`, `level`, `base_score`) VALUES
('u_test_buyer_001', 'buyer', 80, 'premium', 60),
('u_test_buyer_002', 'buyer', 70, 'standard', 60),
('u_test_seller_001', 'seller', 95, 'S', 100),
('u_test_seller_002', 'seller', 85, 'A', 100);

-- 卖家偏好
INSERT INTO `seller_preferences` (`seller_id`, `accept_pools`, `categories`, `regions`, `daily_max`, `min_order_amount`, `max_order_amount`, `min_profit_margin`) VALUES
('u_test_seller_001',
  JSON_ARRAY('standard', 'premium'),
  JSON_ARRAY('热轧卷板', '冷轧卷板'),
  JSON_ARRAY('唐山', '天津', '北京'),
  20, 10000, 10000000, 0.015),
('u_test_seller_002',
  JSON_ARRAY('pilot', 'standard', 'premium'),
  JSON_ARRAY('螺纹钢', 'H 型钢', '角钢'),
  JSON_ARRAY('天津', '北京', '廊坊'),
  30, 5000, 5000000, 0.012);

-- ============================================================
-- 结束
-- ============================================================
