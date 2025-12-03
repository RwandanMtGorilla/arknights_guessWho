import hashlib

# 测试头像URL的生成逻辑
name = "圣聆初雪"
filename = f"头像_{name}.png"

# MediaWiki使用文件名的MD5哈希来生成路径
md5_hash = hashlib.md5(filename.encode('utf-8')).hexdigest()
print(f"文件名: {filename}")
print(f"MD5: {md5_hash}")
print(f"路径前缀: {md5_hash[0]}/{md5_hash[0:2]}/")
print(f"完整URL: https://media.prts.wiki/{md5_hash[0]}/{md5_hash[0:2]}/{filename}")

# 测试几个其他干员
test_names = ["12F", "Castle-3", "阿米娅", "凯尔希"]
for name in test_names:
    filename = f"头像_{name}.png"
    md5_hash = hashlib.md5(filename.encode('utf-8')).hexdigest()
    url = f"https://media.prts.wiki/{md5_hash[0]}/{md5_hash[0:2]}/{filename}"
    print(f"\n{name}: {url}")
