@echo off
rem Builds yakorya_investor.pdf with Microsoft Edge (headless).
rem 1) img\bruegel_winter.jpg  - downloaded from Wikimedia Commons if missing
rem 2) shots\01_hero.png       - screenshot of the demo report if missing
rem 3) yakorya_investor.pdf    - printed from index.html
cd /d "%~dp0"
set "EDGE=%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe"
if not exist "%EDGE%" set "EDGE=%ProgramFiles%\Microsoft\Edge\Application\msedge.exe"
if not exist "%EDGE%" (echo Edge not found & exit /b 1)
set "UD=%TEMP%\deck_edge_profile"
set "REPORT=https://5.181.156.100.sslip.io/neuro/demo/r/brain-report-vladimir-9f7b21.html"

if not exist "img\bruegel_winter.jpg" python get_bruegel.py

if not exist "shots\01_hero.png" (
  echo Screenshot of the report, wait ~20 s...
  "%EDGE%" --headless=new --user-data-dir="%UD%" --hide-scrollbars --force-device-scale-factor=2 --window-size=1440,810 --virtual-time-budget=15000 --screenshot="%~dp0shots\01_hero.png" "%REPORT%"
)

echo Printing PDF...
"%EDGE%" --headless=new --user-data-dir="%UD%" --no-pdf-header-footer --print-to-pdf="%~dp0yakorya_investor.pdf" "%~dp0index.html"
echo Done: %~dp0yakorya_investor.pdf
start "" "%~dp0yakorya_investor.pdf"
