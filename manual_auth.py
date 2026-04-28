"""
手动OAuth2认证脚本
用于在云端环境中生成授权URL
"""
import json
from google_auth_oauthlib.flow import InstalledAppFlow

# 创建OAuth流程（直接使用客户端密钥文件）
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
flow = InstalledAppFlow.from_client_secrets_file(
    'config/youtube_client_secrets.json',
    SCOPES
)

# 获取授权URL
auth_url, _ = flow.authorization_url(
    access_type='offline',
    include_granted_scopes='true',
    prompt='consent'
)

print("=" * 80)
print("YouTube OAuth2 授权流程")
print("=" * 80)
print()
print("请在浏览器中打开以下链接并授权：")
print()
print(auth_url)
print()
print("=" * 80)
print("授权后，浏览器会跳转到一个类似这样的URL：")
print("http://localhost/?code=4/0AX4XfWh...&scope=https://www.googleapis.com/auth/youtube.upload")
print()
print("请将完整的跳转URL（从 http:// 开始到结束）复制并粘贴到下面：")
print()

# 获取授权码
redirect_url = input("请粘贴授权后的跳转URL: ").strip()

# 提取授权码
if 'code=' in redirect_url:
    code = redirect_url.split('code=')[1].split('&')[0]

    # 交换访问令牌
    flow.fetch_token(code=code)

    # 获取凭证
    credentials = flow.credentials

    # 保存凭证
    with open('workspace/youtube_credentials.json', 'w') as f:
        f.write(credentials.to_json())

    print()
    print("=" * 80)
    print("✅ OAuth2认证成功！")
    print("=" * 80)
    print(f"凭证已保存到: workspace/youtube_credentials.json")
    print()
    print("现在你可以使用YouTube API上传视频了！")
else:
    print()
    print("=" * 80)
    print("❌ 无效的授权URL")
    print("=" * 80)
    print("请确保复制了完整的跳转URL")
