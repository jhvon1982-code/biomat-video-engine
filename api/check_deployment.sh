#!/bin/bash
# 检查Render部署状态

echo "📊 检查Render部署状态"
echo ""

# 检查API版本
VERSION=$(curl -s https://biomat-video-engine.onrender.com/api/v1/health | python3 -c "import sys, json; print(json.load(sys.stdin)['version'])")
echo "当前版本: $VERSION"

if [ "$VERSION" = "3.0" ]; then
    echo "✅ 已部署到最新版本"
    echo ""
    echo "🚀 开始测试主API端点..."
    timeout 900 curl -s https://biomat-video-engine.onrender.com/api/v1/generate-video-simple \
        -X POST \
        -H "Authorization: Bearer bm_Pla1ic3_D3y3k3y_2k0k0k0k0k0k0k0k0k0k0k0k0k0k" \
        -H "Content-Type: application/json" \
        -d '{}' | python3 -m json.tool
else
    echo "⏳ 等待部署完成..."
    echo ""
    echo "最新版本应该是 3.0（硬编码环境变量）"
    echo "当前版本是 $VERSION"
    echo ""
    echo "可能的原因："
    echo "1. Render正在部署中（通常需要2-3分钟）"
    echo "2. 部署失败了"
    echo ""
    echo "建议："
    echo "- 在https://dashboard.render.com查看部署日志"
    echo "- 或等待2分钟后再次检查"
fi
