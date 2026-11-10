Unicode true
!include "MUI2.nsh"
Name "MMMN Video Studio 0.15.7 Complete — Offline Burmese AI"
OutFile "..\MMMN-Video-Studio-Complete-0.15.7.exe"
RequestExecutionLevel user
SetCompress off
ShowInstDetails show
!define MUI_ABORTWARNING
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH
!insertmacro MUI_LANGUAGE "English"

Section "Install Video Studio and Offline Burmese Speech Pack"
  ; The only payloads are TWO exact, independently QA-verified unsigned setup EXEs.
  ; All installed files are local. No network, model downloads or paid APIs.
  SetOutPath "$TEMP\MMMN-Complete-0157"
  SetOverwrite on
  File /oname=Studio-Setup.exe "..\payloads\MMMN-Video-Studio-Setup-0.15.7.exe"
  File /oname=Burmese-Addon.exe "..\payloads\MMMN-Burmese-ASR-Offline-Addon-0.15.4.exe"

  DetailPrint "Installing native Windows Video Studio..."
  ExecWait '"$TEMP\MMMN-Complete-0157\Studio-Setup.exe" /S' $0
  StrCmp $0 0 model_start
  MessageBox MB_ICONSTOP "Video Studio setup failed. Burmese add-on was not installed."
  Abort

model_start:
  IfFileExists "$LOCALAPPDATA\Programs\MMMN Video Studio\MMMN-Video-Studio.exe" model_install
  MessageBox MB_ICONSTOP "Video Studio did not install correctly. Burmese add-on was not installed."
  Abort

model_install:
  DetailPrint "Installing optional local Burmese CPU model pack..."
  ExecWait '"$TEMP\MMMN-Complete-0157\Burmese-Addon.exe" /S' $1
  StrCmp $1 0 verify
  MessageBox MB_ICONSTOP "Burmese offline model pack installation failed. Studio remains installed."
  Abort

verify:
  IfFileExists "$LOCALAPPDATA\MMMN-Video-Studio-Trial\addons\BurmeseASR\mmmn-burmese-asr.exe" verify_weights
  MessageBox MB_ICONSTOP "Offline Burmese speech runtime is missing."
  Abort

verify_weights:
  IfFileExists "$LOCALAPPDATA\MMMN-Video-Studio-Trial\addons\BurmeseASR\model\model.safetensors" success
  MessageBox MB_ICONSTOP "Offline Burmese model files are missing."
  Abort

success:
  Delete "$TEMP\MMMN-Complete-0157\Studio-Setup.exe"
  Delete "$TEMP\MMMN-Complete-0157\Burmese-Addon.exe"
  RMDir "$TEMP\MMMN-Complete-0157"
  DetailPrint "Both Windows Studio and Burmese Offline Speech Model installed."
SectionEnd
