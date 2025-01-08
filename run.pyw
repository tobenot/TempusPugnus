import os
import sys

# 获取当前脚本所在目录的父目录
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 将父目录添加到 Python 路径
sys.path.append(parent_dir)

from TempusPugnus.main import main

if __name__ == '__main__':
    main() 