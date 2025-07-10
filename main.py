from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import json
import os
import random
import hashlib
from datetime import datetime
from typing import List, Dict, Any
from pydantic import BaseModel

app = FastAPI(title="明日方舟干员选择游戏")

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该限制具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 静态文件服务
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/avatars", StaticFiles(directory="avatars"), name="avatars")

class OperatorResponse(BaseModel):
    operators: List[Dict[str, Any]]
    verification_code: str
    timestamp: str

def get_time_seed():
    """
    获取基于当前分钟的时间种子
    同一分钟内返回相同的种子
    """
    now = datetime.now()
    # 使用年月日时分作为种子，忽略秒
    time_str = now.strftime("%Y%m%d%H%M")
    return time_str

def generate_verification_code(operators: List[Dict], time_seed: str) -> str:
    """
    生成四位校验码
    基于干员列表和时间种子
    """
    # 创建一个基于干员名称和时间的字符串
    operator_names = [op.get('姓名', '') for op in operators]
    data_str = time_seed + ''.join(sorted(operator_names))
    
    # 生成哈希并取前4位
    hash_obj = hashlib.md5(data_str.encode('utf-8'))
    hash_hex = hash_obj.hexdigest()
    
    # 转换为4位数字码
    verification_code = str(int(hash_hex[:8], 16))[-4:].zfill(4)
    return verification_code

def load_operators_data():
    """
    加载干员数据
    """
    json_file = 'operators_data.json'
    avatars_folder = 'avatars'
    
    if not os.path.exists(json_file):
        raise HTTPException(status_code=500, detail="干员数据文件不存在")
    
    if not os.path.exists(avatars_folder):
        raise HTTPException(status_code=500, detail="头像文件夹不存在")
    
    try:
        with open(json_file, 'r', encoding='utf-8') as file:
            operators_data = json.load(file)
        
        valid_operators = []
        
        for operator in operators_data:
            name = operator.get('姓名', 'Unknown')
            
            if name != 'Unknown':
                # 检查头像文件是否存在
                possible_formats = [
                    f"{name}_头像_{name}.png",
                    f"头像_{name}.png",
                    f"{name}.png",
                    f"{name}_头像.png",
                ]
                
                avatar_url = None
                for format_name in possible_formats:
                    file_path = os.path.join(avatars_folder, format_name)
                    if os.path.exists(file_path):
                        avatar_url = f"/avatars/{format_name}"
                        break
                
                if avatar_url:
                    operator['avatar_url'] = avatar_url
                    valid_operators.append(operator)
        
        return valid_operators
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"加载干员数据时出错: {str(e)}")

@app.get("/")
async def read_root():
    """
    返回主页面
    """
    return FileResponse('static/index.html')

@app.get("/api/operators", response_model=OperatorResponse)
async def get_operators():
    """
    获取干员列表
    基于当前时间分钟生成固定的30个干员
    """
    try:
        # 获取时间种子
        time_seed = get_time_seed()
        
        # 加载所有有效干员
        valid_operators = load_operators_data()
        
        if len(valid_operators) < 30:
            raise HTTPException(
                status_code=500, 
                detail=f"有效干员数量不足，需要30个，当前只有{len(valid_operators)}个"
            )
        
        # 使用时间种子设置随机数种子
        random.seed(time_seed)
        
        # 选择30个干员
        selected_operators = random.sample(valid_operators, 30)
        
        # 生成校验码
        verification_code = generate_verification_code(selected_operators, time_seed)
        
        # 获取当前时间戳
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        return OperatorResponse(
            operators=selected_operators,
            verification_code=verification_code,
            timestamp=current_time
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取干员列表时出错: {str(e)}")

@app.get("/api/health")
async def health_check():
    """
    健康检查接口
    """
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5370)
