package com.yanshi;

import org.mybatis.spring.annotation.MapperScan;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

/**
 * 研时-考研时政智能分析系统后端服务
 */
@SpringBootApplication
@MapperScan("com.yanshi.mapper")
public class YanshiBackendApplication {

    public static void main(String[] args) {
        SpringApplication.run(YanshiBackendApplication.class, args);
        System.out.println("\n==================================================");
        System.out.println("  研时-考研时政智能分析系统后端服务启动成功!");
        System.out.println("  访问地址: http://localhost:8080/api");
        System.out.println("  Swagger文档: http://localhost:8080/api/swagger-ui.html");
        System.out.println("==================================================\n");
    }
}
