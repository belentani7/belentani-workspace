@echo off
echo Reseteando OpenCode...
rmdir /s /q "%APPDATA%\opencode" 2>nul
rmdir /s /q "%LOCALAPPDATA%\opencode" 2>nul
cmdkey /delete:opencode 2>nul
echo Listo. Pulsa una techa para cerrar.
pause >nul