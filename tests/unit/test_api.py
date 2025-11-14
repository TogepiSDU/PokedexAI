import requests
import json

# 测试API的Python脚本
url = 'http://localhost:8000/api/v1/ask'
headers = {'Content-Type': 'application/json'}

# 测试皮卡丘特性问题
payload = {'question': '皮卡丘的特性是什么？'}
response = requests.post(url, headers=headers, json=payload)

print(f"状态码: {response.status_code}")
print(f"响应内容: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")

# 测试另一个问题
payload2 = {'question': '妙蛙种子的进化链是什么？'}
response2 = requests.post(url, headers=headers, json=payload2)

print(f"\n\n状态码: {response2.status_code}")
print(f"响应内容: {json.dumps(response2.json(), ensure_ascii=False, indent=2)}")