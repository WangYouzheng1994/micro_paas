"""Redis 监控服务检查模块"""

import redis

class RedisServiceChecker:
    """Redis 监控器"""

    def __init__(self, instances):
        self.instances = instances

    def check_all(self):
        """检查所有 Redis 实例状态"""
        alerts = []
        for inst in self.instances:
            try:
                r = redis.Redis(host=inst["host"], port=inst["port"], db=inst.get("db",0), password=inst.get("password",""))
                if not r.ping():
                    alerts.append(f"Redis {inst['name']} 不可用")
            except:
                alerts.append(f"Redis {inst['name']} 不可用")
        return alerts
