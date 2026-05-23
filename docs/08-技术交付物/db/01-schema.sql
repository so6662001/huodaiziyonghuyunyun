-- ============================================================
-- 货袋子平台数据库 DDL（MySQL 8.0+）
-- 版本: v2.0.0
-- 字符集: utf8mb4_0900_ai_ci
-- 备注: 包含 33 张核心表，覆盖 PRD v2 全部模块
-- ============================================================

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ============================================================
-- M1: 用户与认证模块
-- ============================================================

DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `user_id` VARCHAR(32) NOT NULL COMMENT '用户ID (u_xxxxxx)',
  `phone` VARCHAR(20) NOT NULL COMMENT '手机号',
  `wechat_open_id` VARCHAR(128) DEFAULT NULL COMMENT '微信小程序 openid',
  `wechat_union_id` VARCHAR(128) DEFAULT NULL COMMENT '微信 unionid',
  `name` VARCHAR(64) DEFAULT NULL COMMENT '姓名',
  `avatar` VARCHAR(512) DEFAULT NULL COMMENT '头像 URL',
  `id_card_hash` CHAR(64) DEFAULT NULL COMMENT '身份证号 SHA256 hash',
  `primary_role` ENUM('buyer', 'seller', 'both') NOT NULL DEFAULT 'both' COMMENT '主身份',
  `current_view` ENUM('buyer', 'seller') NOT NULL DEFAULT 'buyer' COMMENT '当前视角',
  `status` ENUM('active', 'suspended', 'banned') NOT NULL DEFAULT 'active',
  `last_active_at` DATETIME DEFAULT NULL COMMENT '最后活跃时间',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `uk_phone` (`phone`),
  UNIQUE KEY `uk_union_id` (`wechat_union_id`),
  KEY `idx_open_id` (`wechat_open_id`),
  KEY `idx_last_active` (`last_active_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户表';

DROP TABLE IF EXISTS `companies`;
CREATE TABLE `companies` (
  `company_id` VARCHAR(32) NOT NULL COMMENT '企业ID (c_xxxxxx)',
  `business_license_no` VARCHAR(64) NOT NULL COMMENT '统一社会信用代码',
  `name` VARCHAR(128) NOT NULL COMMENT '企业名称',
  `legal_person` VARCHAR(64) DEFAULT NULL COMMENT '法人代表',
  `legal_person_id_hash` CHAR(64) DEFAULT NULL,
  `registered_address` VARCHAR(256) DEFAULT NULL,
  `operating_address` VARCHAR(256) DEFAULT NULL,
  `province` VARCHAR(32) DEFAULT NULL,
  `city` VARCHAR(32) DEFAULT NULL,
  `district` VARCHAR(32) DEFAULT NULL,
  `industry` VARCHAR(64) DEFAULT NULL COMMENT '所属行业',
  `scale` ENUM('small', 'medium', 'large') DEFAULT 'small',
  `ocr_data` JSON DEFAULT NULL COMMENT 'OCR 原始结果',
  `manual_filled` TINYINT(1) NOT NULL DEFAULT 0,
  `verified` TINYINT(1) NOT NULL DEFAULT 0,
  `verification_level` ENUM('L1', 'L2', 'L3', 'L4') NOT NULL DEFAULT 'L1',
  `verified_at` DATETIME DEFAULT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`company_id`),
  UNIQUE KEY `uk_business_license` (`business_license_no`),
  KEY `idx_city_industry` (`city`, `industry`),
  KEY `idx_verification` (`verified`, `verification_level`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='企业表';

DROP TABLE IF EXISTS `user_company_mappings`;
CREATE TABLE `user_company_mappings` (
  `mapping_id` BIGINT NOT NULL AUTO_INCREMENT,
  `user_id` VARCHAR(32) NOT NULL,
  `company_id` VARCHAR(32) NOT NULL,
  `role` ENUM('owner', 'admin', 'purchaser', 'salesperson') NOT NULL,
  `permissions` JSON DEFAULT NULL,
  `joined_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `removed_at` DATETIME DEFAULT NULL,
  PRIMARY KEY (`mapping_id`),
  UNIQUE KEY `uk_user_company_active` (`user_id`, `company_id`, `removed_at`),
  KEY `idx_company_role` (`company_id`, `role`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户-企业关系表';

DROP TABLE IF EXISTS `growth_accounts`;
CREATE TABLE `growth_accounts` (
  `user_id` VARCHAR(32) NOT NULL,
  `total_inquiries` INT NOT NULL DEFAULT 0,
  `total_deals` INT NOT NULL DEFAULT 0,
  `total_savings` DECIMAL(15, 2) NOT NULL DEFAULT 0,
  `current_level` ENUM('novice', 'experienced', 'expert', 'master') NOT NULL DEFAULT 'novice',
  `level_progress` DECIMAL(5, 2) NOT NULL DEFAULT 0,
  `badges` JSON DEFAULT NULL,
  `certifications` JSON DEFAULT NULL,
  `exportable` TINYINT(1) NOT NULL DEFAULT 1,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='个人成长账户';

-- ============================================================
-- M2: 采购会话核心模块
-- ============================================================

DROP TABLE IF EXISTS `purchase_sessions`;
CREATE TABLE `purchase_sessions` (
  `session_id` VARCHAR(32) NOT NULL COMMENT '会话ID (ps_xxxxxx)',
  `initiator_buyer_id` VARCHAR(32) NOT NULL,
  `initiator_company_id` VARCHAR(32) NOT NULL,
  `status` ENUM('active', 'matching', 'quoting', 'negotiating', 'deal', 'expired', 'closed', 'cancelled')
    NOT NULL DEFAULT 'active',
  `priority` ENUM('standard', 'urgent', 'bounty') NOT NULL DEFAULT 'standard',
  `pool_level` ENUM('pilot', 'standard', 'premium') NOT NULL DEFAULT 'standard',
  `project_id` VARCHAR(32) DEFAULT NULL COMMENT '关联项目',
  `procurement_list_id` VARCHAR(32) DEFAULT NULL COMMENT '关联清单',
  `current_card_version` INT NOT NULL DEFAULT 1,
  `source` VARCHAR(32) DEFAULT NULL COMMENT '来源 app/h5/wechat_bot/photo/list',
  `total_quotes` INT NOT NULL DEFAULT 0,
  `total_contacts` INT NOT NULL DEFAULT 0,
  `total_changes` INT NOT NULL DEFAULT 0,
  `last_activity_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `expired_at` DATETIME DEFAULT NULL,
  `closed_at` DATETIME DEFAULT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`session_id`),
  KEY `idx_buyer_status_created` (`initiator_buyer_id`, `status`, `created_at`),
  KEY `idx_status_last_activity` (`status`, `last_activity_at`),
  KEY `idx_project` (`project_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='采购会话';

DROP TABLE IF EXISTS `demand_cards`;
CREATE TABLE `demand_cards` (
  `card_id` VARCHAR(32) NOT NULL,
  `session_id` VARCHAR(32) NOT NULL,
  `version` INT NOT NULL,
  `is_current` TINYINT(1) NOT NULL DEFAULT 1,
  `product_category` VARCHAR(64) NOT NULL COMMENT '品类',
  `material_grade` VARCHAR(64) NOT NULL COMMENT '材质',
  `spec` VARCHAR(128) NOT NULL COMMENT '规格',
  `quantity_ton` DECIMAL(12, 3) NOT NULL,
  `delivery_city` VARCHAR(32) NOT NULL,
  `delivery_district` VARCHAR(32) DEFAULT NULL,
  `delivery_date_start` DATE DEFAULT NULL,
  `delivery_date_end` DATE DEFAULT NULL,
  `payment_terms` ENUM('cash', '3d', '7d', '30d', 'other') DEFAULT 'cash',
  `note` TEXT,
  `required_invoice_type` ENUM('normal', 'special') DEFAULT NULL,
  `required_quality_certificate` TINYINT(1) DEFAULT 0,
  `required_processing` VARCHAR(128) DEFAULT NULL,
  `changed_fields` JSON DEFAULT NULL,
  `changed_by` ENUM('buyer', 'ai_assist') NOT NULL DEFAULT 'buyer',
  `change_reason` VARCHAR(256) DEFAULT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`card_id`),
  UNIQUE KEY `uk_session_version` (`session_id`, `version`),
  KEY `idx_session_current` (`session_id`, `is_current`),
  KEY `idx_category_material_city` (`product_category`, `material_grade`, `delivery_city`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='动态需求卡片';

DROP TABLE IF EXISTS `seller_participations`;
CREATE TABLE `seller_participations` (
  `participation_id` VARCHAR(32) NOT NULL,
  `session_id` VARCHAR(32) NOT NULL,
  `seller_id` VARCHAR(32) NOT NULL,
  `dispatch_score` DECIMAL(5, 2) NOT NULL,
  `pool_level` ENUM('pilot', 'standard', 'premium') NOT NULL,
  `status` ENUM('invited', 'engaged', 'quoted', 'won', 'lost', 'withdrew') NOT NULL DEFAULT 'invited',
  `joined_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `last_response_at` DATETIME DEFAULT NULL,
  PRIMARY KEY (`participation_id`),
  UNIQUE KEY `uk_session_seller` (`session_id`, `seller_id`),
  KEY `idx_seller_status` (`seller_id`, `status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='卖家参与会话';

DROP TABLE IF EXISTS `conversation_streams`;
CREATE TABLE `conversation_streams` (
  `stream_id` VARCHAR(32) NOT NULL,
  `session_id` VARCHAR(32) NOT NULL,
  `buyer_id` VARCHAR(32) NOT NULL,
  `seller_id` VARCHAR(32) NOT NULL,
  `message_count` INT NOT NULL DEFAULT 0,
  `unread_buyer` INT NOT NULL DEFAULT 0,
  `unread_seller` INT NOT NULL DEFAULT 0,
  `last_message_at` DATETIME DEFAULT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`stream_id`),
  UNIQUE KEY `uk_session_pair` (`session_id`, `buyer_id`, `seller_id`),
  KEY `idx_buyer_last` (`buyer_id`, `last_message_at`),
  KEY `idx_seller_last` (`seller_id`, `last_message_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='对话流';

DROP TABLE IF EXISTS `messages`;
CREATE TABLE `messages` (
  `message_id` BIGINT NOT NULL AUTO_INCREMENT,
  `stream_id` VARCHAR(32) NOT NULL,
  `sender_id` VARCHAR(32) NOT NULL,
  `sender_role` ENUM('buyer', 'seller', 'system') NOT NULL,
  `content_type` ENUM('text', 'image', 'file', 'quote_card', 'card_change_notice', 'ai_intent') NOT NULL,
  `content` JSON NOT NULL,
  `ai_intent_id` VARCHAR(32) DEFAULT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`message_id`),
  KEY `idx_stream_created` (`stream_id`, `created_at`),
  KEY `idx_sender_created` (`sender_id`, `created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='消息';

DROP TABLE IF EXISTS `ai_intents`;
CREATE TABLE `ai_intents` (
  `intent_id` VARCHAR(32) NOT NULL,
  `stream_id` VARCHAR(32) NOT NULL,
  `message_id` BIGINT DEFAULT NULL,
  `intent_type` VARCHAR(32) NOT NULL,
  `extracted_fields` JSON DEFAULT NULL,
  `confidence` DECIMAL(4, 3) NOT NULL,
  `natural_summary` VARCHAR(256) DEFAULT NULL,
  `user_confirmed` TINYINT DEFAULT NULL COMMENT '1=确认, 0=拒绝, NULL=未操作',
  `llm_model` VARCHAR(64) DEFAULT NULL,
  `llm_cost` DECIMAL(8, 4) DEFAULT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`intent_id`),
  KEY `idx_stream_created` (`stream_id`, `created_at`),
  KEY `idx_confirmed` (`user_confirmed`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='AI 识变记录';

DROP TABLE IF EXISTS `session_events`;
CREATE TABLE `session_events` (
  `event_id` BIGINT NOT NULL AUTO_INCREMENT,
  `session_id` VARCHAR(32) NOT NULL,
  `event_type` VARCHAR(64) NOT NULL,
  `actor_id` VARCHAR(32) DEFAULT NULL,
  `payload` JSON DEFAULT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`event_id`),
  KEY `idx_session_created` (`session_id`, `created_at`),
  KEY `idx_event_type` (`event_type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='会话时间线';

-- ============================================================
-- M3: 清单采购模块
-- ============================================================

DROP TABLE IF EXISTS `procurement_lists`;
CREATE TABLE `procurement_lists` (
  `list_id` VARCHAR(32) NOT NULL,
  `buyer_id` VARCHAR(32) NOT NULL,
  `company_id` VARCHAR(32) NOT NULL,
  `project_id` VARCHAR(32) DEFAULT NULL,
  `source` ENUM('photo', 'excel', 'pdf', 'wechat_forward', 'paste', 'manual') NOT NULL,
  `original_file_url` VARCHAR(512) DEFAULT NULL,
  `parsing_status` ENUM('parsing', 'ready_for_confirm', 'confirmed', 'dispatched', 'closed', 'failed')
    NOT NULL DEFAULT 'parsing',
  `parsing_job_id` VARCHAR(32) DEFAULT NULL,
  `total_lines` INT NOT NULL DEFAULT 0,
  `ai_uncertain_lines` JSON DEFAULT NULL,
  `mode` ENUM('precise', 'fuzzy') NOT NULL DEFAULT 'precise',
  `total_estimated_value` DECIMAL(15, 2) DEFAULT NULL,
  `confirmed_at` DATETIME DEFAULT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`list_id`),
  KEY `idx_buyer_created` (`buyer_id`, `created_at`),
  KEY `idx_project` (`project_id`),
  KEY `idx_status` (`parsing_status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='采购清单';

DROP TABLE IF EXISTS `procurement_list_lines`;
CREATE TABLE `procurement_list_lines` (
  `line_id` VARCHAR(32) NOT NULL,
  `list_id` VARCHAR(32) NOT NULL,
  `line_number` INT NOT NULL,
  `product_category` VARCHAR(64) NOT NULL,
  `material_grade` VARCHAR(64) NOT NULL,
  `spec` VARCHAR(128) NOT NULL,
  `quantity_ton` DECIMAL(12, 3) NOT NULL,
  `delivery_date` DATE DEFAULT NULL,
  `delivery_location` VARCHAR(128) DEFAULT NULL,
  `notes` VARCHAR(256) DEFAULT NULL,
  `ai_extracted` TINYINT(1) NOT NULL DEFAULT 0,
  `ai_confidence` DECIMAL(4, 3) DEFAULT NULL,
  `ai_uncertain` TINYINT(1) NOT NULL DEFAULT 0,
  `raw_text` TEXT,
  `user_corrected` TINYINT(1) NOT NULL DEFAULT 0,
  `user_corrected_at` DATETIME DEFAULT NULL,
  `dispatched_to_category` VARCHAR(64) DEFAULT NULL,
  `related_session_id` VARCHAR(32) DEFAULT NULL,
  PRIMARY KEY (`line_id`),
  UNIQUE KEY `uk_list_line` (`list_id`, `line_number`),
  KEY `idx_category` (`product_category`),
  KEY `idx_session` (`related_session_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='清单明细行';

DROP TABLE IF EXISTS `list_responses`;
CREATE TABLE `list_responses` (
  `response_id` VARCHAR(32) NOT NULL,
  `list_id` VARCHAR(32) NOT NULL,
  `seller_id` VARCHAR(32) NOT NULL,
  `responded_line_ids` JSON DEFAULT NULL,
  `not_responded_line_ids` JSON DEFAULT NULL,
  `total_quote_value` DECIMAL(15, 2) DEFAULT NULL,
  `pricing_method` ENUM('manual', 'excel_upload', 'voice') NOT NULL DEFAULT 'manual',
  `excel_file_url` VARCHAR(512) DEFAULT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`response_id`),
  UNIQUE KEY `uk_list_seller` (`list_id`, `seller_id`),
  KEY `idx_seller_created` (`seller_id`, `created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='卖家清单应答';

DROP TABLE IF EXISTS `line_quotes`;
CREATE TABLE `line_quotes` (
  `line_quote_id` VARCHAR(32) NOT NULL,
  `response_id` VARCHAR(32) NOT NULL,
  `list_id` VARCHAR(32) NOT NULL,
  `line_id` VARCHAR(32) NOT NULL,
  `seller_id` VARCHAR(32) NOT NULL,
  `unit_price` DECIMAL(12, 2) NOT NULL,
  `include_freight` TINYINT(1) NOT NULL DEFAULT 0,
  `available_qty` DECIMAL(12, 3) NOT NULL,
  `valid_until` DATETIME NOT NULL,
  `notes` VARCHAR(256) DEFAULT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`line_quote_id`),
  KEY `idx_line` (`line_id`),
  KEY `idx_list_seller` (`list_id`, `seller_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='清单逐行报价';

DROP TABLE IF EXISTS `optimal_combos`;
CREATE TABLE `optimal_combos` (
  `combo_id` VARCHAR(32) NOT NULL,
  `list_id` VARCHAR(32) NOT NULL,
  `strategy` ENUM('lowest_cost', 'one_stop', 'fastest', 'highest_credit') NOT NULL,
  `total_cost` DECIMAL(15, 2) NOT NULL,
  `total_sellers` INT NOT NULL,
  `estimated_delivery_days` INT DEFAULT NULL,
  `avg_credit_score` DECIMAL(5, 2) DEFAULT NULL,
  `line_assignments` JSON NOT NULL,
  `is_selected` TINYINT(1) NOT NULL DEFAULT 0,
  `calculated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`combo_id`),
  KEY `idx_list_strategy` (`list_id`, `strategy`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='最优组合方案';

DROP TABLE IF EXISTS `projects`;
CREATE TABLE `projects` (
  `project_id` VARCHAR(32) NOT NULL,
  `buyer_id` VARCHAR(32) NOT NULL,
  `company_id` VARCHAR(32) NOT NULL,
  `name` VARCHAR(128) NOT NULL,
  `description` TEXT,
  `budget` DECIMAL(15, 2) DEFAULT NULL,
  `status` ENUM('active', 'on_hold', 'completed', 'cancelled') NOT NULL DEFAULT 'active',
  `total_lists` INT NOT NULL DEFAULT 0,
  `total_value` DECIMAL(15, 2) NOT NULL DEFAULT 0,
  `total_delivered` DECIMAL(15, 2) NOT NULL DEFAULT 0,
  `progress` DECIMAL(5, 4) NOT NULL DEFAULT 0,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`project_id`),
  KEY `idx_buyer_status` (`buyer_id`, `status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='项目档案';

-- ============================================================
-- M4: 报价系统
-- ============================================================

DROP TABLE IF EXISTS `quotes`;
CREATE TABLE `quotes` (
  `quote_id` VARCHAR(32) NOT NULL,
  `session_id` VARCHAR(32) NOT NULL,
  `card_version` INT NOT NULL,
  `seller_id` VARCHAR(32) NOT NULL,
  `status` ENUM('active', 'updated', 'expired', 'withdrawn', 'won', 'lost', 'superseded')
    NOT NULL DEFAULT 'active',
  `base_unit_price` DECIMAL(12, 2) NOT NULL COMMENT '基础单价/吨',
  `available_qty` DECIMAL(12, 3) NOT NULL,
  `valid_until` DATETIME NOT NULL,
  `tier_pricing` JSON DEFAULT NULL COMMENT '阶梯定价',
  `spec_adjustments` JSON DEFAULT NULL COMMENT '规格调价',
  `add_ons` JSON DEFAULT NULL COMMENT '加项',
  `notes` VARCHAR(256) DEFAULT NULL,
  `market_reference_price` DECIMAL(12, 2) DEFAULT NULL,
  `estimated_profit_margin` DECIMAL(6, 4) DEFAULT NULL,
  `viewed_by_buyer_at` DATETIME DEFAULT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`quote_id`),
  KEY `idx_session_status` (`session_id`, `status`),
  KEY `idx_seller_status` (`seller_id`, `status`),
  KEY `idx_valid_until` (`valid_until`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='报价';

DROP TABLE IF EXISTS `buyer_selections`;
CREATE TABLE `buyer_selections` (
  `selection_id` VARCHAR(32) NOT NULL,
  `quote_id` VARCHAR(32) NOT NULL,
  `buyer_id` VARCHAR(32) NOT NULL,
  `selected_quantity` DECIMAL(12, 3) NOT NULL,
  `selected_spec` VARCHAR(128) NOT NULL,
  `selected_add_ons` JSON DEFAULT NULL,
  `calculated_unit_price` DECIMAL(12, 2) NOT NULL,
  `calculated_total` DECIMAL(15, 2) NOT NULL,
  `saved_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`selection_id`),
  KEY `idx_quote` (`quote_id`),
  KEY `idx_buyer_saved` (`buyer_id`, `saved_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='买家选择';

DROP TABLE IF EXISTS `negotiations`;
CREATE TABLE `negotiations` (
  `negotiation_id` VARCHAR(32) NOT NULL,
  `quote_id` VARCHAR(32) NOT NULL,
  `session_id` VARCHAR(32) NOT NULL,
  `initiator` ENUM('buyer', 'seller') NOT NULL,
  `proposed_price` DECIMAL(12, 2) NOT NULL,
  `reason` VARCHAR(256) DEFAULT NULL,
  `status` ENUM('pending', 'accepted', 'rejected', 'counter_offered', 'expired')
    NOT NULL DEFAULT 'pending',
  `counter_negotiation_id` VARCHAR(32) DEFAULT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `responded_at` DATETIME DEFAULT NULL,
  `expires_at` DATETIME DEFAULT NULL,
  PRIMARY KEY (`negotiation_id`),
  KEY `idx_quote_status` (`quote_id`, `status`),
  KEY `idx_session_created` (`session_id`, `created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='议价记录';

DROP TABLE IF EXISTS `quote_templates`;
CREATE TABLE `quote_templates` (
  `template_id` VARCHAR(32) NOT NULL,
  `seller_id` VARCHAR(32) NOT NULL,
  `name` VARCHAR(64) NOT NULL,
  `template_data` JSON NOT NULL,
  `use_count` INT NOT NULL DEFAULT 0,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`template_id`),
  KEY `idx_seller_use` (`seller_id`, `use_count`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='报价模板';

-- ============================================================
-- M5: 智能匹配引擎
-- ============================================================

DROP TABLE IF EXISTS `dispatches`;
CREATE TABLE `dispatches` (
  `dispatch_id` VARCHAR(32) NOT NULL,
  `session_id` VARCHAR(32) NOT NULL,
  `seller_id` VARCHAR(32) NOT NULL,
  `buyer_pool` ENUM('pilot', 'standard', 'premium') NOT NULL,
  `match_score` DECIMAL(5, 2) NOT NULL,
  `channels` JSON DEFAULT NULL COMMENT '推送通道',
  `dispatched_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `seen_at` DATETIME DEFAULT NULL,
  `responded_at` DATETIME DEFAULT NULL,
  `response_status` ENUM('engaged', 'rejected', 'ignored') DEFAULT NULL,
  `reject_reason` VARCHAR(256) DEFAULT NULL,
  PRIMARY KEY (`dispatch_id`),
  UNIQUE KEY `uk_session_seller` (`session_id`, `seller_id`),
  KEY `idx_seller_dispatched` (`seller_id`, `dispatched_at`),
  KEY `idx_status` (`response_status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='派单记录';

DROP TABLE IF EXISTS `seller_preferences`;
CREATE TABLE `seller_preferences` (
  `seller_id` VARCHAR(32) NOT NULL,
  `accept_pools` JSON NOT NULL COMMENT '愿意接的池子',
  `categories` JSON NOT NULL COMMENT '专精品类',
  `regions` JSON NOT NULL COMMENT '服务区域',
  `time_windows` JSON DEFAULT NULL,
  `daily_max` INT NOT NULL DEFAULT 20,
  `min_order_amount` DECIMAL(12, 2) NOT NULL DEFAULT 10000,
  `max_order_amount` DECIMAL(12, 2) NOT NULL DEFAULT 10000000,
  `min_profit_margin` DECIMAL(4, 4) NOT NULL DEFAULT 0.015,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`seller_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='卖家接单偏好';

DROP TABLE IF EXISTS `buyer_pool_assignments`;
CREATE TABLE `buyer_pool_assignments` (
  `buyer_id` VARCHAR(32) NOT NULL,
  `current_pool` ENUM('pilot', 'standard', 'premium') NOT NULL,
  `credit_score` INT NOT NULL,
  `historical_deals` INT NOT NULL,
  `contact_count_30d` INT NOT NULL,
  `explicit_override` VARCHAR(128) DEFAULT NULL,
  `determined_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`buyer_id`),
  KEY `idx_pool` (`current_pool`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='买家池分配';

DROP TABLE IF EXISTS `market_references`;
CREATE TABLE `market_references` (
  `reference_id` VARCHAR(32) NOT NULL,
  `product_category` VARCHAR(64) NOT NULL,
  `material_grade` VARCHAR(64) NOT NULL,
  `spec_pattern` VARCHAR(128) DEFAULT NULL,
  `region` VARCHAR(32) NOT NULL,
  `median_price` DECIMAL(12, 2) NOT NULL,
  `p25` DECIMAL(12, 2) NOT NULL,
  `p75` DECIMAL(12, 2) NOT NULL,
  `sample_count` INT NOT NULL,
  `timeframe_days` INT NOT NULL DEFAULT 7,
  `computed_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`reference_id`),
  KEY `idx_lookup` (`product_category`, `material_grade`, `region`, `computed_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='市场参考价';

-- ============================================================
-- M6: 信用与信任体系
-- ============================================================

DROP TABLE IF EXISTS `credit_scores`;
CREATE TABLE `credit_scores` (
  `user_id` VARCHAR(32) NOT NULL,
  `role` ENUM('buyer', 'seller') NOT NULL,
  `current_score` INT NOT NULL,
  `level` VARCHAR(16) NOT NULL,
  `base_score` INT NOT NULL,
  `computed_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`user_id`, `role`),
  KEY `idx_level` (`role`, `level`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='信用分';

DROP TABLE IF EXISTS `credit_score_adjustments`;
CREATE TABLE `credit_score_adjustments` (
  `adjustment_id` BIGINT NOT NULL AUTO_INCREMENT,
  `user_id` VARCHAR(32) NOT NULL,
  `role` ENUM('buyer', 'seller') NOT NULL,
  `reason_code` VARCHAR(64) NOT NULL,
  `delta` INT NOT NULL,
  `evidence` JSON DEFAULT NULL,
  `appealable` TINYINT(1) NOT NULL DEFAULT 1,
  `applied_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`adjustment_id`),
  KEY `idx_user_applied` (`user_id`, `role`, `applied_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='信用分变更';

DROP TABLE IF EXISTS `seller_verifications`;
CREATE TABLE `seller_verifications` (
  `verification_id` VARCHAR(32) NOT NULL,
  `seller_id` VARCHAR(32) NOT NULL,
  `type` ENUM('field', 'video', 'document') NOT NULL,
  `status` ENUM('pending', 'completed', 'rejected') NOT NULL DEFAULT 'pending',
  `verifier_id` VARCHAR(32) DEFAULT NULL,
  `verification_date` DATETIME DEFAULT NULL,
  `photos` JSON DEFAULT NULL,
  `report` TEXT,
  `rating` ENUM('A', 'B', 'C') DEFAULT NULL,
  `notes` TEXT,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`verification_id`),
  KEY `idx_seller_status` (`seller_id`, `status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='卖家核验';

DROP TABLE IF EXISTS `video_showcases`;
CREATE TABLE `video_showcases` (
  `showcase_id` VARCHAR(32) NOT NULL,
  `seller_id` VARCHAR(32) NOT NULL,
  `category` ENUM('warehouse', 'production', 'team', 'recent_inventory', 'customer') NOT NULL,
  `video_url` VARCHAR(512) NOT NULL,
  `thumbnail_url` VARCHAR(512) DEFAULT NULL,
  `duration_sec` INT NOT NULL,
  `approved` TINYINT(1) NOT NULL DEFAULT 0,
  `view_count` INT NOT NULL DEFAULT 0,
  `uploaded_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`showcase_id`),
  KEY `idx_seller_approved` (`seller_id`, `approved`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='卖家视频展示';

DROP TABLE IF EXISTS `reviews`;
CREATE TABLE `reviews` (
  `review_id` VARCHAR(32) NOT NULL,
  `reviewer_id` VARCHAR(32) NOT NULL,
  `reviewee_id` VARCHAR(32) NOT NULL,
  `session_id` VARCHAR(32) NOT NULL,
  `rating` TINYINT NOT NULL,
  `comment` TEXT,
  `tags` JSON DEFAULT NULL,
  `visible` TINYINT(1) NOT NULL DEFAULT 1,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`review_id`),
  UNIQUE KEY `uk_session_reviewer` (`session_id`, `reviewer_id`),
  KEY `idx_reviewee` (`reviewee_id`, `visible`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='评价';

DROP TABLE IF EXISTS `appeals`;
CREATE TABLE `appeals` (
  `appeal_id` VARCHAR(32) NOT NULL,
  `appellant_id` VARCHAR(32) NOT NULL,
  `respondent_id` VARCHAR(32) DEFAULT NULL,
  `target_type` ENUM('rating', 'credit_score', 'penalty', 'transaction') NOT NULL,
  `target_id` VARCHAR(64) NOT NULL,
  `reason` TEXT NOT NULL,
  `evidence` JSON DEFAULT NULL,
  `status` ENUM('submitted', 'reviewing', 'first_decision', 'appeal_committee', 'closed')
    NOT NULL DEFAULT 'submitted',
  `first_decision` JSON DEFAULT NULL,
  `committee_decision` JSON DEFAULT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `resolved_at` DATETIME DEFAULT NULL,
  PRIMARY KEY (`appeal_id`),
  KEY `idx_appellant` (`appellant_id`, `status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='申诉';

DROP TABLE IF EXISTS `blacklists`;
CREATE TABLE `blacklists` (
  `blacklist_id` BIGINT NOT NULL AUTO_INCREMENT,
  `owner_id` VARCHAR(32) NOT NULL,
  `blocked_user_id` VARCHAR(32) NOT NULL,
  `reason` VARCHAR(256) DEFAULT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`blacklist_id`),
  UNIQUE KEY `uk_owner_blocked` (`owner_id`, `blocked_user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='黑名单';

-- ============================================================
-- M7: 卖家工具包
-- ============================================================

DROP TABLE IF EXISTS `seller_customers`;
CREATE TABLE `seller_customers` (
  `customer_id` VARCHAR(32) NOT NULL,
  `seller_id` VARCHAR(32) NOT NULL,
  `buyer_id` VARCHAR(32) NOT NULL,
  `first_contact_at` DATETIME NOT NULL,
  `total_inquiries` INT NOT NULL DEFAULT 0,
  `total_contacts` INT NOT NULL DEFAULT 0,
  `total_deals` INT NOT NULL DEFAULT 0,
  `total_amount` DECIMAL(15, 2) NOT NULL DEFAULT 0,
  `tags` JSON DEFAULT NULL,
  `custom_notes` TEXT,
  `last_activity_at` DATETIME DEFAULT NULL,
  PRIMARY KEY (`customer_id`),
  UNIQUE KEY `uk_seller_buyer` (`seller_id`, `buyer_id`),
  KEY `idx_seller_activity` (`seller_id`, `last_activity_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='卖家私域 CRM';

DROP TABLE IF EXISTS `follow_up_tasks`;
CREATE TABLE `follow_up_tasks` (
  `task_id` VARCHAR(32) NOT NULL,
  `seller_id` VARCHAR(32) NOT NULL,
  `customer_id` VARCHAR(32) NOT NULL,
  `description` VARCHAR(256) NOT NULL,
  `due_at` DATETIME NOT NULL,
  `status` ENUM('pending', 'completed', 'cancelled') NOT NULL DEFAULT 'pending',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`task_id`),
  KEY `idx_seller_due_status` (`seller_id`, `due_at`, `status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='跟进任务';

DROP TABLE IF EXISTS `invitation_codes`;
CREATE TABLE `invitation_codes` (
  `code` VARCHAR(16) NOT NULL,
  `seller_id` VARCHAR(32) NOT NULL,
  `qr_code_url` VARCHAR(512) DEFAULT NULL,
  `short_url` VARCHAR(128) DEFAULT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`code`),
  UNIQUE KEY `uk_seller` (`seller_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='邀请码';

DROP TABLE IF EXISTS `invitation_records`;
CREATE TABLE `invitation_records` (
  `record_id` BIGINT NOT NULL AUTO_INCREMENT,
  `inviter_seller_id` VARCHAR(32) NOT NULL,
  `invitee_buyer_id` VARCHAR(32) NOT NULL,
  `milestone` ENUM('M1_registered', 'M2_published', 'M3_engaged', 'M4_deal', 'M5_active') NOT NULL,
  `rewards_paid` JSON DEFAULT NULL,
  `fraud_checked` TINYINT(1) NOT NULL DEFAULT 0,
  `fraud_result` VARCHAR(64) DEFAULT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`record_id`),
  UNIQUE KEY `uk_inviter_invitee_milestone` (`inviter_seller_id`, `invitee_buyer_id`, `milestone`),
  KEY `idx_invitee` (`invitee_buyer_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='邀请记录';

-- ============================================================
-- M8: 买家工具包
-- ============================================================

DROP TABLE IF EXISTS `market_data_subscriptions`;
CREATE TABLE `market_data_subscriptions` (
  `subscription_id` VARCHAR(32) NOT NULL,
  `user_id` VARCHAR(32) NOT NULL,
  `plan` ENUM('free', 'basic_99', 'advanced_299') NOT NULL,
  `watched_products` JSON DEFAULT NULL,
  `status` ENUM('active', 'expired', 'cancelled') NOT NULL DEFAULT 'active',
  `expires_at` DATETIME DEFAULT NULL,
  `total_paid` DECIMAL(10, 2) NOT NULL DEFAULT 0,
  PRIMARY KEY (`subscription_id`),
  KEY `idx_user_status` (`user_id`, `status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='行情订阅';

DROP TABLE IF EXISTS `buyer_suppliers`;
CREATE TABLE `buyer_suppliers` (
  `supplier_id` VARCHAR(32) NOT NULL,
  `buyer_id` VARCHAR(32) NOT NULL,
  `seller_company_id` VARCHAR(32) DEFAULT NULL COMMENT '若已入驻平台',
  `external_supplier_name` VARCHAR(128) DEFAULT NULL COMMENT '未入驻供应商名称',
  `source` ENUM('own_upload', 'platform_match', 'platform_recommend') NOT NULL,
  `contact_info` JSON DEFAULT NULL,
  `primary_category` VARCHAR(64) DEFAULT NULL,
  `total_orders` INT NOT NULL DEFAULT 0,
  `total_amount` DECIMAL(15, 2) NOT NULL DEFAULT 0,
  `avg_on_time_rate` DECIMAL(4, 4) DEFAULT NULL,
  `custom_tags` JSON DEFAULT NULL,
  `private_notes` TEXT COMMENT '仅买家可见',
  `added_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`supplier_id`),
  KEY `idx_buyer` (`buyer_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='我的供应商';

DROP TABLE IF EXISTS `comparison_reports`;
CREATE TABLE `comparison_reports` (
  `report_id` VARCHAR(32) NOT NULL,
  `list_id` VARCHAR(32) NOT NULL,
  `buyer_id` VARCHAR(32) NOT NULL,
  `format` ENUM('pdf', 'excel') NOT NULL,
  `template` ENUM('simple', 'detailed', 'bid_compliant') NOT NULL,
  `file_url` VARCHAR(512) NOT NULL,
  `generated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`report_id`),
  KEY `idx_list_buyer` (`list_id`, `buyer_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='比价单导出';

-- ============================================================
-- M9: 微信集成
-- ============================================================

DROP TABLE IF EXISTS `wechat_bindings`;
CREATE TABLE `wechat_bindings` (
  `binding_id` VARCHAR(32) NOT NULL,
  `user_id` VARCHAR(32) NOT NULL,
  `open_id` VARCHAR(128) NOT NULL,
  `union_id` VARCHAR(128) NOT NULL,
  `is_corporate_wechat` TINYINT(1) NOT NULL DEFAULT 0,
  `bound_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `last_active_at` DATETIME DEFAULT NULL,
  PRIMARY KEY (`binding_id`),
  UNIQUE KEY `uk_user_open` (`user_id`, `open_id`),
  KEY `idx_union` (`union_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='微信绑定';

DROP TABLE IF EXISTS `virtual_number_calls`;
CREATE TABLE `virtual_number_calls` (
  `call_id` VARCHAR(32) NOT NULL,
  `caller_id` VARCHAR(32) NOT NULL,
  `callee_id` VARCHAR(32) NOT NULL,
  `session_id` VARCHAR(32) DEFAULT NULL,
  `virtual_number` VARCHAR(32) NOT NULL,
  `status` ENUM('connecting', 'connected', 'completed', 'failed') NOT NULL,
  `duration_sec` INT DEFAULT NULL,
  `recording_url` VARCHAR(512) DEFAULT NULL,
  `ai_summary` TEXT,
  `flagged_keywords` JSON DEFAULT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`call_id`),
  KEY `idx_caller` (`caller_id`, `created_at`),
  KEY `idx_session` (`session_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='虚拟号通话';

-- ============================================================
-- M10: 商业化产品
-- ============================================================

DROP TABLE IF EXISTS `memberships`;
CREATE TABLE `memberships` (
  `membership_id` VARCHAR(32) NOT NULL,
  `seller_id` VARCHAR(32) NOT NULL,
  `tier` ENUM('basic', 'gold', 'diamond') NOT NULL,
  `start_date` DATE NOT NULL,
  `end_date` DATE NOT NULL,
  `status` ENUM('active', 'expired', 'cancelled', 'refunded') NOT NULL,
  `amount` DECIMAL(10, 2) NOT NULL,
  `payment_method` VARCHAR(32) DEFAULT NULL,
  `invoice_issued` TINYINT(1) NOT NULL DEFAULT 0,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`membership_id`),
  KEY `idx_seller_status` (`seller_id`, `status`),
  KEY `idx_end_date` (`end_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='会员';

DROP TABLE IF EXISTS `traffic_wallets`;
CREATE TABLE `traffic_wallets` (
  `wallet_id` VARCHAR(32) NOT NULL,
  `seller_id` VARCHAR(32) NOT NULL,
  `balance` DECIMAL(12, 2) NOT NULL DEFAULT 0,
  `total_recharged` DECIMAL(12, 2) NOT NULL DEFAULT 0,
  `total_consumed` DECIMAL(12, 2) NOT NULL DEFAULT 0,
  `free_quota_remaining` INT NOT NULL DEFAULT 0,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`wallet_id`),
  UNIQUE KEY `uk_seller` (`seller_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='流量账户';

DROP TABLE IF EXISTS `traffic_charges`;
CREATE TABLE `traffic_charges` (
  `charge_id` VARCHAR(32) NOT NULL,
  `wallet_id` VARCHAR(32) NOT NULL,
  `seller_id` VARCHAR(32) NOT NULL,
  `type` ENUM('cpl', 'cpm', 'cpc', 'subscription') NOT NULL,
  `amount` DECIMAL(10, 2) NOT NULL,
  `related_entity_type` VARCHAR(32) DEFAULT NULL,
  `related_entity_id` VARCHAR(32) DEFAULT NULL,
  `applicable_pricing` JSON DEFAULT NULL,
  `appealed` TINYINT(1) NOT NULL DEFAULT 0,
  `refunded` TINYINT(1) NOT NULL DEFAULT 0,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`charge_id`),
  KEY `idx_seller_created` (`seller_id`, `created_at`),
  KEY `idx_appealed` (`appealed`, `refunded`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='流量费扣费';

DROP TABLE IF EXISTS `saas_contracts`;
CREATE TABLE `saas_contracts` (
  `contract_id` VARCHAR(32) NOT NULL,
  `company_id` VARCHAR(32) NOT NULL,
  `product` ENUM('procurement_saas', 'enterprise_suite', 'vip_buyer_service') NOT NULL,
  `start_date` DATE NOT NULL,
  `end_date` DATE NOT NULL,
  `amount` DECIMAL(12, 2) NOT NULL,
  `invoice_type` ENUM('normal', 'special') NOT NULL,
  `contract_url` VARCHAR(512) DEFAULT NULL,
  `status` ENUM('pending', 'active', 'expired', 'terminated') NOT NULL DEFAULT 'pending',
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`contract_id`),
  KEY `idx_company_status` (`company_id`, `status`),
  KEY `idx_end_date` (`end_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='SaaS 合同';

DROP TABLE IF EXISTS `data_subscriptions`;
CREATE TABLE `data_subscriptions` (
  `subscription_id` VARCHAR(32) NOT NULL,
  `user_id` VARCHAR(32) NOT NULL,
  `product` VARCHAR(64) NOT NULL,
  `start_date` DATE NOT NULL,
  `end_date` DATE NOT NULL,
  `amount` DECIMAL(10, 2) NOT NULL,
  `status` ENUM('active', 'expired', 'cancelled') NOT NULL DEFAULT 'active',
  PRIMARY KEY (`subscription_id`),
  KEY `idx_user_status` (`user_id`, `status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='数据订阅';

-- ============================================================
-- M11: 风控与反作弊
-- ============================================================

DROP TABLE IF EXISTS `risk_rules`;
CREATE TABLE `risk_rules` (
  `rule_id` VARCHAR(16) NOT NULL COMMENT 'R001 - R036',
  `name` VARCHAR(128) NOT NULL,
  `category` ENUM('register', 'invitation', 'demand', 'quote', 'contact', 'deal', 'traffic_fee') NOT NULL,
  `severity` ENUM('L0', 'L1', 'L2', 'L3', 'L4') NOT NULL,
  `enabled` TINYINT(1) NOT NULL DEFAULT 1,
  `conditions` JSON NOT NULL,
  `disposition` JSON NOT NULL,
  `version` INT NOT NULL DEFAULT 1,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`rule_id`),
  KEY `idx_category_enabled` (`category`, `enabled`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='风控规则';

DROP TABLE IF EXISTS `risk_events`;
CREATE TABLE `risk_events` (
  `event_id` BIGINT NOT NULL AUTO_INCREMENT,
  `rule_id` VARCHAR(16) NOT NULL,
  `user_id` VARCHAR(32) NOT NULL,
  `related_entity_type` VARCHAR(32) DEFAULT NULL,
  `related_entity_id` VARCHAR(32) DEFAULT NULL,
  `trigger_data` JSON DEFAULT NULL,
  `disposition` ENUM('L0', 'L1', 'L2', 'L3', 'L4') NOT NULL,
  `status` ENUM('auto_handled', 'pending_review', 'reviewed_kept', 'reviewed_overruled')
    NOT NULL DEFAULT 'auto_handled',
  `appealed` TINYINT(1) NOT NULL DEFAULT 0,
  `appeal_id` VARCHAR(32) DEFAULT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`event_id`),
  KEY `idx_user_rule_created` (`user_id`, `rule_id`, `created_at`),
  KEY `idx_rule_status` (`rule_id`, `status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='风控事件';

DROP TABLE IF EXISTS `region_alerts`;
CREATE TABLE `region_alerts` (
  `alert_id` VARCHAR(32) NOT NULL,
  `region` VARCHAR(32) NOT NULL,
  `alert_type` VARCHAR(64) NOT NULL,
  `severity` ENUM('yellow', 'red', 'purple') NOT NULL,
  `data` JSON NOT NULL,
  `triggered_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `resolved_at` DATETIME DEFAULT NULL,
  PRIMARY KEY (`alert_id`),
  KEY `idx_region_severity_triggered` (`region`, `severity`, `triggered_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='区域风险预警';

DROP TABLE IF EXISTS `device_fingerprints`;
CREATE TABLE `device_fingerprints` (
  `fingerprint_id` VARCHAR(64) NOT NULL,
  `user_id` VARCHAR(32) NOT NULL,
  `device_type` VARCHAR(32) DEFAULT NULL,
  `os` VARCHAR(32) DEFAULT NULL,
  `ip_address` VARCHAR(64) DEFAULT NULL,
  `user_agent` VARCHAR(512) DEFAULT NULL,
  `is_blacklisted` TINYINT(1) NOT NULL DEFAULT 0,
  `blacklist_until` DATETIME DEFAULT NULL,
  `first_seen_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `last_seen_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`fingerprint_id`, `user_id`),
  KEY `idx_user` (`user_id`),
  KEY `idx_blacklist` (`is_blacklisted`, `blacklist_until`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='设备指纹';

-- ============================================================
-- 辅助表
-- ============================================================

DROP TABLE IF EXISTS `audit_logs`;
CREATE TABLE `audit_logs` (
  `log_id` BIGINT NOT NULL AUTO_INCREMENT,
  `user_id` VARCHAR(32) DEFAULT NULL,
  `action` VARCHAR(64) NOT NULL,
  `entity_type` VARCHAR(32) DEFAULT NULL,
  `entity_id` VARCHAR(64) DEFAULT NULL,
  `before_data` JSON DEFAULT NULL,
  `after_data` JSON DEFAULT NULL,
  `ip_address` VARCHAR(64) DEFAULT NULL,
  `user_agent` VARCHAR(512) DEFAULT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`log_id`),
  KEY `idx_user_created` (`user_id`, `created_at`),
  KEY `idx_entity` (`entity_type`, `entity_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='审计日志';

SET FOREIGN_KEY_CHECKS = 1;

-- ============================================================
-- 结束
-- 33 张表，覆盖全部 11 模块
-- ============================================================
