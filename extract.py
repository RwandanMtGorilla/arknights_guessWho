import json
import os
from bs4 import BeautifulSoup
import re
import hashlib

def extract_operators_info(html_file_path):
    """
    从HTML文件中提取所有干员信息
    """
    # 读取HTML文件
    with open(html_file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, 'html.parser')

    # 直接定位到 <div id="filter-data">
    filter_data = soup.find('div', id='filter-data')

    if not filter_data:
        print("错误: 未找到 <div id=\"filter-data\"> 标签")
        return []

    print("成功定位到 <div id=\"filter-data\"> 标签")

    # 获取所有直接子div作为干员容器
    operator_containers = filter_data.find_all('div', recursive=False)

    print(f"找到 {len(operator_containers)} 个干员容器")

    operators_data = []

    for container in operator_containers:
        try:
            operator_info = {}

            # 从data属性中提取所有信息
            attrs = container.attrs

            # 基本信息
            if 'data-zh' in attrs:
                operator_info['姓名'] = attrs['data-zh']

            if 'data-en' in attrs:
                operator_info['英文名'] = attrs['data-en']

            if 'data-ja' in attrs:
                operator_info['日文名'] = attrs['data-ja']

            # 职业信息
            if 'data-profession' in attrs:
                operator_info['职业'] = attrs['data-profession']

            if 'data-subprofession' in attrs:
                operator_info['子职业'] = attrs['data-subprofession']

            # 稀有度和阵营
            if 'data-rarity' in attrs:
                operator_info['稀有度'] = attrs['data-rarity']

            if 'data-logo' in attrs:
                operator_info['势力'] = attrs['data-logo']

            if 'data-nation' in attrs:
                operator_info['国家'] = attrs['data-nation']

            if 'data-group' in attrs and attrs['data-group']:
                operator_info['小队'] = attrs['data-group']

            # 出身和种族
            if 'data-birth_place' in attrs and attrs['data-birth_place']:
                operator_info['出身地'] = attrs['data-birth_place']

            if 'data-race' in attrs and attrs['data-race']:
                operator_info['种族'] = attrs['data-race']

            # 基础属性
            if 'data-hp' in attrs:
                operator_info['生命值'] = attrs['data-hp']

            if 'data-atk' in attrs:
                operator_info['攻击'] = attrs['data-atk']

            if 'data-def' in attrs:
                operator_info['防御'] = attrs['data-def']

            if 'data-res' in attrs:
                operator_info['法术抗性'] = attrs['data-res']

            # 部署属性
            if 'data-re_deploy' in attrs:
                operator_info['再部署时间'] = attrs['data-re_deploy']

            if 'data-cost' in attrs:
                operator_info['部署费用'] = attrs['data-cost']

            if 'data-block' in attrs:
                operator_info['阻挡'] = attrs['data-block']

            if 'data-interval' in attrs:
                operator_info['攻击间隔'] = attrs['data-interval']

            # 标签信息
            if 'data-sex' in attrs:
                operator_info['性别'] = attrs['data-sex']

            if 'data-position' in attrs:
                operator_info['位置'] = attrs['data-position']

            if 'data-tag' in attrs and attrs['data-tag']:
                operator_info['标签'] = attrs['data-tag'].split()

            # 获取方式
            if 'data-obtain_method' in attrs:
                operator_info['获取方式'] = attrs['data-obtain_method']

            # 特性（从div的文本内容获取）
            feature_text = container.get_text(strip=True)
            if feature_text:
                # 移除HTML标签，只保留纯文本
                from bs4 import NavigableString
                feature_text = ''.join(container.stripped_strings)
                operator_info['特性'] = feature_text

            # 构建头像URL（基于干员名称）
            # MediaWiki使用文件名的MD5哈希来生成路径: {hash[0]}/{hash[0:2]}/filename
            if 'data-zh' in attrs:
                name = attrs['data-zh']
                filename = f"头像_{name}.png"

                # 计算MD5哈希
                md5_hash = hashlib.md5(filename.encode('utf-8')).hexdigest()

                # 生成完整URL
                operator_info['头像URL'] = f"https://media.prts.wiki/{md5_hash[0]}/{md5_hash[0:2]}/{filename}"
                operator_info['头像本地路径'] = f"avatars/{filename}"

            # 只添加有姓名的干员
            if '姓名' in operator_info:
                operators_data.append(operator_info)

        except Exception as e:
            # 尝试提取干员名称用于调试
            name = "未知"
            try:
                if 'data-zh' in container.attrs:
                    name = container.attrs['data-zh']
            except:
                pass
            print(f"提取干员 [{name}] 信息时出错: {e}")
            import traceback
            traceback.print_exc()
            continue

    return operators_data

def save_operators_to_json(operators_data, output_file='operators_data.json'):
    """
    将干员数据保存为JSON文件
    """
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(operators_data, file, ensure_ascii=False, indent=2)
    
    print(f"干员信息已保存到 {output_file}")
    print(f"共提取了 {len(operators_data)} 个干员的信息")

if __name__ == "__main__":
    # 提取干员信息
    html_file_path = "input.html"
    
    if not os.path.exists(html_file_path):
        print(f"错误: 找不到文件 {html_file_path}")
        exit(1)
    
    print("开始提取干员信息...")
    operators_data = extract_operators_info(html_file_path)
    
    # 保存为JSON
    save_operators_to_json(operators_data)
    
    # 打印示例数据
    if operators_data:
        print("\n示例干员信息:")
        print(json.dumps(operators_data[0], ensure_ascii=False, indent=2))
