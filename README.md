# 研时-考研时政智能分析系统

<div align="center">

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Language](https://img.shields.io/badge/language-Java%20%2B%20Python%20%2B%20JavaScript-orange.svg)

一个为考研学生提供时政资料收集、分析和智能处理的系统

[功能特性](#功能特性) • [快速开始](#快速开始) • [技术架构](#技术架构) • [项目文档](#项目文档)

</div>

## 📋 目录

- [项目简介](#项目简介)
- [功能特性](#功能特性)
- [技术架构](#技术架构)
- [快速开始](#快速开始)
- [系统预览](#系统预览)
- [项目文档](#项目文档)
- [开发指南](#开发指南)
- [许可证](#许可证)

---

## 🎯 项目简介

研时系统是一个基于AI的考研时政智能分析平台，通过Python爬虫自动获取新华网、人民网等权威网站时政文章，利用AI技术进行内容提炼和知识点抽取，建立结构化时政知识库，帮助考研学生高效学习时政知识。

### 适用场景

- 考研政治科目备考
- 时政热点学习
- 知识点整理复习
- 时政题目分析

---

## ✨ 功能特性

### 🤖 数据采集与处理

- **自动爬取**: 每日定时自动爬取权威网站时政文章
- **多源聚合**: 支持新华网、人民网等多个权威数据源
- **智能去重**: 基于URL哈希自动去重，避免重复数据
- **内容结构化**: 将非结构化文章转换为结构化数据存储

### 🧠 AI智能分析

- **知识点抽取**: 使用通义千问AI自动抽取重要知识点
- **智能分类**: 自动识别文章分类和知识点类型
- **知识关联**: 建立知识点之间的语义关联
- **知识图谱**: 可视化展示知识点网络

### 📊 数据查询与分析

- **灵活查询**: 支持时间范围、分类、关键词等多维查询
- **时间轴分析**: 按时间维度展示时政事件脉络
- **统计分析**: 按来源、分类、日期等多维度统计分析
- **数据导出**: 支持CSV格式数据导出

### 🎨 现代化界面

- **北欧风格**: 简约优雅的北欧设计风格
- **响应式设计**: 支持PC和移动端
- **数据可视化**: ECharts图表展示统计数据
- **交互友好**: 直观的操作界面和流畅的交互体验

---

## 🏗 技术架构

### 技术栈

```
┌─────────────────────────────────────────┐
│           前端技术                       │
│  Vue 3.4+  |  Element Plus 2.4+         │
│  ECharts 6.0+  |  Vite 5.0+             │
├─────────────────────────────────────────┤
│           后端技术                       │
│  Spring Boot 3.2+  |  MyBatis-Plus      │
│  SpringDoc 2.3+                        │
├─────────────────────────────────────────┤
│           爬虫与AI                       │
│  Python 3.10+  |  Requests 2.31+        │
│  BeautifulSoup 4.12+  |  Dashscope       │
├─────────────────────────────────────────┤
│           数据存储                       │
│  MySQL 8.0+  |  Redis 7.0+              │
└─────────────────────────────────────────┘
```

### 系统架构

```
用户层 (Web / 微信小程序)
    ↓
网关层 (Nginx)
    ↓
应用层 (Spring Boot)
    ↓
数据层 (Python爬虫 + AI抽取)
    ↓
存储层 (MySQL + Redis)
```

---

## 🚀 快速开始

### 环境要求

- **Java**: JDK 17+
- **Python**: 3.10+
- **Node.js**: 16+
- **MySQL**: 8.0+
- **Redis**: 7.0+

### 安装步骤

#### 1. 克隆项目

```bash
git clone https://github.com/your-username/yanshi.git
cd yanshi
```

#### 2. 数据库初始化

```bash
# 创建数据库
mysql -u root -p < database/init.sql
```

#### 3. 配置爬虫

```bash
cd crawler

# 安装Python依赖
pip install -r requirements.txt

# 配置数据库连接 (编辑 config.py)
# 配置通义千问API密钥 (编辑 config.py)

# 测试爬虫
python main.py
```

#### 4. 启动后端

```bash
cd backend

# 修改 application.yml 中的数据库配置

# 启动后端服务
mvn spring-boot:run
```

后端服务启动在: `http://localhost:8080/api`

#### 5. 启动前端

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端服务启动在: `http://localhost:3000`

#### 6. 访问系统

打开浏览器访问: http://localhost:3000

---

## 📸 系统预览

### 功能模块

- **文章列表**: 浏览和搜索时政文章
- **文章详情**: 查看文章完整内容
- **知识点管理**: 浏览和管理知识点
- **知识图谱**: 可视化展示知识点关联
- **统计分析**: 多维度数据统计

---

## 📚 项目文档

详细的技术文档请查看 `docs/` 目录：

| 文档 | 说明 |
|------|------|
| [0.项目概述-研时系统.md](./docs/0.项目概述-研时系统.md) | 项目概述、功能介绍、系统架构 |
| [1.爬虫系统技术文档.md](./docs/1.爬虫系统技术文档.md) | 爬虫系统架构、数据模型、API文档 |
| [2.后端系统技术文档.md](./docs/2.后端系统技术文档.md) | 后端架构、接口说明、开发指南 |
| [3.前端系统技术文档.md](./docs/3.前端系统技术文档.md) | 前端架构、页面功能、设计风格 |
| [4.功能拓展-知识点抽取.md](./docs/4.功能拓展-知识点抽取.md) | AI知识点抽取功能、API文档、配置说明 |

---

## 🛠 开发指南

### 爬虫开发

```bash
cd crawler

# 运行爬虫
python main.py

# 只爬取列表，不爬取详情
python main.py --no-detail

# 限制每个数据源爬取数量
python main.py --max 5

# 只爬取指定数据源
python main.py --source xinhua_index

# 启动定时调度器
python scheduler.py

# 立即执行一次
python scheduler.py --run

# AI知识点抽取
python ai_extract.py --article-id 1
python ai_extract.py --all
```

### 后端开发

```bash
cd backend

# 启动开发服务器
mvn spring-boot:run

# 访问API文档
# http://localhost:8080/swagger-ui.html

# 运行测试
mvn test

# 打包
mvn clean package
```

### 前端开发

```bash
cd frontend

# 启动开发服务器
npm run dev

# 构建生产版本
npm run build

# 预览构建
npm run preview
```

---

## 🤝 贡献指南

欢迎贡献代码！请遵循以下步骤：

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

### 代码规范

- 遵循项目现有的代码风格
- 添加必要的注释和文档
- 确保代码通过测试
- 提交前格式化代码

---

## 📄 许可证

本项目采用 Apache License Version 2.0 许可证 - 详见 [LICENSE](LICENSE) 文件

---

<div align="center">

**如果觉得项目有帮助，请给个 ⭐️ Star 支持一下！**

Made with ❤️ by 研时团队

</div>
