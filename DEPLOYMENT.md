# DeepRead 部署指南

本文档介绍如何将 DeepRead 深度阅读应用部署到生产环境。

## 📋 目录

- [环境要求](#环境要求)
- [部署方式](#部署方式)
  - [Docker 部署（推荐）](#docker-部署推荐)
  - [传统方式部署](#传统方式部署)
  - [云平台部署](#云平台部署)
- [配置说明](#配置说明)
- [性能优化](#性能优化)
- [故障排查](#故障排查)

## 🔧 环境要求

### 系统要求
- **操作系统**: Linux / macOS / Windows
- **Python 版本**: 3.10 或更高
- **内存**: 至少 2GB RAM
- **磁盘空间**: 至少 5GB 可用空间

### 依赖软件
- Docker (推荐) 或 Python 3.10+
- Git (可选，用于版本控制)

## 🚀 部署方式

### 方式一：Docker 部署（推荐）

#### 1. 使用 Dockerfile

```bash
# 构建镜像
docker build -t deepread:latest .

# 运行容器
docker run -d \
  --name deepread-app \
  -p 8501:8501 \
  --restart unless-stopped \
  deepread:latest
```

#### 2. 使用 Docker Compose（推荐）

```bash
# 一键启动
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down

# 重启服务
docker-compose restart
```

#### 3. 访问应用

启动成功后，在浏览器中访问：
- **本地**: http://localhost:8501
- **远程**: http://YOUR_SERVER_IP:8501

---

### 方式二：传统方式部署

#### 1. 安装依赖

```bash
# 克隆项目（如果从 Git 仓库）
git clone <repository-url>
cd deepread

# 安装 Python 依赖
pip install -r requirements.txt
```

#### 2. 启动应用

```bash
# 开发模式
streamlit run app_v3.8.py

# 生产模式
streamlit run app_v3.8.py --server.port=8501 --server.address=0.0.0.0 --server.headless=true
```

#### 3. 使用进程管理器（推荐）

**使用 PM2 (Node.js 工具，也可管理 Python)**

```bash
# 安装 PM2
npm install -g pm2

# 启动应用
pm2 start "streamlit run app_v3.8.py --server.port=8501 --server.address=0.0.0.0 --server.headless=true" --name deepread

# 查看状态
pm2 status

# 查看日志
pm2 logs deepread

# 设置开机自启
pm2 startup
pm2 save
```

**使用 Systemd (Linux)**

创建服务文件 `/etc/systemd/system/deepread.service`:

```ini
[Unit]
Description=DeepRead Deep Reading App
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/path/to/deepread
ExecStart=/usr/bin/python -m streamlit run app_v3.8.py --server.port=8501 --server.address=0.0.0.0 --server.headless=true
Restart=always

[Install]
WantedBy=multi-user.target
```

启动服务：
```bash
sudo systemctl daemon-reload
sudo systemctl enable deepread
sudo systemctl start deepread
sudo systemctl status deepread
```

---

### 方式三：云平台部署

#### 1. Streamlit Cloud（最简单）

1. 将代码上传到 GitHub
2. 访问 [share.streamlit.io](https://share.streamlit.io)
3. 连接 GitHub 仓库
4. 选择 `app_v3.8.py` 作为主文件
5. 点击部署

#### 2. Heroku

创建 `Procfile`:
```
web: streamlit run app_v3.8.py --server.port=$PORT --server.address=0.0.0.0
```

部署：
```bash
# 登录 Heroku
heroku login

# 创建应用
heroku create your-app-name

# 推送代码
git push heroku main

# 打开应用
heroku open
```

#### 3. Railway / Render / Fly.io

这些平台都支持从 GitHub 自动部署，只需：
1. 连接 GitHub 仓库
2. 配置构建命令和启动命令
3. 点击部署

---

## ⚙️ 配置说明

### 环境变量

创建 `.env` 文件（不要提交到 Git）：

```bash
# Streamlit 配置
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
STREAMLIT_SERVER_HEADLESS=true
STREAMLIT_LOGGER_LEVEL=info

# 可选：API 密钥（如果使用外部服务）
# GROQ_API_KEY=your_api_key_here
# OPENAI_API_KEY=your_api_key_here
```

### Streamlit 配置文件

创建 `.streamlit/config.toml`:

```toml
[server]
port = 8501
address = "0.0.0.0"
headless = true
enableCORS = false
enableXsrfProtection = true

[logger]
level = "info"

[browser]
gatherUsageStats = false
serverAddress = "localhost"
serverPort = 8501

[theme]
primaryColor = "#667eea"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F8F9FA"
textColor = "#2D3436"
font = "sans serif"
```

---

## 🚄 性能优化

### 1. 缓存优化

应用已内置缓存机制，确保 `lazy_loader.py` 正常工作。

### 2. 内存优化

```bash
# 在 Docker 中限制内存使用
docker run -d \
  --name deepread-app \
  --memory="2g" \
  -p 8501:8501 \
  deepread:latest
```

### 3. 并发优化

在 `config.toml` 中设置：
```toml
[server]
maxUploadSize = 200
maxMessageSize = 200
```

### 4. 静态资源 CDN

如果使用大量静态资源，建议使用 CDN 加速。

---

## 🔍 故障排查

### 问题 1: 应用无法启动

**检查日志**:
```bash
# Docker
docker logs deepread-app

# 传统方式
pm2 logs deepread
# 或
journalctl -u deepread -f
```

**常见原因**:
- 端口被占用：修改端口配置
- 依赖缺失：重新安装 `pip install -r requirements.txt`
- 权限问题：确保有文件读写权限

### 问题 2: 页面加载缓慢

**解决方案**:
- 检查网络连接
- 清除缓存：删除 `__pycache__` 和 `.streamlit/cache`
- 增加内存配置
- 检查服务器资源使用情况

### 问题 3: 数据丢失

**预防措施**:
- 定期备份数据目录
- 使用持久化存储（Docker volumes）
- 配置自动备份脚本

---

## 📊 监控和维护

### 健康检查

访问健康检查端点：
```
http://YOUR_SERVER:8501/_stcore/health
```

### 日志管理

```bash
# Docker 日志
docker logs -f deepread-app --tail 100

# PM2 日志
pm2 logs deepread --lines 100

# Systemd 日志
journalctl -u deepread -f
```

### 更新应用

```bash
# Docker
docker-compose down
docker pull deepread:latest
docker-compose up -d

# 传统方式
git pull
pip install -r requirements.txt
pm2 restart deepread
```

---

## 🔒 安全建议

1. **不要提交敏感信息**
   - 使用 `.gitignore` 忽略 `.env` 文件
   - 不要在代码中硬编码 API 密钥

2. **启用 HTTPS**
   - 使用 Nginx/Caddy 反向代理
   - 配置 SSL 证书（Let's Encrypt 免费证书）

3. **限制访问**
   - 配置防火墙规则
   - 使用 VPN 或 IP 白名单

4. **定期更新**
   - 及时更新依赖包
   - 定期更新系统和 Docker 镜像

---

## 📞 支持

如遇到问题，请：
1. 查看本文档的故障排查部分
2. 检查 GitHub Issues
3. 提交新的 Issue（包含详细的错误日志和环境信息）

---

## 📄 许可证

请参考项目的 LICENSE 文件。
