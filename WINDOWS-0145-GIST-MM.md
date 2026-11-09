# MMMN Video Studio — အတိုချုပ် Gist (Windows 0.14.5)

**အဓိကရည်ရွယ်ချက်:** ကိုယ်တိုင်ဖတ်ထားတဲ့ မြန်မာဝတ္ထုအသံနဲ့ နောက်ခံပုံတွေကို ပေါင်းပြီး **Internet / Paid API မလိုဘဲ Windows ပေါ်မှာ MP4 Video ထုတ်ရန်**။

## လက်ရှိပြီးထားတာ
- **Windows 11 x64 Setup.exe** (Version **0.14.5**) — ZIP၊ VS Code၊ Python၊ CMD မလိုဘဲ Install လုပ်နိုင်ရန်။
- ဝတ္ထုစာသား၊ အသံဖိုင်၊ နောက်ခံပုံ၊ Scene အချိန်ချိန်ညှိခြင်းနဲ့ Manual Scene Edit။
- **YouTube (16:9)**၊ **TikTok/Shorts (9:16)**၊ **Facebook (4:5)** နဲ့ **Square (1:1)** အတွက် H.264/AAC MP4 ထုတ်ခြင်း။
- Video Export **Cancel/Retry**၊ Chapter MP4 ပေါင်းခြင်း၊ Project **Save/Backup/Restore**၊ File SHA-256 စစ်ခြင်းနဲ့ Update လုပ်ရာမှာ Data မပျက်စီးရေး။
- **0.14.5 Fix:** 0.14.4 မှာ ၉၀/၁၂၀ မိနစ် Video ပြီးခါနီး FFprobe ၁၈၀ စက္ကန့် Timeout ဖြစ်ခဲ့တာကို ပြင်ထားပြီး Frame အပြည့်စစ်ဆေးမှုကို ဆက်ထိန်းထားပါတယ်။

## GitHub Windows Runner မှာ တကယ်စမ်းပြီး PASS
| Test | Result |
| --- | --- |
| Windows Build → Install → Upgrade → Backup/Security/UI | **PASS** |
| **၉၀ မိနစ် Full HD MP4** — 1920×1080 / 162,000 frames | **PASS** |
| **၁၂၀ မိနစ် Full HD MP4** — 216,000 frames | **PASS** |
| ပုံ **၆၀ ပုံ**၊ Dissolve **၅၉ ခု**၊ ၁၅ မိနစ် Full HD MP4 | **PASS** |
| မူရင်းအသံ/Backup/ထုတ်ပြီးသား MP4 မပျက်ခြင်း | **PASS** |

[၉၀/၁၂၀ မိနစ် Test](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42499519584) · [ပုံ ၆၀ ပုံ Test](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42499523807) · [Independent Installer QA](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42499308041)

## Setup ဖိုင်
[**MMMN-Video-Studio-Setup-0.14.5.exe**](https://raw.githubusercontent.com/zmozmo/mmmn-video-studio/windows-binaries-0145/downloads/MMMN-Video-Studio-Setup-0.14.5.exe) — 64.8 MB ခန့်။

## ကျန်သေးတာ
- **ကိုယ်ပိုင် Windows 11 Laptop** ပေါ်မှာ Install/အမှန်တကယ် ဝတ္ထုအသံနဲ့ Video Render ကို **မစမ်းရသေး**။
- Installer က **Code-signed မဟုတ်သေး** — Windows SmartScreen Warning ဖြစ်နိုင်တယ်။
- **Android ကို ခဏရပ်ထား**။ Google Drive Auto-sync မပါသေး။
- အထက်ပါ PASS တွေက GitHub Runner ပေါ်မှာ **စမ်းသပ်ဖန်တီးထားတဲ့ Media** နဲ့ ပြုလုပ်ထားတာဖြစ်ပြီး ကိုယ်ပိုင် Laptop Hardware အတွက် အာမခံချက်မဟုတ်။

**လက်ရှိဆုံးဖြတ်ချက်:** Windows 0.14.5 ကို **ပထမဆုံး Laptop အစစ်ပေါ် လက်တွေ့စမ်းသပ်ရန် အသင့်**။ 0.14.4 အစား 0.14.5 ကို သုံးရန်။

[မြန်မာလို အသုံးပြုနည်း](WINDOWS-QUICKSTART-MM.md) · [Release Notes](WINDOWS-0145-RELEASE-NOTES.md)
