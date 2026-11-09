# MMMN Video Studio — Windows အတွက် စတင်အသုံးပြုနည်း

**Version:** 0.14.7 · **Windows 11 x64** · **Offline-first** · **Android ကို ခဏရပ်ထားသည်**

> ဒီစာမျက်နှာက အက်ပ်ကို တကယ် install စမ်းသုံးဖို့ အဆင်သင့်ဖြစ်တဲ့အခါ အသုံးပြုရန်ပါ။ ကိုယ်ပိုင် Windows Laptop မှာ ChatGPT က အခုထိ install မလုပ်ထားပါ။

## ၁။ Setup.exe တစ်ဖိုင်တည်းနဲ့ စတင်ခြင်း

[Windows Setup.exe — MMMN Video Studio 0.14.7](https://raw.githubusercontent.com/zmozmo/mmmn-video-studio/windows-binaries-0147/downloads/MMMN-Video-Studio-Setup-0.14.7.exe)

- ဖိုင်အမည် — `MMMN-Video-Studio-Setup-0.14.7.exe`
- အရွယ်အစား — **64,839,519 bytes**
- SHA-256 — `ca8b984722c6da971008a457c3d4b0dc734142edf0858d940f2c1bdb03c2f4cb`
- VS Code၊ CMD၊ Source ZIP၊ Python၊ Node.js၊ Paid AI API **မလိုပါ**။

Windows SmartScreen မှာ **Unknown Publisher** လို့ ပေါ်နိုင်ပါတယ်။ Installer ကို Digital Code Sign မလုပ်ထားသေးတာကြောင့်ပါ။ မသေချာတဲ့ Installer ကို လုံခြုံရေးပိတ်ပြီး အတင်းမဖွင့်ပါနဲ့။ GitHub Release Branch မှာရှိတဲ့ ဖိုင်နဲ့ SHA-256 ကို စစ်ပြီး ယုံကြည်မှသာ ဆက်လုပ်ပါ။

အက်ပ် Version အဟောင်းကို သုံးနေပြီးသားဆိုရင် **အက်ပ်ကို အရင်ပိတ်၊ Setup.exe အသစ်ကို ထပ် Install** လုပ်ပါ။ Data ဖျက်ရန်/Uninstall မလုပ်ပါနဲ့။ GitHub Windows Runner မှာ In-place Upgrade နဲ့ Data Preservation စစ်ပြီးသား ဖြစ်ပေမဲ့ ကိုယ်ပိုင်စက်မှာ မစမ်းရသေးပါ။

## ၂။ ပထမ Video စမ်းထုတ်ရန်

1. မူရင်းဝတ္ထုဖိုင်ကို မပြင်ဘဲ၊ **စမ်းသပ်စာမူ/Project** တစ်ခုကို အက်ပ်ထဲထည့်ပါ။
2. မိမိကိုယ်တိုင်ဖတ်ထားတဲ့ **WAV / MP3 / M4A စတဲ့ အသံဖိုင်** ကို Import လုပ်ပါ။
3. Background ပုံတွေ Import လုပ်ပြီး Chapter ရဲ့ **Storyboard/Scenes** ထဲမှာ အသံနဲ့ပုံ အချိန်ကိုက်ညှိပါ။
4. Preview ကို ဖွင့်ကြည့်ပြီး ပုံမပြည့်ခြင်း၊ Timing မကိုက်ခြင်း၊ Audio မပြည့်ခြင်း မရှိကြောင်း စစ်ပါ။
5. **MP4 Export → Platform Preset** မှာ YouTube၊ TikTok/Shorts၊ Facebook သို့မဟုတ် Square ရွေးပါ။ **Render Current Chapter** ကို နှိပ်ပါ။
6. ပြီးသွားရင် **Show saved MP4 files** သို့မဟုတ် **Open MP4 Folder** ကနေ Local MP4 ကို စစ်ပါ။

Video ကို Internet မတက်ဘဲ Bundled FFmpeg ဖြင့် Render လုပ်ပါတယ်။ Export လုပ်နေစဉ် Cancel လုပ်လို့ရပါတယ်။ အရင်ထုတ်ထားတဲ့ MP4 တွေကို မဖျက်သင့်ပါ။

## ၃။ YouTube / TikTok / Facebook

| အသုံးပြုမည့်နေရာ | Video ပုံစံ | အရွယ်အစား |
| --- | --- | --- |
| YouTube ရှည် Video | 16:9 | 1920 × 1080 |
| TikTok / YouTube Shorts / Reels | 9:16 | 1080 × 1920 |
| Facebook | 4:5 | 1080 × 1350 |
| Square Video | 1:1 | 1080 × 1080 |

Video Encoding **H.264**, Audio **AAC**, **30 fps** ဖြစ်ပါတယ်။ Platform Preset လေးမျိုးစလုံး Full-quality MP4 ထုတ်နိုင်ကြောင်း GitHub Windows Runner မှာ စမ်းထားပါတယ်။

## ဝတ္ထုတစ်ပုဒ်အတွက် Video ကြာချိန်

အသုံးပြုမည့် ဝတ္ထုတစ်ပုဒ်၏ **ဖတ်ပြချိန်က အများဆုံး ၁ နာရီ ၃၀ မိနစ် (၉၀ မိနစ်)** ဖြစ်ပါတယ်။ ထို့ကြောင့် ၆–၈ နာရီစာဝတ္ထု Video ကို အဓိကလိုအပ်ချက်အဖြစ် မသတ်မှတ်ပါ။

- **အဓိကပန်းတိုင်:** ၉၀ မိနစ်စာ 1920×1080 H.264/AAC MP4 (30 fps၊ 162,000 frames)။
- **အပိုခံနိုင်ရည်:** Intro/Outro နဲ့ အချိန်ပိုအတွက် ၂ နာရီအထိ Full HD MP4 ထုတ်စမ်းပြီး **216,000 frames PASS** ဖြစ်ပါတယ်။
- ဝတ္ထုတစ်ပုဒ်ကို MP4 **တစ်ခုတည်း** ထုတ်နိုင်ဖို့ ဦးစားပေးပြီး အခန်းလိုက်ထုတ်/ပြန်ပေါင်းတာကို ရွေးချယ်စရာအဖြစ် ထားပါမယ်။
- **လက်ရှိ အတည်ပြုပြီးသားအဆင့်:** ဝတ္ထုတစ်ပုဒ်စာ **၉၀ မိနစ် Full HD MP4 တစ်ဖိုင်တည်း**၊ 162,000 frames — [Windows 0.14.5 QA PASS](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42499519584)။
- **၉၀ မိနစ်နဲ့ ၁၂၀ မိနစ် Full HD MP4 စမ်းသပ်မှု နှစ်ခုလုံး PASS ဖြစ်ပါပြီ။** ၁၅ မိနစ်ကြာ Storyboard ပုံ ၆၀ ပုံ၊ Cross-dissolve ၅၉ ခု စမ်းသပ်မှုလည်း PASS ဖြစ်ပါတယ်။ [ပုံ ၆၀ ပုံ စမ်းသပ်မှု အထောက်အထား](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42499523807)။ ကိုယ်ပိုင် Laptop ပေါ်မှာတော့ မစမ်းရသေးပါ။

## ၄။ ပုံအများကြီး မလျှောက်ပြောင်းဘဲ အရေးကြီး Scene မှသာ ပြောင်းနည်း (အသစ်)

Windows 0.14.7 မှာ **“🎬 အရေးကြီး Scene မှသာ ပုံပြောင်း (Auto Draft)”** ဆိုတဲ့ ခလုတ်ကို Timeline / Storyboard မှာ ထည့်ထားပါတယ်။

1. ဝတ္ထုစာသား၊ ကိုယ်တိုင်ဖတ်ထားတဲ့ အသံနဲ့ ဇာတ်ဝင်ခန်းပုံတွေကို App ထဲ Import လုပ်ထားပါ။
2. ရှိရင် **အချိန်မှတ်တမ်းပါတဲ့ SRT** ကို Import လုပ်ပြီး စာသားနဲ့ အချိန်ကို စစ်ပါ။ SRT မရှိရင် App က Offline Audio Pause ကို ခန့်မှန်းသုံးနိုင်ပေမယ့် စကားလုံးတစ်လုံးချင်း အချိန်အတိအကျမဟုတ်ပါ။
3. “🎬 အရေးကြီး Scene မှသာ ပုံပြောင်း” ကိုနှိပ်ပြီး အကြံပြုချက်ကို Review လုပ်ပါ။
4. **သာမန်မိုးရွာခြင်း၊ မိန်းကလေးတစ်ယောက် ပေါ်လာခြင်း၊ စကားပြောခြင်း** အတွက် ပုံမပြောင်းဘဲ မူရင်းပုံကို ဆက်ထားပါမယ်။ **မိုးသည်းပြီး မှောင်မိုက်သွားခြင်း၊ နေရာအဓိကပြောင်းခြင်း၊ လျှို့ဝှက်ချက်အရေးကြီးပေါ်လာခြင်း** တို့လို အပြောင်းအလဲကြီးမှသာ ပုံအသစ် အကြံပြုပါမယ်။
5. Preview မှာ အသံနဲ့ ပုံပြောင်းချိန်ကို ကိုယ်တိုင်စစ်ပြီး မကြိုက်ရင် Replace / Lock / Timing ပြင်ပါ။ အတည်ပြုပြီးသား ပုံနဲ့ Manual Lock ကို Draft က မဖျက်ပါ။
6. ပုံတစ်ပုံကို ၉၀ မိနစ်လုံးထားလည်း ခွင့်ပြုပါတယ်။ Video Renderer အတွက် နောက်ကွယ်မှာ အပိုင်းခွဲပေမယ့် **မြင်ရတဲ့နောက်ခံပုံမပြောင်းပါ**။

**အရေးကြီး:** ဒီစနစ်က Offline စည်းမျဉ်းနဲ့ လက်ရှိ စာသား/SRT/အသံရပ်နားချက်ကို အခြေခံတဲ့ အကြံပြု Draft ပါ။ ဝတ္ထုအသံကို AI က အဓိပ္ပာယ်အပြည့် နားလည်တယ်လို့ မဆိုလိုပါ။ Offline Myanmar Speech-to-Text အတွက် ကိုက်ညီတဲ့ Model သီးခြားရှိဖို့ လိုနိုင်ပြီး စာသား/Timing ကို ပြန်စစ်ရပါမယ်။ **ပုံတွေကို သူ့ဖာသာမဖန်တီးပါ၊ Google Drive ကနေလည်း Auto Sync မလုပ်ပါ။**

## ၅။ 0.14.7 — ပုံလိုအပ်ချက်ကို အရေးကြီး Scene အတွက်သာ ထုတ်ခြင်း

အရင်ဆုံး Timeline မှာ **“🎬 အရေးကြီး Scene မှသာ ပုံပြောင်း”** ကို နှိပ်ပြီး အကြံပြု Scene တွေကို ပြန်စစ်/အတည်ပြုထားပါ။

**“🖼 အရေးကြီး Scene ပုံလိုအပ်ချက်သာ ထုတ်ရန်”** ခလုတ်ကိုနှိပ်ရင် Chapter အတွက် အဓိကပြောင်းသင့်တဲ့ နောက်ခံပုံတွေကိုသာ Markdown စာရင်းထုတ်ပေးပါမယ်။ ပုံရှိပြီးသား၊ ပုံလိုသေးတာ၊ အသံထဲမှာ ဘယ်အချိန်ကစပြဖို့ အကြံပြုထားတယ်ဆိုတာတွေ ပါပါတယ်။ ၉၀ မိနစ်လုံး ပုံတစ်ပုံတည်းထားရင် ပုံအသစ် အများကြီးဖန်တီးဖို့ မတောင်းပါ။

**“🎧 အသံဖတ်ပြချက်နဲ့ အရေးကြီး Scene (Offline Model ရှိမှ)”** ကိုလည်း သုံးနိုင်ပါတယ်။ စက်ထဲမှာ *whisper.cpp executable* နဲ့ *Myanmar ဘာသာပါသော multilingual model* ကို သီးခြားထည့်ထားမှသာ အသံကို Offline SRT အဖြစ် ပြောင်းနိုင်ပါတယ်။ **ဒီ Model ကို Installer ထဲ မထည့်ထားသေးပါ။** Model မရှိတဲ့အခါ အသံရပ်နားချက်အလိုက် ခန့်မှန်းချက်ကိုပဲ သုံးမယ်။ SRT စာသားနဲ့ ပုံပြောင်းချိန်ကို လူကိုယ်တိုင်ပြန်စစ်ဖို့ လိုပါတယ်။

ပုံလိုအပ်ချက် Markdown ဖိုင်မှာ မထုတ်ဝေသေးတဲ့ ဝတ္ထုစာသားတွေ ပါနိုင်တာကြောင့် **ကိုယ်ပိုင်စက်ထဲမှာပဲ သိမ်းပါ။** App က ပုံအသစ်ကို ကိုယ်တိုင် မဖန်တီးသေးသလို Google Drive ကနေလည်း Auto Download မလုပ်ပါ။

## ၆။ ဝတ္ထုအခန်းတွေ ပေါင်းရန်

Chapter MP4 နှစ်ခု သို့မဟုတ် ထို့ထက်ပိုပြီး ထုတ်ပြီးရင် **Combine Selected Chapters to One MP4** ကို သုံးနိုင်ပါတယ်။ Chapter တွေဟာ Resolution၊ FPS၊ Codec တူရမယ်၊ အခန်းစဉ်လိုက်ဖြစ်ရမယ်။ မူရင်း Chapter MP4 တွေကို ဖျက်မပစ်ပါ။

## ၇။ မဖြစ်မနေ Backup ယူရန်

1. **Updates / Storage** မှာ **Create + Verify Full Backup** ကိုနှိပ်ပါ။
2. **Open Backup Folder** နဲ့ Windows Explorer ဖွင့်ပါ။
3. `snapshot-...` Folder **တစ်ခုလုံး** ကို USB / External Drive ထဲ Copy ကူးပါ။ Folder ထဲက `manifest.json`, `project-state.json`, `media/` ကို အတူတူထားပါ။
4. မူရင်းစက်မှာ Verify လုပ်လို့ရတာနဲ့ USB ထဲ ကူးထားတဲ့ဖိုင် အကုန်ကောင်းတယ်လို့ မယူဆပါနဲ့။ ကူးထားတဲ့ဖိုင်အားလုံးနဲ့ အရွယ်အစား/Hash ကို သီးခြား ပြန်စစ်သင့်ပါတယ်။
5. နောက်မှ Recovery လိုတဲ့အခါ Snapshot Folder ကို Project ရဲ့ Snapshots Folder ထဲ ပြန်ထားပြီး **Verify SHA-256** အောင်မှ **Restore Verified Backup** လုပ်ပါ။

**သတိ:** App ရဲ့ Local Disk တစ်ခုထဲမှာပဲ Backup သိမ်းထားရင် Hard Disk ပျက်တာကို မကာကွယ်နိုင်ပါ။

## ၈။ မပါသေးတာ / ကန့်သတ်ချက်များ

- Google Drive ကို အလိုအလျောက် ချိတ်ဆက်/Sync မလုပ်ပါ။ မူရင်းဝတ္ထုကို Drive ပေါ်မှာ ပြောင်းလဲမပေးပါ။
- မြန်မာအသံမှ စာသားပြောင်းရာမှာ Offline Speech Model သီးခြားလိုနိုင်ပြီး အမှားမရှိကြောင်း မအာမခံပါ။
- GitHub Windows Runner မှာ **၉၀ မိနစ်အပြည့် 1920×1080 Full HD MP4** ကို **162,000 frames** စစ်ပြီး PASS ဖြစ်ပါတယ်။ ၅ မိနစ်နဲ့ ၁၅ မိနစ် Test တွေလည်း PASS ဖြစ်ပါတယ်။ [ဝတ္ထု ၉၀/၁၂၀ မိနစ် Windows စမ်းသပ်မှု အထောက်အထား](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42499519584)။ ကိုယ်ပိုင် Laptop မှာတော့ မစမ်းရသေးပါ။
- Installer Digital Signature မရှိသေးပါ။ Windows SmartScreen က Warning ပြနိုင်ပါတယ်။
- ကိုယ်ပိုင်ဝတ္ထုမူရင်း၊ အသံ၊ ဓာတ်ပုံ၊ Password တွေကို Public GitHub Repository ထဲ မတင်ပါနဲ့။

[Release Readiness Report](WINDOWS-RELEASE-READINESS.md) · [Version 0.14.7 Release Notes](WINDOWS-0147-RELEASE-NOTES.md)
