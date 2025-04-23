@echo off
echo -------------------------------
echo ✅ التحقق من جدار الحماية...
echo -------------------------------

REM التحقق إذا القاعدة موجودة
netsh advfirewall firewall show rule name="Allow Flask API" | findstr "Rule Name"
IF %ERRORLEVEL% NEQ 0 (
    echo ❗ القاعدة غير موجودة، يتم إنشاؤها الآن...
    netsh advfirewall firewall add rule name="Allow Flask API" dir=in action=allow protocol=TCP localport=5000 profile=private
) ELSE (
    echo ✅ القاعدة موجودة مسبقًا.
)

echo.
echo 🚀 تشغيل سيرفر Flask...
echo -------------------------------

REM تأكد من أنك في مجلد المشروع الصحيح:
cd /d E:\مسار\مشروعك\

REM شغّل السيرفر
python app.py

pause
