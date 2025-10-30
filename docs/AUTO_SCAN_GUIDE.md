# 🔍 自动扫描参考音频功能指南

## ✨ 功能说明

系统会**自动扫描** `prompt_audios/` 目录中的所有 WAV 音频文件，无需手动在代码中配置说话人列表！

## 🚀 快速开始

### 1. 添加新的说话人

只需 3 步：

#### 步骤 1: 准备音频文件

将音频文件（3-10 秒，WAV 格式）复制到 `prompt_audios/` 目录：

```bash
cp your_voice.wav prompt_audios/female_2.wav
```

#### 步骤 2: 创建文本描述（可选）

创建同名的 `.txt` 文件提供参考文本：

```bash
echo "这是一段清晰的普通话语音示例" > prompt_audios/female_2.txt
```

#### 步骤 3: 重启服务

```bash
bash start.sh
```

**就这么简单！** 系统会自动识别新添加的音频文件。

## 📁 文件命名规范

### 标准命名模式

系统会自动将英文前缀转换为中文显示名：

| 文件名 | 显示名称 | 说明 |
|--------|----------|------|
| `female_1.wav` | 女声1 | 推荐用于女性音色 |
| `female_2.wav` | 女声2 | |
| `male_1.wav` | 男声1 | 推荐用于男性音色 |
| `male_2.wav` | 男声2 | |
| `neutral_1.wav` | 中性1 | 推荐用于中性音色 |
| `child_1.wav` | 童声1 | 推荐用于儿童音色 |

### 自定义命名

支持任意自定义名称：

| 文件名 | 显示名称 |
|--------|----------|
| `female_sweet.wav` | 女声sweet |
| `male_deep.wav` | 男声deep |
| `narrator.wav` | narrator |
| `张三.wav` | 张三 |
| `李四.wav` | 李四 |

## 📝 文本描述文件

### 为什么需要文本描述？

参考文本用于模型理解音色特征，提供更好的生成效果。

### 创建方法

在 `prompt_audios/` 目录创建与音频文件同名的 `.txt` 文件：

```
prompt_audios/
├── female_1.wav
├── female_1.txt       # ← 对应的文本描述
├── male_1.wav
└── male_1.txt         # ← 对应的文本描述
```

### 文本内容建议

- **长度**: 1-3 句话，10-50 个字
- **内容**: 应该是音频中实际说的话
- **语言**: 使用普通话描述

**示例**:

```txt
喜欢攀岩、徒步、滑雪的语言爱好者，以及过两天要带着全部家当去景德镇做陶瓷的白日梦想家。
```

### 如果没有文本描述？

系统会自动生成默认描述：`这是{说话人名称}的参考音频。`

## 🎯 实际应用示例

### 示例 1: 添加新的女声

```bash
# 1. 复制音频文件
cp sweet_voice.wav prompt_audios/female_sweet.wav

# 2. 添加文本描述
cat > prompt_audios/female_sweet.txt << EOF
欢迎来到 AI 语音合成系统，我们提供高质量的语音服务。
EOF

# 3. 重启服务
bash start.sh
```

在 Web 界面中会看到新的选项：**女声sweet**

### 示例 2: 添加名人音色（仅用于学习）

```bash
# 1. 准备音频
cp celebrity_voice.wav prompt_audios/名人名字.wav

# 2. 添加描述
echo "这是一段示例音频" > prompt_audios/名人名字.txt

# 3. 重启
bash start.sh
```

**注意**: 请遵守版权法律，仅在合法范围内使用。

### 示例 3: 批量添加音色

```bash
# 添加多个音色
cp voice1.wav prompt_audios/female_3.wav
cp voice2.wav prompt_audios/male_3.wav
cp voice3.wav prompt_audios/narrator.wav

# 批量添加描述
echo "温柔的女声" > prompt_audios/female_3.txt
echo "磁性的男声" > prompt_audios/male_3.txt
echo "专业的旁白声" > prompt_audios/narrator.txt

# 重启服务
bash start.sh
```

## 🔍 验证扫描结果

### 方法 1: 查看启动日志

```bash
python app.py
```

输出会显示：
```
[INFO] 已扫描到 5 个说话人: Kieran-Phoenix, 女声1, 女声2, 男声1, 旁白
```

### 方法 2: 使用测试脚本

```python
python -c "
from app import SPEAKERS
print('可用的说话人:')
for name in SPEAKERS:
    print(f'  - {name}')
"
```

### 方法 3: 检查 Web 界面

访问 http://localhost:8000，在"说话人"下拉菜单中查看所有选项。

## ⚙️ 高级配置

### 自定义前缀映射

如果需要添加新的前缀识别规则，编辑 `app.py` 中的 `generate_display_name` 函数：

```python
prefix_map = {
    'female': '女声',
    'male': '男声',
    'neutral': '中性',
    'child': '童声',
    # 添加自定义前缀
    'robot': '机器人',
    'elder': '老年',
}
```

### 忽略特定文件

系统自动忽略：
- 隐藏文件（以 `.` 开头）
- 非 WAV 格式文件
- `.txt` 描述文件

## 🎨 音频文件要求

### 格式要求

- **文件格式**: WAV (PCM 16-bit)
- **采样率**: 22050 Hz 或 24000 Hz（推荐）
- **声道**: 单声道（Mono）或立体声（Stereo）
- **时长**: 3-10 秒（推荐 5-8 秒）

### 质量要求

- ✅ **清晰**: 无背景噪音
- ✅ **完整**: 完整的句子或短语
- ✅ **标准**: 发音标准，语速适中
- ❌ **避免**: 音乐、杂音、多人对话

### 录制建议

1. **安静环境**: 选择安静的房间
2. **距离适中**: 麦克风距离嘴巴 10-15cm
3. **自然语调**: 保持自然的说话方式
4. **清晰发音**: 吐字清晰，不要含糊

## 🔧 故障排除

### Q1: 新添加的音频没有被识别

**A**: 检查：
1. 文件扩展名是否为 `.wav`（小写）
2. 文件是否在 `prompt_audios/` 目录
3. 文件名是否以 `.` 开头（隐藏文件会被忽略）
4. 是否重启了服务

### Q2: 显示名称不符合预期

**A**: 
- 检查文件命名是否符合规范
- 使用完全自定义名称（不带前缀）
- 或修改 `app.py` 中的映射规则

### Q3: 生成的语音质量不好

**A**: 
1. 检查参考音频质量（是否有噪音）
2. 确认音频时长（3-10 秒为佳）
3. 提供准确的文本描述（`.txt` 文件）
4. 尝试使用更高质量的参考音频

### Q4: 如何删除说话人？

**A**: 
```bash
# 删除音频文件和对应的文本文件
rm prompt_audios/speaker_name.wav
rm prompt_audios/speaker_name.txt

# 重启服务
bash start.sh
```

## 📊 最佳实践

### 1. 组织音频文件

```
prompt_audios/
├── female_1.wav          # 标准女声
├── female_1.txt
├── female_2.wav          # 甜美女声
├── female_2.txt
├── male_1.wav            # 标准男声
├── male_1.txt
├── male_2.wav            # 深沉男声
├── male_2.txt
├── narrator.wav          # 旁白
├── narrator.txt
└── README.md
```

### 2. 命名建议

- 使用有意义的名称
- 保持命名一致性
- 使用英文或拼音（避免特殊字符）

### 3. 文档化

为每个音频创建描述文件，记录：
- 音色特点
- 适用场景
- 录制日期

### 4. 版本管理

```bash
# 备份原始音频
mkdir -p prompt_audios/backup
cp prompt_audios/*.wav prompt_audios/backup/
```

## 🎓 总结

✅ **优点**:
- 无需修改代码
- 即插即用
- 灵活扩展
- 自动识别

❌ **限制**:
- 需要重启服务才能生效
- 仅支持 WAV 格式
- 音频文件名不能重复

## 📚 相关文档

- [prompt_audios/README.md](prompt_audios/README.md) - 参考音频说明
- [README.md](README.md) - 项目主文档
- [INSTALL.md](INSTALL.md) - 安装指南

---

**提示**: 这个功能让您可以轻松管理和扩展说话人库，无需深入代码！

