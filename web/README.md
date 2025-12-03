# 明日方舟干员选择游戏 - 纯静态版本

这是一个纯静态的明日方舟干员选择游戏，可以直接部署到 GitHub Pages。

## 部署到 GitHub Pages

### 方法一：直接上传

1. 创建一个新的 GitHub 仓库
2. 将 `web` 文件夹中的所有文件上传到仓库根目录
3. 在仓库设置中启用 GitHub Pages，选择 `main` 分支
4. 访问 `https://你的用户名.github.io/仓库名` 即可游玩

### 方法二：使用 Git

```bash
cd web
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/你的用户名/仓库名.git
git push -u origin main
```

然后在 GitHub 仓库设置中启用 Pages。

## 文件结构

```
web/
├── index.html              # 主页面（包含所有游戏逻辑）
├── operators_data.json     # 干员数据（已筛选六星）
├── avatars/                # 干员头像图片文件夹
│   ├── 头像_XXX.png
│   └── ...
└── README.md              # 说明文档
```

## 功能特性

### 与后端版本的对比

| 功能 | 后端版本 | 静态版本 |
|------|---------|---------|
| 干员筛选 | 所有干员 | 仅六星干员（稀有度=5） |
| 随机算法 | Python random + 时间种子 | JS 自定义 LCG + 时间种子 |
| 校验码生成 | MD5 (Python hashlib) | MD5 (CryptoJS) |
| 数据加载 | FastAPI 后端接口 | 静态 JSON 文件 |
| 头像加载 | 动态文件检测 | 静态路径引用 |
| 自动刷新 | 需手动刷新 | 每分钟自动更新 |

### 核心逻辑

1. **时间种子**：使用 `YYYYMMDDHHMM` 格式，确保同一分钟内所有用户获得相同的干员列表
2. **随机算法**：使用线性同余发生器（LCG）实现可重现的随机数序列
3. **校验码**：基于干员姓名和时间种子生成 MD5 哈希，取后4位作为校验码
4. **六星筛选**：仅从稀有度为 "5" 的干员中抽取（明日方舟稀有度从0开始）

### 游戏规则

- **双击干员**：选择干员（红框标记，一局只能选一次，选择后不可更改）
- **单击干员**：排除干员（变灰，可反复切换，已选中的干员也可排除）
- **校验码**：与朋友对比校验码，确保获得相同的干员列表
- **自动刷新**：游戏会在每分钟自动刷新，获取新的干员组合

## 技术实现

### 随机数生成器

使用线性同余发生器（LCG）算法：

```javascript
value = (value * 9301 + 49297) % 233280
random = value / 233280
```

### 校验码算法

```javascript
// 1. 提取所有干员姓名并排序
const operatorNames = operators.map(op => op.姓名).sort()

// 2. 拼接时间种子和姓名
const dataStr = timeSeed + operatorNames.join('')

// 3. 生成 MD5 哈希
const hash = CryptoJS.MD5(dataStr).toString()

// 4. 取前8位16进制转数字，再取后4位
const code = String(parseInt(hash.substring(0, 8), 16)).slice(-4).padStart(4, '0')
```

## 依赖项

- **CryptoJS**：用于 MD5 哈希生成
  - CDN: `https://cdnjs.cloudflare.com/ajax/libs/crypto-js/4.1.1/crypto-js.min.js`

## 浏览器兼容性

- Chrome/Edge: ✅
- Firefox: ✅
- Safari: ✅
- IE11: ❌（不支持 ES6 语法）

## 本地测试

由于浏览器的 CORS 限制，需要使用本地服务器：

### 使用 Python

```bash
# Python 3
cd web
python -m http.server 8000
```

然后访问 `http://localhost:8000`

### 使用 Node.js

```bash
# 安装 http-server
npm install -g http-server

# 启动服务器
cd web
http-server -p 8000
```

### 使用 VS Code

安装 "Live Server" 插件，右键 `index.html` 选择 "Open with Live Server"

## 常见问题

### Q: 为什么只有六星干员？

A: 为了适应 GitHub Pages 的静态部署限制，我们筛选了六星干员以减少数据量，同时保证游戏体验。

### Q: 校验码不一致怎么办？

A: 确保两位玩家在同一分钟内开始游戏。校验码是基于当前时间（精确到分钟）生成的。

### Q: 图片加载失败怎么办？

A: 确保 `avatars` 文件夹中的图片文件名与 `operators_data.json` 中的 `头像本地路径` 字段一致。

### Q: 可以修改干员数量吗？

A: 可以！在 `index.html` 中找到 `selectOperators` 方法，修改 `shuffled.slice(0, 30)` 中的数字即可。

## 开源协议

本项目仅供学习交流使用。所有明日方舟相关素材版权归上海鹰角网络科技有限公司所有。
