@echo off
echo Adding Vortex Tunnel firewall rules...

REM Add inbound rule for port 8080
netsh advfirewall firewall add rule name="Vortex Tunnel Inbound" dir=in action=allow protocol=TCP localport=8080

REM Add outbound rule for port 8080
netsh advfirewall firewall add rule name="Vortex Tunnel Outbound" dir=out action=allow protocol=TCP remoteport=8080

echo Firewall rules added successfully!
echo.
echo Now try connecting in the app again.
pause 