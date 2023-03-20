@echo off
if "%PATH_BASE%" == "" set PATH_BASE=%PATH%
set PATH=%CD%;%PATH_BASE%;

echo "building MultiAPKS"

:: 配置别名和密码
set ks_key_alias=hk.fivexgames.citydunk
set ks_pass=tonglink
set key_pass=tonglink123456

:: 如果目录中存在multi.apks则删除
if exist multi.apks DEL /F /A /Q multi.apks
:: 会找当前目录中的keystore 确保只有一个keystore
for /f "delims=" %%a in ('dir /b *.keystore') do (set key=%%a);

echo keystore=%key%
echo ks_key_alias=%ks_key_alias%
echo ks_pass=%ks_pass%
echo key_pass=%key_pass%

:: build apk
:: 会找当前目录中的aab 确保只有一个aab
for /f "delims=" %%a in ('dir /b *.aab') do (set aab=%%a);
echo aab=%aab%
java -jar "%~dp0\bundletool-all-1.6.1.jar" build-apks --bundle=%aab% --mode=universal --output=universal.apks ^
--ks=%key% ^
--ks-key-alias=%ks_key_alias% ^
--ks-pass=pass:%ks_pass% ^
--key-pass=pass:%key_pass%

pause
