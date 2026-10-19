# NovaProHome social media manager: handoff (as of Mon Oct 19, 2026)

## Who / what
- Owner: Meddy, NovaProHome (one word, always). Smart home, security & EV installer in Sterling, VA. Ring Authorized Dealer + Google Nest Pro. Public email: Meddy@novaprohome.com. Phone: (571) 241-9569.
- My role: Meddy's social media manager with FULL AUTONOMY (chosen Oct 19): create AND schedule posts myself, apply improvements myself, then report. No "go" needed. Never delete published posts. Meddy can pull any post.
- Goals, in order: (1) install bookings via novaprohome.com/contact, (2) affiliate sales via novaprohome.com/shop, (3) YouTube subscribers + monetization (goal: 10 subs; currently 4).

## Where everything lives
- Repo: meddybaraei/meddy-baraei, branch `facebook-ring-nest-post`. Read `video/CONTENT_PLAN.md` FIRST (all rules + history). Commit + push after every render (stop hook wants a clean tree).
- Video tools: `video/tools/` (make_series.py = Shorts/16:9 photo+card videos; make_tiktok.py = Gen Z TikTok cut; make_music.py; logo.png = the real logo, never change it).
  - Every video now auto-adds a "Shop the products we install" QR → novaprohome.com/shop (disable with "shop_qr": false). Extra product QR: scene {"art":"qr","url":...}.
- Media URLs for posting: https://raw.githubusercontent.com/meddybaraei/meddy-baraei/<commit SHA>/<path>
- Scheduling: Metricool MCP, blogId 6916320, timezone America/New_York. Networks: YouTube, Facebook, LinkedIn, TikTok.
  - create/updateScheduledPost need the full payload and ONLY that network's data block (never twitterData/instagramData). Post id changes on update; uuid stays. TikTok needs tiktokData.title. Can't edit published posts.
- Bios text: `website/BIOS.md`. Shop page: https://novaprohome.com/shop (Meddy's site, built by Hadi, hzahedi@prozco.com).

## Content rules (summary; full list in CONTENT_PLAN.md)
- YouTube: NEVER show the phone number (video, title, description, comments). Use Meddy@novaprohome.com + novaprohome.com/contact. TikTok/Facebook/LinkedIn may show the phone.
- Every YouTube video: like & subscribe end-card badge + "👍 Like & subscribe to @NovaProHome for more smart home tips!" + first comment with https://www.youtube.com/@NovaProHome?sub_confirmation=1
- Titles: general search phrase first, then city. 📍 local block + ZIPs + mix of broad and local hashtags.
- Music only, no AI voice. Canva-style look (mix of Canva/Adobe OK), Gen Z style for TikTok.
- Privacy: blur faces, plates, house numbers, Wi-Fi names, lock codes; never show customer names.
- AI footage must be labeled (youtube isAiGeneratedContent true / tiktok isAigc true). Real job photos may be enhanced, never faked.
- Affiliate: always add disclosure. Amazon: "Affiliate link: as an Amazon Associate, NovaProHome earns from qualifying purchases." Ring Battery Doorbell https://link.amazon/B0fNtx7iN · Schlage Encode https://link.amazon/B0aLPKozm. No Amazon links in emails/printed material. Shorts/TikTok caption links aren't clickable → QR on screen + "link in bio" (novaprohome.com/shop).
- Giveaway (Ring Battery Doorbell Pro + install) runs to Nov 11, draw by Nov 18; rules in video/GIVEAWAY_RULES.md. Giveaway block goes on YouTube posts but NOT on posts with affiliate links. Subscribing never required. Entries count only on YouTube/Facebook comments or the contact form (not TikTok).
- UTM links on all website links: ?utm_source=<youtube|facebook|linkedin|social>&utm_medium=social&utm_campaign=<date-slug>. All 66 pending FB/LI/YT posts through Nov 15 are already tagged.
- Weekly mix: 4 job/install posts, 2 product "worth it?" reviews with affiliate links, 1 long YouTube video (6-10 min, watch hours), 1 tip/how-to.

## Scheduled tasks (Claude routines on Meddy's account)
- trig_01DV5goDnLacFxEWNJYxSA3B "Nova Pro Home YouTube: create & post (Mon & Thu)", 9:13 AM ET Mon+Thu.
- trig_01CeroG8rnGBUFx1KQ6giqYA "Nova Pro Home weekly content performance review", Mon 8:41 AM ET.
- Both are bound to the OLD session (session_01NCL7af1hWVs7o3roUBj8CZ). In the new session: recreate both with the same prompts bound to the new session (get_trigger to copy the prompt), then disable the old ones.

## Recently scheduled (all in Metricool)
- Perfume store security job, Reston VA (cameras, NVR, Schlage lock, Wi-Fi, POS): YT Short Mon Oct 19 4:30 PM, TikTok Oct 19 8:30 PM, LinkedIn Thu Oct 22 9 AM, FB Reel Oct 22 6:30 PM (Schlage affiliate QR + link).
- Giveaway push: YT Short Tue Oct 20 7 PM, TikTok Oct 20 8:30 PM, FB Reel Wed Oct 21 12 PM.
- Reolink "Which camera fits your property?": YT Short Sat Oct 24 12 PM, FB carousel Mon Oct 26 12 PM, LinkedIn document Tue Oct 27 9 AM, FB Reel Oct 27 6:30 PM (no Reolink affiliate link yet).
- Chantilly garage doorbell + keypad: TikTok Oct 17 (done), YT Short Thu Oct 22 12 PM, FB Reel Fri Oct 23 6:30 PM.
- Content is scheduled daily through about Oct 27 (YouTube/FB/TikTok) and FB+LinkedIn daily through Nov 15.

## Open items / waiting on Meddy
- Google Gemini API: add env secret GEMINI_API_KEY (environment settings → Edit → Network secrets). Then use Gemini/Nano Banana to enhance photos & thumbnails, Veo for short labeled b-roll (pay per second; tell Meddy cost first).
- Reolink affiliate (impact.com, account 8004136, program by Eztech Digital Inc.): applied Oct 19, waiting for approval. When links arrive: add to Reolink posts (caption + QR) and ask Hadi to add them to the shop's Cameras category.
- Gmail draft to Hadi (hzahedi@prozco.com, "Quick check: tracking links from social"): NOT sent; send only when Meddy says "send it".
- Meddy to paste bios from website/BIOS.md; share the giveaway Reel in 3-5 local Facebook groups; pin YouTube first comments.
- Weekly review recs from Oct 19 still open: switch FB photo posts to Reels; more daily real-job Shorts at 4-8 PM; LinkedIn followers (invite connections).
- Next Thursday how-to: "Make Your Ring Doorbell More Sensitive to Motion" (Oct 29). Plan content after Oct 27 (giveaway reminders, winner announcement Nov 12-18, one long video a week).
- vidIQ out of credits until Nov 7. Proxy blocks reolink.com and novaprohome.com fetches.

## Latest numbers (Oct 12-18)
YouTube 4 subs (+2), ~1,100 views; TikTok 559 views (4x up); Facebook 198 video views, 37 post impressions; LinkedIn 2 impressions. Best: real-job install Shorts (Ring Alarm Pro Chantilly 303 views). Worst: FB photo posts.
