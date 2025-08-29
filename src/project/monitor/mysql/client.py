import pymysql


class MySQLClient:
    def __init__(self, cfg):
        self.cfg = cfg
        self._conn = None

    def connect(self):
        if self._conn:
            return self._conn
        self._conn = pymysql.connect(
            host=self.cfg["host"],
            port=int(self.cfg.get("port", 3306)),
            user=self.cfg["user"],
            password=self.cfg["password"],
            connect_timeout=int(self.cfg.get("timeout", 5)),
            autocommit=True,
            cursorclass=pymysql.cursors.DictCursor
        )
        return self._conn

    def query_one(self, sql):
        conn = self.connect()
        with conn.cursor() as cur:
            cur.execute(sql)
            return cur.fetchone()
    def query_all(self, sql):
        conn = self.connect()
        with conn.cursor() as cur:
            cur.execute(sql)
            return {row["Variable_name"]: row["Value"] for row in cur.fetchall()}

    def close(self):
        if self._conn:
            self._conn.close()
            self._conn = None