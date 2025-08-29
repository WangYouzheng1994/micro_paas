"""
消息发送器工厂：根据配置创建 Sender。
"""
from typing import Dict

from .base import MessageSender
from .dingding import DingDingSender
from .wecom import WeComSender


def build_sender(cfg: Dict) -> MessageSender:
    """
    根据配置构建消息发送器。
    cfg 形如：
    {
      "channel": "dingding" | "wecom",
      "dingding": {"webhook": "..."},
      "wecom": {"webhook": "..."}
    }
    """
    channel = (cfg.get("channel") or "").lower()
    if channel == "dingding":
        ding_cfg = cfg.get("dingding", {})
        return DingDingSender(
            webhook=ding_cfg.get("webhook"),
            secret=ding_cfg.get("secret")
        )
    if channel == "wecom":
        return WeComSender(cfg["wecom"]["webhook"])
    raise ValueError(f"不支持的消息通道: {channel}")