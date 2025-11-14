from typing import Dict, Any
from sqlalchemy.orm import Session
from app.clients.pokeapi_client import PokeAPIClient
from app.repositories.pokemon_repository import PokemonRepository


class PokemonService:
    """宝可梦服务 - 处理宝可梦数据的获取和缓存"""
    
    def __init__(self):
        self.pokeapi_client = PokeAPIClient()
        self.pokemon_repository = PokemonRepository()
    
    async def get_pokemon(self, db: Session, name: str) -> Dict[str, Any]:
        """获取宝可梦数据
        
        首先从数据库缓存中查询，如果不存在则从 PokeAPI 获取并缓存
        
        Args:
            db: 数据库会话
            name: 宝可梦名称
        
        Returns:
            宝可梦的详细信息
        """
        # 先从数据库缓存中查询
        pokemon_data = await self.pokemon_repository.get_pokemon(db, name)
        
        if not pokemon_data:
            # 如果数据库中没有，则从 PokeAPI 获取
            pokemon_data = await self.pokeapi_client.get_pokemon(name)
            # 将获取的数据存入数据库缓存
            await self.pokemon_repository.save_pokemon(db, pokemon_data)
        
        return pokemon_data
    
    async def get_pokemon_species(self, db: Session, name: str) -> Dict[str, Any]:
        """获取宝可梦物种数据
        
        首先从数据库缓存中查询，如果不存在则从 PokeAPI 获取并缓存
        
        Args:
            db: 数据库会话
            name: 宝可梦名称
        
        Returns:
            宝可梦物种的详细信息
        """
        # 先从数据库缓存中查询
        species_data = await self.pokemon_repository.get_pokemon_species(db, name)
        
        if not species_data:
            # 如果数据库中没有，则从 PokeAPI 获取
            species_data = await self.pokeapi_client.get_pokemon_species(name)
            # 将获取的数据存入数据库缓存
            await self.pokemon_repository.save_pokemon_species(db, species_data)
        
        return species_data
    
    async def get_evolution_chain(self, chain_id: int) -> Dict[str, Any]:
        """获取宝可梦进化链信息
        
        Args:
            chain_id: 进化链 ID
        
        Returns:
            进化链的详细信息
        """
        # 直接从 PokeAPI 获取，不缓存（进化链数据相对稳定且不频繁使用）
        return await self.pokeapi_client.get_pokemon_evolution_chain(chain_id)