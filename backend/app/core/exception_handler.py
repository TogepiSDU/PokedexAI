from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from app.core.exceptions import (
    PokedexError,
    PokemonNotFoundError,
    PokeApiError,
    LLMError,
    DatabaseError,
    IntentParseError
)
import logging

# 配置日志记录器
logger = logging.getLogger(__name__)


async def pokedex_error_handler(request: Request, exc: PokedexError):
    """处理所有宝可梦图鉴系统自定义异常"""
    logger.error(f"PokedexError: {exc.message}, 路径: {request.url.path}, 状态码: {exc.status_code}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "type": exc.__class__.__name__,
                "message": exc.message
            },
            "path": request.url.path,
            "success": False
        }
    )


async def http_exception_handler(request: Request, exc: HTTPException):
    """处理FastAPI默认的HTTPException"""
    logger.error(f"HTTPException: {exc.detail}, 路径: {request.url.path}, 状态码: {exc.status_code}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "type": "HTTPException",
                "message": exc.detail
            },
            "path": request.url.path,
            "success": False
        }
    )


async def general_exception_handler(request: Request, exc: Exception):
    """处理所有其他未捕获的异常"""
    logger.error(f"未处理的异常: {str(exc)}, 路径: {request.url.path}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "type": "InternalServerError",
                "message": "服务器内部错误，请稍后重试"
            },
            "path": request.url.path,
            "success": False
        }
    )


def register_exception_handlers(app):
    """注册所有异常处理器到FastAPI应用"""
    # 注册自定义异常处理器
    app.exception_handler(PokedexError)(pokedex_error_handler)
    app.exception_handler(PokemonNotFoundError)(pokedex_error_handler)
    app.exception_handler(PokeApiError)(pokedex_error_handler)
    app.exception_handler(LLMError)(pokedex_error_handler)
    app.exception_handler(DatabaseError)(pokedex_error_handler)
    app.exception_handler(IntentParseError)(pokedex_error_handler)
    
    # 注册FastAPI默认异常处理器
    app.exception_handler(HTTPException)(http_exception_handler)
    
    # 注册通用异常处理器
    app.exception_handler(Exception)(general_exception_handler)