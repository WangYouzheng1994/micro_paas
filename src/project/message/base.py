"""消息发送基类模块"""

from abc import ABC, abstractmethod


class MessageSender(ABC):
    """消息发送抽象类"""

    @abstractmethod
    def send(self, content: str) -> bool:
        """发送消息方法，必须实现"""
        raise NotImplementedError
