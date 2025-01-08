# Tempus Pugnus (时间拳)

[English](../README.md) | [简体中文](README_zh-CN.md)

来自《共鸣之武器》

原设：对所有行动设定时间限制并记录，限制形式为到多少点多少分。中途超出了时间，就再延个时间限制。最终完成时可以记录总结。

延期可以不止一次的，理念其实是限时，如果真没做完可以多延期几次，这个最好也记录下来。不叫延期，叫调整。咱是在主动记录时间，而不是被动地处理延期。

还有一个提醒功能，一个按钮“提醒” 点击后可以滚动输入一个分钟时间，默认为1分钟。然后程序会在这个时间之后进行一个弹框提醒。这种是方便我运行一些需要若干分钟的作业，而我不想等待，但是又怕忘记它的时候使用的。比如编译，比如运行。干等着简直要疯。

## 简介
一个简洁的时间管理工具，通过设定明确的时间限制来帮助用户专注完成任务。采用浮窗形式，始终保持在屏幕顶层，方便用户随时查看剩余时间。

## 功能特点

- 🎯 新建定时任务
- ⏱️ 实时倒计时显示
- 🔄 任务时限调整
- ✅ 任务完成记录
- 📜 历史记录查看
- ⏲️ 快速提醒功能

## 界面预览

[这里可以放几张软件界面截图]

## 安装使用

```bash
# 克隆仓库
git clone https://github.com/tobenot/TempusPugnus.git

# 安装依赖
pip install -r requirements.txt

# 运行程序
python run.pyw
```

## 技术实现

- 使用 PyQt6 构建界面
- 采用 JSON 文件存储任务数据
- 支持日志记录

## 项目结构

```
TempusPugnus/
├── gui/
│   ├── dialogs/           # 对话框组件
│   │   ├── base_dialog.py   # 基础对话框类
│   │   ├── task_dialog.py   # 新建任务对话框
│   │   ├── adjust_dialog.py # 调整时限对话框
│   │   ├── complete_dialog.py # 完成任务对话框
│   │   ├── history_dialog.py # 历史记录对话框
│   │   └── reminder_dialog.py # 快速提醒对话框
│   ├── styles/           # 样式定义
│   └── main_window.py    # 主窗口类
├── core/
│   └── task_manager.py   # 任务管理类
└── data/                 # 数据存储
    ├── tasks.json       # 任务数据
    └── task_manager.log # 操作日志
```

## 界面设计

### 主窗口
- 无边框浮窗设计
- 始终置顶显示
- 支持拖拽移动
- 半透明背景效果

### 对话框
所有对话框保持统一风格：
- 无边框设计
- 渐变背景
- 支持拖拽
- 居中显示

## 数据结构

```json
{
    "id": "唯一标识",
    "task": "任务描述",
    "start_time": "开始时间",
    "initial_deadline": "初始截止时间",
    "current_deadline": "当前截止时间",
    "adjustments": [
        {
            "time": "调整时间",
            "reason": "调整原因",
            "original_deadline": "原截止时间",
            "new_deadline": "新截止时间"
        }
    ],
    "completion_time": "完成时间",
    "summary": "总结",
    "status": "状态"
}
```

## 主题样式

- 背景：深蓝渐变 (#1a1a2e -> #16213e)
- 边框：金色 (#DAA520)
- 文字：金色 (#FFD700)
- 控件：半透明深色 (rgba(44, 62, 80, 180))

## 贡献指南

欢迎提交 Issue 和 Pull Request！

## 许可证

[MIT License](../LICENSE)