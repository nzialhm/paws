@echo off
REM ================================================
REM Python 2.7 전용 Jupyter 설치 스크립트
REM ================================================

REM 1. Python 2.7 가상환경 생성
python -m pip install --upgrade pip
pip install virtualenv
virtualenv .venv27

REM 2. 가상환경 활성화
call .venv27\Scripts\activate.bat

REM 3. pip 업그레이드
pip install --upgrade pip

REM 4. 호환되는 Jupyter 설치
pip install "notebook==5.7.8" "jupyter==1.0.0" "ipywidgets==7.2.1" "qtconsole==4.5.5" "pywinpty==0.5"

REM 5. 설치 확인
jupyter --version
python --version

echo.
echo Jupyter 2.7 환경 설치 완료!
pause