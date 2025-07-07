import sys
import logging
from pathlib import Path
from loguru import logger

from config import settings

# 日志格式
LOG_FORMAT = (
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
    "<level>{message}</level>"
)


class InterceptHandler(logging.Handler):
    """
    拦截标准库logging并重定向到loguru
    """
    
    def emit(self, record: logging.LogRecord) -> None:
        # 获取对应的loguru级别
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno
        
        # 查找调用者
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1
        
        # 使用loguru输出日志
        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def setup_logging() -> None:
    """
    设置日志系统
    """
    # 移除所有处理器
    logger.remove()
    
    # 获取日志级别
    log_level = settings.LOG_LEVEL
    
    # 确保日志目录存在
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    
    # 添加控制台处理器
    logger.add(
        sys.stdout,
        format=LOG_FORMAT,
        level=log_level,
        colorize=True,
    )
    
    # 添加文件处理器
    logger.add(
        logs_dir / "app.log",
        format=LOG_FORMAT,
        level=log_level,
        rotation="10 MB",
        compression="zip",
        retention="1 month",
    )
    
    # 拦截标准库logging
    logging.basicConfig(handlers=[InterceptHandler()], level=0)
    
    # 设置其他库的日志级别
    for logger_name in ("uvicorn", "uvicorn.error", "fastapi"):
        logging_logger = logging.getLogger(logger_name)
        logging_logger.handlers = [InterceptHandler()]
    
    # 记录启动信息
    logger.info(f"Logging initialized with level: {log_level}") 