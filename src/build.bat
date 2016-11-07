rmdir build /S /Q
rmdir dist /S /Q
pyinstaller.exe run.py
rename dist\run\run.exe TOAST.exe
mkdir dist\run\logs
robocopy settings\defaults dist\run\settings /E
robocopy settings\locales dist\run\settings\locales /E
robocopy toasthttp\static dist\run\toasthttp\static /E
robocopy toasthttp\templates dist\run\toasthttp\templates /E
rename dist\run TOAST

pause