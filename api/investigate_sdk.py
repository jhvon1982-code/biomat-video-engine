#!/usr/bin/env python3
"""
查看SDK源码，找出需要的所有环境变量
"""
import inspect
from coze_coding_dev_sdk.video import VideoGenerationClient
from coze_coding_dev_sdk import Config

print("=" * 60)
print("1. 查看 VideoGenerationClient 的源码")
print("=" * 60)

try:
    source = inspect.getsource(VideoGenerationClient.__init__)
    print(source)
except Exception as e:
    print(f"❌ 无法获取源码: {str(e)}")

print("\n" + "=" * 60)
print("2. 查看 Config 类的源码")
print("=" * 60)

try:
    config_source = inspect.getsource(Config.__init__)
    print(config_source)
except Exception as e:
    print(f"❌ 无法获取Config源码: {str(e)}")

print("\n" + "=" * 60)
print("3. 查看 Config 类的所有方法")
print("=" * 60)

try:
    methods = [m for m in dir(Config) if not m.startswith('_')]
    for method in methods:
        print(f"  - {method}")
except Exception as e:
    print(f"❌ 无法获取方法列表: {str(e)}")

print("\n" + "=" * 60)
print("4. 查看 Config 类的属性")
print("=" * 60)

try:
    config = Config()
    attrs = vars(config)
    print("Config实例属性:")
    for k, v in attrs.items():
        print(f"  {k} = {v}")
except Exception as e:
    print(f"❌ 无法获取属性: {str(e)}")

print("\n" + "=" * 60)
print("5. 查看 video_generation 方法的签名")
print("=" * 60)

try:
    sig = inspect.signature(VideoGenerationClient.video_generation)
    print(f"video_generation 方法签名:")
    print(f"  {sig}")
except Exception as e:
    print(f"❌ 无法获取签名: {str(e)}")

print("\n" + "=" * 60)
print("6. 查找所有COZE相关的环境变量名称")
print("=" * 60)

import os
import re

# 查找SDK代码中引用的环境变量
try:
    import coze_coding_dev_sdk
    sdk_path = coze_coding_dev_sdk.__file__
    print(f"SDK路径: {sdk_path}")

    # 读取SDK的主要配置文件
    config_files = [
        sdk_path,
        sdk_path.replace('__init__.py', 'config.py'),
        sdk_path.replace('__init__.py', '_config.py'),
    ]

    env_vars_found = set()
    for file_path in config_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # 查找 os.getenv, os.environ, getEnv 等环境变量引用
                matches = re.findall(r'(?:os\.getenv|os\.environ|getEnv)\s*\([\'"]([^\'"]+)[\'"]', content)
                env_vars_found.update(matches)
        except:
            pass

    if env_vars_found:
        print("\n发现的环境变量:")
        for var in sorted(env_vars_found):
            value = os.getenv(var, 'NOT SET')
            print(f"  {var} = {value[:50]}..." if len(str(value)) > 50 else f"  {var} = {value}")
    else:
        print("\n未找到环境变量引用")

except Exception as e:
    print(f"❌ 无法查找环境变量: {str(e)}")

print("\n" + "=" * 60)
print("7. 检查SDK的常量定义")
print("=" * 60)

try:
    import coze_coding_dev_sdk.constants
    print("\nconstants模块中的常量:")
    for attr in dir(coze_coding_dev_sdk.constants):
        if not attr.startswith('_'):
            value = getattr(coze_coding_dev_sdk.constants, attr)
            if not inspect.isclass(value) and not inspect.isfunction(value):
                print(f"  {attr} = {value}")
except:
    print("未找到constants模块或无法读取")
