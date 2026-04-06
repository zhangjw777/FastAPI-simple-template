"""
数据库初始化模块
读取 schema.sql 并创建表结构
"""
import logging
from pathlib import Path
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine

logger = logging.getLogger(__name__)


async def init_database(engine: AsyncEngine) -> None:
    """
    初始化数据库表结构
    
    Args:
        engine: SQLAlchemy 异步引擎
    """
    # 读取 schema.sql 文件
    schema_file = Path(__file__).parent / "schema.sql"
    
    if not schema_file.exists():
        logger.error(f"Schema file not found: {schema_file}")
        return
    
    schema_sql = schema_file.read_text(encoding="utf-8")
    
    # 分割多条 SQL 语句
    sql_statements = [
        stmt.strip() 
        for stmt in schema_sql.split(";") 
        if stmt.strip()
    ]
    
    # 执行每条 SQL 语句
    async with engine.begin() as conn:
        for sql in sql_statements:
            try:
                await conn.execute(text(sql))
                logger.info(f"Executed SQL: {sql[:50]}...")
            except Exception as e:
                logger.error(f"Failed to execute SQL: {sql[:50]}... Error: {e}")
                raise
    
    logger.info("数据库表结构初始化完成")
