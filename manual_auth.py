"""
手动OAuth2认证脚本（Out of Band模式）
用于在云端环境中生成授权URL
"""
from google_auth_oauthlib.flow import InstalledAppFlow

# 创建OAuth流程（直接读取客户端密钥文件）
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
flow = InstalledAppFlow.from_client_secrets_file(
    'config/youtube_client_secrets.json',
    SCOPES
)

# 获取授权URL
auth_url, state = flow.authorization_url(
    access_type='offline',
    include_granted_scopes='true',
    prompt='consent'
)

print("=" * 80)
print("YouTube OAuth2 授权流程")
print("=" * 80)
print()
print("步骤1: 请在浏览器中打开以下链接并授权")
print()
print(auth_url)
print()
print("=" * 80)
print("步骤2: 授权后，浏览器会显示一个授权码")
print()
print("授权码看起来像这样：4/0AX4XfWh7w...")
print()
print("=" * 80)
print("步骤3: 将授权码粘贴到下面")
print()

# 获取授权码
auth_code = input("请粘贴授权码: ").strip()

if not auth_code:
    print()
    print("=" * 80)
    print("❌ 未输入授权码")
    print("=" * 80)
    exit(1)

try:
    # 交换访问令牌
    flow.fetch_token(code=auth_code)

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
    print()
    print("下一步：")
    print("1. 测试API健康检查: curl http://localhost:8001/health")
    print("2. 上传测试视频")

except Exception as e:
    print()
    print("=" * 80)
    print("❌ 授权失败")
    print("=" * 80)
    print(f"错误: {e}")
