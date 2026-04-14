# Jimeng API Sub-account Configuration
# 火山引擎即梦子账户配置信息
# ⚠️ SECURITY WARNING: Keep this file secure, do not commit to public repositories

# Sub-account Information
JIMENG_SUB_ACCOUNT_NAME = "Biomat_Video_Engine"
JIMENG_SUB_ACCOUNT_ID = "2106811247"
JIMENG_SUB_ACCOUNT_LOGIN_URL = "https://console.volcengine.com/auth/login/user/2106811247"

# API Credentials (Volcengine)
JIMENG_ACCESS_KEY_ID = "YOUR_ACCESS_KEY_ID_HERE"
JIMENG_ACCESS_KEY_SECRET = "YOUR_ACCESS_KEY_SECRET_HERE"

# Status
JIMENG_SUB_ACCOUNT_STATUS = "Active, Reserved for Future Use"
JIMENG_SUB_ACCOUNT_CREATED_AT = "2026-04-13"
JIMENG_SUB_ACCOUNT_USAGE = "Not Currently Used - Using Coze Integration Instead"

# Current System Configuration
CURRENT_SYSTEM_TYPE = "Coze Integration"
CURRENT_MODEL = "doubao-seedance-1-5-pro-251215"
CURRENT_API_KEY = "COZE_WORKLOAD_IDENTITY_API_KEY (Environment Variable)"

# Notes
# - This sub-account is reserved as a backup solution
# - Current system uses Coze Integration API which internally connects to Jimeng
# - To switch to direct Volcengine API calls, modify jimeng_video_tool.py to use these credentials
# - Keep this file secure and do not share publicly
