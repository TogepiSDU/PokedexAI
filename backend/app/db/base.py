"""SQLAlchemy Base 声明模块

提供 ORM 模型的基础类。
"""
from sqlalchemy.ext.declarative import declarative_base

# ORM 基类（所有模型均应继承）
Base = declarative_base()