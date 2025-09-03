import shutil
import time

import psutil

from .client import MySQLClient

# ================= 阈值配置 =================
DEFAULT_THRESHOLDS = {
    "threads_connected": 200,  # 最大连接数告警
    "qps": 500,  # 每秒查询数
    "slow_queries": 10,  # 慢查询累计值
    "disk_usage": 85,  # 磁盘使用率 (%)
    "io_wait": 30  # IO 等待 (%)
}


# ================= MySQL Service Checker =================
class MySQLServiceChecker:
    def __init__(self, instances, thresholds=None):
        self.instances = instances
        self.thresholds = thresholds or DEFAULT_THRESHOLDS

    def check_all(self):
        alerts = []
        for inst in self.instances:
            alerts.extend(self.check_instance(inst))
        return alerts

    def check_instance(self, inst):
        alerts = []
        client = MySQLClient(inst)

        try:
            # 第一次采样
            status1 = client.query_all("SHOW GLOBAL STATUS")
            queries1 = int(status1.get("Queries", 0))

            # 等待 1 秒后采样
            time.sleep(1)
            status2 = client.query_all("SHOW GLOBAL STATUS")
            queries2 = int(status2.get("Queries", 0))

            # 采集指标
            threads = int(status2.get("Threads_connected", 0))
            qps = queries2 - queries1
            slow = int(status2.get("Slow_queries", 0))

            # 磁盘使用率
            total, used, free = shutil.disk_usage("/")
            disk_usage = used * 100 / total

            # IO 等待
            cpu_times = psutil.cpu_times_percent(interval=1)
            io_wait = getattr(cpu_times, "iowait", 0)

            # 阈值检查
            if threads > self.thresholds["threads_connected"]:
                alerts.append(f"⚠️ MySQL实例 {inst['name']} 连接数过高: {threads}")
            if qps > self.thresholds["qps"]:
                alerts.append(f"⚠️ MySQL实例 {inst['name']} QPS 过高: {qps}")
            if slow > self.thresholds["slow_queries"]:
                alerts.append(f"⚠️ MySQL实例 {inst['name']} 慢查询累计过多: {slow}")
            if disk_usage > self.thresholds["disk_usage"]:
                alerts.append(f"⚠️ MySQL实例 {inst['name']} 磁盘使用率过高: {disk_usage:.2f}%")
            if io_wait > self.thresholds["io_wait"]:
                alerts.append(f"⚠️ MySQL实例 {inst['name']} IO等待过高: {io_wait:.2f}%")

        except Exception as e:
            alerts.append(f"❌ MySQL实例 {inst.get('name', 'unknown')} 检查失败: {e}")
        finally:
            client.close()

        return alerts
