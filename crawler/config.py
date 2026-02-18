# 爬虫配置文件
import os

# 数据库配置
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'root',
    'database': 'yanshi',
    'charset': 'utf8mb4'
}

# 爬虫配置
CRAWLER_CONFIG = {
    # 请求超时时间(秒)
    'timeout': 30,
    # 请求间隔(秒)
    'delay': 2,
    # 最大重试次数
    'max_retries': 3,
    # User-Agent
    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
}

# 数据源配置
DATA_SOURCES = {
    'xinhua_index': {
        'name': '新华网-首页',
        'url': 'http://www.news.cn/politics/leaders/index.htm',
        'base_url': 'http://www.news.cn',
        'enabled': True,
        'category': '最新报道'
    },
    'xinhua_meeting': {
        'name': '新华网-会议活动',
        'url': 'http://www.news.cn/politics/leaders/cpc20/hyhd.htm',
        'base_url': 'http://www.news.cn',
        'enabled': True,
        'category': '会议活动'
    },
    'xinhua_comment': {
        'name': '新华网-视评',
        'url': 'https://www.news.cn/comments/zt/xhwsp/index.html',
        'base_url': 'https://www.news.cn',
        'enabled': True,
        'category': '新华网视评'
    },
    'people_comment': {
        'name': '人民网评',
        'url': 'http://opinion.people.com.cn/GB/223228/index.html',
        'base_url': 'http://opinion.people.com.cn',
        'enabled': True,
        'category': '人民网评'
    },
    'people_home': {
        'name': '人民网-首页',
        'url': 'http://www.people.com.cn',
        'base_url': 'http://www.people.com.cn',
        'enabled': False,
        'category': '要闻'
    }
}

# 日志配置
LOG_DIR = os.path.join(os.path.dirname(__file__), 'logs')
os.makedirs(LOG_DIR, exist_ok=True)

LOG_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'standard',
            'stream': 'ext://sys.stdout'
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'DEBUG',
            'formatter': 'standard',
            'filename': os.path.join(LOG_DIR, 'crawler.log'),
            'maxBytes': 10485760,  # 10MB
            'backupCount': 5
        }
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['console', 'file']
    }
}
