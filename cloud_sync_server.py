"""
DeepRead Cloud Sync Server
云端同步后端服务

功能：
1. 用户认证（简单token-based）
2. 数据上传（push）
3. 数据下载（pull）
4. 自动同步
5. 数据版本管理
"""

from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import sqlite3
import json
import uuid
from datetime import datetime, timedelta
import hashlib
import os
from pathlib import Path

# ==================== 配置 ====================
SERVER_DB_PATH = Path(__file__).parent / "cloud_server.db"
SECRET_KEY = os.getenv("DEEPREAD_SECRET_KEY", "deepread-secret-key-change-in-production")
ALGORITHM = "HS256"

# ==================== FastAPI App ====================
app = FastAPI(
    title="DeepRead Cloud Sync API",
    description="云端数据同步服务",
    version="1.0.0"
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应该限制具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== 数据模型 ====================
class UserRegister(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class SyncData(BaseModel):
    token: str
    data: Dict[str, Any]
    client_version: str = "3.8"

class SyncPull(BaseModel):
    token: str
    since_version: Optional[int] = None


# ==================== 数据库初始化 ====================
def init_server_database():
    """初始化服务器数据库"""
    conn = sqlite3.connect(SERVER_DB_PATH)
    cursor = conn.cursor()

    # 用户表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_sync TIMESTAMP,
            subscription_tier TEXT DEFAULT 'free'
        )
    ''')

    # 用户数据表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_data (
            user_id TEXT PRIMARY KEY,
            data_json TEXT NOT NULL,
            version INTEGER DEFAULT 1,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

    # 同步历史表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sync_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            sync_type TEXT NOT NULL,
            client_version TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            success BOOLEAN DEFAULT 1,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

    conn.commit()
    conn.close()


def get_db_connection():
    """获取数据库连接"""
    conn = sqlite3.connect(SERVER_DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# ==================== 工具函数 ====================
def hash_password(password: str) -> str:
    """密码哈希"""
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(password: str, password_hash: str) -> bool:
    """验证密码"""
    return hash_password(password) == password_hash


def generate_token(user_id: str) -> str:
    """生成访问token（简化版，生产环境应使用JWT）"""
    token_data = f"{user_id}:{datetime.now().timestamp()}:{SECRET_KEY}"
    return hashlib.sha256(token_data.encode()).hexdigest()


def verify_token(token: str) -> Optional[str]:
    """验证token并返回user_id"""
    # 简化版本，实际应该查询数据库
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM users WHERE id = (SELECT user_id FROM user_tokens WHERE token = ?)', (token,))
    # 这里简化处理，实际应该有专门的token表
    conn.close()
    return None  # 暂时返回None，需要实现token存储和验证


# ==================== 认证依赖 ====================
async def get_current_user(token: str = Header(...)):
    """从token获取当前用户"""
    # 简化版本，暂时不使用
    # 实际应该查询token表验证用户身份
    return None


# ==================== API端点 ====================

@app.get("/")
async def root():
    """根端点"""
    return {
        "service": "DeepRead Cloud Sync",
        "version": "1.0.0",
        "status": "running"
    }


@app.post("/api/auth/register")
async def register(user: UserRegister):
    """用户注册"""
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # 检查用户名是否已存在
        cursor.execute('SELECT id FROM users WHERE username = ?', (user.username,))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="用户名已存在")

        # 检查邮箱是否已存在
        cursor.execute('SELECT id FROM users WHERE email = ?', (user.email,))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="邮箱已被注册")

        # 创建用户
        user_id = str(uuid.uuid4())
        password_hash = hash_password(user.password)

        cursor.execute('''
            INSERT INTO users (id, username, email, password_hash)
            VALUES (?, ?, ?, ?)
        ''', (user_id, user.username, user.email, password_hash))

        # 生成token
        token = generate_token(user_id)

        conn.commit()
        conn.close()

        return {
            "success": True,
            "user_id": user_id,
            "username": user.username,
            "token": token,
            "message": "注册成功"
        }

    except HTTPException:
        raise
    except Exception as e:
        conn.close()
        raise HTTPException(status_code=500, detail=f"注册失败: {str(e)}")


@app.post("/api/auth/login")
async def login(user: UserLogin):
    """用户登录"""
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # 查找用户
        cursor.execute('SELECT id, password_hash FROM users WHERE username = ?', (user.username,))
        row = cursor.fetchone()

        if not row:
            raise HTTPException(status_code=401, detail="用户名或密码错误")

        user_id = row['id']
        password_hash = row['password_hash']

        # 验证密码
        if not verify_password(user.password, password_hash):
            raise HTTPException(status_code=401, detail="用户名或密码错误")

        # 生成token
        token = generate_token(user_id)

        # 更新最后登录时间
        cursor.execute('UPDATE users SET last_sync = CURRENT_TIMESTAMP WHERE id = ?', (user_id,))
        conn.commit()
        conn.close()

        return {
            "success": True,
            "user_id": user_id,
            "username": user.username,
            "token": token,
            "message": "登录成功"
        }

    except HTTPException:
        raise
    except Exception as e:
        conn.close()
        raise HTTPException(status_code=500, detail=f"登录失败: {str(e)}")


@app.post("/api/sync/push")
async def sync_push(sync_data: SyncData):
    """推送数据到云端"""
    # 简化版：直接使用username作为标识
    # 实际应该从token解析user_id

    try:
        # 从data中提取username（临时方案）
        username = sync_data.data.get("username", "anonymous")
        data_json = json.dumps(sync_data.data, ensure_ascii=False)

        conn = get_db_connection()
        cursor = conn.cursor()

        # 获取用户ID
        cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
        user_row = cursor.fetchone()

        if not user_row:
            # 如果用户不存在，创建一个临时用户
            user_id = str(uuid.uuid4())
            cursor.execute('''
                INSERT INTO users (id, username, email, password_hash)
                VALUES (?, ?, ?, ?)
            ''', (user_id, username, f"{username}@temp.com", hash_password("temp123")))
        else:
            user_id = user_row['id']

        # 获取当前版本
        cursor.execute('SELECT version FROM user_data WHERE user_id = ?', (user_id,))
        row = cursor.fetchone()
        current_version = row['version'] if row else 0
        new_version = current_version + 1

        # 保存或更新数据
        cursor.execute('''
            INSERT OR REPLACE INTO user_data (user_id, data_json, version, last_updated)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP)
        ''', (user_id, data_json, new_version))

        # 记录同步历史
        cursor.execute('''
            INSERT INTO sync_history (user_id, sync_type, client_version, success)
            VALUES (?, ?, ?, 1)
        ''', (user_id, "push", sync_data.client_version))

        conn.commit()
        conn.close()

        return {
            "success": True,
            "version": new_version,
            "timestamp": datetime.now().isoformat(),
            "message": "数据同步成功"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"同步失败: {str(e)}")


@app.post("/api/sync/pull")
async def sync_pull(request: SyncPull):
    """从云端拉取数据"""
    try:
        # 从token或数据中获取username（临时方案）
        # 实际应该从token解析

        conn = get_db_connection()
        cursor = conn.cursor()

        # 简化版：获取所有用户数据（实际应该根据token获取特定用户）
        cursor.execute('SELECT data_json, version, last_updated FROM user_data ORDER BY last_updated DESC LIMIT 1')
        row = cursor.fetchone()

        if not row:
            return {
                "success": True,
                "data": None,
                "version": 0,
                "message": "暂无云端数据"
            }

        conn.close()

        return {
            "success": True,
            "data": json.loads(row['data_json']),
            "version": row['version'],
            "last_updated": row['last_updated'],
            "message": "数据拉取成功"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"拉取失败: {str(e)}")


@app.get("/api/sync/status")
async def sync_status():
    """获取同步状态"""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT COUNT(*) as total_users FROM users')
    total_users = cursor.fetchone()['total_users']

    cursor.execute('SELECT COUNT(*) as total_syncs FROM sync_history')
    total_syncs = cursor.fetchone()['total_syncs']

    cursor.execute('SELECT MAX(timestamp) as last_sync FROM sync_history')
    last_sync = cursor.fetchone()['last_sync']

    conn.close()

    return {
        "status": "healthy",
        "total_users": total_users,
        "total_syncs": total_syncs,
        "last_sync": last_sync
    }


# ==================== 启动服务器 ====================
if __name__ == "__main__":
    import uvicorn

    # 初始化数据库
    init_server_database()
    print("✅ 服务器数据库初始化完成")

    # 启动服务器
    print("🚀 启动DeepRead云端同步服务器...")
    print("📡 API地址: http://localhost:8000")
    print("📚 API文档: http://localhost:8000/docs")

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
