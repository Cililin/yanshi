# 数据模型定义
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Article:
    """文章数据模型"""
    title: str
    url: str
    source: str
    category: str
    publish_date: Optional[datetime] = None
    content: Optional[str] = None
    summary: Optional[str] = None
    keywords: Optional[str] = None
    publish_time: Optional[datetime] = None
    crawl_time: Optional[datetime] = field(default_factory=datetime.now)
    
    def to_dict(self):
        """转换为字典"""
        return {
            'title': self.title,
            'url': self.url,
            'source': self.source,
            'category': self.category,
            'publish_date': self.publish_date,
            'publish_time': self.publish_time,
            'crawl_time': self.crawl_time,
            'content': self.content,
            'summary': self.summary,
            'keywords': self.keywords
        }
