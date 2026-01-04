@echo off
echo Dang quet toan bo du an...

:: 1. Chay script gom code (Lenh Python)
python export_code.py

:: 2. Lay cay thu muc (Lenh Tree)
tree /f /a > structure.txt

echo ------------------------------------------------
echo XONG ROI!
echo Hai file "full_project_context.txt" va "structure.txt" da duoc cap nhat.
echo ------------------------------------------------
pause