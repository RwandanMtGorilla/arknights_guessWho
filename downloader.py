import json
import requests
import os
from urllib.parse import urlparse, urljoin
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import re

def get_session_with_headers():
    """
    创建带有完整请求头的会话
    """
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Cache-Control': 'max-age=0'
    })
    return session

def download_avatar(avatar_info, avatars_folder="avatars", max_retries=3):
    """
    下载单个头像 - 修复版
    """
    name = avatar_info.get('姓名', 'Unknown')
    avatar_url = avatar_info.get('头像URL')
    
    if not avatar_url:
        print(f"警告: {name} 没有头像URL")
        return False, name, "没有URL"
    
    try:
        # 确保URL是完整的
        if not avatar_url.startswith('http'):
            if avatar_url.startswith('//'):
                avatar_url = 'https:' + avatar_url
            else:
                avatar_url = 'https://media.prts.wiki' + avatar_url
        
        # 从URL中提取文件名
        parsed_url = urlparse(avatar_url)
        filename = os.path.basename(parsed_url.path)
        
        # 清理文件名，确保是有效的文件名
        filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
        
        # 如果没有扩展名，默认为png
        if not filename.endswith(('.png', '.jpg', '.jpeg')):
            filename += '.png'
        
        # 为了避免文件名冲突，可以加上干员名称
        name_clean = re.sub(r'[<>:"/\\|?*]', '_', name)
        filename = f"{name_clean}_{filename}"
        
        # 创建文件路径
        file_path = os.path.join(avatars_folder, filename)
        
        # 如果文件已存在，跳过下载
        if os.path.exists(file_path):
            print(f"跳过 {name}: 文件已存在")
            return True, name, "文件已存在"
        
        # 创建会话
        session = get_session_with_headers()
        
        for attempt in range(max_retries):
            try:
                print(f"正在下载 {name} (尝试 {attempt + 1}/{max_retries}): {avatar_url}")
                
                # 首先访问主页面获取cookies
                try:
                    session.get('https://prts.wiki/', timeout=10)
                    time.sleep(1)  # 短暂延迟
                except:
                    pass  # 忽略主页面访问错误
                
                # 请求图片
                response = session.get(avatar_url, timeout=30, stream=True)
                
                # 检查响应状态
                response.raise_for_status()
                
                # 检查内容类型
                content_type = response.headers.get('content-type', '').lower()
                print(f"  内容类型: {content_type}")
                
                # 检查是否是图片
                if 'image' not in content_type and 'png' not in content_type:
                    # 读取一小部分内容检查是否是HTML
                    content_preview = response.content[:200].decode('utf-8', errors='ignore')
                    if '<html>' in content_preview.lower() or '<script>' in content_preview.lower():
                        print(f"  警告: 收到HTML重定向页面而非图片")
                        
                        # 尝试其他方法获取图片
                        # 有时候需要通过引用页面访问
                        session.headers.update({
                            'Referer': 'https://prts.wiki/'
                        })
                        
                        # 重新请求
                        response = session.get(avatar_url, timeout=30, stream=True)
                        response.raise_for_status()
                        
                        content_type = response.headers.get('content-type', '').lower()
                        print(f"  重新请求后内容类型: {content_type}")
                
                # 再次检查内容
                if 'image' not in content_type:
                    content_preview = response.content[:200].decode('utf-8', errors='ignore')
                    if '<html>' in content_preview.lower():
                        raise Exception("仍然收到HTML页面，可能需要登录或有其他限制")
                
                # 保存文件
                with open(file_path, 'wb') as file:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            file.write(chunk)
                
                # 验证文件大小
                file_size = os.path.getsize(file_path)
                if file_size < 100:  # 小于100字节可能不是有效图片
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        if '<html>' in content.lower():
                            os.remove(file_path)
                            raise Exception("下载的文件是HTML页面")
                
                print(f"成功下载 {name}: {filename} ({file_size} 字节)")
                return True, name, filename
                
            except requests.RequestException as e:
                if attempt < max_retries - 1:
                    print(f"下载 {name} 失败，重试 {attempt + 1}/{max_retries}: {e}")
                    time.sleep(3 + attempt)  # 递增延迟
                else:
                    print(f"下载 {name} 最终失败: {e}")
                    return False, name, str(e)
            except Exception as e:
                print(f"下载 {name} 时出现异常: {e}")
                if attempt < max_retries - 1:
                    time.sleep(3 + attempt)
                else:
                    return False, name, str(e)
    
    except Exception as e:
        print(f"处理 {name} 时出错: {e}")
        return False, name, str(e)

def test_single_download(operators_data, avatars_folder='avatars'):
    """
    测试下载单个头像以验证方法是否有效
    """
    if not operators_data:
        print("没有干员数据")
        return
    
    print("测试下载第一个干员的头像...")
    test_operator = operators_data[0]
    
    os.makedirs(avatars_folder, exist_ok=True)
    
    success, name, result = download_avatar(test_operator, avatars_folder)
    
    if success:
        print(f"测试成功！可以继续批量下载")
        return True
    else:
        print(f"测试失败: {result}")
        return False

def download_all_avatars(json_file='operators_data.json', avatars_folder='avatars', max_workers=2):
    """
    批量下载所有头像 - 修复版
    """
    if not os.path.exists(json_file):
        print(f"错误: 找不到文件 {json_file}")
        return
    
    # 创建头像文件夹
    os.makedirs(avatars_folder, exist_ok=True)
    
    # 读取干员数据
    with open(json_file, 'r', encoding='utf-8') as file:
        operators_data = json.load(file)
    
    print(f"找到 {len(operators_data)} 个干员")
    
    # 先测试下载一个
    if not test_single_download(operators_data, avatars_folder):
        print("测试下载失败，请检查网络连接或网站访问限制")
        return
    
    print(f"开始批量下载剩余 {len(operators_data)-1} 个干员的头像...")
    
    # 统计信息
    successful_downloads = 1  # 测试下载成功的那个
    failed_downloads = 0
    skipped_downloads = 0
    
    # 降低并发数以避免被封
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # 提交下载任务（跳过第一个，因为已经测试下载了）
        future_to_operator = {
            executor.submit(download_avatar, operator, avatars_folder): operator 
            for operator in operators_data[1:]  # 跳过第一个
        }
        
        # 处理完成的任务
        for future in as_completed(future_to_operator):
            operator = future_to_operator[future]
            try:
                success, name, result = future.result()
                if success:
                    if result == "文件已存在":
                        skipped_downloads += 1
                    else:
                        successful_downloads += 1
                else:
                    failed_downloads += 1
                
                # 在下载之间添加延迟
                time.sleep(1)
                
            except Exception as e:
                print(f"处理 {operator.get('姓名', 'Unknown')} 时发生异常: {e}")
                failed_downloads += 1
    
    # 输出统计结果
    print(f"\n下载完成!")
    print(f"成功下载: {successful_downloads}")
    print(f"跳过文件: {skipped_downloads}")
    print(f"下载失败: {failed_downloads}")
    print(f"总计处理: {len(operators_data)}")
    print(f"头像保存在: {os.path.abspath(avatars_folder)}")

def verify_downloaded_images(avatars_folder='avatars'):
    """
    验证下载的图片文件
    """
    if not os.path.exists(avatars_folder):
        print("头像文件夹不存在")
        return
    
    files = os.listdir(avatars_folder)
    png_files = [f for f in files if f.endswith(('.png', '.jpg', '.jpeg'))]
    
    print(f"\n验证 {len(png_files)} 个图片文件...")
    
    valid_count = 0
    invalid_count = 0
    
    for filename in png_files:
        filepath = os.path.join(avatars_folder, filename)
        file_size = os.path.getsize(filepath)
        
        if file_size < 100:
            print(f"可疑文件 {filename}: 大小只有 {file_size} 字节")
            # 检查是否是HTML
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    if '<html>' in content.lower():
                        print(f"  -> 这是HTML文件，不是图片")
                        invalid_count += 1
                        continue
            except:
                pass
        
        valid_count += 1
    
    print(f"有效图片: {valid_count}")
    print(f"无效文件: {invalid_count}")

if __name__ == "__main__":
    json_file = 'operators_data.json'
    avatars_folder = 'avatars'
    
    # 下载所有头像
    download_all_avatars(json_file, avatars_folder, max_workers=2)
    
    # 验证下载的图片
    verify_downloaded_images(avatars_folder)
