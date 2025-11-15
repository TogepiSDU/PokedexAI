"""应用配置管理

- 使用 pydantic-settings v2 从 .env 与环境变量加载配置
- 提供数据库、外部服务（Doubao/PokeAPI）与应用参数
- database_url 支持通过 DATABASE_URL_ENV 覆盖
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(str(Path(__file__).resolve().parents[3] / ".env"), override=False)
load_dotenv(str(Path(__file__).resolve().parents[2] / ".env"), override=False)
try:
    p = Path(__file__).resolve().parents[2] / ".env"
    if p.exists():
        for line in p.read_text(encoding="utf-8").splitlines():
            if line.startswith("DOUBAO_API_KEY="):
                import os as _os
                _os.environ["DOUBAO_API_KEY"] = line.split("=",1)[1].strip()
                break
except Exception:
    pass
from typing import Optional

class Settings(BaseSettings):
    """系统配置项

    所有字段均可通过 .env 或进程环境覆盖；参见 model_config 的 env_file 设置。
    """
    # MySQL 数据库配置
    db_host: str = "localhost"
    db_port: int = 3306
    db_user: str = "root"
    db_password: str = "123456"
    db_name: str = "pokedex_ai"
    # 可选：直接提供完整数据库URL以覆盖默认MySQL配置
    database_url_env: Optional[str] = None
    
    # Doubao API 配置
    doubao_api_key: str = ""
    doubao_api_base_url: str = "https://ark.cn-beijing.volces.com/api/v3"
    
    # PokeAPI 配置
    pokeapi_base_url: str = "https://pokeapi.co/api/v2"
    pokeapi_timeout: int = 10
    
    # 应用程序配置
    app_name: str = "Pokédex AI"
    app_version: str = "1.0.0"
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    debug: bool = True
    
    @property
    def database_url(self) -> str:
        """生成数据库连接 URL

        优先返回 DATABASE_URL_ENV，其次按 MySQL 连接串拼装。
        """
        if self.database_url_env:
            return self.database_url_env
        return f"mysql+pymysql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}?charset=utf8mb4"
    
    model_config = SettingsConfigDict(
        env_file=str(Path(__file__).resolve().parents[2] / ".env"),
        case_sensitive=False
    )

settings = Settings()