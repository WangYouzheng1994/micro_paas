"""Oracle 监控服务检查模块"""

try:
    import cx_Oracle
except ImportError:
    cx_Oracle = None

class OracleServiceChecker:
    """Oracle 监控器"""

    def __init__(self, instances):
        self.instances = instances

    def check_all(self):
        """检查所有 Oracle 实例状态"""
        alerts = []
        if cx_Oracle is None:
            alerts.append("cx_Oracle 未安装，无法检查 Oracle")
            return alerts

        for inst in self.instances:
            dsn = cx_Oracle.makedsn(inst["host"], inst["port"], service_name=inst["service_name"])
            try:
                conn = cx_Oracle.connect(inst["user"], inst["password"], dsn, encoding="UTF-8")
                conn.close()
            except:
                alerts.append(f"Oracle {inst['name']} 不可用")
        return alerts
