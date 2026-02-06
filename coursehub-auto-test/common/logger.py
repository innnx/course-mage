import logging
import os
from datetime import datetime

def get_logger():
    """
    创建全局日志器
    功能：
    - 控制台输出
    - 文件输出
    - 自动按天生成日志文件
    """
    logger = logging.getLogger("coursehub")
    logger.setLevel(logging.INFO)

    # 防止重复添加 handler（pytest 多次加载会重复）
    if logger.handlers:
        return logger
    
    # 日志格式
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    #控制台输出
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    #文件输出
    if not os.path.exists("logs"):
        os.mkdir("logs")

    log_file = f"logs/{datetime.now().strftime('%Y-%m-%d')}.log"

    file_handler = logging.FileHandler(log_file,encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger
    
# 全局共享logger
logger = get_logger()