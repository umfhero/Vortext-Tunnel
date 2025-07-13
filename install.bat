@echo off
echo Installing Vortex Tunnel...
echo.

REM Check if Tailscale is installed
tailscale --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Warning: Tailscale is not installed or not in PATH.
    echo Please install Tailscale from https://tailscale.com/
    echo.
    pause
)

REM Copy executable to Program Files
set "INSTALL_DIR=%PROGRAMFILES%\VortexTunnel"
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

copy "VortexTunnel.exe" "%INSTALL_DIR%\"

REM Create desktop shortcut
set "DESKTOP=%USERPROFILE%\Desktop"
set "SHORTCUT=%DESKTOP%\VortexTunnel.lnk"

echo @echo off > "%TEMP%\create_shortcut.vbs"
echo Set oWS = WScript.CreateObject("WScript.Shell") >> "%TEMP%\create_shortcut.vbs"
echo sLinkFile = "%SHORTCUT%" >> "%TEMP%\create_shortcut.vbs"
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> "%TEMP%\create_shortcut.vbs"
echo oLink.TargetPath = "%INSTALL_DIR%\VortexTunnel.exe" >> "%TEMP%\create_shortcut.vbs"
echo oLink.WorkingDirectory = "%INSTALL_DIR%" >> "%TEMP%\create_shortcut.vbs"
echo oLink.Save >> "%TEMP%\create_shortcut.vbs"

cscript //nologo "%TEMP%\create_shortcut.vbs"
del "%TEMP%\create_shortcut.vbs"

echo.
echo Vortex Tunnel has been installed successfully!
echo You can find it on your desktop and in the Start menu.
echo.
pause
