import json
import os
from bs4 import BeautifulSoup
import re

def extract_operators_info(html_file_path):
    """
    从HTML文件中提取所有干员信息
    """
    # 读取HTML文件
    with open(html_file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # 查找所有干员容器
    operator_containers = soup.find_all('div', class_='long-container') # short-container

    operators_data = []
    
    for container in operator_containers:
        try:
            operator_info = {}
            
            # 提取头像URL
            avatar_img = container.find('div', class_='avatar').find('img')
            if avatar_img:
                avatar_url = avatar_img.get('src') or avatar_img.get('data-src')
                operator_info['头像URL'] = avatar_url
                # 从URL中提取文件名作为本地存储路径
                if avatar_url:
                    filename = avatar_url.split('/')[-1]
                    operator_info['头像本地路径'] = f"avatars/{filename}"

            # 提取姓名信息
            name_section = container.find('div', class_='name')
            if name_section:
                name_divs = name_section.find_all('div')
                if len(name_divs) >= 1:
                    # 第一个div包含中文名
                    name_link = name_divs[0].find('a')
                    if name_link:
                        operator_info['姓名'] = name_link.find('div').text.strip()
                    else:
                        operator_info['姓名'] = name_divs[0].text.strip()
                
                # 英文名通常在第二个div
                if len(name_divs) >= 2:
                    operator_info['英文名'] = name_divs[1].text.strip()
                
                # 代号通常在第四个div
                if len(name_divs) >= 4:
                    operator_info['代号'] = name_divs[3].text.strip()
            
            # 提取势力/出身地/种族信息
            camp_section = container.find('div', class_='camp')
            if camp_section:
                camp_divs = camp_section.find_all('div')
                if len(camp_divs) >= 1:
                    operator_info['子职业'] = camp_divs[0].text.strip()
                if len(camp_divs) >= 2:
                    operator_info['势力'] = camp_divs[1].text.strip()
                if len(camp_divs) >= 3:
                    operator_info['出身地'] = camp_divs[2].text.strip()
                if len(camp_divs) >= 4:
                    operator_info['种族'] = camp_divs[3].text.strip()
            
            # 提取基础数据
            data_section = container.find('div', class_='data')
            if data_section:
                hp_elem = data_section.find('div', class_='hp')
                if hp_elem:
                    operator_info['生命值'] = hp_elem.text.strip()
                
                atk_elem = data_section.find('div', class_='atk')
                if atk_elem:
                    operator_info['攻击'] = atk_elem.text.strip()
                
                def_elem = data_section.find('div', class_='def')
                if def_elem:
                    operator_info['防御'] = def_elem.text.strip()
                
                res_elem = data_section.find('div', class_='res')
                if res_elem:
                    operator_info['法术抗性'] = res_elem.text.strip()
            
            # 提取属性信息
            property_section = container.find('div', class_='property')
            if property_section:
                redeploy_elem = property_section.find('div', class_='re_deploy')
                if redeploy_elem:
                    operator_info['再部署时间'] = redeploy_elem.text.strip()
                
                cost_elem = property_section.find('div', class_='cost')
                if cost_elem:
                    operator_info['部署费用'] = cost_elem.text.strip()
                
                block_elem = property_section.find('div', class_='block')
                if block_elem:
                    operator_info['阻挡'] = block_elem.text.strip()
                
                interval_elem = property_section.find('div', class_='interval')
                if interval_elem:
                    operator_info['攻击间隔'] = interval_elem.text.strip()
            
            # 提取获取方式
            obtain_section = container.find('div', class_='obtain')
            if obtain_section:
                operator_info['获取方式'] = obtain_section.text.strip()
            
            # 提取标签信息
            tag_section = container.find('div', class_='tag')
            if tag_section:
                tag_divs = tag_section.find_all('div')
                
                # 性别通常是第一个带class='sex'的div
                sex_elem = tag_section.find('div', class_='sex')
                if sex_elem:
                    operator_info['性别'] = sex_elem.text.strip()
                
                # 位置通常是第二个带class='position'的div
                position_elem = tag_section.find('div', class_='position')
                if position_elem:
                    operator_info['位置'] = position_elem.text.strip()
                
                # 其他标签
                other_tags = []
                for div in tag_divs:
                    if not div.get('class') or ('sex' not in div.get('class') and 'position' not in div.get('class')):
                        tag_text = div.text.strip()
                        if tag_text:
                            other_tags.append(tag_text)
                
                operator_info['标签'] = other_tags
            
            # 提取特性
            feature_section = container.find('div', class_='feature')
            if feature_section:
                # 移除HTML标签，只保留文本
                feature_text = feature_section.get_text(strip=True)
                operator_info['特性'] = feature_text
            
            operators_data.append(operator_info)
            
        except Exception as e:
            print(f"提取干员信息时出错: {e}")
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
