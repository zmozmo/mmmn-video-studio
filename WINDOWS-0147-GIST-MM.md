# MMMN Video Studio 0.14.7 — မြန်မာလို Project အတိုချုပ်

**Windows 11 x64 · Offline Video Studio · Android ကို ခဏရပ်ထား**

## ဘာတွေ ထပ်ပြီးသွားလဲ?

**🎬 အရေးကြီး Scene တွေပဲ ပုံပြောင်းတဲ့စနစ်** — သာမန်မိုးရွာတာ၊ မိန်းကလေးတစ်ယောက် ပေါ်လာတာမျိုးမှာ နောက်ခံပုံမပြောင်းဘူး။ နေရာကြီးပြောင်းတာ၊ မိုးသည်းပြီး မှောင်မိုက်သွားတာ၊ အဓိက လျှို့ဝှက်ချက်ပေါ်တာမျိုးမှာမှ အကြံပြုမယ်။ Manual Lock ကို မထိဘူး။

**🖼 အရေးကြီးပုံစာရင်းထုတ်ခြင်း** — ဝတ္ထုတစ်ပုဒ်မှာ လိုအပ်တဲ့ အဓိကနောက်ခံပုံတွေကိုပဲ Markdown ဖိုင်ထုတ်မယ်။ ရှိပြီးသားပုံနဲ့ လိုသေးတဲ့ပုံ ခွဲပြမယ်။ Video အတွင်းပိုင်း နည်းပညာအတွက် ခွဲထားတဲ့ Scene ကို ပုံအသစ်တစ်ပုံ မတွက်ဘူး။

**🎧 Audio-first Auto Draft (ရွေးချယ်နိုင်)** — စက်ထဲမှာ whisper.cpp နဲ့ Multilingual Speech Model သီးခြားရှိရင် ကိုယ်တိုင်ဖတ်ထားတဲ့အသံကနေ Myanmar SRT ကို စက်ထဲမှာပဲ ထုတ်ပြီး Scene Timing အကြံပြုနိုင်တယ်။ Model မရှိရင် Offline Pause Timing ကိုသုံးမယ်။ **Model ကို Installer ထဲ မထည့်ထားသေးပါ**။

## စမ်းသပ်မှု အခြေအနေ

| အပိုင်း | ရလဒ် |
| --- | --- |
| အရေးကြီး Scene / ပုံစာရင်း Unit Tests ၃၃ ခု | **PASS** |
| Windows 0.14.7 Build / In-place Upgrade / Offline MP4 | **PASS** |
| Published Setup.exe ကို Windows Runner အသစ်မှာ Install ပြန်စမ်း | **PASS** |
| Edge မှာ ပုံလိုအပ်ချက်စာရင်း တကယ် Download ထုတ်ခြင်း | **PASS** |
| Audio-first → Synthetic SRT ၄၀ ကြောင်း → Smart Scene → Save/Reload | **PASS (Model အတုဖြင့် Workflow Test)** |
| Windows 0.14.6 — ပုံတစ်ပုံတည်း ၉၀ မိနစ် Full HD, 162,000 Frames | **PASS** |
| Windows 0.14.7 — ပုံတစ်ပုံတည်း ၉၀ မိနစ် Full Encode | **သီးခြား မစမ်းရသေး** |
| Real Myanmar အသံကို Speech Model အစစ်နဲ့ နားလည်နိုင်မှု | **မစမ်းရသေး** |
| ကိုယ်ပိုင် Windows Laptop မှာ အသုံးပြုခြင်း | **မစမ်းရသေး** |

[Windows Native Build](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42595044624) · [Independent Installed Edge](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42595895083) · [ပုံစာရင်း Download](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42596100140) · [Audio-first Mock Test](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42596129789)

## လက်ရှိ Setup.exe

[**MMMN Video Studio Windows 0.14.7**](https://raw.githubusercontent.com/zmozmo/mmmn-video-studio/windows-binaries-0147/downloads/MMMN-Video-Studio-Setup-0.14.7.exe)

- ဖိုင်အရွယ်အစား — 64,839,519 bytes
- SHA-256 — `ca8b984722c6da971008a457c3d4b0dc734142edf0858d940f2c1bdb03c2f4cb`
- Installer **Digital Signature မရှိသေး**။

**အရေးကြီးတဲ့ ကန့်သတ်ချက်:** မြန်မာဝတ္ထုအသံကို AI က အပြည့်အဝ အဓိပ္ပာယ်နားလည်တာ၊ Scene တိုင်းကို စကားလုံးအချိန်အတိအကျ ချိန်ပေးတာ၊ ပုံအသစ်တွေကို Offline အလိုအလျောက်ဖန်တီးတာ၊ Google Drive ထဲက ပုံတွေ Auto Fetch လုပ်တာ **မပြီးသေးပါ**။ ပုံဖိုင်တွေကို အရင် Import လုပ်ထားရပြီး Auto Draft ကို Preview/Review ပြန်စစ်ရပါမယ်။

[မြန်မာလို အသုံးပြုနည်း](WINDOWS-QUICKSTART-MM.md) · [Release Notes](WINDOWS-0147-RELEASE-NOTES.md) · [Release Readiness](WINDOWS-RELEASE-READINESS.md)
