# 🧪 测试目录

本目录包含项目的所有测试脚本和测试报告。

## 📋 测试脚本

### API 测试
- **test_api_complete.py** - 完整的 API 功能测试
  - 单人 TTS 测试（多种方言）
  - 多人播客测试
  - 示例脚本测试
  - 错误处理测试

### Web 界面测试
- **test_web_interface.py** - Gradio Web 界面测试
  - 页面访问测试
  - 内容验证测试
  - 响应时间测试

### 单元测试
- **test_podcast.py** - 播客工具单元测试
  - 脚本解析测试
  - 脚本验证测试
  - 示例脚本生成测试

### 其他测试
- **test_setup.py** - 环境设置测试
- **test_multiline.py** - 多行文本测试
- **example_usage.py** - 使用示例代码

## 📊 测试报告

- **TEST_REPORT_API.md** - API 测试详细报告
- **TEST_REPORT_WEB.md** - Web 界面测试报告
- **TEST_REPORT_COMPLETE.md** - 完整综合测试报告

## 🚀 运行测试

### 运行所有 API 测试
```bash
cd /Users/zhaojianyun/Downloads/soulx-tts-metal
python tests/test_api_complete.py
```

### 运行 Web 界面测试
```bash
python tests/test_web_interface.py
```

### 运行单元测试
```bash
python tests/test_podcast.py
```

## 📈 测试覆盖

### 功能测试
- ✅ 单人 TTS（多种方言）
- ✅ 多人播客生成
- ✅ 副语言标签（笑声、叹气等）
- ✅ 错误处理
- ✅ API 端点
- ✅ Web 界面

### 性能测试
- ✅ 响应时间
- ✅ 音频生成速度
- ✅ 内存使用

## 🎯 测试结果

最新测试结果请查看：
- `TEST_REPORT_COMPLETE.md` - 最完整的测试报告
- `../docs/测试执行总结.md` - 测试执行总结

## 📁 测试输出

测试生成的音频文件位于：
- `test_outputs/` - 测试音频输出目录
- `../temp/` - 临时测试文件

## 🔧 测试环境要求

- Python 3.8+
- 所有依赖已安装（见 requirements.txt）
- 模型文件已下载
- 服务器已启动（API 测试需要）

