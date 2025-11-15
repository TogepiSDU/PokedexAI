"""数据库会话与引擎管理

职责：提供 SQLAlchemy 引擎与会话工厂，并以依赖的形式在路由中注入 Session。
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# 创建数据库引擎（连接池与预检查）
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """获取数据库会话的依赖函数

    使用 `yield` 保证请求完成后自动关闭会话。
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()