#!/usr/bin/env python3
"""
SoulX-Podcast TTS 安装验证脚本
"""

import sys
import os

def print_status(message, status):
    """打印状态信息"""
    symbols = {"success": "✅", "error": "❌", "warning": "⚠️", "info": "ℹ️"}
    print(f"{symbols.get(status, '•')} {message}")

def check_python_version():
    """检查 Python 版本"""
    version = sys.version_info
    if version.major == 3 and version.minor >= 11:
        print_status(f"Python 版本: {version.major}.{version.minor}.{version.micro}", "success")
        return True
    else:
        print_status(f"Python 版本过低: {version.major}.{version.minor}.{version.micro} (需要 >= 3.11)", "error")
        return False

def check_pytorch():
    """检查 PyTorch 安装"""
    try:
        import torch
        print_status(f"PyTorch 版本: {torch.__version__}", "success")
        
        # 检查设备支持
        if torch.cuda.is_available():
            print_status("  CUDA 可用 (NVIDIA GPU)", "success")
        elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
            print_status("  MPS 可用 (Apple Silicon)", "success")
        else:
            print_status("  仅 CPU 模式（性能较慢）", "warning")
        
        return True
    except ImportError:
        print_status("PyTorch 未安装", "error")
        return False

def check_transformers():
    """检查 Transformers 安装"""
    try:
        import transformers
        print_status(f"Transformers 版本: {transformers.__version__}", "success")
        return True
    except ImportError:
        print_status("Transformers 未安装", "error")
        return False

def check_soulxpodcast():
    """检查 SoulX-Podcast 模块"""
    try:
        from soulxpodcast import __version__
        print_status(f"SoulX-Podcast 模块已集成 (v{__version__})", "success")
        
        # 检查模块结构
        import os
        if os.path.isdir("soulxpodcast"):
            required_files = ["__init__.py", "config.py"]
            required_dirs = ["engine", "models", "utils"]
            
            for f in required_files:
                if not os.path.exists(f"soulxpodcast/{f}"):
                    print_status(f"  缺少文件: {f}", "warning")
                    return False
            
            for d in required_dirs:
                if not os.path.isdir(f"soulxpodcast/{d}"):
                    print_status(f"  缺少目录: {d}", "warning")
                    return False
        
        return True
    except ImportError as e:
        print_status(f"SoulX-Podcast 模块未找到: {e}", "error")
        print_status("  请确认 soulxpodcast/ 目录存在", "info")
        return False

def check_other_packages():
    """检查其他依赖包"""
    packages = {
        "gradio": "Gradio",
        "fastapi": "FastAPI",
        "soundfile": "SoundFile",
        "s3tokenizer": "S3Tokenizer",
    }
    
    all_ok = True
    for pkg, name in packages.items():
        try:
            __import__(pkg)
            print_status(f"{name} 已安装", "success")
        except ImportError:
            print_status(f"{name} 未安装", "error")
            all_ok = False
    
    return all_ok

def check_model_files():
    """检查模型文件"""
    model_path = "pretrained_models/SoulX-Podcast-1.7B-dialect"
    
    if not os.path.exists(model_path):
        print_status(f"模型目录不存在: {model_path}", "error")
        print_status("  请运行: bash setup.sh", "info")
        return False
    
    required_files = [
        "config.json",
        "soulxpodcast_config.json",
        "flow.pt",
        "hift.pt"
    ]
    
    all_ok = True
    for filename in required_files:
        filepath = os.path.join(model_path, filename)
        if os.path.exists(filepath):
            size = os.path.getsize(filepath) / (1024 * 1024)  # MB
            print_status(f"  {filename} ({size:.1f} MB)", "success")
        else:
            print_status(f"  {filename} 缺失", "error")
            all_ok = False
    
    if all_ok:
        print_status("模型文件完整", "success")
    else:
        print_status("模型文件不完整", "error")
    
    return all_ok

def check_prompt_audios():
    """检查参考音频文件"""
    prompt_dir = "prompt_audios"
    required_files = ["female_1.wav", "male_1.wav"]
    
    all_ok = True
    for filename in required_files:
        filepath = os.path.join(prompt_dir, filename)
        if os.path.exists(filepath):
            size = os.path.getsize(filepath) / 1024  # KB
            print_status(f"  {filename} ({size:.1f} KB)", "success")
        else:
            print_status(f"  {filename} 缺失", "warning")
            all_ok = False
    
    if all_ok:
        print_status("参考音频文件就绪", "success")
    else:
        print_status("部分参考音频缺失（可以添加更多）", "warning")
    
    return True  # 不是致命错误

def main():
    """主函数"""
    print("=" * 60)
    print("🔍 SoulX-Podcast TTS 安装验证")
    print("=" * 60)
    print()
    
    checks = [
        ("Python 版本", check_python_version),
        ("PyTorch", check_pytorch),
        ("Transformers", check_transformers),
        ("SoulX-Podcast 包", check_soulxpodcast),
        ("其他依赖包", check_other_packages),
        ("模型文件", check_model_files),
        ("参考音频", check_prompt_audios),
    ]
    
    results = []
    for name, check_func in checks:
        print(f"\n[ {name} ]")
        result = check_func()
        results.append(result)
    
    print()
    print("=" * 60)
    
    if all(results):
        print("✅ 所有检查通过！")
        print()
        print("🚀 可以启动服务:")
        print("   bash start.sh")
        print()
        print("   或:")
        print("   python app.py")
        print()
        return 0
    else:
        print("❌ 部分检查未通过")
        print()
        print("📋 请按照提示修复问题，或运行:")
        print("   bash setup.sh")
        print()
        return 1

if __name__ == "__main__":
    sys.exit(main())

