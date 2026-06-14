@echo off
pushd %~dp0
pyinstaller --onefile --windowed --name Cerebrum --add-data "assets;assets" main.py
popd
