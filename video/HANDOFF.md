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

## Oct 19 evening: Gemini rebuild (session_01EBb8bvqS7qdcrdUoBbigq1)
- Scheduled tasks moved to this session: trig_015fNt17QcfJcGdgBQujTRaL (YouTube Mon/Thu 9:13 AM) and trig_011gPdHHYNGgXqSY8YnscD2H (weekly review Mon 8:41 AM). Old ones disabled.
- Gemini works without GEMINI_API_KEY (the proxy adds the credentials). Models: gemini-3.1-flash-image (Nano Banana), veo-3.1-fast/lite-generate-preview, gemini-3.1-pro-preview (review/brainstorm).
- `video/tools/enhance_photos.py`: Nano Banana color-corrects job photos; only low-frequency tone is kept on the original pixels (nothing added, blurs preserved). Output in video/enhanced/, used automatically by make_series/make_tiktok (NPH_ENHANCED=0 for originals). All 72 photos done.
- `video/tools/gen_images.py`: AI illustrations for tip posts, stamped "AI-generated illustration". make_series now supports {"clip": ..., "ai": true} scenes (labeled Veo b-roll). Veo clips: video/broll/ (6 clips, Fast 1080p 8 s, ~$1 each; letterboxed ones need "crop").
- `video/tools/rebuild_pending.sh` re-rendered every unposted video (Oct 20+) with enhanced photos (+ shop QR; giveaway videos have the QR off).
- 34 text-only FB+LinkedIn posts (Oct 26 to Nov 29) rebuilt as 15 s Reels: video/social/reels/<date>_<slug>.mp4 (spec text_posts.json).
- `video/tools/gemini_review.py`: Gemini watches each video and critiques hook/title/caption (items list in scratchpad; rebuild with the post list).
- (resolved Oct 20) Gemini prepaid credits ran out (HTTP 402) after ~$14 of use. Meddy asked to brainstorm with Gemini before posting anything, so NO Metricool media swaps have been made yet. When credits are topped up: run gemini_review.py on all items + strategy brainstorm, apply good ideas, then updateScheduledPost each pending post with media https://raw.githubusercontent.com/meddybaraei/meddy-baraei/<SHA>/<path> (Reels: facebookData type REEL + title; keep LinkedIn).
- Duplicate FB slot: Thu Oct 22 6:30 PM has ecobee Reel + Reston perfume Reel; move perfume to Fri Oct 23 12 PM when swapping media.

## Oct 20: Gemini review round + Metricool swap (DONE)
- Meddy set up auto-prepaid for Gemini. Gemini 3.1 Pro reviewed all 56 videos (scores 2-8; real-job openers win, slides/product renders/AI images lose) + strategy session: video/GEMINI_STRATEGY_2026-10-19.md.
- Applied: every opener is now a real job photo + question hook; tip Reels use real job photos (AI b-roll only on holiday Reels + EV, labeled on screen and "(Video contains AI-generated b-roll.)" in caption); QR scene 3 s; no subscribe badge on giveaway.
- Ignore Gemini when it calls our own logo a "brand logo", flags the phone on TikTok, or says Ring has no 4K doorbell.
- Metricool: 63 pending posts updated to media from commit d995d23 (all videos Oct 20-27 + 34 FB/LinkedIn text posts Oct 26-Nov 29 now Reels; UTMs added to Nov 16-29). Removed giveaway block from 3 posts that also carry affiliate/shop links (4K Pro review + Short, Reolink Short). Reston perfume FB Reel moved to Wed Oct 28 6:30 PM. Oct 27 Schlage FB is now a Reel.
- Not rebuilt: 12 AI promo posts (promo/*) and Reolink video (art-only). Remaking promos with Veo Fast ~$16.
- Gemini's top asks for Meddy: GA4 + Meta Pixel on the site (Hadi), short phone clips (5-10 s) on every job, seed giveaway comments + share in local FB groups, maybe a $15 local boost on the giveaway Reel, Facebook cadence max 1 feed post/day.


## Gemini budget (owner, Oct 20 2026): MAX $20/month total for all Gemini use. Check and update video/GEMINI_SPEND.md before and after every Gemini job; estimate cost first; prefer gemini-3.5-flash and cached assets; tell Meddy before any Veo batch.

## Six AI-voiced service Shorts (Oct 22)
From the motion-graphics session (branch claude/jolly-knuth-8q5382), saved in video/owner/shorts/. Scheduled YouTube Short 7:00 PM + TikTok 7:30 PM, all AI-labeled (isAiGeneratedContent / isAigc), giveaway block on YouTube, no affiliate links:
Oct 23 EV charger explained · Oct 24 smart bulbs vs switches · Oct 25 smart lock door test · Oct 26 smart garage upgrade · Oct 27 one-app smart home · Oct 28 how NovaProHome works.
Facebook has a Reel every day at noon through Nov 20 (max 1 FB post/day), so instead of new FB slots the Shorts replaced the media of the matching text Reels: Nov 13 smart lighting → bulbs-vs-switches Short, Nov 17 EV panel check → EV Short (FB+LinkedIn). Lock/garage/one-app/how-we-work are still unposted on FB/LinkedIn: use them for late-Nov/Dec Facebook slots.

## Arlington job: Ring full setup (Oct 22, city confirmed Arlington)
12 real photos saved as video/weekly/photos/job2_*.jpg (+ Nano Banana enhanced): Ring Wired Doorbell Pro (3rd gen) + chime, 3 Spotlight Cam Plus with solar panels (siding + fence), Solar Steplights, Ring Bridge. 3 AI illustrations from the same upload were NOT used (Ring logos, garbled text). Built video/weekly/2026-10-23_job-arlington-ring-full-setup.mp4 (34 s, no phone, no QR) + video/tiktok/2026-10-23_arlington-ring-setup_tiktok.mp4 (16 s, phone + shop QR). Scheduled: YouTube Short Thu Oct 29 12 PM, TikTok Thu Oct 29 8:30 PM, Facebook+LinkedIn Reel Tue Nov 3 12 PM (replaced the 'smart thermostat myth' text Reel, which duplicated the Nov 2 thermostat tip). Real job, so no AI label.
Oct 22: added real clean-up photo (job2_cleanup_recycling.jpg, boxes in recycling bin) as a "We leave no mess" scene; all 3 Arlington posts updated with media from commit 530d0e4. Meddy also sent 4 AI how-to illustrations (doorbell wiring, solar cam mount, steplight on fence post, floodlight under deck stairs): NOT used: two carry Ring logos and garbled text ("wiaveroitors", "wiench"), and AI step graphics score low vs real photos.
Oct 22: Meddy confirmed 3 Solar Steplights were installed (no photo); added to final scene, TikTok clip and all 3 captions (media commit 266d417).

## Free leads plan (Oct 24)
See video/FREE_LEADS_PLAN.md. Google Business Profile is NOT connected in Metricool (only FB, LinkedIn, TikTok, YouTube, FB Ads, Google Ads); once Meddy connects it, post 2x/week with real job photos (gmbData type publication/photo). Waiting on Meddy: GBP connection, review link, referral reward approval.
- Oct 24: Google Business Profile CONNECTED in Metricool (gbpData accounts/107627548290470625370/locations/2009781620080554964). Scheduled (gmbData): photo gallery upload Sat Oct 24 1 PM (6 real job photos), posts 10 AM: Oct 25 Arlington full Ring setup, Oct 28 Great Falls doorbell, Oct 31 Chantilly Alarm Pro, Nov 4 Vienna ecobee fix, Nov 7 Reston store cameras, Nov 10 Arlington deck cams. Rule for GBP posts: no phone number in text (Google rejects), no giveaway, city + service in the first line, end with novaprohome.com/contact. Keep 2/week with every new job.
- Oct 24: Meddy said NO $25 referral offer. Never offer paid referral rewards.
- Oct 24: Google Ads (Sep 24-Oct 23): $304.61, 57 clicks, 26 "conversions"; ~$122 on zero-conversion keywords. Waiting on Meddy: real lead count (verify conversion tracking) + OK to pause zero-conversion keywords. Hadi Zahedi (prozco.com) has Manager access to the GBP.
- Oct 24: Google review link https://g.page/r/CeeJDbkRDpk2EAE/review (in FREE_LEADS_PLAN texts) + printable QR card video/reviews_qr_card.png.
- Oct 24: Meddy: only 3 real leads from Google Ads last 30 days (Ads reported 26 conversions) => conversion tracking counts the wrong actions; real cost ~$100/lead. Adspirer quota used up until Nov 14 (can't audit/edit Ads from here). Asked Meddy: how many of the 3 became jobs + job value; fix Primary conversion actions in Google Ads > Goals.
- Oct 24: Google Ads conversion setup (Meddy screenshot): 'Quote request' (Website, Primary) = Needs attention, 0 conv -> form-submit tag not firing; 'AI-qualified call leads' (Call from Ads, Primary) ok; 'Contact (Page load /contact)' Secondary, counts every page load = source of the inflated 'conversions'. Fix needed on website (Hadi/prozco builds site?): fire Quote request on successful form submit. novaprohome.com is blocked from this sandbox.
