package com.yanshi.config;

import io.swagger.v3.oas.models.OpenAPI;
import io.swagger.v3.oas.models.info.Info;
import io.swagger.v3.oas.models.info.Contact;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/**
 * OpenAPI配置
 */
@Configuration
public class OpenApiConfig {

    @Bean
    public OpenAPI customOpenAPI() {
        return new OpenAPI()
                .info(new Info()
                        .title("研时-考研时政智能分析系统 API")
                        .version("1.0.0")
                        .description("提供文章管理和知识点管理的API接口")
                        .contact(new Contact()
                                .name("研时团队")));
    }
}
