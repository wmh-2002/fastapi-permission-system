# FastAPI 权限管理系统

一个基于 FastAPI 构建的综合权限管理系统，具有基于角色的访问控制（RBAC）功能，用于安全的用户认证和授权。

## 🚀 功能特性

- **基于 JWT 的认证系统**: 安全登录和基于令牌的认证
- **基于角色的访问控制 (RBAC)**: 高级权限管理系统
- **用户管理**: 创建、读取、更新和删除用户以及角色分配
- **角色管理**: 定义角色并为角色分配权限
- **权限管理**: 细粒度权限控制系统
- **CORS 支持**: 跨域资源共享，适用于 Web 应用
- **安全密码哈希**: 使用 bcrypt 进行密码加密
- **统一 API 响应格式**: 所有端点的响应结构一致
- **Pydantic 验证**: 强大的数据验证和序列化
- **数据库集成**: 支持 PostgreSQL 与 SQLAlchemy ORM

## 📁 项目结构

```
first-fastapi-project/
├── README.md                    # 项目文档
├── requirements.txt             # 项目依赖
├── backend/
│   ├── main.py                  # 主应用入口
│   ├── config.py                # 配置设置
│   ├── __init__.py
│   ├── api/                     # API 路由和端点
│   │   ├── __init__.py
│   │   ├── deps.py              # 依赖注入工具
│   │   └── v1/                  # 第一版 API 路由
│   │       └── user/            # 用户相关路由
│   │           ├── auth.py      # 认证端点
│   │           ├── users.py     # 用户管理端点
│   │           ├── roles.py     # 角色管理端点
│   │           └── permissions.py # 权限管理端点
│   ├── constants/               # 应用常量
│   │   ├── __init__.py
│   │   └── permissions.py       # 权限定义和默认角色
│   ├── database/                # 数据库层
│   │   ├── __init__.py
│   │   └── user_models.py       # SQLAlchemy 用户模型
│   ├── middleware/              # 自定义中间件（待实现）
│   ├── schemas/                 # 数据验证模式（待实现）
│   ├── services/                # 业务逻辑层（待实现）
│   └── utils/                   # 实用工具函数（待实现）
```

## 🛠️ 技术栈

- **Python 3.8+**
- **FastAPI**: 现代、快速的 API 构建框架
- **SQLAlchemy**: SQL 工具包和对象关系映射（ORM）
- **PostgreSQL**: 对象关系型数据库系统
- **Pydantic**: 数据验证和解析
- **Passlib**: 密码哈希库
- **python-jose**: JSON Web Token (JWT) 支持
- **Uvicorn**: 用于服务应用程序的 ASGI 服务器
- **Alembic**: 数据库迁移支持

## 📦 安装

1. **克隆仓库**
   ```bash
   git clone https://github.com/your-username/first-fastapi-project.git
   cd first-fastapi-project
   ```

2. **创建虚拟环境**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows 系统: venv\Scripts\activate
   ```

3. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

4. **设置环境变量**

   在根目录创建 `.env` 文件并配置以下内容：
   ```env
   DATABASE_URL=postgresql://username:password@localhost/dbname
   SECRET_KEY=your-very-secure-secret-key-here
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   PASSWORD_SALT=your-password-salt-here
   ALLOWED_ORIGINS=["http://localhost", "http://localhost:3000"]
   ```

## 🔧 配置

应用程序使用 `pydantic_settings.BaseSettings` 通过 `backend/config.py` 文件进行配置管理。可以通过环境变量覆盖设置。

关键配置选项：
- **DATABASE_URL**: PostgreSQL 数据库连接字符串
- **SECRET_KEY**: JWT 令牌生成的密钥
- **ALGORITHM**: JWT 令牌加密算法
- **ACCESS_TOKEN_EXPIRE_MINUTES**: 令牌过期时间
- **ALLOWED_ORIGINS**: CORS 允许的来源列表
- **PASSWORD_SALT**: 密码哈希盐值

## ▶️ 运行应用

1. **启动开发服务器**
   ```bash
   uvicorn backend.main:app --reload
   ```
   
   应用程序将在 `http://localhost:8000` 上可用

2. **访问 API 文档**
   - 交互式文档: [http://localhost:8000/docs](http://localhost:8000/docs)
   - 替代文档: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## 🌐 API 端点

### 认证
- `POST /api/v1/login` - 用户登录和 JWT 令牌生成
- `POST /api/v1/register` - 用户注册（待实现）

### 用户管理
- `GET /api/v1/users` - 获取所有用户
- `GET /api/v1/users/{id}` - 获取特定用户
- `POST /api/v1/users` - 创建新用户（待实现）
- `PUT /api/v1/users/{id}` - 更新用户信息（待实现）
- `DELETE /api/v1/users/{id}` - 删除用户（待实现）
- `POST /api/v1/users/{user_id}/roles/{role_id}` - 为用户分配角色（待实现）
- `DELETE /api/v1/users/{user_id}/roles/{role_id}` - 从用户移除角色（待实现）

### 角色管理
- `GET /api/v1/roles` - 获取所有角色
- `GET /api/v1/roles/{id}` - 获取特定角色
- `POST /api/v1/roles` - 创建新角色（待实现）
- `PUT /api/v1/roles/{id}` - 更新角色信息（待实现）
- `DELETE /api/v1/roles/{id}` - 删除角色（待实现）
- `POST /api/v1/roles/{role_id}/permissions/{permission_id}` - 为角色分配权限（待实现）
- `DELETE /api/v1/roles/{role_id}/permissions/{permission_id}` - 从角色移除权限（待实现）

### 权限管理
- `GET /api/v1/permissions` - 获取所有权限
- `GET /api/v1/permissions/{id}` - 获取特定权限
- `POST /api/v1/permissions` - 创建新权限（待实现）
- `PUT /api/v1/permissions/{id}` - 更新权限（待实现）
- `DELETE /api/v1/permissions/{id}` - 删除权限（待实现）

## 🔐 RBAC 系统

应用程序实现了全面的基于角色的访问控制系统（RBAC）：

- **用户** 可以分配到多个 **角色**
- **角色** 可以被授予多个 **权限**
- 用户从其所有分配的角色继承权限
- API 端点可以根据所需的权限进行保护
- 默认角色包括管理员、用户和版主

预定义权限包括：
- 用户管理: `user:create`, `user:read`, `user:update`, `user:delete`
- 角色管理: `role:create`, `role:read`, `role:update`, `role:delete`
- 权限管理: `permission:create`, `permission:read`, `permission:update`, `permission:delete`

## 🧪 测试

使用 pytest 运行测试套件：
```bash
pytest
```

运行带覆盖率的测试：
```bash
pytest --cov=backend
```

## 🚢 部署

对于生产部署，请考虑以下内容：

1. 使用像 Gunicorn 这样的 WSGI/ASGI 服务器配合 Uvicorn 工作进程
2. 配置像 Nginx 这样的反向代理
3. 设置生产级数据库（PostgreSQL）
4. 使用环境变量存储敏感配置
5. 启用 HTTPS/TLS 加密
6. 为生产环境设置适当的 CORS 策略

生产命令示例：
```bash
gunicorn backend.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## 🤝 贡献

1. Fork 仓库
2. 创建功能分支 (`git checkout -b feature/awesome-feature`)
3. 提交您的更改 (`git commit -m 'Add awesome feature'`)
4. 推送到分支 (`git push origin feature/awesome-feature`)
5. 提交 Pull Request

## 📄 许可证

本项目根据 MIT 许可证授权 - 详情请参见 [LICENSE](LICENSE) 文件。

## 📞 支持

如有任何问题或需要帮助，请随时在仓库中提交 issue。