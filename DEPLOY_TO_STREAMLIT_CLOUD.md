# 部署到 Streamlit Cloud - 完整指南

## 为什么选择 Streamlit Cloud？

- ✅ **完全免费** - 每月500小时运行时间
- ✅ **自动HTTPS** - 微信/小红书分享必备
- ✅ **5分钟部署** - 最简单的部署方式
- ✅ **自动更新** - Git推送自动重新部署
- ✅ **官方支持** - Streamlit官方平台

---

## 步骤1：准备代码（3分钟）

### 1.1 创建GitHub仓库

```bash
# 在 deepread 目录下
cd c:\Users\黎又榜\每日新闻推送系统\deepread

# 初始化Git仓库（如果还没有）
git init

# 创建 .gitignore（如果没有）
echo "streamlit/
*.pyc
__pycache__/
.env
data/
cache/
*.log
.DS_Store
" > .gitignore

# 添加所有文件
git add .

# 提交
git commit -m "feat: DeepRead V3.8 深度阅读应用"
```

### 1.2 推送到GitHub

**在GitHub上创建新仓库：**
1. 访问 https://github.com/new
2. 仓库名：`deepread-app`
3. 设为私有或公开都可以
4. 不要初始化README（已有代码）

**推送代码：**
```bash
# 添加远程仓库（替换YOUR_USERNAME）
git remote add origin https://github.com/YOUR_USERNAME/deepread-app.git

# 推送代码
git branch -M main
git push -u origin main
```

---

## 步骤2：部署到 Streamlit Cloud（2分钟）

### 2.1 注册 Streamlit Cloud

1. 访问：https://streamlit.io/cloud
2. 点击 "Sign up" 或 "Login"
3. 使用GitHub账号登录

### 2.2 部署应用

1. 登录后，点击 "New app"
2. 填写信息：
   - **Repository:** 选择 `deepread-app`
   - **Branch:** `main`
   - **Main file path:** `app_v3.8.py`
3. 点击 "Deploy"

### 2.3 等待部署

- 首次部署需要1-2分钟（安装依赖）
- 部署成功后会显示一个URL，例如：
  ```
  https://your-app-name.streamlit.app
  ```

---

## 步骤3：获取分享链接

部署成功后，你会得到一个公网URL：

```
https://deepread-app.streamlit.app
```

**这个链接可以：**
- ✅ 直接分享到微信
- ✅ 直接分享到小红书
- ✅ 任何人都可访问（如果是公开仓库）

---

## 步骤4：配置自定义域名（可选）

如果想要更专业的域名，如 `reading.yourdomain.com`：

### 4.1 在 Streamlit Cloud 中

1. 进入应用设置
2. 点击 "Settings" → "Domains"
3. 添加自定义域名

### 4.2 在域名提供商（如阿里云、腾讯云）

1. 添加CNAME记录：
   ```
   类型: CNAME
   主机记录: reading
   记录值: your-app-name.streamlit.app
   ```

2. 等待DNS生效（最多48小时，通常几分钟）

---

## 步骤5：更新应用

**代码更新后：**
```bash
# 1. 修改代码
# 2. 提交到Git
git add .
git commit -m "描述你的修改"

# 3. 推送到GitHub
git push
```

**Streamlit Cloud会自动：**
- 检测到新代码
- 自动重新部署
- 无需手动操作

---

## 常见问题

### Q1: 部署失败怎么办？

**检查以下几点：**
1. 确保所有依赖都在 `requirements.txt` 中
2. 检查Python版本（3.8-3.11）
3. 查看部署日志（在Streamlit Cloud控制台）

### Q2: 如何设置环境变量？

**在Streamlit Cloud中：**
1. 进入应用设置
2. 点击 "Settings" → "Secrets"
3. 添加环境变量（如API密钥）

**代码中访问：**
```python
import streamlit as st

# 读取密钥
api_key = st.secrets["API_KEY"]
```

### Q3: 数据如何持久化？

**Streamlit Cloud 的限制：**
- 每次重新部署，文件系统会重置
- 需要使用外部数据库或云存储

**推荐方案：**
- **轻量级数据：** 使用 `st.session_state`
- **用户数据：** 连接SQLite/PostgreSQL
- **文件存储：** 使用AWS S3或阿里云OSS

### Q4: 如何保护应用隐私？

**选项1：密码保护**
```python
import streamlit as st

# 在app开头添加
def check_password():
    def password_entered():
        if st.session_state["password"] == "your_password":
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # 不显示密码
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input("密码", type="password", on_change=password_entered, key="password")
        return False

    return st.session_state["password_correct"]

if not check_password():
    st.stop()  # 停止执行

# 你的应用代码...
```

**选项2：限制访问**
- 使用GitHub仓库的私有设置
- Streamlit Cloud私有应用（付费功能）

### Q5: 微信分享后的样式问题？

**优化微信分享效果：**

1. **添加分享元数据**（需要自定义域名）
```html
<!-- index.html -->
<head>
    <meta property="og:title" content="DeepRead 深度阅读"/>
    <meta property="og:description" content="沉浸式阅读，深度思考"/>
    <meta property="og:image" content="https://your-domain.com/preview.png"/>
</head>
```

2. **使用Streamlit Cloud的默认分享卡片**
   - 微信会自动抓取页面标题和描述
   - 首次分享后，微信会缓存预览

---

## 高级配置

### 1. 添加分析统计

**使用Google Analytics：**
```python
# 在app_v3.8.py中
import streamlit as st

st.markdown("""
<!-- Global site tag (gtag.js) - Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
""", unsafe_allow_html=True)
```

### 2. 自定义主题

**创建 `.streamlit/config.toml`：**
```toml
[theme]
primaryColor = "#667eea"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F8F9FA"
textColor = "#2D3436"
font = "sans serif"

[client]
showErrorDetails = false
toolbarMode = "minimal"  # 隐藏菜单栏
```

### 3. 性能优化

**启用缓存：**
```python
import streamlit as st

@st.cache_data(ttl=3600)  # 缓存1小时
def load_books():
    return get_book_content()

@st.cache_resource
def load_model():
    return load_embedding_model()
```

---

## 成本估算

### Streamlit Cloud 免费额度

- ✅ **运行时间：** 每月500小时（约16小时/天）
- ✅ **存储：** 1GB
- ✅ **带宽：** 无限制
- ✅ **应用数量：** 无限制

**适合场景：**
- 个人项目
- 小团队（<10人同时使用）
- 非商业用途

### 付费方案

如果需要更多资源：
- **Professional:** $30/月
  - 无限运行时间
  - 优先支持
  - 更多配置选项

---

## 分享技巧

### 微信分享

**方式1：直接分享链接**
```
https://your-app.streamlit.app
```

**方式2：生成二维码**
```python
import qrcode
from io import BytesIO

url = "https://your-app.streamlit.app"
qr = qrcode.make(url)
img = BytesIO()
qr.save(img, format='PNG')
st.image(img)
```

**方式3：使用小程序卡片（需要开发）**
- 创建微信小程序
- 内嵌WebView打开应用

### 小红书分享

**图文形式：**
1. 截图应用界面（金句卡片、阅读海报）
2. 添加文案：
   ```
   💡 用DeepRead深度阅读
   每天进步一点点
   🔗 链接在评论区
   #深度阅读 #读书 #自我提升
   ```

**视频形式：**
1. 录屏演示应用功能
2. 添加背景音乐和字幕
3. 在描述中放置链接

---

## 备份方案：其他免费平台

如果Streamlit Cloud不可用，可以尝试：

### 1. Railway（免费额度$5/月）
```bash
# 安装Railway CLI
npm install -g railway

# 登录
railway login

# 部署
railway init
railway up
```

### 2. Render（免费额度有限）
- 访问：https://render.com
- 连接GitHub仓库
- 选择 "Web Service"
- 免费版会在15分钟无活动后休眠

### 3. Vercel（推荐前端应用）
- 适合静态网站
- Streamlit应用不太适合

### 4. 自建VPS（阿里云/腾讯云）
- 学生机约¥10/月
- 完全控制
- 需要自己配置环境

---

## 监控和维护

### 查看应用日志

**在Streamlit Cloud：**
1. 进入应用
2. 点击 "Logs"
3. 查看实时日志

### 监控应用状态

**使用Uptime Robot（免费）：**
1. 访问：https://uptimerobot.com
2. 添加监控：`https://your-app.streamlit.app`
3. 应用down时自动发邮件提醒

### 性能监控

**Streamlit Cloud自带：**
- CPU使用率
- 内存使用
- 访问统计

---

## 安全建议

1. **不要在代码中硬编码密钥**
   - 使用 `st.secrets`
   - 环境变量

2. **设置访问限制**
   - 密码保护
   - IP白名单（付费功能）

3. **定期备份**
   - Git仓库自动备份代码
   - 数据库需要定期导出

4. **HTTPS强制**
   - Streamlit Cloud自动提供
   - 无需额外配置

---

## 总结

**5分钟部署流程：**
1. ✅ 推送代码到GitHub
2. ✅ 在Streamlit Cloud连接仓库
3. ✅ 点击Deploy
4. ✅ 获得公网URL
5. ✅ 分享到微信/小红书

**预期结果：**
- 🌐 公网可访问的URL
- 🔒 自动HTTPS加密
- 📱 支持移动端访问
- 🔄 自动更新部署

**下一步：**
- [ ] 创建GitHub仓库
- [ ] 推送代码
- [ ] 部署到Streamlit Cloud
- [ ] 测试访问
- [ ] 分享链接

---

**需要帮助？**
- Streamlit Cloud文档：https://docs.streamlit.io/streamlit-cloud
- 常见问题：https://docs.streamlit.io/streamlit-cloud/get-started/deploy-your-app
