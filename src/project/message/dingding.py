from .base import MessageSender
import requests
import time, hmac, hashlib, base64
from urllib.parse import quote_plus


class DingDingSender(MessageSender):
    """钉钉自定义机器人发送器"""

    def __init__(self, webhook: str, secret: str = None):
        """初始化 webhook 和 secret"""
        self.webhook = webhook
        self.secret = secret

    def _sign(self):
        """根据 secret 生成签名"""
        if not self.secret:
            return None
        timestamp = str(round(time.time() * 1000))
        secret_enc = self.secret.encode('utf-8')
        string_to_sign = f'{timestamp}\n{self.secret}'
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        sign = quote_plus(base64.b64encode(hmac_code))
        return timestamp, sign

    def send(self, content: str) -> bool:
        """发送文本消息"""
        payload = {"msgtype":"text","text":{"content":content}}
        headers = {"Content-Type": "application/json;charset=utf-8"}
        if self.secret:
            timestamp, sign = self._sign()
            url = f"{self.webhook}&timestamp={timestamp}&sign={sign}"
        else:
            url = self.webhook
        try:
            resp = requests.post(url, json=payload, headers=headers, timeout=5)
            print(f"完事了啊, {resp.json()}")
            return resp.status_code == 200
        except Exception as e:
            print(f"[DingDing] 发送失败: {e}")
            return False