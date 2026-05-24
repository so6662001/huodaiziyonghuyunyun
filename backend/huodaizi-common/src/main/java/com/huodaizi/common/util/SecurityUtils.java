package com.huodaizi.common.util;

import cn.dev33.satoken.stp.StpUtil;
import com.huodaizi.common.api.ErrorCode;
import com.huodaizi.common.exception.BusinessException;

/**
 * 安全工具类
 * 封装 Sa-Token，提供当前用户上下文获取。
 */
public class SecurityUtils {

    public static String currentUserId() {
        try {
            return (String) StpUtil.getLoginId();
        } catch (Exception e) {
            throw new BusinessException(ErrorCode.UNAUTHORIZED);
        }
    }

    public static String currentUserIdOrNull() {
        try {
            Object id = StpUtil.getLoginIdDefaultNull();
            return id == null ? null : id.toString();
        } catch (Exception e) {
            return null;
        }
    }

    public static boolean isLoggedIn() {
        return StpUtil.isLogin();
    }

    public static String currentRole() {
        try {
            return (String) StpUtil.getSession().get("role");
        } catch (Exception e) {
            return null;
        }
    }

    public static String currentCompanyId() {
        try {
            return (String) StpUtil.getSession().get("companyId");
        } catch (Exception e) {
            return null;
        }
    }
}
