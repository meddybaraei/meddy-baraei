"""Brainstorm with Google Gemini before posting: it watches each video and critiques hook, title and caption.
Usage: python3 gemini_review.py ITEMS.json OUT.json
ITEMS: [{"key", "file" (mp4, repo path), "platforms", "title", "caption"}]. Results are cached in OUT.json."""
import base64, json, os, subprocess, sys, tempfile, time, urllib.request

MODEL = os.environ.get('NPH_REVIEW_MODEL', 'gemini-3.1-pro-preview')
URL = f'https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent'
ROOT = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + '/../..') + '/'
BRIEF = """You are a senior short-form video strategist reviewing posts for NovaProHome, a smart home, security & EV
installer based in Sterling, VA (Ring Authorized Dealer, Google Nest Pro). Goals in order: (1) install bookings via
novaprohome.com/contact, (2) affiliate sales via novaprohome.com/shop, (3) YouTube subscribers.
What has worked: real-job install Shorts with city in the title (top: "Ring Alarm Pro Installation in Chantilly" 303 views),
problem/question hooks ("X not working?", "which one should I buy?"). Flops: generic promos, Facebook photo posts,
hard-sell CTAs. Average view duration is 2-25 s, so the first second must hook.
House rules you must respect in every suggestion: music only (no voiceover); NEVER a phone number on YouTube;
brand is always written "NovaProHome"; no brand logos as artwork; titles lead with the general search phrase, then the city;
no fake claims; giveaway entries are "comment your city", never require likes/subscribes.
Review the attached video and its post. Reply ONLY with JSON:
{"score": 1-10, "first_second_hook": "is frame 1 a strong hook? why", "video_fixes": ["max 3 concrete, cheap fixes"],
 "better_title": "<=70 chars or null if current is best", "better_first_line": "stronger caption opener <=110 chars",
 "best_time_et": "e.g. Tue 6:30 PM or null", "risk": "any rule/claim/privacy problem you see, or null"}"""


def frames_sheet(path):
    """Fallback for big files: 8-frame contact sheet as JPEG bytes."""
    d = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', path]))
    out = tempfile.mktemp(suffix='.jpg')
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', path, '-vf', f'fps=8/{d},scale=320:-1,tile=8x1', '-frames:v', '1', out], check=True)
    b = open(out, 'rb').read(); os.remove(out); return b


def review(it):
    p = ROOT + it['file']
    if os.path.getsize(p) < 18e6:
        media = {"inlineData": {"mimeType": "video/mp4", "data": base64.b64encode(open(p, 'rb').read()).decode()}}
    else:
        media = {"inlineData": {"mimeType": "image/jpeg", "data": base64.b64encode(frames_sheet(p)).decode()}}
    post = f"Platforms: {it['platforms']}\nCurrent title: {it.get('title')}\nCurrent caption:\n{it.get('caption')}"
    body = {"contents": [{"parts": [media, {"text": BRIEF + "\n\n" + post}]}],
            "generationConfig": {"responseMimeType": "application/json"}}
    for a in range(4):
        try:
            r = json.load(urllib.request.urlopen(urllib.request.Request(URL, json.dumps(body).encode(), {'Content-Type': 'application/json'}), timeout=300))
            return json.loads(r['candidates'][0]['content']['parts'][-1]['text'])
        except Exception as e:
            print('  retry', it['key'], e); time.sleep(6 * (a + 1))
    return {"error": "failed"}


items, out = json.load(open(sys.argv[1])), sys.argv[2]
res = json.load(open(out)) if os.path.exists(out) else {}
for it in items:
    if it['key'] in res and 'error' not in res[it['key']]: continue
    print('reviewing', it['key']); res[it['key']] = review(it)
    json.dump(res, open(out, 'w'), indent=1, ensure_ascii=False)
