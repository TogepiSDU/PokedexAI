"""图鉴问答接口路由

路由前缀：/api/v1/ask
请求模型：AskRequest
响应模型：AskResponse
错误处理：统一由异常处理器负责
"""
from fastapi import APIRouter, Depends, HTTPException
from app.core.exceptions import PokemonNotFoundError, LLMError, IntentParseError
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.ask_schema import AskRequest, AskResponse
from app.services.dex_qa_service import DexQAService

# 创建路由实例（/api/v1/ask），所有问答接口在此挂载
router = APIRouter(prefix="/ask", tags=["图鉴问答"])

# 创建服务实例：封装意图解析、数据获取、回答生成
dex_qa_service = DexQAService()


@router.post("", response_model=AskResponse, summary="宝可梦图鉴问答")
async def ask_pokemon_question(request: AskRequest, db: Session = Depends(get_db)):
    """宝可梦图鉴问答接口
    
    通过自然语言提问宝可梦相关问题，系统会返回基于 PokeAPI 数据的 AI 生成答案。
    
    Args:
        request: 包含用户问题的请求体
        db: 数据库会话依赖
    
    Returns:
        包含自然语言回答和相关信息的响应
    
    Example:
        请求体:
        ```
        {"question": "喷火龙的属性和种族值？"}
        ```
        
        响应:
        
        {
            "answer": "喷火龙是火/飞行属性，种族值总和534...",
            "pokemon_name": "charizard",
            "pokemon_id": 6,
            "intent": 
            {
                "pokemon_name": "charizard",
                "original_name": "喷火龙",
                "intent_type": "basic_info",
                "detail_level": "normal"
            }
        }
        
    """
    try:
        # 调用服务处理问题
        result = await dex_qa_service.answer_question(db, request.question)
        return AskResponse(**result)
    except PokemonNotFoundError:
        # 直接传递PokemonNotFoundError异常
        raise
    except IntentParseError:
        # 直接传递IntentParseError异常
        raise
    except HTTPException:
        # 如果是已定义的 HTTP 异常，直接抛出
        raise
    except Exception as e:
        # 使用自定义LLMError替代通用HTTPException
        raise LLMError(message=f"处理请求时发生错误: {str(e)}")