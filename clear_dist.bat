@echo off
set "folderPath=dist"
del /q /s "%folderPath%\*.*"
rd /s /q "%folderPath%"
mkdir "%folderPath%"