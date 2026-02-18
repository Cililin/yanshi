# 数据库存储模块
import logging
import pymysql
import hashlib
from datetime import datetime
from typing import List, Optional
from contextlib import contextmanager
from models import Article
from config import DB_CONFIG

logger = logging.getLogger(__name__)


def calculate_url_hash(url: str) -> str:
    """
    计算URL的哈希值(用于去重)
    
    Args:
        url: URL字符串
        
    Returns:
        SHA256哈希值(64字符)
    """
    return hashlib.sha256(url.encode('utf-8')).hexdigest()


class DatabaseManager:
    """数据库管理器"""
    
    def __init__(self, config: dict = None):
        """
        初始化数据库连接
        
        Args:
            config: 数据库配置字典
        """
        self.config = config or DB_CONFIG
        self.connection = None
        logger.info("数据库管理器初始化完成")
    
    @contextmanager
    def get_connection(self):
        """获取数据库连接(上下文管理器)"""
        conn = None
        try:
            conn = pymysql.connect(
                host=self.config['host'],
                port=self.config['port'],
                user=self.config['user'],
                password=self.config['password'],
                database=self.config['database'],
                charset=self.config['charset'],
                cursorclass=pymysql.cursors.DictCursor
            )
            yield conn
        except Exception as e:
            logger.error(f"数据库连接失败: {e}")
            raise
        finally:
            if conn:
                conn.close()
    
    def test_connection(self) -> bool:
        """测试数据库连接"""
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT 1")
                    result = cursor.fetchone()
                    if result:
                        logger.info("数据库连接测试成功")
                        return True
        except Exception as e:
            logger.error(f"数据库连接测试失败: {e}")
        return False
    
    def save_article(self, article: Article) -> Optional[int]:
        """
        保存单篇文章
        
        Args:
            article: 文章对象
            
        Returns:
            文章ID或None
        """
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    # 先检查是否已存在
                    url_hash = calculate_url_hash(article.url)
                    check_sql = "SELECT id FROM articles WHERE url_hash = %s"
                    cursor.execute(check_sql, (url_hash,))
                    existing = cursor.fetchone()
                    
                    if existing:
                        logger.debug(f"文章已存在,跳过: {article.url}")
                        return None
                    
                    # 插入新文章
                    sql = """
                    INSERT INTO articles (
                        title, source, url, url_hash, content, summary,
                        keywords, category, publish_date, publish_time, crawl_time,
                        importance_score, status
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                    )
                    """
                    
                    from datetime import datetime
                    now = datetime.now()
                    
                    cursor.execute(sql, (
                        article.title,
                        article.source,
                        article.url,
                        url_hash,
                        article.content,
                        article.summary,
                        article.keywords,
                        article.category,
                        article.publish_date,
                        article.publish_time if article.publish_time else now,
                        now,
                        0.50,  # 默认重要性评分
                        'completed'
                    ))
                    
                    article_id = cursor.lastrowid
                    conn.commit()
                    
                    logger.debug(f"保存文章成功: {article.title} (ID: {article_id})")
                    return article_id
                    
        except pymysql.IntegrityError as e:
            # URL重复,说明文章已存在
            logger.debug(f"文章已存在,跳过: {article.url}")
            return None
        except Exception as e:
            logger.error(f"保存文章失败: {article.title} - {e}")
            import traceback
            logger.error(traceback.format_exc())
            return None
    
    def save_articles_batch(self, articles: List[Article]) -> dict:
        """
        批量保存文章
        
        Args:
            articles: 文章列表
            
        Returns:
            统计信息字典
        """
        stats = {
            'total': len(articles),
            'success': 0,
            'failed': 0,
            'skipped': 0
        }
        
        for article in articles:
            article_id = self.save_article(article)
            if article_id:
                stats['success'] += 1
            elif article_id is None:
                stats['skipped'] += 1
            else:
                stats['failed'] += 1
        
        logger.info(f"批量保存完成: 成功={stats['success']}, 跳过={stats['skipped']}, 失败={stats['failed']}")
        return stats
    
    def get_articles_by_date(self, start_date: datetime, end_date: datetime, 
                             limit: int = 100) -> List[dict]:
        """
        按日期范围查询文章
        
        Args:
            start_date: 开始日期
            end_date: 结束日期
            limit: 返回数量限制
            
        Returns:
            文章列表
        """
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    sql = """
                    SELECT * FROM articles
                    WHERE publish_date BETWEEN %s AND %s
                    ORDER BY publish_date DESC
                    LIMIT %s
                    """
                    
                    cursor.execute(sql, (start_date, end_date, limit))
                    articles = cursor.fetchall()
                    
                    logger.info(f"查询到 {len(articles)} 篇文章 ({start_date} - {end_date})")
                    return articles
                    
        except Exception as e:
            logger.error(f"查询文章失败: {e}")
            return []
    
    def get_article_count(self) -> int:
        """获取文章总数"""
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT COUNT(*) as count FROM articles")
                    result = cursor.fetchone()
                    return result['count'] if result else 0
        except Exception as e:
            logger.error(f"获取文章总数失败: {e}")
            return 0
    
    def get_stats_by_source(self) -> List[dict]:
        """按数据源统计文章数量"""
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    sql = """
                    SELECT 
                        source,
                        COUNT(*) as count,
                        MIN(publish_date) as min_date,
                        MAX(publish_date) as max_date
                    FROM articles
                    GROUP BY source
                    ORDER BY count DESC
                    """
                    cursor.execute(sql)
                    return cursor.fetchall()
        except Exception as e:
            logger.error(f"统计文章失败: {e}")
            return []
    
    def get_recent_articles(self, limit: int = 20) -> List[dict]:
        """获取最新文章"""
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    sql = """
                    SELECT * FROM articles
                    WHERE status = 'completed'
                    ORDER BY crawl_time DESC
                    LIMIT %s
                    """
                    cursor.execute(sql, (limit,))
                    return cursor.fetchall()
        except Exception as e:
            logger.error(f"获取最新文章失败: {e}")
            return []
    
    def delete_article_by_url(self, url: str) -> bool:
        """
        根据URL删除文章
        
        Args:
            url: 文章URL
            
        Returns:
            是否成功
        """
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    sql = "DELETE FROM articles WHERE url = %s"
                    cursor.execute(sql, (url,))
                    conn.commit()
                    
                    logger.info(f"删除文章: {url}")
                    return True
        except Exception as e:
            logger.error(f"删除文章失败: {e}")
            return False
