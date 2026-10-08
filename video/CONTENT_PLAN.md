# Nova Pro Home YouTube Plan (@NovaProHome)

Two videos a week, posted at 4:00 PM Eastern (Claude picked these from Metricool audience data; Wed/Thu/Tue 4 PM are the strongest slots, weekends the weakest):
- **Monday: Job of the week.** A vertical Short (under 60s) built from the newest real job photos/clips. If no new photos were added since the last Monday, make a Short from the next "Tip" topic below instead.
- **Thursday: Tip / How-to.** A 16:9 how-to (60–90s) answering one real YouTube search, plus a vertical Short cut of the same tip (Short posted 4:30 PM).

## Topic queue (from vidIQ search data, Oct 2026)
Work top to bottom; mark each one done with the date.

| # | Topic / title | Monthly searches | Competition | Status |
|---|---|---|---|---|
| 1 | How to Wire a Ring Doorbell (Step by Step Install) | ~5,400 | low (19) | ✅ posted Oct 7 |
| 2 | Ring Doorbell Not Working? 5 Fixes to Try First (long version; a 3-check Short was posted Oct 7) | ~5,400 | low (14) | ✅ Oct 8 (video + Short, music only) |
| 3 | How to Make Your Ring Doorbell More Sensitive to Motion | ~5,300 | very low (12) | |
| 4 | How to Hook Up a Ring Solar Panel (use McLean solar photos) | ~5,300 | low (16) | |
| 5 | How to Reset Your Ring Doorbell | ~5,300 | low (16) | |
| 6 | How to Install a Ring Doorbell Without Drilling | ~5,400 | low (20) | |
| 7 | Do You Need a C-Wire for a Nest Thermostat? | check in vidIQ | | |
| 8 | How to Install a Nest Thermostat | check in vidIQ | | |

## Rules for every video
- Use only Nova Pro Home's own photos/clips (`facebook-post/`, `video/`, or the Drive "Video Inbox" folder) plus simple drawn diagrams. Never use Ring or Google logos as artwork.
- Blur house numbers, license plates and customers' faces before using any photo.
- Keep steps general and correct: check them against Ring's or Google's official help pages, and always tell viewers to follow the instructions in their box. Add a safety note for anything involving wiring or the breaker.
- End every video with the Nova Pro Home end card (novaprohome.com · (571) 241-9569 · Ring Authorized Dealer · Google Nest Pro).
- Audio: AI voiceover (vidIQ voice "Eric") when credits allow, plus the original background music from `video/tools/make_music.py` (royalty-free). Never use copyrighted music.
- AI-generated footage only with the owner's OK, and it must be labeled "altered or synthetic content" on upload.
- **Posting (owner's standing instruction, Oct 7 2026):** Claude acts as the owner's agent for YouTube: creates, schedules and posts directly through Metricool (brand 6916320, YouTube channel @NovaProHome) without asking first. Publish at **4:00 PM ET** Monday & Thursday (Claude chose the days/times at the owner's request). Always: public, not made for kids, category HOWTO_STYLE, `isAiGeneratedContent: true` whenever the video has an AI voice or AI footage. After each post, send the owner a short summary (title, time, planner link).
- Paid AI credits (vidIQ voiceover / AI video): use only when the vidIQ balance stays above 20 credits after the job; otherwise make the video without voiceover (music only) and say so.
- **Metricool plan limit:** on Oct 7 the 11th post failed with "You have reached your Metricool account limit." Before scheduling, check getScheduledPosts for ERROR statuses; if a post hits the limit, tell the owner right away (he can upgrade Metricool or upload that video in YouTube Studio). The AI installer Short (video/ai_installer_clip.mp4) is still unposted.
- Facebook is not part of the standing instruction; cross-post there only when the owner asks.

## Tools
`video/tools/make_tips.py CONFIG.json OUT` (text-led tip video + vertical Short from a JSON config, see video/weekly/*.json), `video/tools/make_video.py` (vertical photo Short) and `video/tools/make_howto.py` (16:9 how-to with steps) render with Pillow + ffmpeg. Copy one, change the scenes/steps, and render to `video/weekly/YYYY-MM-DD_<slug>.mp4`.

## Posted Oct 7, 2026 (YouTube)
Intro, Ring doorbell how-to, 7 topic Shorts (cameras placement, battery vs wired, solar, not working 3 checks, Nest compatibility, Airbnb smart locks, why hire a pro), promo Short, AI installer Short. Don't repeat these topics as-is.

## Smart Home Starter Series (made Oct 8, 2026; music only)
Owner asked for a "why automate your home first" video plus one video per product, using real photos. Files are in `video/series/` (configs + `video/tools/make_series.py`). All scheduled on YouTube via Metricool:
- Fri Oct 9, 4:00 PM: Why Make Your Home Smart? Start With Automation First (16:9). 4:30 PM: Short version.
- Daily at 12:00 PM, Oct 10 to Oct 19: product Shorts 1–10 (Ring Video Doorbell, Smart Lock, Nest Learning Thermostat, Ring Floodlight Cam, Ring Spotlight Cam, Ring Solar Panel, Ring Stick Up Cam, Ring Alarm, Google Nest Cam, Nest Cam with Floodlight).
- Smart Lock (Oct 11) and Nest Thermostat (Oct 12) use drawn product art because there are no install photos yet. If the owner sends photos before then, re-render and swap the media with updateScheduledPost.
