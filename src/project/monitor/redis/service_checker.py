"""Redis 监控服务检查模块"""

import redis

import redis
import psutil

# TODO：默认配置，需要在配置文件中支持可配。
DEFAULT_THRESHOLDS = {
    "connected_clients": 1000,  # 最大连接数
    "used_memory_mb": 1024,  # 内存使用 (MB)
    "blocked_clients": 10,  # 阻塞客户端数
    "cpu_usage": 80  # CPU 使用率 (%)
}


class RedisServiceChecker:
    def __init__(self, instances, thresholds=None):
        self.instances = instances
        self.thresholds = thresholds or DEFAULT_THRESHOLDS

    def check_all(self):
        """
        监测配置文件中的所有节点
        :return:
        """
        alerts = []
        for inst in self.instances:
            alerts.extend(self.check_instance(inst))
        return alerts

    def check_instance(self, inst):
        """
        监测指定的节点
        :param inst:
        :return:
        """
        alerts = []
        try:
            r = redis.StrictRedis(
                host=inst["host"],
                port=inst.get("port", 6379),
                db=inst.get("db", 0),
                password=inst.get("password", None),
                decode_responses=True,
                socket_connect_timeout=5
            )

            info = r.info()

            connected_clients = info.get("connected_clients", 0)
            used_memory_mb = int(info.get("used_memory", 0)) / 1024 / 1024
            blocked_clients = info.get("blocked_clients", 0)

            cpu_percent = psutil.cpu_percent(interval=1)

            if connected_clients > self.thresholds["connected_clients"]:
                alerts.append(f"⚠️ Redis实例 {inst['name']} 连接数过高: {connected_clients}")
            if used_memory_mb > self.thresholds["used_memory_mb"]:
                alerts.append(f"⚠️ Redis实例 {inst['name']} 内存使用过高: {used_memory_mb:.2f}MB")
            if blocked_clients > self.thresholds["blocked_clients"]:
                alerts.append(f"⚠️ Redis实例 {inst['name']} 阻塞客户端数过高: {blocked_clients}")
            if cpu_percent > self.thresholds["cpu_usage"]:
                alerts.append(f"⚠️ Redis实例 {inst['name']} CPU使用率过高: {cpu_percent}%")

        except Exception as e:
            alerts.append(f"❌ Redis实例 {inst.get('name', 'unknown')} 检查失败: {e}")

        return alerts
