"""企业微信消息发送模块"""

from .base import MessageSender
import requests


class WeComSender(MessageSender):
    """企业微信发送器"""

    def __init__(self, webhook: str):
        self.webhook = webhook

    def send(self, content: str) -> bool:
        """发送文本消息"""
        payload = {"msgtype": "text", "text": {"content": content}}
        try:
            resp = requests.post(self.webhook, json=payload, timeout=5)
            return resp.status_code == 200
        except:
            return False
