#!/usr/bin/env python
"""检查构建配置的脚本"""

import os
import sys
from pathlib import Path

def check_file_exists(filepath):
    """检查文件是否存在"""
    if os.path.exists(filepath):
        print(f"[OK] {filepath} 存在")
        return True
    else:
        print(f"[FAIL] {filepath} 不存在")
        return False

def check_package_structure():
    """检查包结构"""
    print("\n检查包结构...")
    required_files = [
        "swagger_sdk/__init__.py",
        "swagger_sdk/builder.py",
        "swagger_sdk/models.py",
        "swagger_sdk/enums.py",
    ]
    all_exist = True
    for file in required_files:
        if not check_file_exists(file):
            all_exist = False
    return all_exist

def check_version_consistency():
    """检查版本号一致性"""
    print("\n检查版本号一致性...")
    
    # 从 __init__.py 读取版本
    init_path = Path("swagger_sdk/__init__.py")
    if not init_path.exists():
        print("✗ swagger_sdk/__init__.py 不存在")
        return False
    
    version_in_init = None
    with open(init_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("__version__"):
                version_in_init = line.split("=")[1].strip().strip('"').strip("'")
                break
    
    if not version_in_init:
        print("[FAIL] 在 __init__.py 中未找到 __version__")
        return False
    
    print(f"[OK] __init__.py 版本: {version_in_init}")
    
    # 检查 pyproject.toml
    if os.path.exists("pyproject.toml"):
        with open("pyproject.toml", "r", encoding="utf-8") as f:
            content = f.read()
            if f'version = "{version_in_init}"' in content:
                print(f"[OK] pyproject.toml 版本一致: {version_in_init}")
                return True
            else:
                print(f"[FAIL] pyproject.toml 版本不一致")
                return False
    
    return True

def check_build_files():
    """检查构建文件"""
    print("\n检查构建文件...")
    required_files = [
        "pyproject.toml",
        "setup.py",
        "MANIFEST.in",
        "LICENSE",
        "README.md",
    ]
    all_exist = True
    for file in required_files:
        if not check_file_exists(file):
            all_exist = False
    return all_exist

def check_metadata():
    """检查元数据"""
    print("\n检查元数据...")
    warnings = []
    
    # 检查 pyproject.toml
    if os.path.exists("pyproject.toml"):
        with open("pyproject.toml", "r", encoding="utf-8") as f:
            content = f.read()
            if "your.email@example.com" in content:
                warnings.append("[WARN] pyproject.toml 中的作者邮箱需要更新")
            if "yourusername" in content:
                warnings.append("[WARN] pyproject.toml 中的 GitHub 用户名需要更新")
    
    # 检查 setup.py
    if os.path.exists("setup.py"):
        with open("setup.py", "r", encoding="utf-8") as f:
            content = f.read()
            if "Your Name" in content:
                warnings.append("[WARN] setup.py 中的作者信息需要更新")
    
    if warnings:
        for warning in warnings:
            print(warning)
        return False
    else:
        print("[OK] 元数据检查通过")
        return True

def main():
    """主函数"""
    print("=" * 50)
    print("swagger-sdk 发布前检查")
    print("=" * 50)
    
    checks = [
        ("包结构", check_package_structure),
        ("版本一致性", check_version_consistency),
        ("构建文件", check_build_files),
        ("元数据", check_metadata),
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"[FAIL] {name} 检查出错: {e}")
            results.append((name, False))
    
    print("\n" + "=" * 50)
    print("检查结果汇总:")
    print("=" * 50)
    
    all_passed = True
    for name, result in results:
        status = "[OK] 通过" if result else "[FAIL] 失败"
        print(f"{name}: {status}")
        if not result:
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("[OK] 所有检查通过！可以开始构建和发布。")
        print("\n下一步:")
        print("1. 更新 pyproject.toml 和 setup.py 中的作者和 URL 信息")
        print("2. 运行: python -m build")
        print("3. 运行: twine check dist/*")
        print("4. 运行: twine upload dist/*")
        return 0
    else:
        print("[FAIL] 部分检查未通过，请修复后重试。")
        return 1

if __name__ == "__main__":
    sys.exit(main())

