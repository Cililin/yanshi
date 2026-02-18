#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
研时-定时任务调度器
功能:每日12点定时爬取文章数据
"""

import logging
import logging.config
import schedule
import time
from datetime import datetime
from main import YanshiCrawler
from config import LOG_CONFIG

# 配置日志
log_config = LOG_CONFIG.copy()
log_config['handlers']['file']['filename'] = 'logs/scheduler.log'

logging.config.dictConfig(log_config)
logger = logging.getLogger(__name__)


class CrawlerScheduler:
    """爬虫定时任务调度器"""
    
    def __init__(self):
        """初始化调度器"""
        self.crawler = None
        self.is_running = False
        
    def init_crawler(self):
        """初始化爬虫"""
        try:
            logger.info("初始化爬虫实例...")
            self.crawler = YanshiCrawler()
            
            # 测试数据库连接
            if not self.crawler.test_database():
                logger.error("数据库连接失败，定时任务无法启动")
                return False
            
            # 初始化爬虫
            self.crawler.init_spiders()
            
            if not self.crawler.spiders:
                logger.error("没有可用的爬虫，定时任务无法启动")
                return False
            
            logger.info(f"成功初始化 {len(self.crawler.spiders)} 个爬虫")
            return True
            
        except Exception as e:
            logger.error(f"初始化爬虫失败: {e}", exc_info=True)
            return False
    
    def crawl_job(self):
        """爬取任务"""
        if self.is_running:
            logger.warning("爬取任务正在运行中，跳过本次调度")
            return
        
        self.is_running = True
        start_time = datetime.now()
        logger.info("=" * 80)
        logger.info(f"定时爬取任务开始: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info("=" * 80)
        
        try:
            # 重新初始化爬虫以确保连接正常
            if not self.crawler:
                if not self.init_crawler():
                    logger.error("爬虫初始化失败，终止任务")
                    return
            
            # 执行爬取，默认不爬取详情以提高速度
            stats = self.crawler.crawl_all(fetch_detail=False)
            
            # 显示统计
            self.crawler.show_stats()
            
            # 输出结果
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            logger.info("\n" + "=" * 80)
            logger.info("定时爬取任务完成")
            logger.info("=" * 80)
            logger.info(f"开始时间: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
            logger.info(f"结束时间: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
            logger.info(f"耗时: {duration:.2f} 秒")
            logger.info(f"总爬取: {stats['total_articles']} 篇")
            logger.info(f"成功保存: {stats['saved_articles']} 篇")
            logger.info(f"跳过重复: {stats['skipped_articles']} 篇")
            
            if stats['sources']:
                logger.info("\n各数据源:")
                for source_key, source_stats in stats['sources'].items():
                    if 'error' in source_stats:
                        logger.info(f"  {source_stats['name']}: 失败 - {source_stats['error']}")
                    else:
                        logger.info(f"  {source_stats['name']}: 爬取={source_stats['crawled']}, 保存={source_stats['saved']}")
            
            logger.info("=" * 80)
            
        except Exception as e:
            logger.error(f"定时爬取任务执行失败: {e}", exc_info=True)
        
        finally:
            self.is_running = False
            logger.info("任务状态重置为空闲\n")
    
    def run_once(self):
        """立即执行一次爬取任务"""
        logger.info("立即执行模式: 手动触发爬取任务")
        self.crawl_job()
    
    def run_scheduler(self):
        """运行定时调度器"""
        logger.info("=" * 80)
        logger.info("研时定时任务调度器启动")
        logger.info("=" * 80)
        
        # 初始化爬虫
        if not self.init_crawler():
            logger.error("爬虫初始化失败，程序退出")
            return
        
        # 设置定时任务：每天12:00执行
        schedule.every().day.at("12:00").do(self.crawl_job)
        
        # 可选: 设置额外的调度时间
        # schedule.every().day.at("08:00").do(self.crawl_job)
        # schedule.every(6).hours.do(self.crawl_job)
        
        logger.info("定时任务已配置: 每天 12:00 执行")
        logger.info("输入 'q' 或 'quit' 退出程序")
        logger.info("输入 'r' 或 'run' 立即执行一次爬取")
        logger.info("=" * 80 + "\n")
        
        # 启动时立即执行一次（可选）
        # logger.info("启动时立即执行一次爬取...")
        # self.crawl_job()
        
        # 运行调度循环
        import sys
        import platform

        try:
            if platform.system() == 'Windows':
                # Windows环境: 使用msvcrt进行非阻塞输入检测
                try:
                    import msvcrt
                    while True:
                        schedule.run_pending()

                        # 检查是否有按键
                        if msvcrt.kbhit():
                            cmd = msvcrt.getch().decode('utf-8').lower()
                            if cmd == 'q':
                                logger.info("接收到退出指令，程序即将退出")
                                break
                            elif cmd == 'r':
                                logger.info("接收到手动执行指令")
                                self.crawl_job()
                            elif cmd == 's':
                                logger.info("下次执行时间:")
                                for job in schedule.get_jobs():
                                    logger.info(f"  {job.next_run}")

                        time.sleep(1)
                except ImportError:
                    # Windows但msvcrt不可用，使用简化模式
                    logger.warning("Windows环境下无法启用交互模式，使用简化运行模式")
                    while True:
                        schedule.run_pending()
                        time.sleep(1)
            else:
                # Linux/Mac环境: 使用select进行非阻塞输入检测
                import select
                while True:
                    schedule.run_pending()

                    if select.select([sys.stdin], [], [], 0.1)[0]:
                        cmd = sys.stdin.readline().strip().lower()
                        if cmd in ['q', 'quit', 'exit']:
                            logger.info("接收到退出指令，程序即将退出")
                            break
                        elif cmd in ['r', 'run']:
                            logger.info("接收到手动执行指令")
                            self.crawl_job()
                        elif cmd == 's':
                            logger.info("下次执行时间:")
                            for job in schedule.get_jobs():
                                logger.info(f"  {job.next_run}")

                    time.sleep(1)

        except KeyboardInterrupt:
            logger.info("\n接收到中断信号，程序即将退出")
        
        finally:
            # 清理资源
            if self.crawler:
                self.crawler.cleanup()
            logger.info("定时任务调度器已关闭")


def main():
    """主函数"""
    import sys
    
    scheduler = CrawlerScheduler()
    
    # 检查命令行参数
    if len(sys.argv) > 1:
        if sys.argv[1] in ['--run', '-r']:
            # 立即执行一次模式
            scheduler.init_crawler()
            scheduler.run_once()
        else:
            print("用法:")
            print("  python scheduler.py           # 启动定时调度器（每天12:00执行）")
            print("  python scheduler.py --run     # 立即执行一次爬取任务")
            print("  python scheduler.py -r        # 立即执行一次爬取任务")
            sys.exit(0)
    else:
        # 定时调度模式
        scheduler.run_scheduler()


if __name__ == '__main__':
    main()
