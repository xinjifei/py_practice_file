import requests

response = requests.get("https://www.bilibili.com/")

print(response.text)