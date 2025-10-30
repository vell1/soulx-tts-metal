#!/usr/bin/env python3
"""
测试多行文本处理功能
"""
import sys
sys.path.insert(0, '.')
from app import preprocess_text

def test_preprocess():
    """测试文本预处理"""
    
    print("=" * 60)
    print("测试多行文本预处理")
    print("=" * 60)
    
    # 测试用例 1: 简单多行文本
    test1 = """系统通过验收需满足以下标准：
1. **功能完整性**：所有功能模块按照设计实现，功能测试通过
2. **兼容性要求**：所有信创组件兼容性测试通过，无阻塞性问题
3. **系统稳定性**：系统运行稳定，具备良好的容错和恢复能力
4. **安全要求**：通过安全扫描，无高危漏洞
5. **文档完整性**：提供完整的部署文档、运维文档、测试报告"""
    
    result1 = preprocess_text(test1)
    print("\n测试 1 - 多行列表:")
    print(f"原始文本行数: {len(test1.splitlines())}")
    print(f"处理后文本: {result1}")
    print(f"处理后长度: {len(result1)} 字符")
    
    # 测试用例 2: 带有副语言标签
    test2 = """欢迎来到语音合成系统<|laugh|>
这是一个测试文本
包含多个段落"""
    
    result2 = preprocess_text(test2)
    print("\n测试 2 - 带副语言标签:")
    print(f"原始文本: {test2}")
    print(f"处理后文本: {result2}")
    
    # 测试用例 3: 空行和多余空格
    test3 = """第一行

第三行（前面有空行）
    第四行（带缩进）
"""
    
    result3 = preprocess_text(test3)
    print("\n测试 3 - 空行和空格:")
    print(f"处理后文本: {result3}")
    
    # 测试用例 4: Windows 换行符
    test4 = "第一行\r\n第二行\r\n第三行"
    result4 = preprocess_text(test4)
    print("\n测试 4 - Windows 换行符:")
    print(f"处理后文本: {result4}")
    
    print("\n" + "=" * 60)
    print("✅ 所有测试完成！")
    print("=" * 60)


if __name__ == "__main__":
    test_preprocess()

