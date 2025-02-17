import PyInstaller.__main__
import sys
import os

# 현재 스크립트의 디렉토리를 기준으로 상대 경로 설정
current_dir = os.path.dirname(os.path.abspath(__file__))
main_path = os.path.join(current_dir, "Main.py")

PyInstaller.__main__.run([
    main_path,
    '--name=InspectionDataViewer',
    '--onefile',
    '--windowed',
    '--add-data=LICENSE;.',
    '--hidden-import=PySide6.QtWebEngineCore',
    '--hidden-import=plotly',
    '--hidden-import=dependency_injector.containers',
    '--hidden-import=dependency_injector.providers',
    '--hidden-import=dependency_injector.errors',
    '--hidden-import=dependency_injector.wiring',
    '--collect-data=plotly',
]) 