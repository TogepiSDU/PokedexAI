from typing import Dict, Any
from app.clients.doubao_client import DoubaoClient


class IntentParserService:
    """意图解析服务"""
    
    def __init__(self):
        self.doubao_client = DoubaoClient()
    
    async def parse_intent(self, question: str) -> Dict[str, Any]:
        """解析用户问题的意图
        
        Args:
            question: 用户的自然语言问题
        
        Returns:
            结构化的意图信息
        """
        return await self.doubao_client.parse_question_to_intent(question)