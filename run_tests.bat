@echo off
echo ============================
echo Running Pytest in venv ...
echo ============================

:: 切换到 .bat 所在目录
cd /d %~dp0

:: 激活虚拟环境
call venv\Scripts\activate

:: 运行 pytest 测试
pytest

:: 保持窗口别一闪而过
pause
