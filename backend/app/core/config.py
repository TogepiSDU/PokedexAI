from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # MySQL 数据库配置
    db_host: str = "localhost"
    db_port: int = 3306
    db_user: str = "root"
    db_password: str = "123456"
    db_name: str = "pokedex_ai"
    
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
        return f"mysql+pymysql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}?charset=utf8mb4"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()