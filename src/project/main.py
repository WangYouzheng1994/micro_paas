"""项目主入口，加载配置 -> 初始化消息发送器 -> 监控实例 -> 发送告警"""
import yaml

from project.config.loader import ConfigLoader
from project.monitor.mysql.service_checker import MySQLServiceChecker
from project.message.factory import build_sender


def main():
    """
    给cli脚本用的

    :return:
    """
    config = ConfigLoader().config
    sender = build_sender(config.get("message", {}))

    alerts = []
    # 调用mysql检测器
    alerts.extend(MySQLServiceChecker(config["monitor"].get("mysql", [])).check_all())

    for msg in alerts:
        sender.send(msg)

    if not alerts:
        sender.send("监控通过")


def run_checks(config):
    """本地调试执行监控任务"""
    # config = ConfigLoader().config
    sender = build_sender(config.get("message", {}))

    alerts = []
    # 调用mysql检测器
    alerts.extend(MySQLServiceChecker(config["monitor"].get("mysql", [])).check_all())
    # 调用redis检测器
    # alerts.extend(RedisServiceChecker(config["monitor"].get("redis", [])).check_all())
    # 调用oracle检测器
    # alerts.extend(OracleServiceChecker(config["monitor"].get("oracle", [])).check_all())

    for msg in alerts:
        sender.send(msg)

    if not alerts:
        sender.send("监控通过")


"""
此方法主要是用于调试，手动加载指定的配置文件。因为使用了poetry来进行项目打包管理，需要用poetry进行run，但是不利于调试（环境配置问题）
"""
if __name__ == "__main__":
    main()
    # test() 本地调试用


def test():
    with open("../../config/config.yaml", "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
        run_checks(config)
