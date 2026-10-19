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
| 3 | How to Make Your Ring Doorbell More Sensitive to Motion | ~5,300 | very low (12) | moved to Thu Oct 29 |
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
- Oct 8 update: owner sent install photos + ring.com product screenshots (saved, faces/stickers blurred, in `video/series/photos/`). Re-rendered #1, #4, #7, #8 and swapped them in Metricool; added bonus Short "Ring Elite 180 4K" on Tue Oct 20, 12:00 PM.
- Owner also sent two 10s AI (Gemini) promo videos; not posted yet. If posted, set isAiGeneratedContent true. The first shows a Ring logo on a thermostat (no such product), so don't use it as is.
- Oct 9: owner sent a real ecobee heat-pump job (Vienna). Made Monday's Job of the Week Short `video/weekly/2026-10-12_job-ecobee-heat-pump.mp4` (Mon Oct 12, 4:00 PM). Swapped the last scene of series #3 (Nest thermostat) for the real wiring photo. Never show the customer's name (the Amazon screenshot had it; only the product crop is used).

## Local SEO rule (owner, Oct 9 2026)
Every YouTube and Facebook video targets the home-base area only:
- Title names a city ("... Installation in Sterling & Ashburn, VA"; use the real job city when known, e.g. Vienna, McLean).
- First line of the description names the service + cities. Say "based in Sterling, VA".
- Add the 📍 Serving line (Sterling, Ashburn, Herndon, Reston, Chantilly, South Riding, Leesburg, Vienna, McLean, Fairfax, Arlington) and ZIPs 20164 · 20165 · 20166 · 20147 · 20148 · 20170 · 20190 · 20151 · 20152 · 20175 · 22180 · 22101 · 22030.
- Tags: "<service> installation sterling va", "<service> installer ashburn va", "... northern virginia", "loudoun county".
- Hashtags: #SterlingVA #AshburnVA #LoudounCounty #NorthernVirginia (+ #ViennaVA / #McLeanVA for jobs there).
Organic YouTube/Facebook reach can't be locked to ZIP codes; only paid boosts/ads can.
All 14 pending YouTube posts and the Oct 10 Facebook video were rewritten this way on Oct 9.
- Oct 10: owner sent a Ring Alarm Pro job (14-piece kit + 2 extra sensors, "Chantilly" from voice note). Made `video/weekly/2026-10-13_job-ring-alarm-pro-chantilly.mp4` (Tue Oct 13, 4 PM) and re-rendered series #8 Ring Alarm with the real install photos. Wi-Fi network name on the phone screen is blurred.
- Oct 10: owner asked for the Chantilly job on Facebook too (Reel, Tue Oct 13 6:30 PM) and a reference how-to "How to Install a Ring Alarm Pro 14-Piece Kit" from the same photos: YouTube video Thu Oct 15 4:00 PM + Short 4:30 PM, Facebook video Thu Oct 15 6:30 PM. This takes the Oct 15 Thursday tip slot; topic #3 (motion sensitivity) moves to Oct 22.

## Review series: "Worth Buying? (Installer's Review)" (owner, Oct 10 2026)
Owner shared two reference videos (techmania "Ring Doorbell 4K Elite Review – Worth Buying?", Pixel Review "Ring Elite Wired Doorbell Review"): 4–6 min product reviews, feature-by-feature chapters with specs, verdict, shop links. Our version: 16:9 + Short, one product each, chapters (features → power/install → app & subscription → pros/cons → verdict), owner's install photos, ends with "Want it installed?". Music only for now (owner's choice, Oct 10). Only put specs on screen that are confirmed (ring.com is blocked from the agent; use the owner's screenshots or ask).
- #1 Ring Wired Doorbell 4K Pro: `video/reviews/ring-wired-doorbell-4k-pro-review(.mp4|_short.mp4)`, YouTube Tue Oct 20 4:00 PM (video) + 4:30 PM (Short).
- #2 Ring Alarm Pro: `video/reviews/ring-alarm-pro-review(.mp4|_short.mp4)`, YouTube Tue Oct 27 4:00 PM (video) + 4:30 PM (Short). Owner asked (Oct 11) for a totally different look from the earlier videos: review series uses `"theme": "warm"` in make_series.py (cream background, white panels, orange accent). https://link.amazon/B0fNtx7iN is the owner's Amazon AFFILIATE link for the Ring Battery Doorbell (confirmed Oct 11), not the Alarm Pro.

## Giveaway (Oct 11 – Nov 11, 2026)
Ring Battery Doorbell Pro + install. Rules: `video/GIVEAWAY_RULES.md` (public link until novaprohome.com/giveaway is live: https://github.com/meddybaraei/meddy-baraei/blob/facebook-ring-nest-post/video/GIVEAWAY_RULES.md). Entry = comment your city; never ask for likes/subscribes as entry. Guaranteed final drawing within 7 days after Nov 11 + bonus drawing per 1,000-subscriber milestone. Every new YouTube post until Nov 11 gets the giveaway block in its description. Announcement Short: `video/giveaway/2026-10-11_giveaway-announcement_short.mp4`, Oct 11 5:00 PM.

## Affiliate links
- Ring Battery Doorbell (Amazon affiliate, owner earns commission): https://link.amazon/B0fNtx7iN
- Schlage Encode Smart WiFi Deadbolt, Camelot trim, Aged Bronze (Amazon affiliate, owner Oct 16): https://link.amazon/B0aLPKozm
- Every post using an affiliate link must say so next to it: "Affiliate link: as an Amazon Associate, Nova Pro Home earns from qualifying purchases."
- Only use it where a battery doorbell fits; never in giveaway posts (no purchase necessary).
- Owner's standard doorbell install price: $100. Giveaway ARV $329.99. Owner can't edit novaprohome.com, so rules stay on the GitHub link.
- Giveaway area (owner, Oct 11, revised): Virginia homes within 20 miles of the office in Sterling 20165 (Sterling, Ashburn, Leesburg, Herndon, Reston, Chantilly, South Riding, Centreville, Fairfax, Vienna, McLean). Owner wants subscribers: encourage subscribing ("subscribe to see the winner reveal") but never make it a condition of entry (YouTube fake-engagement policy).

## Approval rule (owner, Oct 11)
Before scheduling or changing any post, show the owner the video + title + description and wait for "go". Posts already approved can publish as scheduled.

## TikTok (connected Oct 11, @NovaProHome via Metricool)
- Owner rule (Oct 11): EVERY post on every platform includes a link to the website (default https://novaprohome.com/contact). TikTok captions aren't clickable, so write "novaprohome.com/contact (link in bio)".
- Metricool TikTok posts need tiktokData.title. Post Shorts there at ~6 PM ET (weekend noon), commercialContentOwnBrand true, isAigc false.
- Scheduled: Oct 12 alarm job, Oct 15 how-to, Oct 17 ecobee, Oct 20 doorbell review, Oct 27 alarm review.
- Giveaway is NOT on TikTok (rules only count YouTube/Facebook comments).
- TikTok style (owner approved Oct 11): Gen Z cut via `video/tools/make_tiktok.py` — POV/question hook on frame 1, 4-beat punch-zoom cuts at 140 bpm, bold Inter Black captions with yellow keywords, original phonk beat (music "phonk"), 14–18 s, CTA card "link in bio". Configs in `video/tiktok/`. Captions start with the hook; add #SmartHome #FirstHome. Business accounts can't use copyrighted chart songs (only TikTok Commercial Music Library).

## Brand name (owner, Oct 12) — ALWAYS "NovaProHome" (one word). Never "Nova Pro Home". Use the real logo (youtube-branding/logo_full_white_bg.png / Drive "LOGO.png"), never a re-drawn version.

## Logo + tools (owner, Oct 12)
- Logo confirmed: youtube-branding/logo_full_white_bg.png (= video/tools/logo.png) is the real logo. Use it unchanged.
- Mix production tools: make some videos with Adobe Express and some with Canva (plus our own cuts). Owner prefers the CANVA style (Oct 12) — default to Canva. Still show each one for "go" before scheduling.
- Backyard deck Ring cams job (Oct 2026) was in Arlington, VA.

## YouTube monetization goal (owner, Oct 12)
- Goal: get into the YouTube Partner Program. Status Oct 12: 1 subscriber, ~1.3K views (mostly Shorts).
- Targets: 500 subs + 3,000 public watch hours (12 mo) for fan-funding tier; 1,000 subs + 4,000 watch hours for ad revenue. (Shorts path: 3M / 10M Shorts views in 90 days — unrealistic for now.)
- Strategy: more long-form (6-10 min reviews/how-tos) for watch hours; every Short points to a long video (related video link); subscribe CTA; track subs + watch hours in the Monday report. Owner applies himself in YouTube Studio > Earn once eligible.

## Weekly review — Oct 5–11, 2026
- YouTube: 1,531 views (first week live), 1 sub. Best: question/problem Shorts ("No outlet? Ring Solar Panel" 144, "Ring Doorbell not working? 3 things" 121, "Battery vs Wired" 64). Worst: generic promo Short (1 view). 10 uploads in 40 min on Oct 7 diluted reach. Avg view duration 2–25 s → hooks must land in first second.
- TikTok: first video 96 views, 1 like.
- Facebook: 423 media views (vs 62), followers 9 (+2); 2 posts same day = 0 impressions; hard-sell CTA posts flop; install album + how-to reel did best.
- LinkedIn: 6 impressions, 1 click.
- Website tracking: Metricool shows 0 visits → pixel likely not installed; no way to measure clicks per post yet.
- vidIQ comments blocked ("Not enough credits"); Metricool shows 0 YouTube comments.
- Trend: problem/question topics > promos. Double down on "X not working? / Which one should I buy?" formats.

## Contact info + reach (owner, Oct 12) — overrides older rules mentioning the phone
- YouTube: NEVER show the phone number (not in video, title, description or comments). Use **Meddy@novaprohome.com** + **https://novaprohome.com/contact** (and https://novaprohome.com). Video end cards now show the email (video/tools/* updated; TikTok, Facebook and LinkedIn may keep the phone number — owner OK, Oct 12).
- Every post must sell locally AND pull views from everywhere: title leads with the general search phrase (e.g. "How to Install a Ring Floodlight Cam") then the city ("| Sterling, VA"); description first line = general benefit, then the local SEO block; tags/hashtags mix general (#RingCamera #SmartHome #HomeSecurity #DIY) with local (#SterlingVA #NorthernVirginia).

## Ecobee humidity fix (owner's field-guide deck, Oct 12) — scheduled after owner's "go"
Real job, Vienna VA (Carrier heat pump + ecobee Premium). Files: video/weekly/2026-10-22_ecobee-humidity-fix(.json|.mp4|_short.mp4), video/tiktok/2026-10-22_ecobee-humidity_tiktok.mp4, video/social/ecobee-humidity/slide-01..12.jpg.
- YouTube Thu Oct 22 4:00 PM (video) + 4:30 PM (Short); TikTok Oct 22 6 PM; Facebook Reel Oct 22 6:30 PM; LinkedIn PDF guide Fri Oct 23 9 AM; Facebook photo set Sat Oct 24 12 PM.
- Took the Oct 22 Thursday tip slot; topic #3 (Ring motion sensitivity) moves to Thu Oct 29.

## Long-form compilations (owner asked Oct 15 for longer YouTube videos; for watch hours)
- `video/long/` configs merge existing configs with chapter cards (`"art": "chapter"` in make_series.py). Covers: *_cover.jpg.
- Sat Oct 17 4 PM: Smart Home Starter Guide, 11 Devices Explained (5:48). Fri Oct 23 4 PM: 5 Real Smart Home Installs in Northern Virginia (4:04).
- YouTube chapters: first at 0:00 and each ≥10 s (fold the short intro into chapter 1).
- Keep making 1 long video per week (aim 6–10 min) alongside Shorts.

## Like & subscribe (owner, Oct 15) — every YouTube video
- End card shows a red "LIKE & SUBSCRIBE · for more smart home tips" badge (make_series.py default; set "subscribe": "" in a config to hide).
- Every YouTube description includes: "👍 Like & subscribe to @NovaProHome for more smart home tips!"
- Subscribing is never a condition of the giveaway entry.

## Weekly review Oct 12–18 (trends)
- YouTube: 4 subscribers (+2 this week). Views on that week's new videos 912 (8 videos) vs 3,238 (18 videos) the week before; fewer uploads = fewer views. Shorts feed (2,635) and YouTube search (1,602) are the main traffic sources, so "<Product> Installation in <City>, VA" titles keep working.
- Top: Ring Alarm Pro Installation in Chantilly #shorts (303 views), Ring Solar Panel McLean #shorts (132), Ring Floodlight Cam Sterling #shorts (124). Real-job install Shorts win; long how-to (Ring Alarm Pro step by step) got 5 views.
- Facebook: photo posts get 1–2 impressions; Reels get ~27 views each. Prefer Reels.
- LinkedIn: 2 followers, ~2 impressions/week. Needs followers before content matters.
- TikTok: 7 videos, 559 views (up from 142). Ring Alarm explainer and ecobee "7 wires" POV best (109 each).
- Giveaway: 0 comment entries on the giveaway Short so far (Metricool count).
- vidIQ out of credits until Nov 7 (no comment text / CTR). No website-traffic data: UTM links + Metricool pixel still missing.

## Reolink affiliate link (pending)
- Meddy will send a Reolink affiliate link. When it arrives: add it (caption link + QR scene, like the Schlage one) to the Reolink "which camera fits your property" Short/carousel and future Reolink posts on all platforms, with the disclosure "Affiliate link: NovaProHome earns a commission from qualifying purchases." No giveaway block on posts carrying it. Hold Reolink posts until the link arrives (or Meddy says post without it).

## Role (Oct 19): social media manager
Meddy: "act as my social media manager to promote my business and services, and work on my platforms to get people to use the affiliate links to buy products so we make money."
Two goals, in this order: (1) install bookings via novaprohome.com/contact, (2) affiliate sales (Amazon: Ring Battery Doorbell, Schlage Encode; Reolink via impact.com once approved).
Affiliate funnel rules:
- YouTube Shorts / TikTok captions: links are not clickable. Put the affiliate link on screen as a QR code + "link in bio", and point bios to one "Shop our picks" page (novaprohome.com/picks, Meddy to add) listing every affiliate product.
- Clickable affiliate links live in: long YouTube videos (description + pinned comment), Facebook posts/Reels, LinkedIn posts.
- Every affiliate post carries the disclosure; Amazon: "As an Amazon Associate, NovaProHome earns from qualifying purchases." No giveaway block on posts with affiliate links. Never put Amazon links in emails or printed/offline material (Amazon Associates rule).
- Content mix per week: 4 job/install posts (trust + bookings), 2 product "worth it?" reviews or comparisons with affiliate link, 1 long video (6-10 min, watch hours + clickable links), 1 tip/how-to.

## Approval rule (UPDATED Oct 19): FULL AUTONOMY
Meddy chose "Full autonomy": I create AND schedule posts myself following this plan, and apply weekly improvements myself. No "go" needed. Report what was scheduled/changed (short message) and send the weekly report every Monday. Never delete published posts; Meddy can pull any post. This replaces the older "wait for go" rule above.
- (Oct 19) Meddy's site already has a "Shop by category" section on novaprohome.com (cameras & doorbells, thermostats, lighting, locks, Wi-Fi, EV charging, ...) with his affiliate links. Use novaprohome.com as the "link in bio" shop until Hadi adds a direct /shop link. No separate /picks page.
- Shop URL confirmed: https://novaprohome.com/shop. Use it as the "link in bio" shop and the shop QR target in videos ("Shop the products we install: novaprohome.com/shop").
- (Oct 19) Every video now ends with a "Shop the products we install" QR scene → novaprohome.com/shop (make_series: before the end card, disable with "shop_qr": false; make_tiktok: default QR slide unless the config sets its own "qr"). Product-specific affiliate QR (e.g. Schlage) can be added as an extra "art":"qr" scene.
