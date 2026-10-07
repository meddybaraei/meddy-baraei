# Nova Pro Home YouTube Plan (@NovaProHome)

Two videos a week, ready by 8 AM Eastern:
- **Tuesday: Job of the week.** A vertical Short (under 60s) built from the newest real job photos/clips. If no new photos were added since the last Tuesday, make a Short from the next "Tip" topic below instead.
- **Sunday: Tip / How-to.** A 16:9 how-to (60–90s) answering one real YouTube search, plus a vertical Short cut of the same tip.

## Topic queue (from vidIQ search data, Oct 2026)
Work top to bottom; mark each one done with the date.

| # | Topic / title | Monthly searches | Competition | Status |
|---|---|---|---|---|
| 1 | How to Wire a Ring Doorbell (Step by Step Install) | ~5,400 | low (19) | ✅ made Oct 7 (`how_to_install_ring_wired_doorbell.mp4`) |
| 2 | Ring Doorbell Not Working? 5 Fixes to Try First | ~5,400 | low (14) | |
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
- No music baked in (the owner adds licensed music in the YouTube app).
- AI-generated footage only with the owner's OK, and it must be labeled "altered or synthetic content" on upload.
- Nothing is uploaded or posted automatically. The owner reviews and uploads.

## Tools
`video/tools/make_video.py` (vertical photo Short) and `video/tools/make_howto.py` (16:9 how-to with steps) render with Pillow + ffmpeg. Copy one, change the scenes/steps, and render to `video/weekly/YYYY-MM-DD_<slug>.mp4`.
