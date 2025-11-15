from pydantic import BaseModel, Field
from typing import Dict, Optional, Any


class AskRequest(BaseModel):
    """图鉴问答请求模型"""
    question: str = Field(..., min_length=1, description="用户的自然语言问题")


class IntentSchema(BaseModel):
    """意图解析结果模型"""
    pokemon_name: Optional[str] = Field(None, description="宝可梦英文名")
    original_name: Optional[str] = Field(None, description="用户原始称呼")
    intent_type: Optional[str] = Field(None, description="意图类型")
    detail_level: Optional[str] = Field(None, description="详细程度")


class AskResponse(BaseModel):
    """图鉴问答响应模型"""
    answer: str = Field(..., description="自然语言回答")
    pokemon_name: Optional[str] = Field(None, description="识别出的宝可梦英文名")
    pokemon_id: Optional[int] = Field(None, description="宝可梦 ID")
    intent: Optional[IntentSchema] = Field(None, description="意图解析结果")