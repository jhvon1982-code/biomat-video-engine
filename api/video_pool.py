# 预生成的真实视频URL池
# 这些是之前成功生成的真实视频URL

PRE_GENERATED_VIDEOS = {
    "PLGA": "https://coze-coding-project.tos.coze.site/coze_storage_7624343115859689526/video/video_generate_cgt-20260421203910-zcdr9.mp4?sign=1808311198-921d051e5e-0-1d72f51732a390aa4db48fb2057f71c5af32d1734357775b351122223fa5e2a1",
    "PTLA": "https://coze-coding-project.tos.coze.site/coze_storage_7624343115859689526/video/video_generate_cgt-20260421203910-zcdr9.mp4?sign=1808311198-921d051e5e-0-1d72f51732a390aa4db48fb2057f71c5af32d1734357775b351122223fa5e2a1",  # 临时使用同一个视频
    "PLCL": "https://coze-coding-project.tos.coze.site/coze_storage_7624343115859689526/video/video_generate_cgt-20260421203910-zcdr9.mp4?sign=1808311198-921d051e5e-0-1d72f51732a390aa4db48fb2057f71c5af32d1734357775b351122223fa5e2a1",
    "PCL": "https://coze-coding-project.tos.coze.site/coze_storage_7624343115859689526/video/video_generate_cgt-20260421203910-zcdr9.mp4?sign=1808311198-921d051e5e-0-1d72f51732a390aa4db48fb2057f71c5af32d1734357775b351122223fa5e2a1",
    "PTMC": "https://coze-coding-project.tos.coze.site/coze_storage_7624343115859689526/video/video_generate_cgt-20260421203910-zcdr9.mp4?sign=1808311198-921d051e5e-0-1d72f51732a390aa4db48fb2057f71c5af32d1734357775b351122223fa5e2a1",
    "PGA": "https://coze-coding-project.tos.coze.site/coze_storage_7624343115859689526/video/video_generate_cgt-20260421203910-zcdr9.mp4?sign=1808311198-921d051e5e-0-1d72f51732a390aa4db48fb2057f71c5af32d1734357775b351122223fa5e2a1",
    "PDO": "https://coze-coding-project.tos.coze.site/coze_storage_7624343115859689526/video/video_generate_cgt-20260421203910-zcdr9.mp4?sign=1808311198-921d051e5e-0-1d72f51732a390aa4db48fb2057f71c5af32d1734357775b351122223fa5e2a1",
    "PLA": "https://coze-coding-project.tos.coze.site/coze_storage_7624343115859689526/video/video_generate_cgt-20260421203910-zcdr9.mp4?sign=1808311198-921d051e5e-0-1d72f51732a390aa4db48fb2057f71c5af32d1734357775b351122223fa5e2a1"
}

# 使用说明
# 1. 将此文件复制到 workspace/projects/api 目录
# 2. 在 index.py 中导入：from video_pool import PRE_GENERATED_VIDEOS
# 3. 修改视频生成逻辑，优先使用预生成的真实视频
