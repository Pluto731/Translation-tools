# 桌面翻译工具

一个功能强大的桌面翻译应用，支持文本翻译、文件翻译和全局框选翻译。

## 功能特性

- **文本翻译**: 支持多种语言互译
- **文件翻译**: 支持 TXT、DOCX、PDF 文件格式
- **框选翻译**: 全局快捷键（Ctrl+Alt+T）触发，鼠标框选文本后自动翻译
- **翻译历史**: 自动保存翻译记录，支持搜索、导出和管理
- **单词详解**: 支持单词音标、释义和例句展示
- **多引擎支持**: 集成百度翻译和有道翻译 API
- **系统托盘**: 最小化到系统托盘，随时唤起
- **悬浮窗显示**: 框选翻译结果以悬浮窗形式展示

## 技术栈

- **GUI框架**: PyQt5
- **HTTP客户端**: httpx
- **数据模型**: Pydantic (不可变模型)
- **数据库**: SQLite + SQLAlchemy
- **PDF解析**: PyMuPDF
- **DOCX解析**: python-docx
- **编码检测**: chardet
- **全局快捷键**: pynput
- **剪贴板**: pyperclip
- **测试框架**: pytest + pytest-qt

## 安装依赖

```bash
pip install -r requirements.txt
```

## 配置 API 密钥

首次运行需要配置翻译 API 密钥：

1. **百度翻译**:
   - 前往 [百度翻译开放平台](https://fanyi-api.baidu.com/) 注册并获取 APP ID 和密钥

2. **有道翻译**:
   - 前往 [有道智云](https://ai.youdao.com/) 注册并获取 APP Key 和 APP Secret

3. 启动应用后，点击菜单 **设置 → 偏好设置**，填入 API 密钥

## 运行应用

```bash
python main.py
```

## 使用说明

### 文本翻译

1. 打开主窗口，切换到"文本翻译"标签
2. 选择源语言和目标语言
3. 输入要翻译的文本
4. 点击"翻译"按钮
5. 翻译结果将显示在下方文本框

### 文件翻译

1. 切换到"文件翻译"标签
2. 点击"选择文件"按钮，选择 TXT、DOCX 或 PDF 文件
3. 选择源语言和目标语言
4. 点击"翻译文件"按钮
5. 等待翻译完成，结果显示在文本框中
6. 可点击"保存翻译结果"导出

### 框选翻译

1. 确保应用正在运行（可最小化到托盘）
2. 在任意应用中用鼠标选中要翻译的文本
3. 按下全局快捷键 **Ctrl+Alt+T**
4. 翻译结果将在鼠标附近弹出悬浮窗

### 翻译历史

1. 切换到"翻译历史"标签
2. 查看所有翻译记录
3. 支持关键词搜索
4. 可导出为 CSV 或 TXT 格式
5. 支持删除单条或清空全部记录

## 项目结构

```
Project/
├── main.py                     # 应用入口
├── requirements.txt            # Python 依赖
├── pytest.ini                  # pytest 配置
│
├── src/
│   ├── app.py                  # 应用主类
│   ├── config/                 # 配置管理
│   ├── translation/            # 翻译引擎（策略模式）
│   ├── file_parser/            # 文件解析器
│   ├── clipboard/              # 框选翻译
│   ├── history/                # 翻译历史
│   ├── database/               # 数据库连接
│   ├── services/               # 业务服务
│   ├── ui/                     # 用户界面
│   └── utils/                  # 工具函数
│
└── tests/
    ├── unit/                   # 单元测试
    └── integration/            # 集成测试
```

## 架构设计

### 翻译引擎 - 策略模式

```
EngineManager (策略上下文)
    ├── BaiduEngine   (百度翻译)
    └── YoudaoEngine  (有道翻译)
```

- 支持动态切换翻译引擎
- 易于扩展新引擎（只需实现 `TranslationEngine` 接口）

### 数据模型 - 不可变设计

所有数据模型使用 Pydantic 的 `frozen=True` 确保不可变性：

```python
class TranslationRequest(BaseModel, frozen=True):
    text: str
    from_lang: str = "auto"
    to_lang: str = "zh"
```

### 异步处理 - QRunnable + QThreadPool

使用 Qt 的线程池处理耗时操作，避免 UI 卡顿：

```python
worker = AsyncWorker(translate_fn, request)
worker.signals.finished.connect(on_finished)
QThreadPool.globalInstance().start(worker)
```

## 运行测试

```bash
# 运行所有测试
pytest tests/ -v

# 运行单元测试
pytest tests/unit/ -v

# 运行集成测试
pytest tests/integration/ -v

# 查看测试覆盖率
pytest tests/ --cov=src --cov-report=html
```

## 开发规范

- **不可变性**: 所有数据模型使用不可变模式，避免副作用
- **小文件原则**: 每个文件不超过 800 行，函数不超过 50 行
- **错误处理**: 所有 API 调用和文件操作都有异常处理
- **输入验证**: 使用 Pydantic 进行数据验证
- **测试覆盖**: 目标测试覆盖率 ≥ 80%

## 注意事项

1. **API 配额**: 百度翻译和有道翻译都有免费配额限制，请合理使用
2. **全局快捷键**: 快捷键可能与其他应用冲突，可在设置中修改
3. **文件编码**: TXT 文件会自动检测编码，支持 UTF-8、GBK 等
4. **PDF 解析**: 复杂 PDF（扫描版、图片）可能无法正确提取文本

## License

MIT License

## 作者

Desktop Translation Tool Development Team
