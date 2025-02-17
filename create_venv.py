import os
import platform
import subprocess

is_windows = platform.system() == "Windows"

# 환경 변수 설정
os.environ["PIPENV_VENV_IN_PROJECT"] = "true"
os.environ["PIPENV_IGNORE_VIRTUALENVS"] = "1"

# pipenv install 실행
if platform.system() == "Windows":
    subprocess.run(["pipenv", "install"], shell=False)
else:
    subprocess.run(["pipenv", "install"], shell=False)