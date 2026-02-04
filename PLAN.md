# 桌面翻译工具 - 实现计划

## 需求概述

桌面悬浮窗翻译工具（类似有道词典），支持鼠标框选文本弹出翻译。

**核心功能**：
- 文本翻译（选择语言对，输出结果）
- 鼠标框选翻译（全局快捷键触发，悬浮窗显示结果）
- 文件翻译（txt/docx/pdf）
- 翻译历史记录（搜索、导出）
- 单词详解（音标、释义、例句）

**翻译API**：百度翻译 + 有道翻译（策略模式，可扩展）

---

## 技术栈

| 用途 | 技术选型 | 说明 |
|------|---------|------|
| GUI框架 | PyQt5 | 悬浮窗、系统托盘、主窗口 |
| HTTP客户端 | httpx | 调用翻译API |
| 数据模型 | Pydantic | 请求/响应模型，frozen=True 保证不可变 |
| 数据库 | SQLite + SQLAlchemy | 翻译历史持久化 |
| PDF解析 | PyMuPDF | 提取PDF文本 |
| DOCX解析 | python-docx | 提取Word文本 |
| 编码检测 | chardet | TXT文件编码自动检测 |
| 全局快捷键 | pynput | 监听热键、模拟Ctrl+C |
| 剪贴板 | pyperclip | 读写剪贴板内容 |
| 测试 | pytest + pytest-qt | 单元测试 + UI测试 |

---

## 项目结构

```
Project/
├── main.py                            # 入口
├── requirements.txt
├── pytest.ini
│
├── src/
│   ├── __init__.py
│   ├── app.py                         # QApplication 初始化、信号连接
│   │
│   ├── config/
│   │   ├── __init__.py
│   │   ├── settings.py                # Pydantic AppSettings，JSON持久化
│   │   └── constants.py               # API地址、语言代码映射
│   │
│   ├── translation/                   # 翻译引擎（策略模式）
│   │   ├── __init__.py
│   │   ├── base_engine.py             # 抽象基类 TranslationEngine
│   │   ├── baidu_engine.py            # 百度翻译 API 实现
│   │   ├── youdao_engine.py           # 有道翻译 API 实现
│   │   ├── engine_factory.py          # 工厂：根据配置创建引擎
│   │   ├── engine_manager.py          # 策略上下文：管理当前引擎
│   │   └── models.py                  # TranslationRequest/Result/WordDetail
│   │
│   ├── file_parser/                   # 文件解析（策略模式）
│   │   ├── __init__.py
│   │   ├── base_parser.py             # 抽象基类 FileParser
│   │   ├── txt_parser.py              # TXT + 编码检测
│   │   ├── docx_parser.py             # DOCX 解析
│   │   ├── pdf_parser.py              # PDF 解析
│   │   └── parser_factory.py          # 按扩展名选择解析器
│   │
│   ├── clipboard/                     # 框选翻译
│   │   ├── __init__.py
│   │   ├── hotkey_manager.py          # pynput 全局热键监听
│   │   └── selection_handler.py       # 模拟Ctrl+C、读剪贴板、发信号
│   │
│   ├── history/                       # 翻译历史
│   │   ├── __init__.py
│   │   ├── models.py                  # SQLAlchemy ORM: TranslationRecord
│   │   ├── repository.py             # CRUD、搜索、分页
│   │   └── export_service.py          # 导出CSV/TXT
│   │
│   ├── database/
│   │   ├── __init__.py
│   │   ├── connection.py              # SQLite引擎、Session工厂
│   │   └── migrations.py              # 建表
│   │
│   ├── services/                      # 业务编排层
│   │   ├── __init__.py
│   │   ├── translation_service.py     # 翻译 + 存历史 + 发UI信号
│   │   └── file_translation_service.py # 文件解析 + 分块翻译 + 进度
│   │
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── main_window.py             # 主窗口（QTabWidget: 翻译/文件/历史）
│   │   ├── floating_popup.py          # 无边框悬浮翻译窗口
│   │   ├── system_tray.py             # 系统托盘图标和菜单
│   │   ├── widgets/
│   │   │   ├── __init__.py
│   │   │   ├── translation_panel.py   # 文本翻译面板
│   │   │   ├── word_detail_panel.py   # 单词详解面板（音标+释义+例句）
│   │   │   ├── file_translate_panel.py # 文件翻译面板（进度条+预览）
│   │   │   ├── history_panel.py       # 历史记录面板（搜索+分页+导出）
│   │   │   ├── settings_dialog.py     # 设置对话框（API密钥+偏好）
│   │   │   └── language_selector.py   # 语言选择下拉框
│   │   └── styles/
│   │       ├── __init__.py
│   │       └── theme.py               # QSS样式
│   │
│   └── utils/
│       ├── __init__.py
│       ├── crypto.py                  # API密钥加密存储
│       ├── text_utils.py              # 文本分块、单词检测
│       └── async_worker.py            # QRunnable 异步任务执行器
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── unit/
│   │   ├── test_baidu_engine.py
│   │   ├── test_youdao_engine.py
│   │   ├── test_engine_manager.py
│   │   ├── test_file_parsers.py
│   │   ├── test_history_repository.py
│   │   └── test_settings.py
│   └── integration/
│       ├── test_baidu_api_live.py
│       └── test_database.py
│
└── resources/
    └── icons/
```

---

## 核心架构设计

### 翻译引擎 - 策略模式

```
EngineManager (策略上下文)
    ├── BaiduEngine   (百度翻译API)
    └── YoudaoEngine  (有道翻译API)
    └── 新引擎...     (只需实现 TranslationEngine 接口)
```

- `TranslationEngine` 抽象基类定义 `translate()` 和 `lookup_word()` 接口
- `EngineManager` 持有所有引擎，委派给当前激活的引擎
- `EngineFactory` 根据配置创建引擎实例
- 新增引擎只需：创建实现文件 + 注册到工厂，无需改动其他代码

### 数据模型（Pydantic, frozen=True）

- `TranslationRequest`: text, from_lang, to_lang
- `TranslationResult`: source_text, translated_text, engine_name, word_detail?
- `WordDetail`: word, phonetic, uk_phonetic, us_phonetic, explains, examples

### 数据库表: `translation_history`

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER PK | 主键 |
| source_text | TEXT | 原文 |
| translated_text | TEXT | 译文 |
| from_lang | VARCHAR(10) | 源语言 |
| to_lang | VARCHAR(10) | 目标语言 |
| engine_name | VARCHAR(50) | 引擎名称 |
| is_word | INTEGER | 是否单词 |
| word_detail_json | TEXT | WordDetail JSON |
| created_at | DATETIME | 创建时间 |

### 框选翻译流程

```
用户框选文本 → 按 Ctrl+Alt+T → HotkeyManager 检测
  → SelectionHandler: 释放修饰键 → 模拟Ctrl+C → 读剪贴板 → 恢复剪贴板
  → 通过 QObject 信号桥发送到UI线程
  → TranslationService 调用翻译引擎
  → FloatingPopup 在鼠标附近弹出翻译结果
```

### 异步方案

PyQt5事件循环与asyncio冲突，使用 **QRunnable + QThreadPool**：
- 翻译请求在线程池中执行（用同步 httpx.Client）
- 通过 pyqtSignal 将结果传回UI线程
- UI保持响应，不卡顿

---

## 分阶段实现顺序

### Phase 1: 基础架构
- 项目结构搭建、requirements.txt、依赖安装
- config (settings.py, constants.py)
- translation/models.py（数据模型）
- translation/base_engine.py（抽象接口）
- translation/baidu_engine.py（第一个引擎）
- translation/engine_manager.py
- 单元测试验证翻译功能

### Phase 2: 数据库与历史
- database/connection.py, migrations.py
- history/models.py, repository.py, export_service.py
- 单元测试验证 CRUD 和搜索

### Phase 3: 主窗口 UI
- ui/styles/theme.py
- ui/widgets/language_selector.py, translation_panel.py
- utils/async_worker.py（QRunnable封装）
- ui/main_window.py（翻译Tab）
- app.py, main.py
- **验证**: 启动应用，输入文本，获得翻译结果

### Phase 4: 有道引擎 + 单词详解
- translation/youdao_engine.py
- translation/engine_factory.py
- ui/widgets/word_detail_panel.py
- 引擎切换功能

### Phase 5: 系统托盘 + 悬浮窗
- ui/system_tray.py
- ui/floating_popup.py（无边框、置顶、鼠标附近弹出）
- clipboard/hotkey_manager.py, selection_handler.py
- services/translation_service.py
- **验证**: 任意位置框选文本 → 快捷键 → 悬浮窗显示翻译

### Phase 6: 文件翻译
- file_parser/ 全部文件
- services/file_translation_service.py（分块翻译 + 进度）
- ui/widgets/file_translate_panel.py

### Phase 7: 历史 UI + 设置
- ui/widgets/history_panel.py（搜索、分页、导出）
- ui/widgets/settings_dialog.py（API密钥、快捷键、偏好）
- utils/crypto.py（密钥加密存储）

### Phase 8: 打磨与测试
- 全面错误处理、输入校验
- 补充单元测试达到 80%+ 覆盖率
- UI打磨、边界情况处理

---

## 验证方案

1. **Phase 1 验证**: 运行 `pytest tests/unit/test_baidu_engine.py` 确认API调用和签名正确
2. **Phase 3 验证**: 运行 `python main.py`，在主窗口中输入文本翻译
3. **Phase 5 验证**: 最小化到托盘后，框选任意文本按 Ctrl+Alt+T，悬浮窗弹出翻译
4. **Phase 6 验证**: 上传PDF/DOCX文件，观察进度条和翻译结果
5. **Phase 7 验证**: 查看历史记录、搜索、导出CSV；修改设置后重启验证持久化
6. **全量测试**: `pytest tests/ -v` 全部通过，覆盖率 ≥ 80%

---

## 关键文件（修改/创建）

- `src/translation/base_engine.py` - 策略模式基石
- `src/translation/baidu_engine.py` - 首个引擎，验证架构
- `src/ui/main_window.py` - UI 中枢
- `src/clipboard/selection_handler.py` - 框选翻译核心（技术难点最高）
- `src/services/translation_service.py` - 业务编排层

## 需要安装的依赖

```
pip install PyQt5 httpx pydantic sqlalchemy PyMuPDF python-docx pynput pyperclip chardet pytest pytest-qt
```
