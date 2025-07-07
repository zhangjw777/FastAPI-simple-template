import os
import argparse
import uvicorn
from config import settings

def main():
    """
    运行应用的入口点
    """
    parser = argparse.ArgumentParser(description="FastAPI应用运行脚本")
    parser.add_argument("--host", type=str, default=settings.APP_HOST, help="主机地址")
    parser.add_argument("--port", type=int, default=settings.APP_PORT, help="端口号")
    parser.add_argument("--reload", action="store_true", help="是否热重载")
    parser.add_argument("--workers", type=int, default=1, help="工作进程数")
    parser.add_argument("--env", type=str, default=settings.APP_ENV, help="环境:development/production/testing")
    
    args = parser.parse_args()
    
    # 设置环境变量
    os.environ["APP_ENV"] = args.env
    
    # 运行应用
    uvicorn.run(
        "main:app",
        host=args.host,
        port=args.port,
        reload=args.reload,
        workers=args.workers if not args.reload else 1,
    )

if __name__ == "__main__":
    main() 