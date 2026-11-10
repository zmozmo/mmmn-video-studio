Unicode true
!include "MUI2.nsh"
Name "MMMN Burmese Offline ASR Add-on 0.15.4"
OutFile "..\MMMN-Burmese-ASR-Offline-Addon-0.15.4.exe"
InstallDir "$LOCALAPPDATA\MMMN-Video-Studio-Trial\addons\BurmeseASR"
RequestExecutionLevel user
SetCompressor /SOLID lzma
ShowInstDetails show
ShowUninstDetails show
!define MUI_ABORTWARNING
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_LANGUAGE "English"
Section "Install local CPU model and Python runtime"
 SetOutPath "$INSTDIR"
 File /r "..\dist\mmmn-burmese-asr\*.*"
 SetOutPath "$INSTDIR\model"
 File "..\public-model\model.safetensors"
 File "..\public-model\model.py"
 File "..\public-model\transcribe.py"
 File "..\public-model\vocab.json"
 File "..\public-model\config.json"
 File "..\public-model\cmvn.json"
 File "..\public-model\preprocessor_config.json"
 SetOutPath "$INSTDIR"
 File "..\offline-asr-license-notice-0154.txt"
 WriteUninstaller "$INSTDIR\Uninstall-MMMN-Burmese-ASR.exe"
SectionEnd
Section "Uninstall"
 Delete "$INSTDIR\mmmn-burmese-asr.exe"
 RMDir /r "$INSTDIR\_internal"
 RMDir /r "$INSTDIR\model"
 Delete "$INSTDIR\offline-asr-license-notice-0154.txt"
 Delete "$INSTDIR\Uninstall-MMMN-Burmese-ASR.exe"
 RMDir "$INSTDIR"
 ; Never delete the user's chapters, original audio, photos, or corrected SRT.
SectionEnd
