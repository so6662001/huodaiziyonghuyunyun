package com.huodaizi.user.entity;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import com.huodaizi.domain.entity.BaseEntity;
import com.huodaizi.domain.enums.UserRole;
import lombok.Data;
import lombok.EqualsAndHashCode;

import java.time.LocalDateTime;

/**
 * 用户实体（对应 users 表）
 */
@Data
@EqualsAndHashCode(callSuper = true)
@TableName("users")
public class User extends BaseEntity {

    @TableId(type = IdType.INPUT)
    private String userId;

    private String phone;

    private String wechatOpenId;

    private String wechatUnionId;

    private String name;

    private String avatar;

    private String idCardHash;

    private UserRole primaryRole;

    private String currentView;

    private String status;

    private LocalDateTime lastActiveAt;
}
