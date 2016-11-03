rmdir build /S /Q
rmdir dist /S /Q
pyinstaller.exe --onefile run.py
rename dist\run.exe TOAST.exe
mkdir dist\logs
robocopy settings\defaults dist\settings /E
robocopy settings\locales dist\settings\locales /E
robocopy toasthttp\static dist\toasthttp\static /E
robocopy toasthttp\templates dist\toasthttp\templates /E

pause