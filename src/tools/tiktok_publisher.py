"""
TikTok发布指南生成工具
为TikTok个人账号提供详细的手动发布指南
"""
import os
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from langchain.tools import tool


def _generate_tiktok_publishing_guide(
    material_name: str,
    video_urls: List[str],
    seo_package: Dict,
    publish_time: Optional[str] = None
) -> str:
    """
    生成TikTok发布指南。

    Args:
        material_name: 材料名称
        video_urls: 视频URL列表
        seo_package: SEO包装数据
        publish_time: 发布时间（可选）

    Returns:
        发布指南Markdown内容
    """
    # 计算推荐发布时间
    if not publish_time:
        # 默认在8小时后发布
        publish_time = (datetime.now() + timedelta(hours=8)).strftime("%Y-%m-%d %H:%M")

    # 获取视频信息
    video_count = len(video_urls)

    # 生成指南
    guide = f"""# 📱 TikTok发布指南

生成时间：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
材料：{material_name}

---

## 🎬 视频信息

### 视频列表
"""

    for i, video_url in enumerate(video_urls, 1):
        guide += f"""
**视频 {i}**
- 下载链接：{video_url}
- 提示：点击链接下载视频文件
- 文件名建议：tiktok_{material_name.lower()}_video{i}_{datetime.now().strftime("%Y%m%d")}.mp4
"""

    guide += f"""
**总数**：{video_count}个视频

**注意**：
- 视频链接24小时内有效，请立即下载
- 建议下载到 `Downloads` 或 `Desktop` 文件夹
- 下载后检查视频是否正常播放

---

## 📝 发布内容

### 推荐标题
{seo_package.get('tiktok', {}).get('title', f'{material_name}: 生物材料应用')}

### 推荐描述
{seo_package.get('tiktok', {}).get('description', f'{material_name}生物材料，用于组织工程和医疗应用。')}

### 推荐标签
{', '.join(seo_package.get('tiktok', {}).get('hashtags', ['#Biomaterial', '#Medical']))}

---

## ⏰ 发布时间

**建议发布时间**：{publish_time}（北京时间）

**最佳发布时段**：
- 北京时间：20:00 - 23:00
- 周末发布效果更好

---

## 📋 发布步骤（详细）

### 步骤1：准备视频
```
1. 点击上面的视频下载链接
2. 等待下载完成
3. 检查视频是否正常播放
4. 记住视频文件的保存位置
```

### 步骤2：打开TikTok App
```
1. 打开手机上的TikTok应用
2. 确保已登录你的账号
```

### 步骤3：上传视频
```
1. 点击右下角的 "+" 按钮
2. 选择"上传"或直接从相册选择
3. 找到刚才下载的视频文件
4. 点击"下一步"
```

### 步骤4：添加内容
```
标题/描述：
复制并粘贴下面的内容：

{seo_package.get('tiktok', {}).get('title', f'{material_name}: 生物材料应用')}

{seo_package.get('tiktok', {}).get('description', f'{material_name}生物材料，用于组织工程和医疗应用。')}

标签：
{', '.join(seo_package.get('tiktok', {}).get('hashtags', ['#Biomaterial', '#Medical']))}
```

### 步骤5：设置发布选项
```
1. 选择"谁可以观看"：公开
2. 选择"允许评论"：允许所有人评论
3. 选择"允许下载"：允许（推荐）
4. 选择"允许合拍"：允许（推荐）
```

### 步骤6：发布
```
1. 检查标题、描述、标签是否正确
2. 预览视频效果
3. 点击"发布"按钮
4. 等待发布完成
```

---

## ✅ 发布后检查

### 检查项
```
□ 视频是否正常播放
□ 标题是否正确显示
□ 标签是否生效
□ 视频是否公开可见
□ 评论功能是否正常
```

### 查看发布状态
```
1. 点击右下角"我"
2. 点击"作品"
3. 查看最新发布的视频
4. 检查播放数、点赞数、评论数
```

---

## 💡 优化建议

### 标题优化
- 使用数字和emoji吸引注意力
- 例如："{material_name}的3个关键特性 🔬"
- 长度：15-30个字符

### 标签优化
- 使用3-5个相关标签
- 包含热门标签（如 #Biomaterial #TikTokScience）
- 包含小众标签（精准定位）

### 发布时间
- 避开工作日的高峰时段（18:00-19:00）
- 选择用户活跃时段（20:00-23:00）
- 周末发布效果通常更好

### 互动建议
- 发布后30分钟内回复评论
- 主动点赞和回复粉丝互动
- 在评论区补充更多信息

---

## 📊 预期效果

### 目标受众
- 生物材料研究人员
- 医疗器械工程师
- 生物医药行业从业者
- 医学生物专业学生

### 预期数据（首周）
- 播放量：1,000 - 5,000
- 点赞率：5-10%
- 评论率：1-3%
- 分享率：1-2%

### 转化目标
- WhatsApp咨询：5-10次/周
- 技术咨询：3-5次/周
- 商业合作：1-2次/周

---

## 🔗 相关链接

### WhatsApp联系
+1 (213) 275-7332

### 更多资源
- 视频完整版：查看YouTube频道
- 技术文档：联系WhatsApp获取
- 合作咨询：WhatsApp +1 (213) 275-7332

---

## 📞 需要帮助？

如果在发布过程中遇到问题：

1. **视频无法下载**：检查网络连接，重新点击链接
2. **视频格式不支持**：TikTok支持MP4、MOV、WebM格式
3. **标题字符限制**：TikTok标题限制150字符
4. **标签数量限制**：最多添加5个标签
5. **发布失败**：检查网络，重新尝试

---

**生成工具**：Biomat_Video_Engine Pro v2.0
**版本**：2.0
**更新时间**：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""

    return guide


@tool
def generate_tiktok_publishing_guide(
    material_name: str,
    video_url: str,
    title: str = "",
    description: str = "",
    hashtags: str = ""
) -> str:
    """
    生成TikTok发布指南（适用于个人账号）。

    Args:
        material_name: 材料名称（如 "PCL", "PLLA"）
        video_url: 视频下载链接
        title: 推荐标题（可选）
        description: 推荐描述（可选）
        hashtags: 推荐标签，逗号分隔（可选）

    Returns:
        完整的TikTok发布指南Markdown内容
    """
    # 构建SEO包
    seo_package = {
        "tiktok": {
            "title": title or f"{material_name}: 生物材料应用创新",
            "description": description or f"{material_name}生物可降解聚合物，用于组织工程、医疗器械和药物输送系统。",
            "hashtags": hashtags.split(",") if hashtags else [
                f"#{material_name}",
                "#Biomaterial",
                "#TissueEngineering",
                "#MedicalPolymer",
                "#Biodegradable"
            ]
        }
    }

    # 生成指南
    guide = _generate_tiktok_publishing_guide(
        material_name=material_name,
        video_urls=[video_url],
        seo_package=seo_package
    )

    return guide


@tool
def save_tiktok_publishing_guide(
    material_name: str,
    video_url: str,
    title: str = "",
    description: str = "",
    hashtags: str = "",
    save_path: str = "/tmp"
) -> str:
    """
    生成并保存TikTok发布指南到本地文件。

    Args:
        material_name: 材料名称
        video_url: 视频下载链接
        title: 推荐标题
        description: 推荐描述
        hashtags: 推荐标签
        save_path: 保存路径（默认：/tmp）

    Returns:
        保存的文件路径
    """
    # 生成指南内容
    guide_content = generate_tiktok_publishing_guide(
        material_name=material_name,
        video_url=video_url,
        title=title,
        description=description,
        hashtags=hashtags
    )

    # 生成文件名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"tiktok_publishing_guide_{material_name.lower()}_{timestamp}.md"
    filepath = os.path.join(save_path, filename)

    # 保存文件
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(guide_content)

    result = f"✅ TikTok发布指南已生成并保存！\n\n"
    result += f"**文件路径**: {filepath}\n"
    result += f"**文件名**: {filename}\n"
    result += f"\n📝 该指南包含完整的发布步骤、推荐内容、最佳实践和优化建议。\n"
    result += f"\n🚀 请打开文件查看详细指南，按照步骤手动发布到TikTok。"

    return result
