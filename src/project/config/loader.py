"""配置加载器"""
import os, yaml
from pathlib import Path


class ConfigLoader:
    def __init__(self, config_path=None):
        self.path = Path(config_path or os.getenv("PROJECT_CONFIG") or "config/config.yaml")
        self._config = None

    def load(self):
        if not self.path.exists():
            raise FileNotFoundError(f"配置文件 {self.path} 不存在")
        with open(self.path, "r", encoding="utf-8") as f:
            self._config = yaml.safe_load(f)
        return self._config

    @property
    def config(self):
        if self._config is None:
            return self.load()
        return self._config
