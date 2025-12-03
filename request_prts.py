#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
request_prts.py - 从PRTS wiki获取干员一览页面HTML

访问 https://prts.wiki/w/干员一览 并将返回的HTML保存到 input.html
"""

import requests


def fetch_operators_html():
    """获取干员一览页面的HTML内容"""
    url = "https://prts.wiki/w/干员一览"

    # 设置请求头，模拟浏览器访问
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    }

    print(f"正在访问: {url}")

    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()  # 检查响应状态码

        # 设置正确的编码
        response.encoding = response.apparent_encoding

        print(f"✓ 成功获取页面，大小: {len(response.text)} 字符")

        return response.text

    except requests.RequestException as e:
        print(f"✗ 请求失败: {e}")
        return None


def save_html(html_content, output_file="input.html"):
    """将HTML内容保存到文件"""
    if html_content is None:
        print("没有内容可保存")
        return False

    try:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(html_content)

        print(f"✓ HTML已保存到: {output_file}")
        return True

    except IOError as e:
        print(f"✗ 保存文件失败: {e}")
        return False


def main():
    """主函数"""
    print("=" * 50)
    print("PRTS Wiki 干员一览页面获取工具")
    print("=" * 50)

    # 获取HTML
    html_content = fetch_operators_html()

    # 保存到文件
    if html_content:
        save_html(html_content)
        print("\n完成!")
    else:
        print("\n失败!")


if __name__ == "__main__":
    main()
