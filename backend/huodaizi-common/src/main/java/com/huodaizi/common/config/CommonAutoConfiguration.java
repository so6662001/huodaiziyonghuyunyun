package com.huodaizi.common.config;

import com.huodaizi.common.exception.GlobalExceptionHandler;
import com.huodaizi.common.web.RequestIdFilter;
import org.springframework.boot.autoconfigure.AutoConfiguration;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.ComponentScan;

/**
 * Common 模块自动配置
 * 业务服务引入本模块后，自动注册全局异常处理、RequestId 过滤器等。
 */
@AutoConfiguration
@ComponentScan(basePackages = "com.huodaizi.common")
public class CommonAutoConfiguration {

    @Bean
    public GlobalExceptionHandler globalExceptionHandler() {
        return new GlobalExceptionHandler();
    }

    @Bean
    public RequestIdFilter requestIdFilter() {
        return new RequestIdFilter();
    }
}
