# FastAPI 简易模板

一个基于 FastAPI 的起步项目模板，采用**分层架构设计**，使用 **SQLAlchemy Core + 原生 SQL**，便于快速开发高性能 Web API 服务。

> 🎉 **最新更新**: 项目已重构为使用 SQLAlchemy Core + 原生 SQL，提供更直接的数据库控制和更好的性能。详见 [REFACTORING.md](./REFACTORING.md)

## ✨ 项目特性

- **🏗️ 分层架构**: API 层 → Service 层 → Repository 层的清晰分离
- **💾 SQLAlchemy Core**: 使用原生 SQL 查询，不依赖 ORM
- **📝 统一响应格式**: 标准化的 API 响应结构
- **🔐 JWT 认证**: 完整的身份认证和授权支持
- **📊 Alembic 迁移**: 专业的数据库版本管理
- **✅ Pydantic 验证**: 强大的请求/响应数据验证
- **🌐 多数据库支持**: PostgreSQL、MySQL、SQLite
- **⚡ 异步操作**: 全异步设计，高性能
- **📖 自动 API 文档**: OpenAPI (Swagger UI + ReDoc)
- **🧪 测试框架**: pytest 支持
- **🐳 Docker 支持**: 容器化部署
- **📝 日志系统**: Loguru 日志管理

## 🚀 快速开始

### 环境要求

- Python 3.10+
- 数据库 (PostgreSQL / MySQL / SQLite)
- Docker (可选)

### 本地开发

1. **克隆项目**
```bash
git clone https://github.com/zhangjw777/fastAPI-simple-template.git
cd fastAPI-simple-template
```

2. **创建虚拟环境**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate
```

3. **安装依赖**
```bash
pip install -r requirements.txt
```

4. **配置环境变量**
```bash
cp env.example .env
# 编辑 .env 文件设置数据库连接等
```

5. **运行应用**
```bash
# 应用启动时会自动初始化数据库表
python run.py
```

6. **访问 API 文档**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- 健康检查: http://localhost:8000/api/health

### Docker 部署

```bash
# 构建并启动
docker-compose up -d --build

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

## 📁 项目结构

```
FastAPI-simple-template/
├── alembic/                    # 数据库迁移
│   └── versions/               # 迁移版本
├── app/                        # 应用主目录
│   ├── api/v1/                 # API 路由（v1版本）
│   │   ├── endpoints/          # 端点实现
│   │   │   ├── auth.py         # 认证接口
│   │   │   ├── health.py       # 健康检查
│   │   │   ├── users.py        # 用户管理
│   │   │   └── items.py        # 示例资源
│   │   └── api.py              # 路由聚合
│   ├── core/                   # 核心配置
│   │   ├── application.py      # 应用工厂
│   │   └── events.py           # 生命周期事件
│   ├── db/                     # 数据库层
│   │   ├── database.py         # 数据库连接（Core）
│   │   ├── schema.sql          # SQL 表结构定义
│   │   ├── init_db.py          # 初始化脚本
│   │   ├── session.py          # 会话管理
│   │   └── repositories/       # 数据访问层（原生 SQL）
│   │       ├── user_repository.py
│   │       └── item_repository.py
│   ├── schemas/                # Pydantic 模型
│   │   ├── response.py         # 📌 统一响应格式
│   │   ├── user.py
│   │   ├── item.py
│   │   └── token.py
│   ├── services/               # 业务逻辑层
│   │   ├── user_service.py
│   │   └── item_service.py
│   ├── middlewares/            # 中间件
│   │   └── exception_handler.py
│   └── utils/                  # 工具函数
│       ├── auth.py             # 认证工具
│       ├── security.py         # 加密/JWT
│       └── logger.py           # 日志配置
├── config/                     # 配置文件
│   └── settings.py             # 环境变量配置
├── tests/                      # 测试目录
├── main.py                     # 应用入口
├── run.py                      # 运行脚本
├── requirements.txt            # Python 依赖
├── Dockerfile                  # Docker 构建
├── docker-compose.yml          # Docker Compose
└── REFACTORING.md              # 🔥 重构说明文档
```

## 🎯 核心概念

### 统一响应格式

所有 API 响应遵循统一结构：

```json
{
  "success": true,
  "data": { ... },
  "message": "操作成功",
  "code": 200
}
```

### 原生 SQL 查询示例

```python
# Repository 层
async def get_by_email(self, email: str) -> Optional[dict]:
    sql = """
        SELECT id, email, username, is_active, role
        FROM users
        WHERE email = :email
    """
    result = await self.conn.execute(text(sql), {"email": email})
    row = result.first()
    return dict(row._mapping) if row else None
```

### 三层架构

```
API 层 (endpoints)
    ↓ 调用
Service 层 (业务逻辑)
    ↓ 调用
Repository 层 (数据访问)
    ↓ 执行
数据库 (原生 SQL)
```

## 🛠️ 开发指南

### 添加新功能模块

#### 1. 定义数据库表 (`app/db/schema.sql`)

```sql
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price REAL NOT NULL,
    stock INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 2. 创建 Pydantic 模型 (`app/schemas/product.py`)

```python
from pydantic import BaseModel, Field
from datetime import datetime

class ProductCreate(BaseModel):
    name: str = Field(..., description="产品名称")
    description: str = None
    price: float = Field(..., gt=0)
    stock: int = Field(default=0, ge=0)

class Product(BaseModel):
    id: int
    name: str
    description: str | None
    price: float
    stock: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class ProductResponse(BaseModel):
    id: int
    name: str
    price: float
    stock: int
    
    class Config:
        from_attributes = True
```

#### 3. 创建 Repository (`app/db/repositories/product_repository.py`)

```python
from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy import text
from typing import Optional

class ProductRepository:
    def __init__(self, conn: AsyncConnection):
        self.conn = conn
    
    async def create(self, name: str, description: str, price: float, stock: int) -> dict:
        sql = """
            INSERT INTO products (name, description, price, stock)
            VALUES (:name, :description, :price, :stock)
            RETURNING id, name, description, price, stock, created_at, updated_at
        """
        result = await self.conn.execute(
            text(sql),
            {"name": name, "description": description, "price": price, "stock": stock}
        )
        return dict(result.first()._mapping)
    
    async def get_by_id(self, product_id: int) -> Optional[dict]:
        sql = "SELECT * FROM products WHERE id = :id"
        result = await self.conn.execute(text(sql), {"id": product_id})
        row = result.first()
        return dict(row._mapping) if row else None
```

#### 4. 创建 Service (`app/services/product_service.py`)

```python
from sqlalchemy.ext.asyncio import AsyncConnection
from app.db.repositories.product_repository import ProductRepository
from app.schemas.product import ProductCreate, Product

class ProductService:
    def __init__(self, conn: AsyncConnection):
        self.repository = ProductRepository(conn)
    
    async def create_product(self, product_in: ProductCreate) -> Product:
        product_data = await self.repository.create(
            name=product_in.name,
            description=product_in.description,
            price=product_in.price,
            stock=product_in.stock
        )
        return Product(**product_data)
```

#### 5. 创建 API 端点 (`app/api/v1/endpoints/products.py`)

```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncConnection

from app.db.session import get_db
from app.schemas.product import ProductCreate, ProductResponse
from app.schemas.response import ApiResponse, success_response
from app.services.product_service import ProductService

router = APIRouter()

@router.post("", response_model=ApiResponse[ProductResponse])
async def create_product(
    product_in: ProductCreate,
    conn: AsyncConnection = Depends(get_db)
):
    service = ProductService(conn)
    product = await service.create_product(product_in)
    return success_response(data=product, message="产品创建成功")
```

#### 6. 注册路由 (`app/api/v1/api.py`)

```python
from app.api.v1.endpoints import products

api_router.include_router(
    products.router, 
    prefix="/products", 
    tags=["products"]
)
```

#### 7. 创建数据库迁移

```bash
# 生成迁移文件
alembic revision --autogenerate -m "Add products table"

# 应用迁移
alembic upgrade head
```

## 🔐 认证使用

### 1. 注册用户（需要登录权限）

```bash
curl -X POST "http://localhost:8000/api/users" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "email": "user@example.com",
    "username": "testuser",
    "password": "password123",
    "role": "user"
  }'
```

### 2. 登录获取 Token

```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=password123"
```

响应:
```json
{
  "success": true,
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIs...",
    "token_type": "bearer"
  },
  "message": "登录成功",
  "code": 200
}
```

### 3. 使用 Token 访问受保护资源

```bash
curl -X GET "http://localhost:8000/api/users/1" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIs..."
```

## 🗄️ 数据库管理

### 方式一：使用 Alembic（推荐用于生产环境）

```bash
# 创建迁移
alembic revision --autogenerate -m "描述变更"

# 应用迁移
alembic upgrade head

# 回滚一个版本
alembic downgrade -1

# 查看迁移历史
alembic history

# 查看当前版本
alembic current
```

### 方式二：直接使用 schema.sql（开发环境快速迭代）

```bash
# 删除旧数据库
rm app.db

# 重启应用，自动创建表
python run.py
```

## 📊 API 响应示例

### 成功响应

```json
{
  "success": true,
  "data": {
    "id": 1,
    "username": "testuser",
    "email": "user@example.com",
    "is_active": true,
    "role": "user"
  },
  "message": "操作成功",
  "code": 200
}
```

### 错误响应

```json
{
  "detail": "用户不存在"
}
```

## 🧪 测试

```bash
# 运行所有测试
pytest

# 详细输出
pytest -v

# 测试覆盖率
pytest --cov=app

# 测试特定文件
pytest tests/test_api/test_health.py
```

## 🔧 环境配置

`.env` 文件配置示例:

```bash
# 应用配置
APP_NAME=FastAPI-Template
APP_VERSION=0.1.0
APP_ENV=development
APP_DEBUG=True
APP_HOST=0.0.0.0
APP_PORT=8000

# 数据库配置
DATABASE_URL=sqlite:///./app.db
# DATABASE_URL=postgresql+asyncpg://user:pass@localhost/dbname
# DATABASE_URL=mysql+aiomysql://user:pass@localhost/dbname
DATABASE_ECHO=True

# JWT 配置
JWT_SECRET_KEY=your-secret-key-here-change-in-production
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=1440

# 日志配置
LOG_LEVEL=INFO
```

## 📝 最佳实践

1. **参数化查询** - 始终使用参数化避免 SQL 注入
   ```python
   # ✅ 正确
   sql = "SELECT * FROM users WHERE id = :id"
   result = await conn.execute(text(sql), {"id": user_id})
   
   # ❌ 错误
   sql = f"SELECT * FROM users WHERE id = {user_id}"
   ```

2. **统一响应** - 使用 `success_response()` 和 `error_response()`

3. **异常处理** - Service 层抛出业务异常，API 层转换为 HTTP 异常

4. **事务管理** - Repository 不处理事务，由 Service 层控制

5. **日志记录** - 使用 Loguru 记录关键操作

## 🚀 部署指南

### 生产环境配置

```bash
# 设置环境变量
export APP_ENV=production
export APP_DEBUG=False
export DATABASE_URL=postgresql+asyncpg://user:pass@db/prod
export JWT_SECRET_KEY=$(openssl rand -hex 32)
```

### 使用 Gunicorn + Uvicorn

```bash
# 安装
pip install gunicorn

# 运行
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --access-logfile - \
  --error-logfile -
```

### Nginx 反向代理

```nginx
server {
    listen 80;
    server_name yourdomain.com;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 📚 更多资源

- [FastAPI 官方文档](https://fastapi.tiangolo.com/)
- [SQLAlchemy Core 教程](https://docs.sqlalchemy.org/en/20/core/)
- [Pydantic 文档](https://docs.pydantic.dev/)
- [Alembic 文档](https://alembic.sqlalchemy.org/)
- [重构说明文档](./REFACTORING.md)

---

**维护者:** zhangjw777  
**更新日期:** 2026-04-06  
**版本:** 2.0 (重构版)
