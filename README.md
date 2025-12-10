# FastAPI 权限管理系统

一个基于 FastAPI 构建的综合权限管理系统，提供基于角色的访问控制（RBAC）功能。

## 功能特性

- JWT 基于的认证系统
- 基于角色的访问控制（RBAC）
- 用户、角色和权限管理
- 统一的 API 响应模板
- 权限检查机制
- 安全的密码哈希

## 项目结构

```
first-fastapi-project/
├── app/
│   ├── __init__.py
│   ├── main.py                    # 主应用入口
│   ├── config.py                  # 配置设置
│   ├── database/                  # 数据库相关模块
│   │   ├── __init__.py
│   │   ├── connection.py          # 数据库连接设置
│   │   └── models.py              # SQLAlchemy 模型
│   ├── schemas/                   # Pydantic 模式定义
│   │   ├── __init__.py
│   │   └── user.py                # 用户、角色、权限模式
│   ├── api/                       # API 路由
│   │   ├── __init__.py
│   │   ├── deps.py                # 依赖注入
│   │   ├── auth.py                # 认证端点
│   │   └── v1/                    # 版本 1 API 路由
│   │       ├── __init__.py
│   │       ├── users.py
│   │       ├── roles.py
│   │       └── permissions.py
│   ├── services/                  # 业务逻辑
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   ├── user_service.py
│   │   ├── role_service.py
│   │   └── permission_service.py
│   ├── utils/                     # 工具函数
│   │   ├── __init__.py
│   │   ├── security.py            # 安全工具（密码哈希、JWT）
│   │   └── responses.py           # 统一 API 响应模板
│   ├── middleware/                # 自定义中间件
│   │   ├── __init__.py
│   │   └── auth_middleware.py
│   └── constants/                 # 常量和枚举
│       ├── __init__.py
│       └── permissions.py
├── tests/                         # 测试文件
├── requirements.txt               # 项目依赖
└── README.md                      # 项目文档
```

## 环境设置

1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 在 `.env` 文件中设置环境变量：
```env
DATABASE_URL=postgresql://username:password@localhost/dbname
SECRET_KEY=your-very-secure-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

3. 运行应用：
```bash
uvicorn app.main:app --reload
```

应用将在 `http://localhost:8000` 上可用。

## API 端点

### 认证
- `POST /api/v1/login` - 用户登录
- `POST /api/v1/register` - 用户注册

### 用户管理
- `GET /api/v1/users` - 获取所有用户
- `GET /api/v1/users/{id}` - 获取特定用户
- `POST /api/v1/users` - 创建新用户
- `PUT /api/v1/users/{id}` - 更新用户
- `DELETE /api/v1/users/{id}` - 删除用户
- `POST /api/v1/users/{user_id}/roles/{role_id}` - 为用户分配角色
- `DELETE /api/v1/users/{user_id}/roles/{role_id}` - 从用户移除角色

### 角色管理
- `GET /api/v1/roles` - 获取所有角色
- `GET /api/v1/roles/{id}` - 获取特定角色
- `POST /api/v1/roles` - 创建新角色
- `PUT /api/v1/roles/{id}` - 更新角色
- `DELETE /api/v1/roles/{id}` - 删除角色
- `POST /api/v1/roles/{role_id}/permissions/{permission_id}` - 为角色添加权限
- `DELETE /api/v1/roles/{role_id}/permissions/{permission_id}` - 从角色移除权限

### 权限管理
- `GET /api/v1/permissions` - 获取所有权限
- `GET /api/v1/permissions/{id}` - 获取特定权限
- `POST /api/v1/permissions` - 创建新权限
- `PUT /api/v1/permissions/{id}` - 更新权限
- `DELETE /api/v1/permissions/{id}` - 删除权限

## 权限系统

系统实现了基于角色的访问控制（RBAC）模型：
- 用户可以被分配到多个角色
- 角色可以被分配多个权限
- 用户从其分配的角色继承权限
- API 端点可以通过特定权限要求进行保护

## API 响应格式

所有 API 响应都遵循统一模板：
```json
{
    "success": true,
    "code": 200,
    "message": "Success",
    "data": {},
    "error": null
}
```

## 测试

使用 pytest 运行测试：
```bash
pytest
```