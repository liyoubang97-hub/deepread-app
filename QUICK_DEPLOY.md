# 🚀 快速部署指南

这份指南帮助您在 **5 分钟内** 部署 DeepRead 应用。

## 📦 部署前准备

### 1️⃣ 检查文件

确保以下文件存在：
- ✅ `app_v3.8.py` - 主应用文件
- ✅ `requirements.txt` - 依赖列表
- ✅ `lazy_loader.py` - 数据加载器
- ✅ `practice_tasks_enhanced.py` - 30天任务数据
- ✅ `demo_data_v2.py` - 书籍数据

### 2️⃣ 选择部署方式

| 部署方式 | 难度 | 适用场景 | 推荐度 |
|---------|------|---------|--------|
| **Docker** | ⭐⭐ | 生产环境、服务器 | ⭐⭐⭐⭐⭐ |
| **传统方式** | ⭐ | 快速测试、本地使用 | ⭐⭐⭐ |
| **Streamlit Cloud** | 简单 | 个人项目、演示 | ⭐⭐⭐⭐⭐ |

---

## 🎯 推荐部署方式

### 方式 A：Docker 部署（服务器）

```bash
# 1. 一键启动
docker-compose up -d

# 2. 访问应用
# 浏览器打开: http://YOUR_SERVER_IP:8501
```

**优点**：
- ✅ 环境隔离，不会污染系统
- ✅ 一键启动，一键停止
- ✅ 自动重启，稳定可靠

### 方式 B：传统方式部署（本地/简单）

**Windows:**
```bash
# 双击运行
start_production.bat
```

**Linux/Mac:**
```bash
# 添加执行权限
chmod +x start_production.sh

# 运行
./start_production.sh
```

**或者手动启动：**
```bash
pip install -r requirements.txt
streamlit run app_v3.8.py --server.port=8501
```

### 方式 C：Streamlit Cloud（零配置）

1. 将代码上传到 GitHub
2. 访问 [share.streamlit.io](https://share.streamlit.io)
3. 点击 "New app"
4. 选择 GitHub 仓库和 `app_v3.8.py`
5. 点击 "Deploy"

**完成！** 🎉

---

## ⚙️ 首次部署检查清单

- [ ] Python 3.10+ 已安装
- [ ] 所有依赖已安装（`pip install -r requirements.txt`）
- [ ] 端口 8501 未被占用
- [ ] 防火墙允许访问 8501 端口（远程部署）
- [ ] 浏览器可以访问 http://localhost:8501

---

## 🔧 常见问题

### Q1: 端口被占用怎么办？

**修改端口**：
```bash
# 使用其他端口
streamlit run app_v3.8.py --server.port=8502
```

### Q2: 依赖安装失败？

**使用国内镜像**：
```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### Q3: 应用启动慢？

**正常现象**：
- 首次启动需要加载模型和数据
- 后续启动会使用缓存，速度会快很多

### Q4: 如何在公网访问？

**方案 1：使用云服务器**
- 阿里云、腾讯云、AWS 等
- 配置安全组开放 8501 端口

**方案 2：使用 Streamlit Cloud**
- 自动分配公网域名
- 免费，适合个人使用

**方案 3：内网穿透**
- 使用 ngrok、frp 等工具

---

## 📊 性能建议

### 服务器配置建议

| 用户数 | CPU | 内存 | 带宽 |
|--------|-----|------|------|
| 1-10人 | 1核 | 2GB | 1Mbps |
| 10-50人 | 2核 | 4GB | 3Mbps |
| 50+人 | 4核 | 8GB | 5Mbps |

### 优化建议

1. **启用缓存**：应用已内置缓存机制
2. **定期清理**：每周清理一次缓存（`python clean_cache.py`）
3. **监控资源**：使用 `htop` 或 `top` 监控资源使用

---

## 🔒 安全提醒

1. **不要公开部署密钥**：如果有 API 密钥，使用环境变量
2. **启用 HTTPS**：生产环境建议使用 SSL 证书
3. **定期备份**：备份用户数据和配置

---

## 📞 需要帮助？

1. 查看 [完整部署文档](DEPLOYMENT.md)
2. 检查 GitHub Issues
3. 提交新的 Issue

---

**祝您部署顺利！** 🎉
