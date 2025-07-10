
# 猜！干！员！（pvp激情对战版）
此代码用于启动一个明日方舟干员猜猜网页端，玩法参考: 
[b站视频 【超小杯】猜干员第四弹 | 让我知道我什么杯](https://www.bilibili.com/video/BV1oe9JYfEoY)

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

## 代码解释

- `main.py`: 基于fastapi 启动网页端后端
- `index.html`: 网页端前端代码
- `excel_generator_packaged.py` 适合没有公网ip条件时 用excel作为游戏载体


- `input.html`: [方舟wiki](https://prts.wiki/w/%E5%B9%B2%E5%91%98%E4%B8%80%E8%A7%88) 上复制来的htlm页面代码 （只含6星干员 可自选其他范围）
- `extract.py`: 读取`input.html` 抽取出信息，存入`operators_data.json`
- `operators_data.json`: 干员名称等页面抽取到的信息
- `downloader`: 读取`operators_data.json`获取头像链接 并下载头像png存储于`avatars`文件夹


