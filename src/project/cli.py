"""命令行入口"""

import click
import yaml

from project.main import main
from project.message.factory import build_sender
from project.monitor.mysql.service_checker import MySQLServiceChecker


@click.group()
def cli():
    """统一监控入口"""
    pass

@cli.command()
@click.option("--config", default="config.yaml", help="配置文件路径")
def check_all(config):
    """检查所有 MySQL 实例"""
    with open(config, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    instances = cfg.get("monitor", {}).get("mysql", [])
    if not instances:
        click.echo("❌ 没有在配置文件中找到 monitor.mysql 配置")
        return

    checker = MySQLServiceChecker(instances)


    alerts = []
    sender = build_sender(cfg.get("message", {}))

    # 调用mysql检测器
    alerts.extend(checker.check_all())

    for msg in alerts:
        sender.send(msg)

    if not alerts:
        sender.send("监控通过")

if __name__ == "__main__":
    cli()





