@echo off
setlocal

:: Select Source File
for /f "usebackq delims=" %%i in (`powershell -command "Add-Type -AssemblyName System.Windows.Forms; $ofd = New-Object System.Windows.Forms.OpenFileDialog; $ofd.Title = 'Select SOURCE image file'; $ofd.InitialDirectory = [Environment]::GetFolderPath('MyPictures'); if ($ofd.ShowDialog() -eq 'OK') { $ofd.FileName }"`) do set "SOURCE=%%i"

if not defined SOURCE (
    echo No source file selected. Exiting.
    exit /b 1
)

:: Select Target File
for /f "usebackq delims=" %%i in (`powershell -command "Add-Type -AssemblyName System.Windows.Forms; $ofd = New-Object System.Windows.Forms.OpenFileDialog; $ofd.Title = 'Select TARGET image file'; $ofd.InitialDirectory = [Environment]::GetFolderPath('MyPictures'); if ($ofd.ShowDialog() -eq 'OK') { $ofd.FileName }"`) do set "TARGET=%%i"

if not defined TARGET (
    echo No target file selected. Exiting.
    exit /b 1
)

echo Copying metadata from:
echo   %SOURCE%
echo to:
echo   %TARGET%
echo.

exiftool -overwrite_original -TagsFromFile "%SOURCE%" "%TARGET%"

if %errorlevel% equ 0 (
    echo Metadata copied successfully.
) else (
    echo Error occurred while copying metadata.
)

endlocal
pause
