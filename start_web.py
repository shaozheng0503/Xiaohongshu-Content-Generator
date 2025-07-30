#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小红书内容生成器 - Web版启动脚本
"""

import os
import sys
import subprocess
import webbrowser
import time
from pathlib import Path

def check_python_version():
    """检查Python版本"""
    if sys.version_info < (3, 7):
        print("❌ 错误：需要Python 3.7或更高版本")
        print(f"当前版本：{sys.version}")
        return False
    print(f"✅ Python版本检查通过：{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    return True

def install_package(package):
    """安装Python包"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        return True
    except subprocess.CalledProcessError:
        return False

def check_and_install_dependencies():
    """检查并安装依赖"""
    print("\n🔍 检查Python依赖...")
    
    # 必需的依赖包
    required_packages = [
        ("flask", "Flask==2.3.3"),
        ("markdown", "markdown==3.5.1"),
        ("PIL", "Pillow==10.0.1"),
        ("requests", "requests==2.31.0"),
        ("bs4", "beautifulsoup4==4.12.2"),
        ("lxml", "lxml==4.9.3"),
        ("pygments", "pygments==2.16.1"),
        ("html2image", "html2image==2.0.4.3")
    ]
    
    missing_packages = []
    
    for import_name, package_name in required_packages:
        try:
            if import_name == "PIL":
                import PIL
            elif import_name == "bs4":
                import bs4
            else:
                __import__(import_name)
            print(f"  ✅ {package_name}")
        except ImportError:
            print(f"  ❌ {package_name} (缺失)")
            missing_packages.append(package_name)
    
    if missing_packages:
        print(f"\n📦 发现 {len(missing_packages)} 个缺失的依赖包")
        install_choice = input("是否自动安装缺失的依赖？(y/n): ").lower().strip()
        
        if install_choice in ['y', 'yes', '是']:
            print("\n🔧 正在安装依赖...")
            failed_packages = []
            
            for package in missing_packages:
                print(f"  📥 安装 {package}...")
                if install_package(package):
                    print(f"  ✅ {package} 安装成功")
                else:
                    print(f"  ❌ {package} 安装失败")
                    failed_packages.append(package)
            
            if failed_packages:
                print(f"\n⚠️  警告：以下包安装失败：")
                for pkg in failed_packages:
                    print(f"    - {pkg}")
                print("\n请手动运行以下命令安装：")
                print(f"pip install {' '.join(failed_packages)}")
                
                # 特别提醒html2image的依赖
                if any('html2image' in pkg for pkg in failed_packages):
                    print("\n📝 html2image安装提示：")
                    print("如果html2image安装失败，可能需要安装Chrome浏览器。")
                    print("Windows用户：确保已安装Chrome浏览器")
                    print("Linux用户：sudo apt-get install google-chrome-stable")
                    print("macOS用户：brew install --cask google-chrome")
                    
                return False
            else:
                print("\n✅ 所有依赖安装完成！")
        else:
            print("\n❌ 依赖未安装，程序可能无法正常运行")
            print("您可以手动运行以下命令安装：")
            print(f"pip install -r requirements_web.txt")
            return False
    
    return True

def check_xhs_tools_directory():
    """检查xhs-tools目录和必要文件"""
    print("\n🔍 检查项目文件...")
    
    xhs_tools_path = Path("xhs-tools")
    if not xhs_tools_path.exists():
        print("❌ 错误：找不到xhs-tools目录")
        print("请确保在正确的项目根目录下运行此脚本")
        return False
    
    required_files = [
        "xhs-tools/parser.py",
        "xhs-tools/nlp_gen.py", 
        "xhs-tools/html_render.py"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
        else:
            print(f"  ✅ {file_path}")
    
    if missing_files:
        print("❌ 错误：缺少必要文件：")
        for file_path in missing_files:
            print(f"    - {file_path}")
        return False
    
    print("✅ 项目文件检查通过")
    return True

def create_required_directories():
    """创建必要的目录"""
    print("\n📁 创建必要目录...")
    
    directories = [
        "uploads",
        "temp_images", 
        "web_history",
        "templates",
        "static/css",
        "static/js",
        "static/img"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"  ✅ {directory}")

def check_web_files():
    """检查Web相关文件"""
    print("\n🌐 检查Web文件...")
    
    web_files = [
        "web_app.py",
        "templates/index.html",
        "static/css/style.css", 
        "static/js/app.js"
    ]
    
    missing_files = []
    for file_path in web_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
        else:
            print(f"  ✅ {file_path}")
    
    if missing_files:
        print("❌ 错误：缺少Web文件：")
        for file_path in missing_files:
            print(f"    - {file_path}")
        return False
    
    return True

def start_web_server():
    """启动Web服务器"""
    print("\n🚀 启动Web服务器...")
    
    try:
        # 导入Flask应用
        sys.path.insert(0, os.getcwd())
        from web_app import app
        
        print("✅ Web应用加载成功")
        print("\n" + "="*50)
        print("🌟 小红书内容生成器 - Web版")
        print("="*50)
        print("📍 服务地址：http://localhost:5000")
        print("🎯 功能特色：")
        print("  • 14种精美样式模板")
        print("  • 智能内容分割")
        print("  • 实时预览生成")
        print("  • 单张/批量下载")
        print("  • 响应式设计")
        print("="*50)
        
        # 延迟打开浏览器
        def open_browser():
            time.sleep(1.5)
            try:
                webbrowser.open('http://localhost:5000')
                print("🌐 已自动打开浏览器")
            except:
                print("⚠️  无法自动打开浏览器，请手动访问：http://localhost:5000")
        
        import threading
        threading.Thread(target=open_browser, daemon=True).start()
        
        # 启动服务器
        app.run(debug=False, host='0.0.0.0', port=5000, use_reloader=False)
        
    except ImportError as e:
        print(f"❌ 导入错误：{e}")
        print("请检查依赖是否正确安装")
        return False
    except Exception as e:
        print(f"❌ 启动失败：{e}")
        return False

def main():
    """主函数"""
    print("🎉 小红书内容生成器 - Web版启动器")
    print("="*50)
    
    # 检查Python版本
    if not check_python_version():
        input("\n按回车键退出...")
        return
    
    # 检查并安装依赖
    if not check_and_install_dependencies():
        input("\n按回车键退出...")
        return
    
    # 检查项目文件
    if not check_xhs_tools_directory():
        input("\n按回车键退出...")
        return
    
    # 检查Web文件
    if not check_web_files():
        input("\n按回车键退出...")
        return
    
    # 创建必要目录
    create_required_directories()
    
    print("\n✅ 所有检查通过，准备启动服务器...")
    
    try:
        start_web_server()
    except KeyboardInterrupt:
        print("\n\n👋 服务器已停止")
    except Exception as e:
        print(f"\n❌ 启动过程中发生错误：{e}")
        input("\n按回车键退出...")

if __name__ == "__main__":
    main() 