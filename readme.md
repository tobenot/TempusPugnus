# Tempus Pugnus

[English](README.md) | [简体中文](docs/README_zh-CN.md)

Inspired by "Resonant Weapons" (来自《共鸣之武器》)

A minimalist time management tool with floating window interface. Set time limits for tasks, track progress, and get reminders - helping you stay focused and productive.

## Introduction
A clean and efficient time management tool that helps users focus on completing tasks by setting clear time limits. It uses a floating window that stays on top of the screen, making it easy to check remaining time.

## Features

- 🎯 Create timed tasks
- ⏱️ Real-time countdown display
- 🔄 Task time limit adjustment
- ✅ Task completion records
- 📜 History viewing
- ⏲️ Quick reminder function

## Preview

[Screenshots will be added here]

## Installation

```bash
# Clone repository
git clone https://github.com/tobenot/TempusPugnus.git

# Install dependencies
pip install -r requirements.txt

# Run the program
python run.pyw
```

## Technical Implementation

- Built with PyQt6
- JSON file storage for task data
- Logging support

## Project Structure

```
TempusPugnus/
├── gui/
│   ├── dialogs/           # Dialog components
│   │   ├── base_dialog.py   # Base dialog class
│   │   ├── task_dialog.py   # New task dialog
│   │   ├── adjust_dialog.py # Time adjustment dialog
│   │   ├── complete_dialog.py # Task completion dialog
│   │   ├── history_dialog.py # History dialog
│   │   └── reminder_dialog.py # Quick reminder dialog
│   ├── styles/           # Style definitions
│   └── main_window.py    # Main window class
├── core/
│   └── task_manager.py   # Task management class
└── data/                 # Data storage
    ├── tasks.json       # Task data
    └── task_manager.log # Operation logs
```

## Interface Design

### Main Window
- Borderless floating window
- Always on top
- Drag support
- Semi-transparent background

### Dialogs
All dialogs maintain a consistent style:
- Borderless design
- Gradient background
- Drag support
- Center display

## Data Structure

```json
{
    "id": "unique identifier",
    "task": "task description",
    "start_time": "start time",
    "initial_deadline": "initial deadline",
    "current_deadline": "current deadline",
    "adjustments": [
        {
            "time": "adjustment time",
            "reason": "adjustment reason",
            "original_deadline": "original deadline",
            "new_deadline": "new deadline"
        }
    ],
    "completion_time": "completion time",
    "summary": "summary",
    "status": "status"
}
```

## Theme Style

- Background: Deep blue gradient (#1a1a2e -> #16213e)
- Border: Gold (#DAA520)
- Text: Gold (#FFD700)
- Controls: Semi-transparent dark (rgba(44, 62, 80, 180))

## Contributing

Issues and Pull Requests are welcome!

## License

[MIT License](LICENSE)
