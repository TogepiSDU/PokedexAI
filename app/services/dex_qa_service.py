from typing import Dict, Any
from sqlalchemy.orm import Session
from app.clients.doubao_client import DoubaoClient
from app.services.intent_parser_service import IntentParserService
from app.services.pokemon_service import PokemonService


class DexQAService:
    """图鉴问答服务 - 处理整个图鉴问答流程"""
    
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
        # 1. 解析用户意图
        intent = await self.intent_parser_service.parse_intent(question)
        
        pokemon_name = intent.get("pokemon_name")
        if not pokemon_name:
            # 如果无法识别宝可梦名称，返回兜底回复
            return {
                "answer": "我没太确定你说的是哪只宝可梦，可以再具体一点吗？",
                "pokemon_name": None,
                "pokemon_id": None,
                "intent": intent
            }
        
        # 2. 获取宝可梦数据
        pokemon_data = await self.pokemon_service.get_pokemon(db, pokemon_name)
        species_data = await self.pokemon_service.get_pokemon_species(db, pokemon_name)
        
        # 3. 使用豆包生成自然语言回答
        answer = await self.doubao_client.build_answer_with_doubao(
            question=question,
            pokemon_data=pokemon_data,
            species_data=species_data
        )
        
        # 4. 构造返回结果
        return {
            "answer": answer,
            "pokemon_name": pokemon_name,
            "pokemon_id": pokemon_data.get("id"),
            "intent": intent
        }