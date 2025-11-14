from typing import Dict, Any
from app.clients.http_client import HTTPClient
from app.core.config import settings


class PokeAPIClient:
    """PokeAPI 客户端"""
    
    def __init__(self):
        self.http_client = HTTPClient(
            base_url=settings.pokeapi_base_url,
            timeout=settings.pokeapi_timeout
        )
    
    async def get_pokemon(self, name_or_id: str) -> Dict[str, Any]:
        """获取宝可梦详细信息
        
        Args:
            name_or_id: 宝可梦的名称或 ID
        
        Returns:
            宝可梦的详细信息（JSON 格式）
        """
        endpoint = f"pokemon/{name_or_id.lower()}"
        return await self.http_client.get(endpoint)
    
    async def get_pokemon_species(self, name_or_id: str) -> Dict[str, Any]:
        """获取宝可梦物种信息
        
        Args:
            name_or_id: 宝可梦的名称或 ID
        
        Returns:
            宝可梦物种的详细信息（JSON 格式）
        """
        endpoint = f"pokemon-species/{name_or_id.lower()}"
        return await self.http_client.get(endpoint)
    
    async def get_pokemon_evolution_chain(self, chain_id: int) -> Dict[str, Any]:
        """获取宝可梦进化链信息
        
        Args:
            chain_id: 进化链 ID
        
        Returns:
            进化链的详细信息（JSON 格式）
        """
        endpoint = f"evolution-chain/{chain_id}"
        return await self.http_client.get(endpoint)