#!/usr/bin/env python3
"""
测试多人播客功能

运行方式：
    python test_podcast.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from soulxpodcast.utils.podcast_utils import (
    auto_parse_script, 
    validate_script,
    create_example_script,
    create_example_json_script
)

def test_parse_simple_script():
    """测试简单格式脚本解析"""
    print("=" * 60)
    print("测试 1: 解析简单格式脚本")
    print("=" * 60)
    
    script_text = """
    # 角色定义
    @角色: 主持人, 女声1, 普通话
    @角色: 嘉宾, 男声1, 四川话
    
    # 对话内容
    [主持人]: 大家好，欢迎收听今天的节目！
    [嘉宾]: 你好啊，很高兴来到这里。<|laughter|>
    [主持人]: 今天我们要聊聊人工智能。
    [嘉宾]: 好的，这个话题很有意思。
    """
    
    try:
        script = auto_parse_script(script_text)
        print(f"✅ 解析成功！")
        print(f"   角色数量: {len(script.speakers)}")
        print(f"   对话数量: {len(script.dialogues)}")
        
        print("\n角色信息:")
        for name, config in script.speakers.items():
            print(f"  - {name}: {config['voice']} ({config['dialect']})")
        
        print("\n对话内容:")
        for i, dialogue in enumerate(script.dialogues, 1):
            print(f"  {i}. [{dialogue['speaker']}]: {dialogue['text'][:50]}...")
        
        return True
    except Exception as e:
        print(f"❌ 解析失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_parse_json_script():
    """测试 JSON 格式脚本解析"""
    print("\n" + "=" * 60)
    print("测试 2: 解析 JSON 格式脚本")
    print("=" * 60)
    
    script_text = create_example_json_script()
    
    try:
        script = auto_parse_script(script_text)
        print(f"✅ 解析成功！")
        print(f"   角色数量: {len(script.speakers)}")
        print(f"   对话数量: {len(script.dialogues)}")
        return True
    except Exception as e:
        print(f"❌ 解析失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_validate_script():
    """测试脚本验证"""
    print("\n" + "=" * 60)
    print("测试 3: 脚本验证")
    print("=" * 60)
    
    # 创建一个测试脚本
    script_text = """
    @角色: 主持人, 女声1, 普通话
    @角色: 嘉宾, 男声1, 普通话
    
    [主持人]: 你好！
    [嘉宾]: 你好！
    """
    
    script = auto_parse_script(script_text)
    
    # 测试有效脚本
    available_voices = ["女声1", "男声1", "女声2"]
    is_valid, error_msg = validate_script(script, available_voices)
    
    if is_valid:
        print("✅ 有效脚本验证通过")
    else:
        print(f"❌ 验证失败: {error_msg}")
        return False
    
    # 测试无效脚本（使用不存在的声音）
    script_text_invalid = """
    @角色: 主持人, 未知声音, 普通话
    
    [主持人]: 你好！
    """
    
    script_invalid = auto_parse_script(script_text_invalid)
    is_valid, error_msg = validate_script(script_invalid, available_voices)
    
    if not is_valid:
        print(f"✅ 无效脚本正确检测: {error_msg}")
        return True
    else:
        print("❌ 应该检测到无效脚本，但验证通过了")
        return False


def test_example_scripts():
    """测试示例脚本生成"""
    print("\n" + "=" * 60)
    print("测试 4: 示例脚本生成")
    print("=" * 60)
    
    # 简单格式示例
    simple_example = create_example_script()
    print("简单格式示例脚本长度:", len(simple_example), "字符")
    print("前 200 字符:")
    print(simple_example[:200])
    
    # JSON 格式示例
    json_example = create_example_json_script()
    print("\nJSON 格式示例脚本长度:", len(json_example), "字符")
    
    # 尝试解析
    try:
        script1 = auto_parse_script(simple_example)
        script2 = auto_parse_script(json_example)
        print(f"\n✅ 两种格式的示例脚本都可以成功解析")
        return True
    except Exception as e:
        print(f"\n❌ 示例脚本解析失败: {e}")
        return False


def test_edge_cases():
    """测试边界情况"""
    print("\n" + "=" * 60)
    print("测试 5: 边界情况")
    print("=" * 60)
    
    # 测试空脚本
    try:
        script = auto_parse_script("")
        available_voices = ["女声1", "男声1"]
        is_valid, error_msg = validate_script(script, available_voices)
        if not is_valid:
            print(f"✅ 空脚本正确识别: {error_msg}")
        else:
            print("❌ 空脚本应该无效")
            return False
    except Exception as e:
        print(f"✅ 空脚本抛出异常: {e}")
    
    # 测试只有角色定义没有对话
    script_text = """
    @角色: 主持人, 女声1, 普通话
    @角色: 嘉宾, 男声1, 普通话
    """
    
    try:
        script = auto_parse_script(script_text)
        available_voices = ["女声1", "男声1"]
        is_valid, error_msg = validate_script(script, available_voices)
        if not is_valid:
            print(f"✅ 无对话脚本正确识别: {error_msg}")
        else:
            print("❌ 无对话脚本应该无效")
            return False
    except Exception as e:
        print(f"✅ 无对话脚本抛出异常: {e}")
    
    # 测试使用未定义的角色
    script_text = """
    @角色: 主持人, 女声1, 普通话
    
    [主持人]: 你好！
    [未定义角色]: 你好！
    """
    
    try:
        script = auto_parse_script(script_text)
        print("❌ 应该在解析时检测到未定义的角色")
        return False
    except ValueError as e:
        print(f"✅ 未定义角色正确检测: {e}")
    
    return True


def main():
    """运行所有测试"""
    print("\n")
    print("*" * 60)
    print("*" + " " * 58 + "*")
    print("*" + "  多人播客功能测试".center(56) + "*")
    print("*" + " " * 58 + "*")
    print("*" * 60)
    print("\n")
    
    tests = [
        ("解析简单格式脚本", test_parse_simple_script),
        ("解析 JSON 格式脚本", test_parse_json_script),
        ("脚本验证", test_validate_script),
        ("示例脚本生成", test_example_scripts),
        ("边界情况", test_edge_cases),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            success = test_func()
            results.append((name, success))
        except Exception as e:
            print(f"\n❌ 测试 '{name}' 发生异常: {e}")
            import traceback
            traceback.print_exc()
            results.append((name, False))
    
    # 总结
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for name, success in results:
        status = "✅ 通过" if success else "❌ 失败"
        print(f"{status}: {name}")
    
    print("\n" + "=" * 60)
    print(f"总计: {passed}/{total} 个测试通过")
    
    if passed == total:
        print("🎉 所有测试通过！")
        return 0
    else:
        print("⚠️  部分测试失败，请检查")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)

