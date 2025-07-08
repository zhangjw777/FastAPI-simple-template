# FastAPI简易模板

一个基于FastAPI的起步项目模板，结构类似于SpringBoot项目，便于快速开发新应用。该模板采用分层架构设计，提供完整的项目结构和基础功能，帮助开发者快速构建高质量的Web API服务。

## 项目特性

- **分层架构设计**：控制器(API)-服务层-数据访问层的清晰分离
- **集成SQLAlchemy ORM**：强大的ORM支持，简化数据库操作
- **环境变量配置**：灵活的配置管理
- **全局异常处理**：统一的错误响应
- **日志系统**：完整的日志记录
- **数据验证**：基于Pydantic的请求和响应验证
- **身份认证基础结构**：JWT认证支持
- **数据库迁移支持**：使用Alembic进行版本控制
- **自动API文档**：基于OpenAPI的文档生成
- **测试框架集成**：支持单元测试和集成测试

## 详细项目结构

```
├── alembic/                # 数据库迁移相关文件
│   ├── versions/           # 迁移版本目录
│   ├── env.py              # Alembic环境配置
│   └── script.py.mako      # 迁移脚本模板
├── app/                    # 应用主目录
│   ├── api/                # API路由模块
│   │   ├── v1/             # API版本控制
│   │   │   ├── endpoints/  # 各模块的API端点
│   │   │   │   ├── auth.py         # 认证相关接口
│   │   │   │   ├── health.py       # 健康检查接口
│   │   │   │   ├── items.py        # 示例Item接口
│   │   │   │   └── users.py        # 用户管理接口
│   │   │   └── api.py      # API路由注册
│   ├── core/               # 核心配置模块
│   │   ├── application.py  # 应用实例创建
│   │   └── events.py       # 应用生命周期事件
│   ├── db/                 # 数据库相关
│   │   ├── models/         # SQLAlchemy数据模型
│   │   │   ├── base.py     # 基础模型类
│   │   │   ├── item.py     # Item模型
│   │   │   └── user.py     # 用户模型
│   │   ├── repositories/   # 数据访问层
│   │   │   ├── base.py     # 基础仓库类
│   │   │   ├── item_repository.py  # Item仓库
│   │   │   └── user_repository.py  # 用户仓库
│   │   └── session.py      # 数据库会话管理
│   ├── middlewares/        # 中间件
│   │   └── exception_handler.py  # 异常处理中间件
│   ├── schemas/            # Pydantic模型(数据验证)
│   │   ├── health.py       # 健康检查模型
│   │   ├── item.py         # Item相关模型
│   │   ├── token.py        # 令牌模型
│   │   └── user.py         # 用户相关模型
│   ├── services/           # 业务逻辑层
│   │   ├── item_service.py # Item服务
│   │   └── user_service.py # 用户服务
│   └── utils/              # 工具函数
│       ├── auth.py         # 认证相关工具
│       ├── logger.py       # 日志工具
│       └── security.py     # 安全相关工具
├── config/                 # 配置文件目录
│   └── settings.py         # 应用配置设置
├── tests/                  # 测试目录
│   ├── test_api/           # API测试
│   │   └── test_health.py  # 健康检查API测试
│   └── conftest.py         # 测试配置
├── .env.example            # 环境变量示例
├── main.py                 # 应用入口
├── run.py                  # 辅助运行脚本
├── requirements.txt        # 项目依赖
├── Dockerfile              # Docker构建文件
└── docker-compose.yml      # Docker Compose配置
```

## 环境准备

### 必要条件

- Python 3.8+
- 数据库(PostgreSQL, MySQL, SQLite等)
- 可选: Docker和Docker Compose(用于容器化部署)

## 快速开始

### 本地开发环境搭建

1. **克隆项目模板**

```bash
git clone https://github.com/zhangjw777/fastAPI-simple-template.git
cd fastAPI-simple-template
```

2. **创建虚拟环境**

```bash
# 使用venv
python -m venv venv
# Windows激活
venv\Scripts\activate
# Linux/macOS激活
source venv/bin/activate
```

3. **安装依赖**

```bash
pip install -r requirements.txt
```

4. **配置环境变量**

```bash
# 复制环境变量示例文件
cp env.example .env
# 编辑.env文件设置数据库连接等环境变量
```

5. **初始化数据库**

```bash
# 创建初始迁移
alembic revision --autogenerate -m "Initial migration"
# 应用迁移
alembic upgrade head
```

6. **运行应用**

```bash
# 使用uvicorn直接运行
uvicorn main:app --reload --host 0.0.0.0 --port 8000
# 或使用辅助脚本
python run.py
```

7. **访问API文档**

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Docker部署

1. **构建并启动容器**

```bash
docker-compose up -d --build
```

2. **运行数据库迁移**

```bash
docker-compose exec app alembic upgrade head
```

3. **访问API**

- API服务: http://localhost:8000
- API文档: http://localhost:8000/docs

## 开发指南

### 添加新API端点

1. **创建数据库模型** (如需要)

在`app/db/models/`目录下创建新模型:

```python
# app/db/models/product.py
from sqlalchemy import Column, Integer, String, Float
from app.db.models.base import Base

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
```

2. **创建Pydantic模型**

在`app/schemas/`目录创建对应的验证模型:

```python
# app/schemas/product.py
from pydantic import BaseModel
from typing import Optional

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    name: Optional[str] = None
    price: Optional[float] = None

class Product(ProductBase):
    id: int
    
    class Config:
        orm_mode = True
```

3. **创建仓库类**

在`app/db/repositories/`目录添加仓库:

```python
# app/db/repositories/product_repository.py
from app.db.repositories.base import BaseRepository
from app.db.models.product import Product
from sqlalchemy.orm import Session
from typing import List, Optional

class ProductRepository(BaseRepository):
    def create(self, db: Session, name: str, description: str, price: float) -> Product:
        product = Product(name=name, description=description, price=price)
        db.add(product)
        db.commit()
        db.refresh(product)
        return product
        
    def get_by_id(self, db: Session, product_id: int) -> Optional[Product]:
        return db.query(Product).filter(Product.id == product_id).first()
        
    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[Product]:
        return db.query(Product).offset(skip).limit(limit).all()
```

4. **创建服务类**

在`app/services/`目录添加服务:

```python
# app/services/product_service.py
from app.db.repositories.product_repository import ProductRepository
from app.schemas.product import ProductCreate, ProductUpdate, Product
from sqlalchemy.orm import Session
from typing import List, Optional

class ProductService:
    def __init__(self):
        self.repository = ProductRepository()
    
    def create_product(self, db: Session, product: ProductCreate) -> Product:
        return self.repository.create(
            db=db,
            name=product.name,
            description=product.description,
            price=product.price
        )
    
    def get_product(self, db: Session, product_id: int) -> Optional[Product]:
        return self.repository.get_by_id(db=db, product_id=product_id)
    
    def get_products(self, db: Session, skip: int = 0, limit: int = 100) -> List[Product]:
        return self.repository.get_all(db=db, skip=skip, limit=limit)
```

5. **创建API端点**

在`app/api/v1/endpoints/`目录添加API端点:

```python
# app/api/v1/endpoints/products.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.schemas.product import Product, ProductCreate, ProductUpdate
from app.services.product_service import ProductService

router = APIRouter()
service = ProductService()

@router.post("/", response_model=Product, status_code=status.HTTP_201_CREATED)
def create_product(
    product: ProductCreate, 
    db: Session = Depends(get_db)
):
    return service.create_product(db=db, product=product)

@router.get("/{product_id}", response_model=Product)
def get_product(
    product_id: int, 
    db: Session = Depends(get_db)
):
    product = service.get_product(db=db, product_id=product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.get("/", response_model=List[Product])
def get_products(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    return service.get_products(db=db, skip=skip, limit=limit)
```

6. **注册路由**

在`app/api/v1/api.py`文件中注册新路由:

```python
# app/api/v1/api.py
from fastapi import APIRouter
from app.api.v1.endpoints import users, items, auth, health, products

api_router = APIRouter()
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(items.router, prefix="/items", tags=["items"])
api_router.include_router(products.router, prefix="/products", tags=["products"])
```

7. **创建数据库迁移**

```bash
alembic revision --autogenerate -m "Add product model"
alembic upgrade head
```

### 添加身份认证

本模板已集成JWT认证基础结构，使用方法:

1. **获取令牌**:
   - 使用`/api/v1/auth/login`端点登录并获取访问令牌
```

### 自定义中间件

在`app/middlewares/`目录添加自定义中间件:

```python
# app/middlewares/timing.py
import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

class TimingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response
```

在`app/core/application.py`中注册中间件:

```python
from app.middlewares.timing import TimingMiddleware

def create_application() -> FastAPI:
    # ... 其他代码
    application = FastAPI(...)
    application.add_middleware(TimingMiddleware)
    # ... 其他代码
    return application
```

## 测试

### 运行测试

```bash
# 运行所有测试
pytest

# 运行特定测试
pytest tests/test_api/test_health.py

# 带详细输出
pytest -v
```

### 编写测试

在`tests/`目录添加测试文件，示例:

```python
# tests/test_api/test_products.py
from fastapi.testclient import TestClient
import pytest

def test_create_product(client, db_session):
    response = client.post(
        "/api/v1/products/",
        json={"name": "Test Product", "description": "Test Description", "price": 99.99}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Product"
    assert data["price"] == 99.99
    assert "id" in data
```

## 部署指南

### 生产环境配置

1. **环境变量设置**

在生产环境中设置以下环境变量:

- `ENVIRONMENT=production` - 设置环境为生产环境
- `SECRET_KEY` - 安全密钥，用于JWT等
- `DATABASE_URL` - 数据库连接URI
- `LOG_LEVEL=INFO` - 生产环境日志级别

2. **HTTPS配置**

在生产环境中建议使用HTTPS，可通过反向代理(如Nginx)配置:

```nginx
server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name yourdomain.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 容器化部署

使用Docker Compose进行部署:

```bash
# 生产环境启动
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

创建`docker-compose.prod.yml`用于生产环境特定配置:

```yaml
version: '3'
services:
  app:
    restart: always
    environment:
      - ENVIRONMENT=production
      - LOG_LEVEL=INFO
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 1G
```

## 常见问题与解决方案

1. **数据库连接问题**
   - 检查`.env`文件中的`DATABASE_URL`是否正确
   - 确保数据库服务正在运行
   - 验证数据库用户权限

2. **Alembic迁移错误**
   - 确保模型已正确导入到`alembic/env.py`
   - 尝试使用`alembic revision --autogenerate -m "message"`手动生成迁移

3. **依赖安装问题**
   - 尝试更新pip: `pip install --upgrade pip`
   - 检查Python版本兼容性(需要3.8+)


