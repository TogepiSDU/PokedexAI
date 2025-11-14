from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from app.db.models import Pokemon, PokemonSpecies


class PokemonRepository:
    """宝可梦数据仓库 - 处理数据库交互"""
    
    @staticmethod
    async def get_pokemon(db: Session, name: str) -> Optional[Dict[str, Any]]:
        """获取宝可梦数据
        
        首先从数据库中查询，如果存在则返回，否则返回 None
        
        Args:
            db: 数据库会话
            name: 宝可梦名称
        
        Returns:
            宝可梦数据，如果不存在则返回 None
        """
        pokemon = db.query(Pokemon).filter(Pokemon.name == name.lower()).first()
        return pokemon.data if pokemon else None
    
    @staticmethod
    async def save_pokemon(db: Session, pokemon_data: Dict[str, Any]) -> None:
        """保存宝可梦数据到数据库
        
        Args:
            db: 数据库会话
            pokemon_data: 宝可梦数据
        """
        name = pokemon_data.get("name", "").lower()
        if not name:
            return
        
        # 检查是否已存在
        existing = db.query(Pokemon).filter(Pokemon.name == name).first()
        
        if existing:
            # 更新现有记录
            existing.data = pokemon_data
        else:
            # 创建新记录
            pokemon = Pokemon(
                id=pokemon_data.get("id"),
                name=name,
                data=pokemon_data
            )
            db.add(pokemon)
        
        db.commit()
    
    @staticmethod
    async def get_pokemon_species(db: Session, name: str) -> Optional[Dict[str, Any]]:
        """获取宝可梦物种数据
        
        首先从数据库中查询，如果存在则返回，否则返回 None
        
        Args:
            db: 数据库会话
            name: 宝可梦名称
        
        Returns:
            宝可梦物种数据，如果不存在则返回 None
        """
        species = db.query(PokemonSpecies).filter(PokemonSpecies.name == name.lower()).first()
        return species.data if species else None
    
    @staticmethod
    async def save_pokemon_species(db: Session, species_data: Dict[str, Any]) -> None:
        """保存宝可梦物种数据到数据库
        
        Args:
            db: 数据库会话
            species_data: 宝可梦物种数据
        """
        name = species_data.get("name", "").lower()
        if not name:
            return
        
        # 检查是否已存在
        existing = db.query(PokemonSpecies).filter(PokemonSpecies.name == name).first()
        
        if existing:
            # 更新现有记录
            existing.data = species_data
        else:
            # 创建新记录
            species = PokemonSpecies(
                id=species_data.get("id"),
                name=name,
                data=species_data
            )
            db.add(species)
        
        db.commit()