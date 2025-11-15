from fastapi import HTTPException, status


class PokedexError(Exception):
    """所有宝可梦图鉴系统异常的基类"""
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class PokemonNotFoundError(PokedexError):
    """宝可梦数据未找到异常"""
    def __init__(self, pokemon_name: str):
        super().__init__(
            message=f"未找到宝可梦: {pokemon_name}",
            status_code=status.HTTP_404_NOT_FOUND
        )


class PokeApiError(PokedexError):
    """PokeAPI 调用异常"""
    def __init__(self, message: str = "PokeAPI 调用失败"):
        super().__init__(
            message=message,
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE
        )


class LLMError(PokedexError):
    """大语言模型调用异常"""
    def __init__(self, message: str = "语言模型服务调用失败"):
        super().__init__(
            message=message,
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE
        )


class DatabaseError(PokedexError):
    """数据库操作异常"""
    def __init__(self, message: str = "数据库操作失败"):
        super().__init__(
            message=message,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


class IntentParseError(PokedexError):
    """意图解析失败异常"""
    def __init__(self, message: str = "无法解析用户意图"):
        super().__init__(
            message=message,
            status_code=status.HTTP_400_BAD_REQUEST
        )