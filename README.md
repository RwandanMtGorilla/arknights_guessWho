
# 猜！干！员！（pvp激情对战版）
此代码用于启动一个明日方舟干员猜猜网页端，玩法参考: 
[b站视频 【超小杯】猜干员第四弹 | 让我知道我什么杯](https://www.bilibili.com/video/BV1oe9JYfEoY)

访问地址: [https://rwandanmtgorilla.github.io/arknights_guessWho/](https://rwandanmtgorilla.github.io/arknights_guessWho/)

## 玩法
### 游戏准备
1. 玩家双方确保可以相互联系(对话/通话)
2. 同时点击 `开始游戏`/`重新开始`。
3. 网页上方将出现四位数哈希值互相确认以确保拿到的是相同的牌型。(若不相同，回到2)
### 开始游戏
4. `双击`某干员头像 用以`选定`对方要猜的干员(此动作在一次对局中不可逆)
5. 相互轮流提问 `单击`以`排除`/`取消排除`某一干员

## install
```shell
git clone https://github.com/RwandanMtGorilla/arknights_guessWho.git

uv venv --python 3.9
.venv\Scripts\activate

uv pip install -r requirements.txt -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple


```
## run
```shell
# 启动游戏网页端
uv run main.py

```

## 更新干员数据

安装依赖后，在项目根目录执行以下命令。

```powershell
uv run update_data.py
```

也可以用已安装依赖的 Python 运行 `python update_data.py`。脚本会抓取 PRTS 干员一览、提取数据并补齐头像，全部成功后才替换 `input.html` 和 `operators_data.json`。头像下载失败后可以重跑，脚本会跳过已经下载的文件。更新成功后，在游戏页面点「重新开始」即可读取新数据。

## 代码解释

- `main.py`: 基于fastapi 启动网页端后端
- `index.html`: 网页端前端代码
- `excel_generator_packaged.py` 适合没有公网ip条件时 用excel作为游戏载体


- `request_prts.py`: 获取 [PRTS Wiki 干员一览](https://prts.wiki/w/%E5%B9%B2%E5%91%98%E4%B8%80%E8%A7%88) 页面，保存为 `input.html`
- `input.html`: 干员一览 HTML 快照
- `extract.py`: 读取`input.html` 抽取出信息，存入`operators_data.json`
- `operators_data.json`: 干员名称等页面抽取到的信息
- `downloader.py`: 读取干员数据中的头像链接，下载到 `avatars` 文件夹


