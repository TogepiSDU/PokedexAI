"""图鉴问答服务

职责：编排意图解析 → 数据获取（PokeAPI/缓存） → 回答生成（Doubao/兜底）。
"""
from typing import Dict, Any
from sqlalchemy.orm import Session
from app.clients.doubao_client import DoubaoClient
from app.services.intent_parser_service import IntentParserService
from app.services.pokemon_service import PokemonService


class DexQAService:
    """处理整个图鉴问答流程的应用服务"""
    
    def __init__(self):
        self.intent_parser_service = IntentParserService()
        self.pokemon_service = PokemonService()
        self.doubao_client = DoubaoClient()
    
    async def answer_question(self, db: Session, question: str) -> Dict[str, Any]:
        """回答用户的宝可梦问题
        
        Args:
            db: 数据库会话
            question: 用户的自然语言问题
        
        Returns:
            包含回答和相关信息的字典
        """
        # 1. 解析用户意图（识别宝可梦名称与问题类型）
        intent = await self.intent_parser_service.parse_intent(question)
        
        pokemon_name = intent.get("pokemon_name")
        if not pokemon_name:
            # 如果无法识别宝可梦名称，返回兜底回复，明确提示未找到
            return {
                "answer": "未找到对应的宝可梦，请更具体一些再试试。",
                "pokemon_name": None,
                "pokemon_id": None,
                "intent": intent
            }
        
        # 2. 获取宝可梦数据（优先读库缓存，缺失时调用 PokeAPI 并写库）
        pokemon_data = await self.pokemon_service.get_pokemon(db, pokemon_name)
        species_data = await self.pokemon_service.get_pokemon_species(db, pokemon_name)
        
        # 3. 生成自然语言回答（外部 LLM 不可用时在客户端兜底）
        answer = await self.doubao_client.build_answer_with_doubao(
            question=question,
            pokemon_data=pokemon_data,
            species_data=species_data
        )
        
        # 4. 构造返回结果（包含回答、识别名称、ID、意图）
        return {
            "answer": answer,
            "pokemon_name": pokemon_name,
            "pokemon_id": pokemon_data.get("id"),
            "intent": intent
        }