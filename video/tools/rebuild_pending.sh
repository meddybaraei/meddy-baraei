#!/bin/bash
# Re-render every unposted video (Oct 20+) with Gemini-enhanced photos. Run from repo root.
set -e
S="python3 video/tools/make_series.py"; T="python3 video/tools/make_tiktok.py"
$S video/series/11_ring_elite_180_4k.json video/series/11_ring_elite_180_4k.mp4 v
$S video/reviews/ring-wired-doorbell-4k-pro-review.json video/reviews/ring-wired-doorbell-4k-pro-review.mp4 h
$S video/reviews/ring-wired-doorbell-4k-pro-review.json video/reviews/ring-wired-doorbell-4k-pro-review_short.mp4 v
$S video/reviews/ring-alarm-pro-review.json video/reviews/ring-alarm-pro-review.mp4 h
$S video/reviews/ring-alarm-pro-review.json video/reviews/ring-alarm-pro-review_short.mp4 v
for j in 2026-10-17_job-chantilly-garage-doorbell-keypad 2026-10-18_job-perfume-store-security 2026-10-19_job-schlage-smart-lock 2026-10-20_giveaway-push; do
  $S video/weekly/$j.json video/weekly/$j.mp4 v; done
$S video/weekly/2026-10-22_ecobee-humidity-fix.json video/weekly/2026-10-22_ecobee-humidity-fix.mp4 h
$S video/weekly/2026-10-22_ecobee-humidity-fix.json video/weekly/2026-10-22_ecobee-humidity-fix_short.mp4 v
$S video/long/2026-10-23_real-installs-nova.json video/long/2026-10-23_real-installs-nova.mp4 h
for j in 2026-10-20_giveaway 2026-10-20_ring-doorbell-4k-pro 2026-10-21_ring-solar 2026-10-22_ecobee-humidity 2026-10-23_ring-stick-up \
         2026-10-24_nest-cam 2026-10-25_nest-floodlight 2026-10-26_ring-elite-180 2026-10-27_ring-alarm-pro-review; do
  $T video/tiktok/${j}_tiktok.json video/tiktok/${j}_tiktok.mp4; done
