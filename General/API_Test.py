import requests

# 目标API的URL
url = 'https://jsonplaceholder.typicode.com/posts'

# 准备提交的数据
data = {
    'title': 'My New Post',
    'body': 'This is the content of my new post.',
    'userId': 2
}

# 发起POST请求
response = requests.post(url, json=data)

# 检查请求是否成功
if response.status_code == 201:
    # 打印创建的帖子信息
    post = response.json()
    print(f"Post created with ID: {post['id']}, Title: {post['title']}")
else:
    print('Failed to post data', response.status_code)
