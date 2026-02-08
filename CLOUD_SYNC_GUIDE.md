# DeepRead 云端同步功能使用指南

## 功能概述

DeepRead V3.8 现已支持真正的云端自动同步功能，可以实现：
- 🔄 自动数据同步（每5分钟）
- 📤 手动上传数据到云端
- 📥 手动从云端下载数据
- 👥 多设备数据同步
- 🔐 用户认证和授权

## 快速开始

### 1. 启动云端同步服务器

#### Windows:
```bash
start_cloud_server.bat
```

#### Linux/Mac:
```bash
chmod +x start_cloud_server.sh
./start_cloud_server.sh
```

或者直接运行:
```bash
python cloud_sync_server.py
```

服务器启动后，你将看到:
```
✅ 服务器数据库初始化完成
🚀 启动DeepRead云端同步服务器...
📡 API地址: http://localhost:8000
📚 API文档: http://localhost:8000/docs
```

### 2. 启动DeepRead应用

在另一个终端窗口运行:
```bash
streamlit run app_v3.8.py
```

### 3. 登录云端同步

1. 在DeepRead侧边栏找到 "☁️ 云端同步"
2. 点击 "🌐 云端自动同步" 展开
3. 如果是新用户，点击 "注册" 标签:
   - 输入用户名
   - 输入邮箱
   - 输入密码
   - 点击 "📝 注册"

4. 如果已有账号，点击 "登录" 标签:
   - 输入用户名
   - 输入密码
   - 点击 "🔑 登录"

登录成功后，自动同步将启用！

## 功能说明

### 自动同步

- 登录后，应用会每5分钟自动同步数据
- 同步包括:
  - 阅读目标
  - 阅读统计
  - 成就进度
  - 阅读历史
  - 用户偏好

### 手动同步

你可以随时手动触发同步:
- **📤 上传**: 将本地数据上传到云端
- **📥 下载**: 从云端下载数据到本地（自动合并）
- **🔗 测试**: 测试与云服务器的连接

### 本地备份

云端同步功能还包括本地备份能力:
- **导出数据**: 将所有数据导出为JSON文件
- **导入数据**: 从JSON文件恢复数据
- **智能合并**: 导入时自动合并冲突数据

## 多设备使用

### 设备A (主设备)

1. 启动服务器和DeepRead
2. 注册/登录账号
3. 开始使用，数据自动同步

### 设备B (其他设备)

1. 启动DeepRead (连接到同一服务器)
2. 使用相同的账号登录
3. 自动下载云端数据
4. 所有设备保持同步！

## API端点

服务器提供以下API端点:

### 认证
- `POST /api/auth/register` - 用户注册
- `POST /api/auth/login` - 用户登录

### 数据同步
- `POST /api/sync/push` - 推送数据到云端
- `POST /api/sync/pull` - 从云端拉取数据
- `GET /api/sync/status` - 获取同步状态

完整API文档: http://localhost:8000/docs

## 配置选项

### 服务器地址

默认服务器地址: `http://localhost:8000`

如需修改，设置环境变量:
```bash
export CLOUD_SYNC_SERVER=http://your-server:8000
```

### 同步间隔

默认每5分钟自动同步一次，可在代码中修改 `auto_sync_interval` 变量。

## 故障排除

### 无法连接到服务器

1. 检查服务器是否正在运行
2. 使用 "🔗 测试" 按钮测试连接
3. 查看服务器日志

### 同步失败

1. 检查网络连接
2. 确认用户名和密码正确
3. 尝试手动同步

### 数据丢失

1. 使用本地备份功能
2. 从最近的JSON备份文件恢复
3. 联系技术支持

## 安全说明

1. **密码存储**: 服务器使用SHA256哈希存储密码
2. **Token认证**: 使用token-based认证机制
3. **数据加密**: 建议在生产环境使用HTTPS
4. **备份**: 定期导出本地备份

## 生产部署

### 使用Docker

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY cloud_sync_server.py .
COPY cloud_server.db ./cloud_server.db

EXPOSE 8000

CMD ["python", "cloud_sync_server.py"]
```

### 使用Nginx反向代理

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 技术架构

- **后端框架**: FastAPI
- **数据库**: SQLite
- **认证**: Token-based
- **同步策略**: 智能合并
- **协议**: HTTP/REST API

## 未来改进

- [ ] 端到端加密
- [ ] 增量同步（只传输变化）
- [ ] 冲突解决UI
- [ ] 多用户协作
- [ ] 数据版本控制
- [ ] WebSocket实时同步

## 支持

如有问题，请访问:
- GitHub Issues: https://github.com/liyoubang97-hub/deepread-app/issues
- API文档: http://localhost:8000/docs

---

**享受深度阅读，数据永远同步！** 🚀📚
