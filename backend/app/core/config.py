from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # MySQL 数据库配置
    mysql_host: str = "localhost"
    mysql_port: int = 3306
    mysql_user: str = "root"
    mysql_password: str = "123456"
    mysql_database: str = "pokedex_ai"
    
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
        return f"mysql+pymysql://{self.mysql_user}:{self.mysql_password}@{self.mysql_host}:{self.mysql_port}/{self.mysql_database}?charset=utf8mb4"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()