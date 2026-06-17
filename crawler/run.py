"""R1 CLI 入口。

用法:
    python run.py init              # 建表
    python run.py --site lagou      # 跑拉勾（HTTP）
    python run.py --site lagou_stealth  # 跑拉勾（Playwright-stealth，反检测）
    python run.py --site 51job      # 跑前程无忧（HTTP）
    python run.py --site 51job_stealth # 跑前程无忧（Playwright-stealth）
    python run.py --site bosszhipin # 跑 BOSS（Playwright-stealth）
    python run.py --site all        # 跑 3 个站点（HTTP 版）
    python run.py --site stealth_all    # 跑 3 个站点（stealth 版）
    python run.py stats             # 统计
"""
from __future__ import annotations

import argparse
import asyncio
import json
import logging
import sys
from pathlib import Path

# 让脚本可独立运行
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from crawler import config  # noqa: E402
from crawler.persistence import dao  # noqa: E402
from crawler.persistence.models import JdStatus  # noqa: E402

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
log = logging.getLogger("r1")


def cmd_init(_args):
    log.info("建表...")
    dao.init_schema()
    log.info("OK")


def cmd_stats(_args):
    log.info("统计 jd_raw ...")
    total = dao.count_jd()
    by_status = dao.count_by_status()
    print(json.dumps({"total": total, "by_status": by_status}, ensure_ascii=False, indent=2))


def _scrapy_settings() -> dict:
    """Scrapy 公共 settings（含入库 pipeline）。"""
    return {
        "USER_AGENT": config.USER_AGENTS[0],
        "ROBOTSTXT_OBEY": True,
        "DOWNLOAD_DELAY": 2,
        "CONCURRENT_REQUESTS": 1,
        "LOG_LEVEL": "INFO",
        "ITEM_PIPELINES": {
            "crawler.pipelines.storage.JdStoragePipeline": 300,
        },
    }


def cmd_crawl_lagou(args):
    from crawler.spiders.lagou import LagouSpider
    from scrapy.crawler import CrawlerProcess

    process = CrawlerProcess(settings=_scrapy_settings())
    process.crawl(LagouSpider, max_per_site=args.max)
    process.start()


def cmd_crawl_51job(args):
    from crawler.spiders.job51 import Job51Spider
    from scrapy.crawler import CrawlerProcess

    process = CrawlerProcess(settings=_scrapy_settings())
    process.crawl(Job51Spider, max_per_site=args.max)
    process.start()


def cmd_crawl_boss(args):
    from crawler.spiders.boss import run_sync
    items = run_sync(keyword=args.keyword or "python", max_count=args.max, proxy=args.proxy)
    log.info("BOSS 拿到 %d 条", len(items))
    inserted = 0
    for it in items:
        rec = {
            "source_site": it["source_site"],
            "source_url": it["source_url"],
            "raw_html": it["raw_html"],
            "clean_text": it["clean_text"],
            "job_title": it["job_title"],
            "company": it["company"],
            "salary_min": it["salary_min"],
            "salary_max": it["salary_max"],
            "location": it["location"],
            "publish_date": it["publish_date"],
            "content_hash": it["content_hash"],  # spider 已计算
            "status": JdStatus.raw,
        }
        r = dao.upsert_jd(rec)
        if r == "inserted":
            inserted += 1
    log.info("BOSS 入库 %d 条", inserted)


def cmd_crawl_lagou_stealth(args):
    from crawler.spiders.lagou_stealth import run_sync
    items = run_sync(keyword=args.keyword or "python", max_count=args.max, proxy=args.proxy)
    log.info("拉勾(stealth) 拿到 %d 条", len(items))
    inserted = 0
    for it in items:
        rec = {
            "source_site": it["source_site"],
            "source_url": it["source_url"],
            "raw_html": it["raw_html"],
            "clean_text": it["clean_text"],
            "job_title": it["job_title"],
            "company": it["company"],
            "salary_min": it["salary_min"],
            "salary_max": it["salary_max"],
            "location": it["location"],
            "publish_date": it["publish_date"],
            "content_hash": it["content_hash"],
            "status": JdStatus.raw,
        }
        r = dao.upsert_jd(rec)
        if r == "inserted":
            inserted += 1
    log.info("拉勾(stealth) 入库 %d 条", inserted)


def cmd_crawl_51job_stealth(args):
    from crawler.spiders.job51_stealth import run_sync
    items = run_sync(keyword=args.keyword or "python", max_count=args.max, proxy=args.proxy)
    log.info("51job(stealth) 拿到 %d 条", len(items))
    inserted = 0
    for it in items:
        rec = {
            "source_site": it["source_site"],
            "source_url": it["source_url"],
            "raw_html": it["raw_html"],
            "clean_text": it["clean_text"],
            "job_title": it["job_title"],
            "company": it["company"],
            "salary_min": it["salary_min"],
            "salary_max": it["salary_max"],
            "location": it["location"],
            "publish_date": it["publish_date"],
            "content_hash": it["content_hash"],
            "status": JdStatus.raw,
        }
        r = dao.upsert_jd(rec)
        if r == "inserted":
            inserted += 1
    log.info("51job(stealth) 入库 %d 条", inserted)


def _add_common_args(sp):
    """给 spider 子命令加通用参数。"""
    sp.add_argument("--max", type=int, default=config.MAX_PER_SITE)
    sp.add_argument("--keyword", default="python")
    sp.add_argument("--proxy", help="代理地址 (http://user:pass@host:port)")


def main():
    p = argparse.ArgumentParser(prog="r1-crawler")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("init", help="建 jd_raw / compliance_log 表")
    sub.add_parser("stats", help="统计 jd_raw")

    # HTTP 版 spider
    for site, fn in (("lagou", cmd_crawl_lagou), ("51job", cmd_crawl_51job)):
        sp = sub.add_parser(site, help=f"爬 {site} (HTTP)")
        _add_common_args(sp)
        sp.set_defaults(func=fn)

    # BOSS（已经是 Playwright）
    sp_boss = sub.add_parser("bosszhipin", help="爬 BOSS 直聘 (Playwright-stealth)")
    _add_common_args(sp_boss)
    sp_boss.set_defaults(func=cmd_crawl_boss)

    # Playwright-stealth 版
    for site, fn in (
        ("lagou_stealth", cmd_crawl_lagou_stealth),
        ("51job_stealth", cmd_crawl_51job_stealth),
    ):
        sp = sub.add_parser(site, help=f"爬 {site} (Playwright-stealth)")
        _add_common_args(sp)
        sp.set_defaults(func=fn)

    # all = HTTP 版 3 站点
    sp_all = sub.add_parser("all", help="跑 3 个站点 (HTTP)")
    _add_common_args(sp_all)
    sp_all.set_defaults(func=lambda a: (
        cmd_crawl_lagou(argparse.Namespace(max=a.max, keyword=a.keyword, proxy=None)),
        cmd_crawl_51job(argparse.Namespace(max=a.max, keyword=a.keyword, proxy=None)),
        cmd_crawl_boss(argparse.Namespace(max=a.max, keyword=a.keyword, proxy=None)),
    ))

    # stealth_all = stealth 版 3 站点
    sp_stealth_all = sub.add_parser("stealth_all", help="跑 3 个站点 (Playwright-stealth)")
    _add_common_args(sp_stealth_all)
    sp_stealth_all.set_defaults(func=lambda a: (
        cmd_crawl_lagou_stealth(argparse.Namespace(max=a.max, keyword=a.keyword, proxy=a.proxy)),
        cmd_crawl_51job_stealth(argparse.Namespace(max=a.max, keyword=a.keyword, proxy=a.proxy)),
        cmd_crawl_boss(argparse.Namespace(max=a.max, keyword=a.keyword, proxy=a.proxy)),
    ))

    args = p.parse_args()
    if args.cmd == "init":
        cmd_init(args)
    elif args.cmd == "stats":
        cmd_stats(args)
    elif hasattr(args, "func"):
        args.func(args)
    else:
        p.print_help()


if __name__ == "__main__":
    main()
