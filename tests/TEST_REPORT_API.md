# API 测试报告

## 测试概览

- **开始时间**: 2025-10-30T09:53:47.986061
- **结束时间**: 2025-10-30T09:55:45.138650
- **总测试数**: 13
- **通过**: 12 ✅
- **失败**: 1 ❌
- **通过率**: 92.3%

## 测试结果详情


### 服务健康检查

- **状态**: ✅ PASS
- **信息**: 服务正常运行 (HTTP 200)
- **耗时**: 0.01s

### 单人TTS - 基础功能

- **状态**: ✅ PASS
- **信息**: 音频生成成功，文件大小: 184364 bytes
- **耗时**: 13.58s
- **详情**: {
  "file_size": 184364,
  "output": "test_outputs/test_single_basic.wav"
}

### 单人TTS - 四川话

- **状态**: ✅ PASS
- **信息**: 音频生成成功，文件大小: 96044 bytes
- **耗时**: 11.03s
- **详情**: {
  "file_size": 96044,
  "output": "test_outputs/test_single_四川话.wav"
}

### 单人TTS - 粤语

- **状态**: ✅ PASS
- **信息**: 音频生成成功，文件大小: 107564 bytes
- **耗时**: 13.80s
- **详情**: {
  "file_size": 107564,
  "output": "test_outputs/test_single_粤语.wav"
}

### 单人TTS - 河南话

- **状态**: ✅ PASS
- **信息**: 音频生成成功，文件大小: 92204 bytes
- **耗时**: 11.59s
- **详情**: {
  "file_size": 92204,
  "output": "test_outputs/test_single_河南话.wav"
}

### 单人TTS - 副语言标签

- **状态**: ✅ PASS
- **信息**: 音频生成成功，文件大小: 245804 bytes
- **耗时**: 6.66s
- **详情**: {
  "file_size": 245804,
  "output": "test_outputs/test_single_emotions.wav"
}

### 单人TTS - 错误处理（空文本）

- **状态**: ❌ FAIL
- **信息**: 应该返回错误但返回了200

### 多人播客 - 基础两人对话

- **状态**: ✅ PASS
- **信息**: 播客生成成功，文件大小: 582764 bytes
- **耗时**: 16.84s
- **详情**: {
  "file_size": 582764,
  "output": "test_outputs/test_podcast_basic.wav"
}

### 多人播客 - 多人对话

- **状态**: ✅ PASS
- **信息**: 播客生成成功，文件大小: 265964 bytes
- **耗时**: 10.89s
- **详情**: {
  "file_size": 265964,
  "output": "test_outputs/test_podcast_multi.wav"
}

### 多人播客 - 多方言混合

- **状态**: ✅ PASS
- **信息**: 播客生成成功，文件大小: 355244 bytes
- **耗时**: 27.73s
- **详情**: {
  "file_size": 355244,
  "output": "test_outputs/test_podcast_dialect.wav"
}

### 多人播客 - 错误处理（格式错误）

- **状态**: ✅ PASS
- **信息**: 正确检测到格式错误

### 示例API - 简单格式

- **状态**: ✅ PASS
- **信息**: 成功获取示例，长度: 385 字符

### 示例API - JSON格式

- **状态**: ✅ PASS
- **信息**: 成功获取示例，长度: 801 字符

## 总结

⚠️  有 1 个测试失败，请检查相关功能。
