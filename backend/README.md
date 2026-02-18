# 研时-考研时政智能分析系统后端服务

## 项目简介

研时后端是基于 Spring Boot 3.2.2 开发的 RESTful API 服务，用于管理和展示爬虫获取的考研时政文章数据。系统提供文章管理、知识点管理、统计分析等功能，支持通过 Apifox 等工具进行接口测试。

## 技术栈

- **框架**: Spring Boot 3.2.2
- **ORM**: MyBatis Plus 3.5.5
- **数据库**: MySQL 8.0+
- **API文档**: SpringDoc OpenAPI 2.3.0
- **构建工具**: Maven
- **JDK版本**: Java 17（推荐）
- **测试框架**: JUnit 5 + Mockito
- **API测试工具**: Apifox

## 快速启动

### 前置要求

1. **安装 JDK 17**
   - 下载: https://adoptium.net/temurin/releases/?version=17
   - 安装路径: D:\doc\develop\environment\jdk17
   - 配置 JAVA_HOME 环境变量

2. **安装 Maven 3.6+**
   - 下载: https://maven.apache.org/download.cgi

3. **启动 MySQL 数据库**
   - 创建数据库: `yanshi`
   - 导入数据: 见 `database/` 目录

### 启动步骤

**方式一：使用 Java 17 脚本启动（推荐）**

Windows:
```bash
cd d:/doc/develop/yanshi/backend
powershell -ExecutionPolicy Bypass -File run-with-java17.ps1
```

**方式二：使用默认启动脚本**

Windows:
```bash
cd d:/doc/develop/yanshi/backend
start.bat
```

Linux/Mac:
```bash
cd /path/to/yanshi/backend
chmod +x start.sh
./start.sh
```

### 验证启动成功

看到以下日志表示启动成功：
```
Started YanshiBackendApplication in X.XXX seconds
```

## API 文档

### 访问地址

- **Swagger UI**: http://localhost:8080/api/swagger-ui.html
- **API JSON**: http://localhost:8080/api/v3/api-docs
- **服务根地址**: http://localhost:8080/api

### Apifox 导入

项目提供了完整的 API 文档文件，可直接导入 Apifox 进行测试：

#### 导入方式

**方式一：导入 OpenAPI YAML 文件**
1. 打开 Apifox
2. 点击 "导入" → "OpenAPI"
3. 选择 `src/main/resources/openapi.yaml`
4. 开始导入

**方式二：导入测试用例 JSON 文件**
1. 打开 Apifox
2. 点击 "导入" → "OpenAPI"
3. 选择 `apifox-test-cases.json`
4. 开始导入

**方式三：从 URL 导入（推荐）**
启动后端服务后，直接导入：
```
http://localhost:8080/api/v3/api-docs
```

详细导入说明请参考：[Apifox导入指南.md](Apifox导入指南.md)

### 主要接口

#### 文章管理

| 接口 | 方法 | 说明 | 参数 |
|------|------|------|------|
| `/articles` | GET | 分页查询文章列表 | title, source, category, startDate, endDate, current, size |
| `/articles/{id}` | GET | 查询文章详情 | id (路径参数) |
| `/articles/recent` | GET | 获取最新文章 | limit (默认10) |
| `/articles/statistics` | GET | 获取统计信息 | 无 |
| `/articles/statistics/source` | GET | 按来源统计 | 无 |
| `/articles/statistics/category` | GET | 按分类统计 | 无 |
| `/articles/statistics/date` | GET | 按日期统计 | startDate, endDate (可选) |

#### 知识点管理

| 接口 | 方法 | 说明 | 参数 |
|------|------|------|------|
| `/knowledge-points` | GET | 获取所有知识点 | 无 |
| `/knowledge-points/{id}` | GET | 根据ID查询 | id (路径参数) |
| `/knowledge-points/category/{category}` | GET | 按分类查询 | category (路径参数) |
| `/knowledge-points/top` | GET | 获取顶级知识点 | 无 |

### 请求示例

```bash
# 查询文章列表
curl "http://localhost:8080/articles?current=1&size=10"

# 查询文章详情
curl "http://localhost:8080/articles/1"

# 获取最新文章
curl "http://localhost:8080/articles/recent?limit=5"

# 获取统计信息
curl "http://localhost:8080/articles/statistics"

# 按日期统计
curl "http://localhost:8080/articles/statistics/date?startDate=2024-01-01&endDate=2024-12-31"

# 查询知识点
curl "http://localhost:8080/knowledge-points"

# 根据分类查询知识点
curl "http://localhost:8080/knowledge-points/category/政治"
```

## 配置说明

### 数据库配置

配置文件: `src/main/resources/application.yml`

```yaml
spring:
  datasource:
    url: jdbc:mysql://localhost:3306/yanshi?useUnicode=true&characterEncoding=utf8&useSSL=false&serverTimezone=Asia/Shanghai
    username: root
    password: root
    driver-class-name: com.mysql.cj.jdbc.Driver
```

### 服务器配置

```yaml
server:
  port: 8080
```

### MyBatis Plus 配置

```yaml
mybatis-plus:
  configuration:
    map-underscore-to-camel-case: true
    log-impl: org.apache.ibatis.logging.stdout.StdOutImpl
  global-config:
    db-config:
      logic-delete-field: deleted
      logic-delete-value: 1
      logic-not-delete-value: 0
```

## 项目结构

```
backend/
├── src/
│   ├── main/
│   │   ├── java/com/yanshi/
│   │   │   ├── YanshiBackendApplication.java    # 主启动类
│   │   │   ├── common/
│   │   │   │   └── Result.java                  # 统一响应类
│   │   │   ├── config/
│   │   │   │   ├── CorsConfig.java              # 跨域配置
│   │   │   │   ├── OpenApiConfig.java           # API文档配置
│   │   │   │   └── MyMetaObjectHandler.java     # 字段自动填充
│   │   │   ├── controller/
│   │   │   │   ├── ArticleController.java      # 文章控制器
│   │   │   │   └── KnowledgePointController.java # 知识点控制器
│   │   │   ├── dto/
│   │   │   │   ├── ArticleQueryDTO.java         # 文章查询DTO
│   │   │   │   └── ArticleStatisticsDTO.java   # 统计DTO
│   │   │   ├── entity/
│   │   │   │   ├── Article.java                # 文章实体
│   │   │   │   └── KnowledgePoint.java         # 知识点实体
│   │   │   ├── mapper/
│   │   │   │   ├── ArticleMapper.java          # 文章Mapper接口
│   │   │   │   └── KnowledgePointMapper.java   # 知识点Mapper接口
│   │   │   └── service/
│   │   │       ├── ArticleService.java        # 文章服务接口
│   │   │       ├── KnowledgePointService.java  # 知识点服务接口
│   │   │       └── impl/
│   │   │           ├── ArticleServiceImpl.java     # 文章服务实现
│   │   │           └── KnowledgePointServiceImpl.java # 知识点服务实现
│   │   └── resources/
│   │       ├── application.yml                  # 应用配置
│   │       ├── openapi.yaml                    # OpenAPI 3.0文档
│   │       └── mapper/                          # MyBatis映射文件
│   │           ├── ArticleMapper.xml
│   │           └── KnowledgePointMapper.xml
│   └── test/
│       └── java/com/yanshi/                    # 测试代码
│           ├── controller/
│           ├── service/
│           └── common/
├── pom.xml                                      # Maven配置
├── apifox-test-cases.json                       # Apifox测试用例
├── Apifox导入指南.md                            # Apifox导入说明
├── run-with-java17.ps1                          # Java 17启动脚本
├── run-with-java17.bat                          # Java 17启动脚本(BAT)
├── start.bat                                    # Windows启动脚本
├── start.sh                                     # Linux/Mac启动脚本
└── README.md                                    # 本文档
```

## 响应格式

所有接口返回统一格式：

```json
{
  "code": 200,
  "message": "success",
  "data": { ... }
}
```

- **code**: 状态码 (200=成功, 500=失败)
- **message**: 提示信息
- **data**: 返回数据

## 测试

### 运行测试

```bash
# 运行所有测试
mvn test

# 运行特定测试类
mvn test -Dtest=ArticleControllerTest

# 运行特定测试方法
mvn test -Dtest=ArticleControllerTest#testGetArticleById_Success
```

### 测试覆盖率

```bash
# 生成测试报告
mvn test jacoco:report
```

报告位置: `target/site/jacoco/index.html`

## 常见问题

### Q1: 编译失败,提示Java版本?

**A**: 确保使用 Java 17，不要使用 Java 24。设置 JAVA_HOME 环境变量：

```bash
# Windows
set JAVA_HOME=D:\doc\develop\environment\jdk17
set PATH=%JAVA_HOME%\bin;%PATH%

# Linux/Mac
export JAVA_HOME=/path/to/jdk17
export PATH=$JAVA_HOME/bin:$PATH
```

### Q2: 启动失败,数据库连接错误?

**A**: 检查以下内容：
1. MySQL 是否启动
2. 数据库 `yanshi` 是否存在
3. 用户名密码是否正确
4. 检查 `application.yml` 中的数据库配置

### Q3: 端口8080被占用?

**A**: 修改 `application.yml` 中的 `server.port` 配置，或者结束占用 8080 端口的进程：

```bash
# Windows
netstat -ano | findstr :8080
taskkill /PID <进程ID> /F

# Linux/Mac
lsof -ti:8080 | xargs kill -9
```

### Q4: Swagger 无法访问?

**A**: 检查 context-path 配置，访问地址应该是：`http://localhost:8080/swagger-ui.html`

### Q5: 如何在 Apifox 中导入 API?

**A**: 参考 [Apifox导入指南.md](Apifox导入指南.md)，提供了三种导入方式：
1. 导入 openapi.yaml 文件
2. 导入 apifox-test-cases.json 文件
3. 从 URL 直接导入（推荐）

### Q6: 运行测试报错?

**A**: 确保以下几点：
1. Java 版本正确（Java 17）
2. 测试数据库配置正确
3. 依赖下载完成
4. 运行 `mvn clean test` 重新编译测试

## 数据库表结构

### articles (文章表)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | BIGINT | 主键，自增 |
| title | VARCHAR(500) | 标题 |
| source | VARCHAR(100) | 来源 (新华网/人民网) |
| url | VARCHAR(1000) | 文章链接 |
| url_hash | VARCHAR(64) | URL哈希值，用于去重 |
| content | TEXT | 文章内容 |
| summary | TEXT | 摘要 |
| keywords | VARCHAR(500) | 关键词，逗号分隔 |
| category | VARCHAR(100) | 分类 |
| publish_date | DATE | 发布日期 |
| publish_time | DATETIME | 发布时间 |
| crawl_time | DATETIME | 爬取时间 |
| importance_score | DECIMAL(5,2) | 重要性分数 (0-10) |
| status | VARCHAR(20) | 状态 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

### knowledge_points (知识点表)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | BIGINT | 主键，自增 |
| name | VARCHAR(200) | 知识点名称 |
| category | VARCHAR(100) | 分类 |
| description | TEXT | 描述 |
| parent_id | INT | 父知识点ID，NULL表示顶级 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

## 开发说明

### 代码规范

1. **不使用 Lombok**: 所有实体类使用手动 getter/setter
2. **日志使用**: 使用 SLF4J 进行日志记录
3. **统一响应**: 使用 Result 类封装返回结果
4. **RESTful 设计**: 遵循 RESTful API 设计规范
5. **异常处理**: 统一异常处理机制

### 新增接口步骤

1. 在 Controller 中添加接口，添加 Swagger 注解
2. 在 Service 中实现业务逻辑
3. 在 Mapper 中添加数据访问方法（如有需要）
4. 更新 openapi.yaml 文档（可选，自动生成）
5. 编写单元测试

### API 文档维护

项目使用 SpringDoc 自动生成 OpenAPI 3.0 文档：

1. 启动服务后访问 Swagger UI
2. 使用 `@Tag`、`@Operation` 等注解描述接口
3. 导出 OpenAPI 规范文件供 Apifox 导入

## 相关文档

- [Apifox导入指南.md](Apifox导入指南.md) - Apifox 使用说明
- [Java版本兼容性解决方案.md](Java版本兼容性解决方案.md) - Java 版本问题
- [项目重建完成.md](项目重建完成.md) - 项目重建说明
- [快速启动.md](快速启动.md) - 快速启动指南

## 联系方式

- 项目文档: docs/ 目录
- 问题反馈: 见项目主页
- 技术支持: 参考 README 和各文档

---

**祝使用愉快!**
