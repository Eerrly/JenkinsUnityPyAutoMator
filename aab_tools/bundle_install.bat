@echo off
if "%PATH_BASE%" == "" set PATH_BASE=%PATH%
set PATH=%CD%;%PATH_BASE%;

echo ">>> Install Android App Bundle <<<"

:: 配置别名和密码
set ks_key_alias=com.cyou.freestyle2.gp
set ks_pass=jielan2
set key_pass=jielan2

:: 如果目录中存在multi.apks则删除
if exist multi.apks DEL /F /A /Q multi.apks
:: 会找当前目录中的keystore 确保只有一个keystore
for /f "delims=" %%a in ('dir /b *.keystore') do (set key=%%a);

echo "Step 1: Build Apks ..."
:: 会找当前目录中的aab 确保只有一个aab
for /f "delims=" %%a in ('dir /b *.aab') do (set aab=%%a);
echo aab=%aab%
java -jar "%~dp0\bundletool-all-1.6.1.jar" build-apks --connected-device --bundle=%aab% --output=multi.apks ^
--ks=%key% ^
--ks-key-alias=%ks_key_alias% ^
--ks-pass=pass:%ks_pass% ^
--key-pass=pass:%key_pass%

echo "Step 2: Install Apks ..."
java -jar "%~dp0\bundletool-all-1.6.1.jar" install-apks --apks=multi.apks

pause
