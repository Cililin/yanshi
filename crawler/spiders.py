# 基础爬虫类
import logging
import time
import requests
from bs4 import BeautifulSoup
from typing import List, Optional
from urllib.parse import urljoin
from models import Article
from config import CRAWLER_CONFIG

logger = logging.getLogger(__name__)


class BaseSpider:
    """爬虫基类"""
    
    def __init__(self, source_config: dict):
        """
        初始化爬虫
        
        Args:
            source_config: 数据源配置字典
        """
        self.name = source_config['name']
        self.url = source_config['url']
        self.base_url = source_config.get('base_url', '')
        self.category = source_config.get('category', '未分类')
        self.enabled = source_config.get('enabled', True)
        
        # 请求会话
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': CRAWLER_CONFIG['user_agent']
        })
        
        logger.info(f"初始化爬虫: {self.name}")
    
    def fetch_html(self, url: str) -> Optional[str]:
        """
        获取HTML内容
        
        Args:
            url: 目标URL
            
        Returns:
            HTML字符串或None
        """
        for attempt in range(CRAWLER_CONFIG['max_retries']):
            try:
                logger.debug(f"请求URL: {url} (尝试 {attempt + 1}/{CRAWLER_CONFIG['max_retries']})")
                response = self.session.get(
                    url,
                    timeout=CRAWLER_CONFIG['timeout']
                )
                response.raise_for_status()
                
                # 设置正确的编码
                if response.encoding == 'ISO-8859-1':
                    response.encoding = 'utf-8'
                
                logger.info(f"成功获取: {url} (状态码: {response.status_code})")
                return response.text
                
            except requests.RequestException as e:
                logger.error(f"请求失败: {url} - {str(e)}")
                if attempt < CRAWLER_CONFIG['max_retries'] - 1:
                    time.sleep(CRAWLER_CONFIG['delay'])
        
        return None
    
    def parse_article_list(self, html: str) -> List[Article]:
        """
        解析文章列表(子类实现)
        
        Args:
            html: HTML字符串
            
        Returns:
            文章列表
        """
        raise NotImplementedError("子类必须实现此方法")
    
    def parse_article_detail(self, html: str) -> dict:
        """
        解析文章详情(子类实现)
        
        Args:
            html: HTML字符串
            
        Returns:
            文章详情字典
        """
        raise NotImplementedError("子类必须实现此方法")
    
    def crawl_list(self) -> List[Article]:
        """
        爬取文章列表
        
        Returns:
            文章列表
        """
        if not self.enabled:
            logger.info(f"爬虫 {self.name} 已禁用,跳过")
            return []
        
        logger.info(f"开始爬取: {self.name}")
        
        html = self.fetch_html(self.url)
        if not html:
            logger.error(f"获取 {self.name} 列表失败")
            return []
        
        articles = self.parse_article_list(html)
        logger.info(f"{self.name} 解析到 {len(articles)} 篇文章")
        
        # 延迟,避免请求过快
        time.sleep(CRAWLER_CONFIG['delay'])
        
        return articles
    
    def crawl_detail(self, article: Article) -> Article:
        """
        爬取文章详情

        Args:
            article: 文章对象

        Returns:
            包含详情的文章对象
        """
        full_url = urljoin(self.base_url, article.url)
        html = self.fetch_html(full_url)

        if not html:
            logger.error(f"获取文章详情失败: {full_url}")
            return article

        detail = self.parse_article_detail(html)

        # 更新文章内容
        article.content = detail.get('content', '')
        article.summary = detail.get('summary', '')
        article.keywords = detail.get('keywords', article.keywords)
        if detail.get('publish_time'):
            article.publish_time = detail.get('publish_time')

        logger.debug(f"成功获取详情: {article.title}")

        return article
    
    def close(self):
        """关闭爬虫"""
        self.session.close()
        logger.info(f"爬虫 {self.name} 已关闭")


class XinhuaIndexSpider(BaseSpider):
    """新华网首页爬虫"""
    
    def parse_article_list(self, html: str) -> List[Article]:
        """解析新华网首页文章列表"""
        from datetime import datetime
        soup = BeautifulSoup(html, 'html.parser')
        articles = []
        
        # 方法1: 查找 .column-center-item (主要文章列表)
        for item in soup.select('.column-center-item'):
            title_elem = item.select_one('.tit a, .tit span a')
            if not title_elem:
                continue
            
            title = title_elem.get_text(strip=True)
            url = title_elem.get('href', '')
            
            if not title or not url:
                continue
            
            # 转换相对URL为绝对URL
            full_url = urljoin(self.base_url, url)
            
            article = Article(
                title=title,
                url=full_url,
                source='新华网',
                category=self.category
            )
            articles.append(article)
        
        # 方法2: 查找 .xpage-content-list li (备用)
        if not articles:
            for li in soup.select('.xpage-content-list li'):
                title_elem = li.select_one('.tit a, .tit span')
                if not title_elem:
                    continue
                
                title = title_elem.get_text(strip=True)
                url = title_elem.get('href', '')
                
                if not title or not url:
                    continue
                
                full_url = urljoin(self.base_url, url)
                
                article = Article(
                    title=title,
                    url=full_url,
                    source='新华网',
                    category=self.category
                )
                articles.append(article)
        
        return articles
    
    def parse_article_detail(self, html: str) -> dict:
        """解析新华网文章详情"""
        from datetime import datetime
        soup = BeautifulSoup(html, 'html.parser')

        # 查找文章内容 - 新华网文章在 #detail 下的 #detailContent 中
        content_container = soup.select_one('#detailContent')
        if not content_container:
            # 备用方案
            content_container = soup.select_one('#detail')
            if not content_container:
                content_container = soup.select_one('article')

        # 提取 HTML 内容
        content_html = ''
        if content_container:
            # 克隆容器，避免修改原始 HTML
            container_copy = content_container.__copy__()

            # 移除不需要的元素
            for tag in container_copy(['script', 'style', 'nav', 'header', 'footer',
                                     'div.player-container', 'div.advertisement',
                                     'div.share', 'div.related']):
                tag.decompose()

            # 获取 HTML 内容
            content_html = str(container_copy).strip()

        # 提取摘要（纯文本）
        summary = ''
        if content_container:
            # 移除不需要的元素
            for tag in content_container(['script', 'style', 'nav', 'header', 'footer',
                                        'div.player-container', 'div.advertisement']):
                tag.decompose()
            text_content = content_container.get_text(separator='\n', strip=True)
            summary = text_content[:300] if text_content else ''

        # 提取发布时间
        publish_time = None
        time_elem = soup.select_one('.date, .time, .publish-time, #pubtime')
        if time_elem:
            time_text = time_elem.get_text(strip=True)
            try:
                # 尝试解析各种时间格式
                for fmt in ['%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M', '%Y-%m-%d',
                           '%Y年%m月%d日 %H:%M', '%Y年%m月%d日']:
                    try:
                        publish_time = datetime.strptime(time_text, fmt)
                        break
                    except ValueError:
                        continue
            except:
                pass

        # 提取关键词
        keywords = ''
        keywords_elem = soup.select_one('.keywords, .tags, .article-keywords')
        if keywords_elem:
            keywords = keywords_elem.get_text(strip=True)

        return {
            'content': content_html,
            'summary': summary,
            'publish_time': publish_time,
            'keywords': keywords
        }


class XinhuaMeetingSpider(BaseSpider):
    """新华网会议活动爬虫"""
    
    def parse_article_list(self, html: str) -> List[Article]:
        """解析新华网会议活动列表"""
        from datetime import datetime
        soup = BeautifulSoup(html, 'html.parser')
        articles = []
        
        # 查找列表项 .xpage-content-list li
        for li in soup.select('.xpage-content-list li'):
            title_elem = li.select_one('.tit a')
            time_elem = li.select_one('.time')
            
            if not title_elem:
                continue
            
            title = title_elem.get_text(strip=True)
            url = title_elem.get('href', '')
            
            if not title or not url:
                continue
            
            # 解析时间
            publish_date = None
            if time_elem:
                time_text = time_elem.get_text(strip=True)
                try:
                    publish_date = datetime.strptime(time_text, '%Y-%m-%d').date()
                except ValueError:
                    pass
            
            full_url = urljoin(self.base_url, url)
            
            article = Article(
                title=title,
                url=full_url,
                source='新华网',
                category=self.category,
                publish_date=publish_date
            )
            articles.append(article)
        
        return articles
    
    def parse_article_detail(self, html: str) -> dict:
        """解析新华网会议活动文章详情"""
        return XinhuaIndexSpider.parse_article_detail(self, html)


class XinhuaCommentSpider(BaseSpider):
    """新华网视评爬虫"""
    
    def parse_article_list(self, html: str) -> List[Article]:
        """解析新华网视评文章列表"""
        from datetime import datetime
        soup = BeautifulSoup(html, 'html.parser')
        articles = []
        
        # 查找列表项 .part02_con li
        for li in soup.select('.part02_con li'):
            title_elem = li.select_one('.h3Tit a, h3 a')
            
            if not title_elem:
                continue
            
            title = title_elem.get_text(strip=True)
            url = title_elem.get('href', '')
            
            if not title or not url:
                continue
            
            # 从URL中提取日期 (格式: /comments/20260214/...)
            import re
            date_match = re.search(r'/(\d{4})(\d{2})(\d{2})/', url)
            if date_match:
                try:
                    year, month, day = date_match.groups()
                    publish_date = datetime(int(year), int(month), int(day)).date()
                except ValueError:
                    publish_date = None
            else:
                publish_date = None
            
            full_url = urljoin(self.base_url, url)
            
            article = Article(
                title=title,
                url=full_url,
                source='新华网',
                category=self.category,
                publish_date=publish_date
            )
            articles.append(article)
        
        return articles
    
    def parse_article_detail(self, html: str) -> dict:
        """解析新华网视评文章详情"""
        return XinhuaIndexSpider.parse_article_detail(self, html)


class PeopleCommentSpider(BaseSpider):
    """人民网评爬虫"""
    
    def parse_article_list(self, html: str) -> List[Article]:
        """解析人民网评文章列表"""
        from datetime import datetime
        
        soup = BeautifulSoup(html, 'html.parser')
        articles = []
        
        # 查找列表项 .list_14 li
        for li in soup.select('.list_14 li'):
            link = li.select_one('a')
            time_elem = li.select_one('i.gray')
            
            if not link:
                continue
            
            title = link.get_text(strip=True)
            url = link.get('href', '')
            
            if not title or not url:
                continue
            
            # 解析时间
            publish_date = None
            if time_elem:
                time_text = time_elem.get_text(strip=True)
                try:
                    # 格式: 2026-02-14 09:51
                    publish_date = datetime.strptime(time_text, '%Y-%m-%d %H:%M')
                except ValueError:
                    pass
            
            full_url = urljoin(self.base_url, url)
            
            article = Article(
                title=title,
                url=full_url,
                source='人民网',
                category=self.category,
                publish_date=publish_date
            )
            articles.append(article)
        
        return articles
    
    def parse_article_detail(self, html: str) -> dict:
        """解析人民网评文章详情"""
        from datetime import datetime
        soup = BeautifulSoup(html, 'html.parser')

        # 查找文章内容 - 人民网文章在 .show_text #rm_txt_zw 中
        content_container = soup.select_one('.show_text, #rm_txt_zw, .rm_txt_con, article')

        # 提取 HTML 内容
        content_html = ''
        if content_container:
            # 克隆容器，避免修改原始 HTML
            container_copy = content_container.__copy__()

            # 移除不需要的元素
            for tag in container_copy(['script', 'style', 'nav', 'header', 'footer',
                                     'div.voice-wrap', 'div.edit', 'div.share',
                                     'div.advertisement', 'div.related']):
                tag.decompose()

            # 获取 HTML 内容
            content_html = str(container_copy).strip()

        # 提取摘要（纯文本）
        summary = ''
        if content_container:
            # 移除不需要的元素
            for tag in content_container(['script', 'style', 'nav', 'header', 'footer',
                                        'div.voice-wrap', 'div.edit', 'div.share']):
                tag.decompose()
            text_content = content_container.get_text(separator='\n', strip=True)
            summary = text_content[:300] if text_content else ''

        # 提取发布时间
        publish_time = None
        time_elem = soup.select_one('.date, .time, .publish-time, .gray, .channel-01')
        if time_elem:
            time_text = time_elem.get_text(strip=True)
            try:
                # 尝试解析各种时间格式
                for fmt in ['%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M', '%Y-%m-%d',
                           '%Y年%m月%d日 %H:%M', '%Y年%m月%d日']:
                    try:
                        publish_time = datetime.strptime(time_text, fmt)
                        break
                    except ValueError:
                        continue
            except:
                pass

        # 提取关键词
        keywords = ''
        keywords_elem = soup.select_one('.keywords, .tags, .article-keywords')
        if keywords_elem:
            keywords = keywords_elem.get_text(strip=True)

        return {
            'content': content_html,
            'summary': summary,
            'publish_time': publish_time,
            'keywords': keywords
        }


# 爬虫工厂
def create_spider(source_key: str, source_config: dict) -> BaseSpider:
    """
    创建爬虫实例
    
    Args:
        source_key: 数据源键
        source_config: 数据源配置
        
    Returns:
        爬虫实例
    """
    spider_map = {
        'xinhua_index': XinhuaIndexSpider,
        'xinhua_meeting': XinhuaMeetingSpider,
        'xinhua_comment': XinhuaCommentSpider,
        'people_comment': PeopleCommentSpider
    }
    
    spider_class = spider_map.get(source_key)
    if not spider_class:
        raise ValueError(f"未知的爬虫类型: {source_key}")
    
    return spider_class(source_config)
