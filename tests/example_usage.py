#!/usr/bin/env python3
"""
多人播客功能使用示例

演示如何使用 Python 代码生成多人播客
"""

import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def example_1_simple_usage():
    """
    示例 1: 基本使用
    
    演示最简单的多人播客生成流程
    """
    print("=" * 60)
    print("示例 1: 基本使用")
    print("=" * 60)
    
    from soulxpodcast.utils.podcast_utils import auto_parse_script
    from app import generate_multiperson_podcast, SPEAKERS
    import soundfile as sf
    
    # 检查是否有可用的说话人
    if not SPEAKERS:
        print("❌ 没有可用的说话人，请先配置参考音频")
        return
    
    # 简单的播客脚本
    script_text = f"""
    @角色: 主持人, {list(SPEAKERS.keys())[0]}, 普通话
    @角色: 嘉宾, {list(SPEAKERS.keys())[min(1, len(SPEAKERS)-1)]}, 普通话
    
    [主持人]: 大家好，欢迎收听今天的节目！
    [嘉宾]: 你好，很高兴来到这里。
    [主持人]: 今天我们要聊聊人工智能。
    [嘉宾]: 好的，这是一个很有趣的话题。
    """
    
    print("脚本内容:")
    print(script_text)
    print()
    
    # 解析脚本
    script = auto_parse_script(script_text)
    
    # 生成播客
    audio_array = generate_multiperson_podcast(script, silence_duration=0.5)
    
    # 保存音频
    output_file = "example_podcast_simple.wav"
    sf.write(output_file, audio_array, 24000)
    
    print(f"\n✅ 播客已生成: {output_file}")
    print(f"   音频时长: {len(audio_array)/24000:.2f} 秒")


def example_2_load_from_file():
    """
    示例 2: 从文件加载脚本
    
    演示如何从文件读取脚本并生成播客
    """
    print("\n" + "=" * 60)
    print("示例 2: 从文件加载脚本")
    print("=" * 60)
    
    from soulxpodcast.utils.podcast_utils import auto_parse_script
    from app import generate_multiperson_podcast
    import soundfile as sf
    
    # 脚本文件路径
    script_file = "examples/podcast_example_simple.txt"
    
    if not os.path.exists(script_file):
        print(f"❌ 脚本文件不存在: {script_file}")
        return
    
    # 读取脚本
    with open(script_file, 'r', encoding='utf-8') as f:
        script_text = f.read()
    
    print(f"正在加载脚本: {script_file}")
    print(f"脚本长度: {len(script_text)} 字符\n")
    
    # 解析脚本
    script = auto_parse_script(script_text)
    
    print(f"角色数量: {len(script.speakers)}")
    print(f"对话数量: {len(script.dialogues)}\n")
    
    # 生成播客
    audio_array = generate_multiperson_podcast(script, silence_duration=0.5)
    
    # 保存音频
    output_file = "example_podcast_from_file.wav"
    sf.write(output_file, audio_array, 24000)
    
    print(f"\n✅ 播客已生成: {output_file}")
    print(f"   音频时长: {len(audio_array)/24000:.2f} 秒")


def example_3_batch_generation():
    """
    示例 3: 批量生成
    
    演示如何批量生成多个播客
    """
    print("\n" + "=" * 60)
    print("示例 3: 批量生成")
    print("=" * 60)
    
    from soulxpodcast.utils.podcast_utils import auto_parse_script
    from app import generate_multiperson_podcast
    import soundfile as sf
    import glob
    
    # 查找所有示例脚本
    script_files = glob.glob("examples/podcast_example_*.txt")
    
    if not script_files:
        print("❌ 没有找到示例脚本文件")
        return
    
    print(f"找到 {len(script_files)} 个脚本文件\n")
    
    # 批量生成
    for i, script_file in enumerate(script_files, 1):
        print(f"[{i}/{len(script_files)}] 正在处理: {os.path.basename(script_file)}")
        
        try:
            # 读取脚本
            with open(script_file, 'r', encoding='utf-8') as f:
                script_text = f.read()
            
            # 解析脚本
            script = auto_parse_script(script_text)
            
            # 生成播客
            audio_array = generate_multiperson_podcast(script, silence_duration=0.5)
            
            # 保存音频
            output_file = os.path.basename(script_file).replace('.txt', '_output.wav')
            sf.write(output_file, audio_array, 24000)
            
            print(f"  ✅ 已生成: {output_file} ({len(audio_array)/24000:.2f}s)\n")
            
        except Exception as e:
            print(f"  ❌ 生成失败: {e}\n")


def example_4_custom_script():
    """
    示例 4: 程序化生成脚本
    
    演示如何通过代码动态创建播客脚本
    """
    print("\n" + "=" * 60)
    print("示例 4: 程序化生成脚本")
    print("=" * 60)
    
    from soulxpodcast.utils.podcast_utils import PodcastScript, validate_script
    from app import generate_multiperson_podcast, SPEAKERS
    import soundfile as sf
    
    if not SPEAKERS:
        print("❌ 没有可用的说话人")
        return
    
    # 创建脚本对象
    script = PodcastScript()
    
    # 添加角色
    available_voices = list(SPEAKERS.keys())
    script.add_speaker("主持人", available_voices[0], "普通话")
    script.add_speaker("专家", available_voices[min(1, len(available_voices)-1)], "普通话")
    
    # 动态生成对话
    questions = [
        "今天我们要聊的话题是什么？",
        "您能详细介绍一下吗？",
        "这个观点很有意思，还有什么要补充的吗？"
    ]
    
    answers = [
        "今天我们要聊人工智能的发展。",
        "当然可以。人工智能正在改变我们的生活方式。",
        "我认为AI的未来充满无限可能。"
    ]
    
    # 开场
    script.add_dialogue("主持人", "大家好，欢迎收听今天的节目！<|laughter|>")
    script.add_dialogue("专家", "大家好，很高兴来到这里。")
    
    # 添加问答
    for question, answer in zip(questions, answers):
        script.add_dialogue("主持人", question)
        script.add_dialogue("专家", answer)
    
    # 结束
    script.add_dialogue("主持人", "今天的节目就到这里，感谢大家的收听！")
    
    print(f"程序化生成的脚本:")
    print(f"  角色数量: {len(script.speakers)}")
    print(f"  对话数量: {len(script.dialogues)}\n")
    
    # 验证脚本
    is_valid, error_msg = validate_script(script, list(SPEAKERS.keys()))
    if not is_valid:
        print(f"❌ 脚本验证失败: {error_msg}")
        return
    
    print("✅ 脚本验证通过\n")
    
    # 生成播客
    audio_array = generate_multiperson_podcast(script, silence_duration=0.5)
    
    # 保存音频
    output_file = "example_podcast_programmatic.wav"
    sf.write(output_file, audio_array, 24000)
    
    print(f"\n✅ 播客已生成: {output_file}")
    print(f"   音频时长: {len(audio_array)/24000:.2f} 秒")


def main():
    """主函数"""
    print("\n")
    print("*" * 60)
    print("*" + " " * 58 + "*")
    print("*" + "  多人播客功能使用示例".center(56) + "*")
    print("*" + " " * 58 + "*")
    print("*" * 60)
    print("\n")
    
    examples = [
        ("基本使用", example_1_simple_usage),
        ("从文件加载", example_2_load_from_file),
        ("批量生成", example_3_batch_generation),
        ("程序化生成", example_4_custom_script),
    ]
    
    print("请选择要运行的示例:")
    for i, (name, _) in enumerate(examples, 1):
        print(f"  {i}. {name}")
    print(f"  0. 运行所有示例")
    print()
    
    try:
        choice = input("请输入选项 (0-4): ").strip()
        
        if choice == "0":
            # 运行所有示例
            for name, func in examples:
                try:
                    func()
                except Exception as e:
                    print(f"\n❌ 示例 '{name}' 执行失败: {e}")
                    import traceback
                    traceback.print_exc()
        elif choice in ["1", "2", "3", "4"]:
            # 运行指定示例
            idx = int(choice) - 1
            name, func = examples[idx]
            try:
                func()
            except Exception as e:
                print(f"\n❌ 示例 '{name}' 执行失败: {e}")
                import traceback
                traceback.print_exc()
        else:
            print("❌ 无效的选项")
    
    except KeyboardInterrupt:
        print("\n\n已取消")
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

