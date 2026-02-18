# 研时爬虫系统

从新华网、人民网等权威网站爬取时政文章并存储到MySQL数据库。

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置数据库连接

编辑 `config.py` 中的 `DB_CONFIG`:

```python
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'your_password',
    'database': 'yanshi',
    'charset': 'utf8mb4'
}
```

### 3. 运行爬虫

```bash
# 爬取所有数据源
python main.py

# 只爬取列表，不爬取详情
python main.py --no-detail

# 限制每个数据源爬取数量
python main.py --max 5

# 只爬取指定数据源
python main.py --source xinhua_index
```

## 使用方法

### 命令行参数

- `--max N`: 限制每个数据源爬取N篇文章
- `--source NAME`: 只爬取指定数据源(xinhua_index, xinhua_meeting, xinhua_comment, people_comment)
- `--no-detail`: 不爬取文章详情内容

### 定时任务

```bash
# 启动调度器(每天12:00执行)
python scheduler.py

# 立即执行一次
python scheduler.py --run
```

### 数据源配置

在 `config.py` 中配置数据源：

```python
DATA_SOURCES = {
    'xinhua_index': {
        'name': '新华网-首页',
        'url': 'http://www.news.cn/politics/leaders/index.htm',
        'enabled': True,
        'category': '最新报道'
    },
    'xinhua_meeting': {
        'name': '新华网-会议活动',
        'url': 'http://www.news.cn/politics/leaders/cpc20/hyhd.htm',
        'enabled': True,
        'category': '会议活动'
    },
    'xinhua_comment': {
        'name': '新华网-视评',
        'url': 'https://www.news.cn/comments/zt/xhwsp/index.html',
        'enabled': True,
        'category': '视评'
    },
    'people_comment': {
        'name': '人民网评',
        'url': 'http://opinion.people.com.cn/GB/223228/index.html',
        'enabled': True,
        'category': '人民网评'
    }
}
```

## 文件结构

```
crawler/
├── config.py            # 配置文件(数据库连接、数据源)
├── models.py            # 数据模型(Article类)
├── spiders.py           # 爬虫实现
├── db_storage.py        # 数据库操作
├── main.py              # 主程序入口
├── scheduler.py         # 定时任务调度器
├── ai_extract.py        # AI知识点抽取
├── requirements.txt     # Python依赖
└── logs/                # 日志目录
```

## 数据库表结构

```sql
CREATE TABLE articles (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(500) NOT NULL,
    source VARCHAR(50) NOT NULL,
    url_hash VARCHAR(64) UNIQUE,
    url VARCHAR(1000) NOT NULL,
    content TEXT,
    summary TEXT,
    keywords VARCHAR(500),
    category VARCHAR(100),
    publish_date DATE,
    publish_time DATETIME,
    crawl_time DATETIME,
    importance_score DECIMAL(3,2),
    status ENUM('pending', 'processing', 'completed', 'failed'),
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

## 爬虫特性

- **自动去重**: 使用URL哈希值避免重复存储
- **重试机制**: 失败请求最多重试3次
- **请求延迟**: 每次请求间隔2秒
- **User-Agent伪装**: 模拟真实浏览器
- **批量保存**: 提高数据库写入效率
- **HTML保留**: 文章内容保留原始HTML格式

## AI知识点抽取

支持使用通义千问 AI 模型从文章中抽取知识点：

```bash
# 为指定文章抽取知识点
python ai_extract.py --article-id 1

# 为所有未处理的文章抽取
python ai_extract.py --all
```

在 `config.py` 中配置 API 密钥。

## 支持的数据源

| 数据源 | URL | 说明 |
|--------|-----|------|
| 新华网-首页 | http://www.news.cn/politics/leaders/index.htm | 重要时政新闻 |
| 新华网-会议活动 | http://www.news.cn/politics/leaders/cpc20/hyhd.htm | 会议报道 |
| 新华网-视评 | https://www.news.cn/comments/zt/xhwsp/index.html | 视评类文章 |
| 人民网评 | http://opinion.people.com.cn/GB/223228/index.html | 人民网评论 |

## 许可证

本项目仅供学习研究使用,请遵守目标网站的robots.txt协议。
