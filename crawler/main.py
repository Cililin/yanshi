#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
研时-考研时政智能分析系统 爬虫主程序
功能:爬取新华网、人民网等权威媒体的时政文章
"""

import logging
import logging.config
from datetime import datetime
from typing import List
from models import Article
from config import DATA_SOURCES, LOG_CONFIG
from spiders import create_spider
from db_storage import DatabaseManager

# 配置日志
logging.config.dictConfig(LOG_CONFIG)
logger = logging.getLogger(__name__)


class YanshiCrawler:
    """研时爬虫主类"""
    
    def __init__(self):
        """初始化爬虫"""
        self.db = DatabaseManager()
        self.spiders = {}
        logger.info("=" * 60)
        logger.info("研时爬虫系统启动")
        logger.info("=" * 60)
    
    def init_spiders(self):
        """初始化所有爬虫"""
        logger.info("初始化爬虫实例...")
        
        for source_key, source_config in DATA_SOURCES.items():
            if source_config.get('enabled', False):
                try:
                    spider = create_spider(source_key, source_config)
                    self.spiders[source_key] = spider
                    logger.info(f"✓ 初始化爬虫: {source_config['name']}")
                except Exception as e:
                    logger.error(f"✗ 初始化爬虫失败: {source_key} - {e}")
    
    def test_database(self) -> bool:
        """测试数据库连接"""
        logger.info("测试数据库连接...")
        if self.db.test_connection():
            logger.info("✓ 数据库连接正常")
            return True
        else:
            logger.error("✗ 数据库连接失败")
            return False
    
    def crawl_all(self, fetch_detail: bool = False, max_articles: int = None) -> dict:
        """
        爬取所有数据源

        Args:
            fetch_detail: 是否爬取文章详情
            max_articles: 每个数据源最大爬取数量

        Returns:
            统计信息
        """
        total_stats = {
            'total_articles': 0,
            'saved_articles': 0,
            'skipped_articles': 0,
            'sources': {}
        }

        logger.info("开始爬取所有数据源...")
        logger.info("-" * 60)

        for source_key, spider in self.spiders.items():
            source_name = DATA_SOURCES[source_key]['name']
            logger.info(f"\n[{source_name}] 开始爬取...")

            try:
                # 爬取文章列表
                articles = spider.crawl_list()

                # 限制数量
                if max_articles and len(articles) > max_articles:
                    articles = articles[:max_articles]
                    logger.info(f"  限制爬取数量为: {max_articles}")

                total_stats['total_articles'] += len(articles)

                if not articles:
                    logger.info(f"  未获取到文章")
                    continue

                # 可选:爬取文章详情
                if fetch_detail:
                    logger.info(f"  开始爬取详情 ({len(articles)} 篇)...")
                    for i, article in enumerate(articles, 1):
                        spider.crawl_detail(article)
                        if i % 5 == 0:
                            logger.info(f"  进度: {i}/{len(articles)}")

                # 保存到数据库
                save_stats = self.db.save_articles_batch(articles)

                source_stats = {
                    'name': source_name,
                    'crawled': len(articles),
                    'saved': save_stats['success'],
                    'skipped': save_stats['skipped']
                }

                total_stats['saved_articles'] += save_stats['success']
                total_stats['skipped_articles'] += save_stats['skipped']
                total_stats['sources'][source_key] = source_stats

                logger.info(f"  ✓ 完成: 爬取={len(articles)}, 保存={save_stats['success']}, 跳过={save_stats['skipped']}")

            except Exception as e:
                logger.error(f"  ✗ 爬取失败: {e}")
                import traceback
                logger.error(traceback.format_exc())
                total_stats['sources'][source_key] = {
                    'name': source_name,
                    'error': str(e)
                }

        logger.info("-" * 60)
        return total_stats
    
    def crawl_source(self, source_key: str, fetch_detail: bool = False) -> dict:
        """
        爬取指定数据源
        
        Args:
            source_key: 数据源键
            fetch_detail: 是否爬取详情
            
        Returns:
            统计信息
        """
        if source_key not in self.spiders:
            logger.error(f"未知的爬虫: {source_key}")
            return {'error': 'Unknown spider'}
        
        spider = self.spiders[source_key]
        source_name = DATA_SOURCES[source_key]['name']
        
        logger.info(f"\n[{source_name}] 开始爬取...")
        
        try:
            articles = spider.crawl_list()
            
            if fetch_detail:
                logger.info(f"爬取详情 ({len(articles)} 篇)...")
                for article in articles:
                    spider.crawl_detail(article)
            
            save_stats = self.db.save_articles_batch(articles)
            
            stats = {
                'name': source_name,
                'crawled': len(articles),
                'saved': save_stats['success'],
                'skipped': save_stats['skipped']
            }
            
            logger.info(f"完成: 爬取={len(articles)}, 保存={save_stats['success']}, 跳过={save_stats['skipped']}")
            return stats
            
        except Exception as e:
            logger.error(f"爬取失败: {e}")
            return {'error': str(e)}
    
    def show_stats(self):
        """显示统计信息"""
        logger.info("\n" + "=" * 60)
        logger.info("数据库统计")
        logger.info("=" * 60)
        
        total_count = self.db.get_article_count()
        logger.info(f"文章总数: {total_count}")
        
        source_stats = self.db.get_stats_by_source()
        if source_stats:
            logger.info("\n按来源统计:")
            for stat in source_stats:
                logger.info(f"  {stat['source']}: {stat['count']} 篇")
        
        recent = self.db.get_recent_articles(limit=5)
        if recent:
            logger.info("\n最新文章:")
            for article in recent:
                logger.info(f"  - {article['title'][:50]}... ({article['publish_date']})")
    
    def cleanup(self):
        """清理资源"""
        for spider in self.spiders.values():
            spider.close()
        logger.info("爬虫系统已关闭")


def main():
    """主函数"""
    import sys
    import argparse

    # 创建爬虫实例
    crawler = YanshiCrawler()

    # 解析命令行参数
    parser = argparse.ArgumentParser(description='研时爬虫 - 考研时政智能分析系统')
    parser.add_argument('--no-detail', action='store_true', help='不爬取文章详情')
    parser.add_argument('--max', type=int, help='每个数据源最大爬取数量')
    parser.add_argument('--source', type=str, help='指定爬取的数据源 (xinhua_index/xinhua_meeting/xinhua_comment/people_comment)')
    args = parser.parse_args()

    try:
        # 测试数据库连接
        if not crawler.test_database():
            logger.error("数据库连接失败,请检查配置")
            sys.exit(1)

        # 初始化爬虫
        crawler.init_spiders()

        if not crawler.spiders:
            logger.error("没有可用的爬虫")
            sys.exit(1)

        # 执行爬取
        if args.source:
            # 爬取指定数据源
            stats = crawler.crawl_source(args.source, fetch_detail=not args.no_detail)
        else:
            # 爬取所有数据源
            stats = crawler.crawl_all(fetch_detail=not args.no_detail, max_articles=args.max)

        # 显示统计
        crawler.show_stats()

        # 显示爬取结果
        logger.info("\n" + "=" * 60)
        logger.info("爬取统计汇总")
        logger.info("=" * 60)
        logger.info(f"总爬取: {stats['total_articles']} 篇")
        logger.info(f"成功保存: {stats['saved_articles']} 篇")
        logger.info(f"跳过(重复): {stats['skipped_articles']} 篇")
        logger.info(f"详情爬取: {'已启用' if not args.no_detail else '未启用'}")

        if stats.get('sources'):
            logger.info("\n各数据源详情:")
            for source_key, source_stats in stats['sources'].items():
                if 'error' in source_stats:
                    logger.info(f"  {source_stats['name']}: 失败 - {source_stats['error']}")
                else:
                    logger.info(f"  {source_stats['name']}: 爬取={source_stats['crawled']}, 保存={source_stats['saved']}, 跳过={source_stats['skipped']}")

        logger.info("=" * 60)
        logger.info("爬取完成!")

    except KeyboardInterrupt:
        logger.info("\n用户中断爬取")
    except Exception as e:
        logger.error(f"爬取过程出错: {e}", exc_info=True)
    finally:
        crawler.cleanup()


if __name__ == '__main__':
    main()
