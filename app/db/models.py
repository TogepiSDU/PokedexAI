from sqlalchemy import Column, Integer, String, DateTime, JSON
from sqlalchemy.sql import func

from app.db.base import Base


class Pokemon(Base):
    """宝可梦数据模型 - 缓存 /pokemon API 返回的数据"""
    __tablename__ = "pokemon"
    
    id = Column(Integer, primary_key=True, index=True, comment="宝可梦 ID，对应 PokeAPI ID")
    name = Column(String(64), unique=True, index=True, comment="宝可梦英文名（小写）")
    data = Column(JSON, comment="/pokemon/{name} 接口返回的完整 JSON 数据")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="数据更新时间")


class PokemonSpecies(Base):
    """宝可梦物种数据模型 - 缓存 /pokemon-species API 返回的数据"""
    __tablename__ = "pokemon_species"
    
    id = Column(Integer, primary_key=True, index=True, comment="宝可梦物种 ID，对应 PokeAPI species ID")
    name = Column(String(64), unique=True, index=True, comment="宝可梦物种英文名（小写）")
    data = Column(JSON, comment="/pokemon-species/{name} 接口返回的完整 JSON 数据")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="数据更新时间")