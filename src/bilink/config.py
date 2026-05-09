from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Config(BaseSettings):
    """全局配置管理"""

    poll_interval: float = Field(default=1.0, description="轮询消息的时间间隔(秒)")
    cache_dir: str = Field(default="bilink_cache", description="缓存目录路径")
    timeout: float = Field(default=10.0, description="API请求超时时间")

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


config = Config()
