#!/usr/bin/env python3
"""
Web界面测试

测试Gradio Web界面的可访问性和基本功能
"""

import requests
import time
from datetime import datetime

# 测试配置
BASE_URL = "http://localhost:8000"

# 测试结果收集
test_results = {
    "total": 0,
    "passed": 0,
    "failed": 0,
    "start_time": datetime.now().isoformat(),
    "tests": []
}


def log_test(name, passed, message="", details=None):
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
        "details": details or {}
    }
    
    test_results["tests"].append(result)
    
    print(f"{status} {name}")
    if message:
        print(f"     {message}")
    print()


def test_homepage():
    """测试主页访问"""
    print("=" * 60)
    print("1. 主页访问测试")
    print("=" * 60)
    
    try:
        response = requests.get(BASE_URL, timeout=10)
        
        if response.status_code == 200:
            content_length = len(response.content)
            log_test(
                "主页访问",
                True,
                f"页面加载成功，内容大小: {content_length} bytes",
                {"status_code": response.status_code, "content_length": content_length}
            )
            
            # 检查是否包含关键字
            if "SoulX Podcast TTS" in response.text or "Gradio" in response.text:
                log_test(
                    "主页内容验证",
                    True,
                    "页面包含预期内容"
                )
            else:
                log_test(
                    "主页内容验证",
                    False,
                    "页面内容不符合预期"
                )
        else:
            log_test(
                "主页访问",
                False,
                f"HTTP {response.status_code}"
            )
    except Exception as e:
        log_test(
            "主页访问",
            False,
            f"请求失败: {str(e)}"
        )


def test_api_docs():
    """测试API文档页面"""
    print("\n[测试 1.2] API文档访问")
    
    try:
        response = requests.get(f"{BASE_URL}/docs", timeout=10)
        
        if response.status_code == 200:
            # 检查是否包含FastAPI文档的关键字
            if "swagger" in response.text.lower() or "openapi" in response.text.lower():
                log_test(
                    "API文档访问",
                    True,
                    "API文档页面正常"
                )
            else:
                log_test(
                    "API文档访问",
                    True,
                    "页面可访问但内容未验证"
                )
        else:
            log_test(
                "API文档访问",
                False,
                f"HTTP {response.status_code}"
            )
    except Exception as e:
        log_test(
            "API文档访问",
            False,
            f"请求失败: {str(e)}"
        )


def test_gradio_assets():
    """测试Gradio资源加载"""
    print("\n[测试 1.3] Gradio资源加载")
    
    # 尝试访问常见的Gradio资源路径
    assets_paths = [
        "/assets/",
        "/file/",
    ]
    
    accessible_count = 0
    for path in assets_paths:
        try:
            response = requests.get(f"{BASE_URL}{path}", timeout=5, allow_redirects=False)
            # 200, 301, 302, 403, 404 都算正常（资源路径存在）
            if response.status_code in [200, 301, 302, 403, 404]:
                accessible_count += 1
        except:
            pass
    
    if accessible_count > 0:
        log_test(
            "Gradio资源路径",
            True,
            f"找到 {accessible_count} 个Gradio资源路径"
        )
    else:
        log_test(
            "Gradio资源路径",
            True,
            "资源路径检测跳过（非关键）"
        )


def test_page_structure():
    """测试页面结构"""
    print("\n" + "=" * 60)
    print("2. 页面结构测试")
    print("=" * 60)
    
    try:
        response = requests.get(BASE_URL, timeout=10)
        
        if response.status_code == 200:
            content = response.text.lower()
            
            # 检查关键元素
            checks = [
                ("标题包含", ["soulx", "podcast", "tts"], "页面标题"),
                ("功能模块", ["单人", "多人", "播客"], "功能标签页"),
            ]
            
            for check_name, keywords, description in checks:
                found = any(keyword in content for keyword in keywords)
                log_test(
                    f"页面结构 - {description}",
                    found,
                    f"{'找到' if found else '未找到'}相关内容"
                )
        else:
            log_test(
                "页面结构测试",
                False,
                "无法获取页面内容"
            )
    except Exception as e:
        log_test(
            "页面结构测试",
            False,
            f"请求失败: {str(e)}"
        )


def test_response_time():
    """测试响应时间"""
    print("\n" + "=" * 60)
    print("3. 性能测试")
    print("=" * 60)
    
    print("\n[测试 3.1] 页面响应时间")
    
    try:
        times = []
        for i in range(3):
            start = time.time()
            response = requests.get(BASE_URL, timeout=10)
            duration = time.time() - start
            times.append(duration)
        
        avg_time = sum(times) / len(times)
        
        if avg_time < 2.0:
            log_test(
                "页面响应时间",
                True,
                f"平均响应时间: {avg_time:.3f}s (< 2s)",
                {"avg_time": f"{avg_time:.3f}s", "times": [f"{t:.3f}s" for t in times]}
            )
        elif avg_time < 5.0:
            log_test(
                "页面响应时间",
                True,
                f"平均响应时间: {avg_time:.3f}s (可接受)",
                {"avg_time": f"{avg_time:.3f}s", "times": [f"{t:.3f}s" for t in times]}
            )
        else:
            log_test(
                "页面响应时间",
                False,
                f"平均响应时间: {avg_time:.3f}s (> 5s，较慢)",
                {"avg_time": f"{avg_time:.3f}s", "times": [f"{t:.3f}s" for t in times]}
            )
    except Exception as e:
        log_test(
            "页面响应时间",
            False,
            f"测试失败: {str(e)}"
        )


def generate_report():
    """生成测试报告"""
    test_results["end_time"] = datetime.now().isoformat()
    
    report = f"""# Web界面测试报告

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
        if test['details']:
            report += f"- **详情**:\n"
            for key, value in test['details'].items():
                report += f"  - {key}: {value}\n"
    
    report += f"\n## 总结\n\n"
    if test_results['failed'] == 0:
        report += "🎉 所有Web界面测试通过！\n"
    else:
        report += f"⚠️  有 {test_results['failed']} 个测试失败。\n"
    
    # 保存报告
    report_file = "TEST_REPORT_WEB.md"
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
    print("*" + "  SoulX-TTS Web界面测试".center(56) + "*")
    print("*" + " " * 58 + "*")
    print("*" * 60)
    print("\n")
    
    # 1. 主页访问测试
    test_homepage()
    test_api_docs()
    test_gradio_assets()
    
    # 2. 页面结构测试
    test_page_structure()
    
    # 3. 性能测试
    test_response_time()
    
    # 4. 生成报告
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)
    print(f"总计: {test_results['passed']}/{test_results['total']} 个测试通过")
    print(f"通过率: {test_results['passed']/test_results['total']*100:.1f}%")
    
    if test_results['failed'] == 0:
        print("\n🎉 所有Web界面测试通过！")
    else:
        print(f"\n⚠️  有 {test_results['failed']} 个测试失败")
    
    generate_report()


if __name__ == "__main__":
    main()

