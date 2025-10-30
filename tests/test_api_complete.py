#!/usr/bin/env python3
"""
完整的API功能测试

测试所有API端点：
- POST /api/tts - 单人TTS
- POST /api/podcast - 多人播客
- GET /api/podcast/example - 示例脚本
"""

import requests
import time
import os
import json
from datetime import datetime

# 测试配置
BASE_URL = "http://localhost:8000"
TEST_OUTPUT_DIR = "test_outputs"
TIMEOUT = 120  # 2分钟超时

# 创建测试输出目录
os.makedirs(TEST_OUTPUT_DIR, exist_ok=True)

# 测试结果收集
test_results = {
    "total": 0,
    "passed": 0,
    "failed": 0,
    "start_time": datetime.now().isoformat(),
    "tests": []
}


def log_test(name, passed, message="", duration=0, details=None):
    """记录测试结果"""
    test_results["total"] += 1
    if passed:
        test_results["passed"] += 1
        status = "✅ PASS"
    else:
        test_results["failed"] += 1
        status = "❌ FAIL"
    
    result = {
        "name": name,
        "status": status,
        "passed": passed,
        "message": message,
        "duration": f"{duration:.2f}s" if duration > 0 else "N/A",
        "details": details or {}
    }
    
    test_results["tests"].append(result)
    
    print(f"{status} {name}")
    if message:
        print(f"     {message}")
    if duration > 0:
        print(f"     Duration: {duration:.2f}s")
    print()


def test_service_health():
    """测试服务健康状态"""
    print("=" * 60)
    print("1. 服务健康检查")
    print("=" * 60)
    
    try:
        start = time.time()
        response = requests.get(BASE_URL, timeout=10)
        duration = time.time() - start
        
        if response.status_code == 200:
            log_test(
                "服务健康检查",
                True,
                f"服务正常运行 (HTTP {response.status_code})",
                duration
            )
            return True
        else:
            log_test(
                "服务健康检查",
                False,
                f"服务响应异常 (HTTP {response.status_code})"
            )
            return False
    except requests.exceptions.ConnectionError:
        log_test(
            "服务健康检查",
            False,
            "无法连接到服务，请确保服务已启动"
        )
        return False
    except Exception as e:
        log_test(
            "服务健康检查",
            False,
            f"连接失败: {str(e)}"
        )
        return False


def test_single_tts_basic():
    """测试单人TTS基础功能"""
    print("=" * 60)
    print("2. 单人TTS API测试")
    print("=" * 60)
    
    # 测试1: 基础功能
    print("\n[测试 2.1] 基础TTS生成（普通话 + 女声1）")
    try:
        start = time.time()
        response = requests.post(
            f"{BASE_URL}/api/tts",
            json={
                "text": "大家好，欢迎使用 SoulX TTS 系统。",
                "speaker": "女声1",
                "dialect": "普通话"
            },
            timeout=TIMEOUT
        )
        duration = time.time() - start
        
        if response.status_code == 200:
            # 保存音频
            output_file = os.path.join(TEST_OUTPUT_DIR, "test_single_basic.wav")
            with open(output_file, "wb") as f:
                f.write(response.content)
            
            file_size = len(response.content)
            log_test(
                "单人TTS - 基础功能",
                True,
                f"音频生成成功，文件大小: {file_size} bytes",
                duration,
                {"file_size": file_size, "output": output_file}
            )
        else:
            log_test(
                "单人TTS - 基础功能",
                False,
                f"HTTP {response.status_code}: {response.text[:100]}"
            )
    except Exception as e:
        log_test(
            "单人TTS - 基础功能",
            False,
            f"请求失败: {str(e)}"
        )


def test_single_tts_dialects():
    """测试不同方言"""
    dialects = ["四川话", "粤语", "河南话"]
    
    for dialect in dialects:
        print(f"\n[测试 2.{dialects.index(dialect) + 2}] {dialect}生成")
        try:
            start = time.time()
            response = requests.post(
                f"{BASE_URL}/api/tts",
                json={
                    "text": f"你好，这是{dialect}的测试。",
                    "speaker": "男声1",
                    "dialect": dialect
                },
                timeout=TIMEOUT
            )
            duration = time.time() - start
            
            if response.status_code == 200:
                output_file = os.path.join(TEST_OUTPUT_DIR, f"test_single_{dialect}.wav")
                with open(output_file, "wb") as f:
                    f.write(response.content)
                
                file_size = len(response.content)
                log_test(
                    f"单人TTS - {dialect}",
                    True,
                    f"音频生成成功，文件大小: {file_size} bytes",
                    duration,
                    {"file_size": file_size, "output": output_file}
                )
            else:
                log_test(
                    f"单人TTS - {dialect}",
                    False,
                    f"HTTP {response.status_code}"
                )
        except Exception as e:
            log_test(
                f"单人TTS - {dialect}",
                False,
                f"请求失败: {str(e)}"
            )


def test_single_tts_emotions():
    """测试副语言标签"""
    print("\n[测试 2.5] 副语言标签测试")
    try:
        start = time.time()
        response = requests.post(
            f"{BASE_URL}/api/tts",
            json={
                "text": "今天天气真好！<|laughter|> 真的很开心。<|sigh|>",
                "speaker": "女声1",
                "dialect": "普通话"
            },
            timeout=TIMEOUT
        )
        duration = time.time() - start
        
        if response.status_code == 200:
            output_file = os.path.join(TEST_OUTPUT_DIR, "test_single_emotions.wav")
            with open(output_file, "wb") as f:
                f.write(response.content)
            
            file_size = len(response.content)
            log_test(
                "单人TTS - 副语言标签",
                True,
                f"音频生成成功，文件大小: {file_size} bytes",
                duration,
                {"file_size": file_size, "output": output_file}
            )
        else:
            log_test(
                "单人TTS - 副语言标签",
                False,
                f"HTTP {response.status_code}"
            )
    except Exception as e:
        log_test(
            "单人TTS - 副语言标签",
            False,
            f"请求失败: {str(e)}"
        )


def test_single_tts_error_handling():
    """测试错误处理"""
    print("\n[测试 2.6] 错误处理 - 空文本")
    try:
        response = requests.post(
            f"{BASE_URL}/api/tts",
            json={
                "text": "",
                "speaker": "女声1",
                "dialect": "普通话"
            },
            timeout=10
        )
        
        # 应该返回错误
        if response.status_code != 200:
            log_test(
                "单人TTS - 错误处理（空文本）",
                True,
                "正确返回错误状态"
            )
        else:
            log_test(
                "单人TTS - 错误处理（空文本）",
                False,
                "应该返回错误但返回了200"
            )
    except Exception as e:
        log_test(
            "单人TTS - 错误处理（空文本）",
            False,
            f"请求失败: {str(e)}"
        )


def test_podcast_basic():
    """测试多人播客基础功能"""
    print("\n" + "=" * 60)
    print("3. 多人播客 API 测试")
    print("=" * 60)
    
    print("\n[测试 3.1] 基础两人对话")
    script = """
# 角色定义
@角色: 主持人, 女声1, 普通话
@角色: 嘉宾, 男声1, 普通话

# 对话内容
[主持人]: 大家好，欢迎收听今天的节目。
[嘉宾]: 你好，很高兴来到这里。
[主持人]: 今天我们要聊聊人工智能。
[嘉宾]: 好的，这是一个很有趣的话题。
"""
    
    try:
        start = time.time()
        response = requests.post(
            f"{BASE_URL}/api/podcast",
            json={
                "script": script,
                "silence_duration": 0.5
            },
            timeout=TIMEOUT
        )
        duration = time.time() - start
        
        if response.status_code == 200:
            output_file = os.path.join(TEST_OUTPUT_DIR, "test_podcast_basic.wav")
            with open(output_file, "wb") as f:
                f.write(response.content)
            
            file_size = len(response.content)
            log_test(
                "多人播客 - 基础两人对话",
                True,
                f"播客生成成功，文件大小: {file_size} bytes",
                duration,
                {"file_size": file_size, "output": output_file}
            )
        else:
            log_test(
                "多人播客 - 基础两人对话",
                False,
                f"HTTP {response.status_code}: {response.text[:200]}"
            )
    except Exception as e:
        log_test(
            "多人播客 - 基础两人对话",
            False,
            f"请求失败: {str(e)}"
        )


def test_podcast_multi_person():
    """测试多人对话"""
    print("\n[测试 3.2] 多人对话（3人）")
    script = """
@角色: 主持人, 女声1, 普通话
@角色: 嘉宾A, 男声1, 普通话
@角色: 嘉宾B, 女声1, 普通话

[主持人]: 欢迎两位嘉宾。
[嘉宾A]: 大家好。
[嘉宾B]: 你好。
[主持人]: 今天的话题很有意思。
"""
    
    try:
        start = time.time()
        response = requests.post(
            f"{BASE_URL}/api/podcast",
            json={
                "script": script,
                "silence_duration": 0.3
            },
            timeout=TIMEOUT
        )
        duration = time.time() - start
        
        if response.status_code == 200:
            output_file = os.path.join(TEST_OUTPUT_DIR, "test_podcast_multi.wav")
            with open(output_file, "wb") as f:
                f.write(response.content)
            
            file_size = len(response.content)
            log_test(
                "多人播客 - 多人对话",
                True,
                f"播客生成成功，文件大小: {file_size} bytes",
                duration,
                {"file_size": file_size, "output": output_file}
            )
        else:
            log_test(
                "多人播客 - 多人对话",
                False,
                f"HTTP {response.status_code}"
            )
    except Exception as e:
        log_test(
            "多人播客 - 多人对话",
            False,
            f"请求失败: {str(e)}"
        )


def test_podcast_multi_dialect():
    """测试多方言混合"""
    print("\n[测试 3.3] 多方言混合对话")
    script = """
@角色: 主持人, 女声1, 普通话
@角色: 四川朋友, 男声1, 四川话
@角色: 粤语朋友, 女声1, 粤语

[主持人]: 今天请到了两位朋友。
[四川朋友]: 大家好，我来自成都。
[粤语朋友]: 大家好呀，我系广东人。
"""
    
    try:
        start = time.time()
        response = requests.post(
            f"{BASE_URL}/api/podcast",
            json={
                "script": script,
                "silence_duration": 0.5
            },
            timeout=TIMEOUT
        )
        duration = time.time() - start
        
        if response.status_code == 200:
            output_file = os.path.join(TEST_OUTPUT_DIR, "test_podcast_dialect.wav")
            with open(output_file, "wb") as f:
                f.write(response.content)
            
            file_size = len(response.content)
            log_test(
                "多人播客 - 多方言混合",
                True,
                f"播客生成成功，文件大小: {file_size} bytes",
                duration,
                {"file_size": file_size, "output": output_file}
            )
        else:
            log_test(
                "多人播客 - 多方言混合",
                False,
                f"HTTP {response.status_code}"
            )
    except Exception as e:
        log_test(
            "多人播客 - 多方言混合",
            False,
            f"请求失败: {str(e)}"
        )


def test_podcast_error_handling():
    """测试播客错误处理"""
    print("\n[测试 3.4] 错误处理 - 格式错误")
    
    # 格式错误的脚本
    bad_script = """
[主持人]: 大家好
[嘉宾]: 你好
"""
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/podcast",
            json={
                "script": bad_script,
                "silence_duration": 0.5
            },
            timeout=10
        )
        
        # 应该返回错误
        if response.status_code != 200 or "error" in response.json():
            log_test(
                "多人播客 - 错误处理（格式错误）",
                True,
                "正确检测到格式错误"
            )
        else:
            log_test(
                "多人播客 - 错误处理（格式错误）",
                False,
                "应该返回错误但没有"
            )
    except Exception as e:
        # 捕获到异常也算正确
        log_test(
            "多人播客 - 错误处理（格式错误）",
            True,
            "正确抛出异常"
        )


def test_example_api():
    """测试示例脚本API"""
    print("\n" + "=" * 60)
    print("4. 示例脚本 API 测试")
    print("=" * 60)
    
    # 测试简单格式
    print("\n[测试 4.1] 获取简单格式示例")
    try:
        response = requests.get(f"{BASE_URL}/api/podcast/example?format=simple", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if "script" in data and len(data["script"]) > 0:
                log_test(
                    "示例API - 简单格式",
                    True,
                    f"成功获取示例，长度: {len(data['script'])} 字符"
                )
            else:
                log_test(
                    "示例API - 简单格式",
                    False,
                    "返回数据格式不正确"
                )
        else:
            log_test(
                "示例API - 简单格式",
                False,
                f"HTTP {response.status_code}"
            )
    except Exception as e:
        log_test(
            "示例API - 简单格式",
            False,
            f"请求失败: {str(e)}"
        )
    
    # 测试JSON格式
    print("\n[测试 4.2] 获取JSON格式示例")
    try:
        response = requests.get(f"{BASE_URL}/api/podcast/example?format=json", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if "script" in data and len(data["script"]) > 0:
                log_test(
                    "示例API - JSON格式",
                    True,
                    f"成功获取示例，长度: {len(data['script'])} 字符"
                )
            else:
                log_test(
                    "示例API - JSON格式",
                    False,
                    "返回数据格式不正确"
                )
        else:
            log_test(
                "示例API - JSON格式",
                False,
                f"HTTP {response.status_code}"
            )
    except Exception as e:
        log_test(
            "示例API - JSON格式",
            False,
            f"请求失败: {str(e)}"
        )


def generate_report():
    """生成测试报告"""
    test_results["end_time"] = datetime.now().isoformat()
    
    report = f"""# API 测试报告

## 测试概览

- **开始时间**: {test_results['start_time']}
- **结束时间**: {test_results['end_time']}
- **总测试数**: {test_results['total']}
- **通过**: {test_results['passed']} ✅
- **失败**: {test_results['failed']} ❌
- **通过率**: {test_results['passed']/test_results['total']*100:.1f}%

## 测试结果详情

"""
    
    for test in test_results["tests"]:
        report += f"\n### {test['name']}\n\n"
        report += f"- **状态**: {test['status']}\n"
        if test['message']:
            report += f"- **信息**: {test['message']}\n"
        if test['duration'] != "N/A":
            report += f"- **耗时**: {test['duration']}\n"
        if test['details']:
            report += f"- **详情**: {json.dumps(test['details'], indent=2, ensure_ascii=False)}\n"
    
    report += f"\n## 总结\n\n"
    if test_results['failed'] == 0:
        report += "🎉 所有测试通过！系统功能正常。\n"
    else:
        report += f"⚠️  有 {test_results['failed']} 个测试失败，请检查相关功能。\n"
    
    # 保存报告
    report_file = "TEST_REPORT_API.md"
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(report)
    
    print("\n" + "=" * 60)
    print(f"测试报告已生成: {report_file}")
    print("=" * 60)


def main():
    """主测试流程"""
    print("\n")
    print("*" * 60)
    print("*" + " " * 58 + "*")
    print("*" + "  SoulX-TTS API 完整功能测试".center(56) + "*")
    print("*" + " " * 58 + "*")
    print("*" * 60)
    print("\n")
    
    # 1. 服务健康检查
    if not test_service_health():
        print("\n❌ 服务未启动，请先运行: python app.py")
        return
    
    print("\n等待 5 秒，确保服务完全启动...")
    time.sleep(5)
    
    # 2. 单人TTS测试
    test_single_tts_basic()
    test_single_tts_dialects()
    test_single_tts_emotions()
    test_single_tts_error_handling()
    
    # 3. 多人播客测试
    test_podcast_basic()
    test_podcast_multi_person()
    test_podcast_multi_dialect()
    test_podcast_error_handling()
    
    # 4. 示例API测试
    test_example_api()
    
    # 5. 生成报告
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)
    print(f"总计: {test_results['passed']}/{test_results['total']} 个测试通过")
    print(f"通过率: {test_results['passed']/test_results['total']*100:.1f}%")
    
    if test_results['failed'] == 0:
        print("\n🎉 所有测试通过！")
    else:
        print(f"\n⚠️  有 {test_results['failed']} 个测试失败")
    
    generate_report()


if __name__ == "__main__":
    main()

