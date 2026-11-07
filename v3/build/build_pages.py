#!/usr/bin/env python3
"""Build NovaProHome service pages, the FAQ page, the shared stylesheet and the sitemap.

The home page (v3/index.html) is the source of truth for styles, header and footer.
Run from anywhere:  python3 v3/build/build_pages.py
"""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://novaprohome.com"
NAME = "NovaProHome"
PHONE = "(571) 241-9569"
TEL = "+15712419569"
CITIES = ["Sterling", "Ashburn", "Leesburg", "Herndon", "Reston", "Chantilly",
          "South Riding", "Centreville", "Fairfax", "Vienna", "McLean", "Arlington"]
BIZ_ID = SITE + "/#business"

SERVICES = [
    {
        "slug": "video-doorbells",
        "video": ("esbnKEEaq_M", "This Old Intercom Just Became a Video Doorbell (Chantilly install)"),
        "photos": [('chantilly-doorbell-after', 'Ring doorbell replacing an old intercom, Chantilly'), ('great-falls-doorbell-after', 'Slim wired doorbell upgrade, Great Falls'), ('ring-doorbell-brick', 'Wired video doorbell on brick')],
        "noun": "video doorbells",
        "name": "Video Doorbell Installation",
        "short": "Video Doorbells",
        "brand": "Ring Authorized Partner",
        "lead": "Wired and battery video doorbells installed cleanly, with the chime, transformer and Wi-Fi checked so the doorbell stays online and the button still rings inside.",
        "included": [
            "Doorbell selection for your door frame, power and Wi-Fi",
            "Transformer and chime check, with an upgrade when the old one is too weak",
            "Angled or wedge mounts when the door sits in a recess",
            "Replacement of old intercom or button-only systems",
            "App setup, motion zones and alerts for everyone in the house",
        ],
        "steps": [
            ("Check power", "We measure the existing doorbell transformer. Many older homes have one too weak for a video doorbell."),
            ("Check Wi-Fi at the door", "We test the signal where the doorbell will hang and fix weak spots before mounting."),
            ("Mount and wire", "The doorbell is leveled, sealed and connected to your existing chime or a new one."),
            ("Set it up with you", "We set motion zones and alerts on your phone so you are not flooded with notifications."),
        ],
        "know": [
            ("Wired or battery?", "A wired doorbell never needs recharging and supports more features. Battery models suit doors with no existing doorbell wiring."),
            ("Old intercoms", "Many NoVA townhomes and older homes still have intercom panels. We can retire them and put a video doorbell in their place."),
        ],
        "faq": [
            ("Will my existing chime still ring?", "Usually yes. We test your chime and transformer first. If either is incompatible, we explain the options before any work starts."),
            ("Can you install a video doorbell where there is no doorbell wiring?", "Yes. A battery doorbell needs no wiring, or we can run new low-voltage wire when the wall allows it."),
            ("Do I need a subscription?", "Live view and alerts work without one. Recorded video history usually requires the manufacturer's optional plan, and we explain it before you decide."),
            ("How long does a doorbell install take?", "Most video doorbell installs take one to two hours, including app setup."),
        ],
    },
    {
        "slug": "security-cameras",
        "photos": [('ring-floodlight-brick', 'Floodlight camera on brick'), ('vienna-nest-cam-garage', 'Nest camera over the driveway, Vienna'), ('reston-ring-floodlight', 'Floodlight camera, Reston')],
        "noun": "security cameras",
        "name": "Security Camera Installation",
        "short": "Security Cameras",
        "brand": "Ring Authorized Partner",
        "lead": "Indoor and outdoor cameras placed for real coverage of driveways, entries, side yards and packages, with wiring concealed wherever the structure allows.",
        "included": [
            "Coverage plan showing what each camera will see before we mount it",
            "Wired (PoE) and Wi-Fi camera options",
            "Floodlight and spotlight cameras for driveways and back yards",
            "Concealed cable runs through attics, soffits and basements where possible",
            "Phone setup, motion zones and sharing with family members",
        ],
        "steps": [
            ("Walk the property", "We look at entries, blind spots and where people actually approach the house."),
            ("Plan coverage", "You see where each camera goes and what it covers, and get a written quote."),
            ("Install and conceal", "Cameras are mounted, sealed against weather and wired as cleanly as the structure allows."),
            ("Tune alerts", "We set detection zones so you get alerts for people and cars, not swaying trees."),
        ],
        "know": [
            ("Wired vs. Wi-Fi cameras", "Wired cameras get power and data over one cable and don't need charging. Wi-Fi and battery cameras install anywhere but depend on a strong signal."),
            ("Brick and stone", "Masonry walls, common in Northern Virginia, weaken Wi-Fi. We test the signal at every mounting spot first."),
        ],
        "faq": [
            ("How many cameras does my house need?", "Most single-family homes in our area are well covered with a doorbell plus three to five exterior cameras. We confirm the number during the free assessment."),
            ("Can cameras record without the internet?", "Wired systems that record to a local recorder keep recording during an internet outage. Cloud cameras need the internet to save video."),
            ("Will there be visible wires?", "We conceal wiring wherever the structure allows and tell you up front if anything can't be hidden."),
            ("Do you install cameras for businesses?", "Yes. We cover entrances, registers, stockrooms and parking for offices and small retail."),
        ],
    },
    {
        "slug": "ring-alarm",
        "photos": [('ring-alarm-keypad', 'Ring Alarm keypad by the entry'), ('ring-alarm-pro-base', 'Ring Alarm Pro base station')],
        "noun": "Ring Alarm systems",
        "name": "Ring Alarm Installation",
        "short": "Ring Alarm",
        "brand": "Ring Authorized Partner",
        "lead": "A Ring Alarm system set up properly: base station, keypad, door and window sensors and motion detectors placed where they actually catch entry.",
        "included": [
            "Sensor plan for every ground-floor entry and key interior paths",
            "Base station, keypad and range extender placement",
            "Contact sensors on doors and windows, motion detectors in hallways",
            "Optional smoke, flood and freeze sensors",
            "Modes (Home, Away, Disarmed) set up with you and your family",
        ],
        "steps": [
            ("Map the entries", "We list every door and accessible window and plan sensor coverage room by room."),
            ("Place the base and keypad", "The base station goes where it has good Wi-Fi and reach to every sensor."),
            ("Install and test", "Every sensor is mounted, named and tested so alerts tell you exactly which door opened."),
            ("Teach the household", "We walk everyone through arming, disarming and what to do on an alarm."),
        ],
        "know": [
            ("Self-monitored or professional", "Ring Alarm works with phone alerts on its own. Professional 24/7 monitoring is an optional Ring plan, and we explain it before you decide."),
            ("Works with your doorbell", "Ring Alarm and Ring doorbells and cameras show up in the same app."),
        ],
        "faq": [
            ("Do I need professional monitoring?", "No. Ring Alarm can send alerts to your phone without a plan. Professional monitoring is optional and billed by Ring."),
            ("Will pets trigger the motion detectors?", "We place and adjust motion detectors to reduce false alarms from pets, and can rely on door sensors in pet areas instead."),
            ("Can you add sensors to an existing Ring Alarm?", "Yes. We can add sensors, extenders and keypads to a system you already own."),
        ],
    },
    {
        "slug": "nest-thermostats",
        "photos": [('thermostat-wiring-check', "Checking the old thermostat's wiring before an install")],
        "noun": "Nest thermostats",
        "name": "Nest Thermostat Installation",
        "short": "Nest Thermostats",
        "brand": "Google Nest Pro",
        "lead": "Google Nest thermostats installed by a Nest Pro, with your heating and cooling system checked for compatibility so it works right on day one.",
        "included": [
            "Compatibility check of your furnace, air handler or heat pump wiring",
            "Power solution when there is no C-wire",
            "Clean wall plate or trim so old paint lines are covered",
            "Multi-zone homes with one thermostat per zone",
            "Schedules, Eco temperatures and app sharing set up with you",
        ],
        "steps": [
            ("Check the system", "We identify your equipment and existing wiring before removing the old thermostat."),
            ("Solve power", "If your system lacks a common wire, we add one or use the right power accessory."),
            ("Install and configure", "The thermostat is mounted, leveled and set for your exact system type."),
            ("Test heating and cooling", "We run each stage so you know the system responds correctly."),
        ],
        "know": [
            ("Heat pumps", "Many Northern Virginia homes use heat pumps with auxiliary heat. Correct setup keeps the expensive backup heat from running when it doesn't need to."),
            ("Zoned homes", "Two- and three-story homes often have separate zones. Each zone gets its own thermostat, and all of them appear in one app."),
        ],
        "faq": [
            ("Does a Nest thermostat work with my system?", "Most forced-air and heat pump systems are compatible. We confirm before installing and tell you up front if yours needs extra parts."),
            ("What if I don't have a C-wire?", "We can add one where possible or use the power accessory designed for your system."),
            ("Can you install thermostats for multiple zones?", "Yes. We install one per zone and set them all up in the same app."),
        ],
    },
    {
        "slug": "smart-locks",
        "photos": [('smart-lock-keypad', 'Keypad smart lock, fitted and aligned')],
        "noun": "smart locks",
        "name": "Smart Lock Installation",
        "short": "Smart Locks",
        "brand": "Smart entry",
        "lead": "Keyless smart locks fitted to your doors so they lock smoothly every time, with codes for family, guests and service visits.",
        "included": [
            "Lock selection for your door, deadbolt and style",
            "Door and strike adjustment so the bolt never binds",
            "Keypad, app and voice control setup",
            "Guest and service codes that can expire on schedule",
            "Rental and short-term stay setups for hosts",
        ],
        "steps": [
            ("Check the door", "We measure the deadbolt and check door alignment, because a sticking bolt drains batteries."),
            ("Fit the lock", "We install the lock and adjust the strike plate for a smooth throw."),
            ("Connect it", "The lock is paired to Wi-Fi or your hub and added to your app."),
            ("Set codes", "We create codes for each person and show you how to share temporary ones."),
        ],
        "know": [
            ("Alignment matters", "Most smart lock complaints come from doors that rub or bolts that bind. We fix the door, not just swap the lock."),
            ("For hosts", "Short-term rental hosts can give each guest a code that works only during their stay."),
        ],
        "faq": [
            ("Will a smart lock fit my door?", "Most standard deadbolt doors in our area fit common smart locks. We check measurements first."),
            ("What happens if the batteries die?", "Most smart locks warn you well in advance, and many keep a physical key or an emergency power option."),
            ("Can I give temporary codes to guests or cleaners?", "Yes. We show you how to create codes that work only on certain days or times."),
        ],
    },
    {
        "slug": "lutron-lighting",
        "noun": "Lutron lighting",
        "name": "Lutron Lighting Control",
        "short": "Lutron Lighting",
        "brand": "Lutron Preferred Pro",
        "lead": "Lutron smart dimmers, switches and keypads from a Lutron Preferred Pro, from a few rooms with Caséta to whole-home RadioRA 3 systems.",
        "included": [
            "Caséta smart dimmers and switches for main living areas",
            "RadioRA 3 systems with keypads for larger homes and renovations",
            "Scenes such as Good Morning, Movie and Good Night",
            "Schedules and away-mode lighting",
            "Voice assistant and app setup",
        ],
        "steps": [
            ("Plan the rooms", "We list each room, its switches and how you use the lights."),
            ("Choose the system", "Caséta or RadioRA 3, based on the size of the project and the keypads you want."),
            ("Install", "Smart dimmers go into existing switch boxes, with no rewiring in most homes."),
            ("Program scenes", "We set the scenes and schedules you'll actually use."),
        ],
        "know": [
            ("Caséta", "The simple, affordable way to start with smart lighting in a few rooms."),
            ("RadioRA 3", "Lutron's professional system for whole-home lighting with engraved keypads. It is designed and installed by Lutron-trained professionals."),
        ],
        "faq": [
            ("Do I need new wiring for smart dimmers?", "Usually not. Lutron dimmers replace standard switches in existing boxes."),
            ("Caséta or RadioRA 3?", "Caséta suits a few rooms. RadioRA 3 suits whole-home systems and renovations with keypads at every entry."),
            ("Do my bulbs need to be special?", "Use dimmable bulbs. We check your existing fixtures for compatibility."),
        ],
    },
    {
        "slug": "mesh-wifi",
        "noun": "mesh Wi-Fi and networks",
        "name": "Mesh Wi-Fi and Network Installation",
        "short": "Whole-Home Wi-Fi",
        "brand": "Every system starts here",
        "lead": "Fast Wi-Fi in every room, the basement and the back yard, using mesh systems or wired access points sized to your home.",
        "included": [
            "Signal survey of every floor, the basement and outdoor areas",
            "Mesh systems or ceiling-mounted wired access points",
            "Ethernet runs for backhaul, offices and TVs where needed",
            "Separate guest and smart-device networks",
            "Small network racks and cable cleanup",
        ],
        "steps": [
            ("Survey the signal", "We measure Wi-Fi speed in each room and find the dead zones."),
            ("Design the layout", "We pick the number and position of access points for your floors and walls."),
            ("Install and wire", "Units are mounted cleanly, with cable backhaul wherever we can run it."),
            ("Verify speed", "We test speed in each room before we leave."),
        ],
        "know": [
            ("Mesh vs. wired access points", "Mesh is quick to set up. Wired access points deliver full speed in every room. Most larger homes do best with a mix."),
            ("Basements and brick", "Finished basements and masonry walls block Wi-Fi. A wired unit on each floor solves most problems."),
        ],
        "faq": [
            ("Why is my Wi-Fi slow upstairs or in the basement?", "Floors, brick and distance weaken the signal from a single router. Adding properly placed access points fixes it."),
            ("Do I need to change internet providers?", "Usually not. Most slow-Wi-Fi problems are inside the home, not with the provider."),
            ("Can you set up a separate network for smart devices?", "Yes. We separate guest and smart-device networks from your personal devices."),
        ],
    },
]

GENERAL_FAQ = [
    ("Is the assessment really free?", "Yes. We visit, look at your home and network, and talk through what you want. You get a recommendation with no obligation."),
    ("Which areas does NovaProHome serve?", "NovaProHome is based in Sterling, Virginia and serves " + ", ".join(CITIES[:-1]) + " and " + CITIES[-1] + ", plus the rest of Loudoun County, Fairfax County and Northern Virginia."),
    ("What certifications does NovaProHome have?", "NovaProHome is a Google Nest Pro, a Ring Authorized Partner and a Lutron Preferred Pro."),
    ("Can you work with devices I already own?", "Usually. We review what you have, keep what works and recommend upgrades only where they make a real difference."),
    ("Do I need a monthly subscription?", "Not from us. Some manufacturers offer optional cloud plans, such as recorded video history. We explain exactly what each one does so you can decide."),
    ("What happens if something stops working?", "Call us. You'll talk to the same team that installed your system."),
]


def esc(t):
    return html.escape(t, quote=True)


def ld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False).replace("</", "<\\/") + "</script>"


def extract(src):
    style = re.search(r"<style>(.*?)</style>", src, re.S).group(1)
    head_links = re.search(r'(<link rel="preconnect".*?display=swap">)', src, re.S).group(1)
    icon = re.search(r'<link rel="icon" href="[^"]*">', src).group(0)
    topbar = re.search(r'<div class="topbar">.*?</div>\n</div>', src, re.S).group(0)
    header = re.search(r'<header class="header">.*?</header>', src, re.S).group(0)
    footer = re.search(r'<footer class="footer">.*?</footer>', src, re.S).group(0)
    callbar = re.search(r'<nav class="callbar".*?</nav>', src, re.S).group(0)
    follow = re.search(r'<div class="follow">.*?</div>', src, re.S).group(0)

    def rooted(h):
        h = h.replace('href="#top"', 'href="/"')
        return re.sub(r'href="#([a-z][\w-]*)"', r'href="/#\1"', h)

    return {
        "style": style, "head_links": head_links, "icon": icon, "follow": follow,
        "topbar": topbar, "header": rooted(header), "footer": rooted(footer), "callbar": rooted(callbar),
    }


NAV_JS = """<script>
(function () {
  var nav = document.getElementById("nav"), burger = document.getElementById("burger");
  burger.addEventListener("click", function () {
    var open = nav.classList.toggle("open");
    burger.setAttribute("aria-expanded", String(open));
  });
  Array.prototype.forEach.call(document.querySelectorAll(".dd"), function (dd) {
    var b = dd.querySelector("button");
    b.addEventListener("click", function (e) {
      e.stopPropagation();
      var open = dd.classList.toggle("open");
      b.setAttribute("aria-expanded", String(open));
    });
  });
  document.addEventListener("click", function (e) {
    if (!e.target.closest(".dd")) Array.prototype.forEach.call(document.querySelectorAll(".dd"), function (o) { o.classList.remove("open"); });
  });
  var y = document.getElementById("yr"); if (y) y.textContent = new Date().getFullYear();
})();
</script>"""


def page(parts, *, path, title, desc, body, schema):
    url = SITE + path
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="theme-color" content="#161615">
<link rel="canonical" href="{url}">
{parts['icon']}
<meta property="og:type" content="website">
<meta property="og:site_name" content="{NAME}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
{ld(schema)}
{parts['head_links']}
<link rel="stylesheet" href="/assets/site.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
{parts['topbar']}
{parts['header']}
<main id="main">
{body}
</main>
{parts['footer']}
{parts['callbar']}
{NAV_JS}
</body>
</html>
"""


def faq_html(items):
    return "\n".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in items)


def faq_schema(items):
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items]}


def crumbs_schema(trail):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + u} for i, (n, u) in enumerate(trail)]}


def cta_band(parts, heading):
    return f"""<section class="band cta-band">
  <div class="wrap" style="display:grid;gap:20px">
    <span class="eyebrow">Free in-home assessment</span>
    <h2 style="font-size:clamp(1.9rem,3.6vw,2.8rem)">{esc(heading)}</h2>
    <p style="color:var(--muted);max-width:60ch">Tell us about your home and we'll reply within one business day. Prefer to talk? Call {PHONE}.</p>
    <div class="cta-row"><a class="btn btn--gold" href="/#contact">Get a Free Quote</a><a class="btn btn--dark" href="tel:{TEL}">Call {PHONE}</a></div>
    <p class="follow__label">See our installs on</p>
    {parts['follow']}
  </div>
</section>"""


def service_page(parts, s):
    path = f"/services/{s['slug']}/"
    city_line = ", ".join(CITIES[:-1]) + " and " + CITIES[-1]
    title = f"{s['name']} in Sterling, Ashburn & Northern VA | {NAME}"
    desc = f"{NAME} provides {s['name'].lower()} in {city_line}, Virginia. {s['brand'] if s['brand'] not in ('Smart entry', 'Every system starts here') else 'Engineer-led'} installer. Free in-home assessment."
    included = "\n".join(f"<li>{esc(i)}</li>" for i in s["included"])
    steps = "\n".join(f"<li><span><b>{esc(t)}.</b> {esc(d)}</span></li>" for t, d in s["steps"])
    know = "\n".join(f"<p><b>{esc(t)}{'' if t[-1] in '?.!' else '.'}</b> {esc(d)}</p>" for t, d in s["know"])
    cities = "".join(f"<span>{esc(c)}</span>" for c in CITIES)
    vid = ""
    if s.get("video"):
        vid_id, vid_title = s["video"]
        vid = f'''<div class="vid" style="margin-top:22px"><div class="vid__copy"><span class="eyebrow">Watch the install</span><h3>{esc(vid_title)}</h3><a class="btn btn--dark btn--sm" href="https://www.youtube.com/@NovaProHome?sub_confirmation=1" target="_blank" rel="noopener">More installs on YouTube</a></div><div class="vid__frame"><iframe src="https://www.youtube-nocookie.com/embed/{vid_id}" title="{esc(vid_title)}" loading="lazy" allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe></div></div>'''
    photos = ""
    if s.get("photos"):
        figs = "".join(f'<figure class="shot"><img src="/assets/work/{f}.jpg" alt="{esc(c)}" loading="lazy" width="1050" height="1400"><figcaption>{esc(c)}</figcaption></figure>' for f, c in s["photos"])
        photos = f"""<section class="band">
  <div class="wrap">
    <div class="head"><span class="eyebrow">From our installs</span><h2>Real {esc(s['noun'])} jobs by {NAME}</h2></div>
    <div class="photos">{figs}</div>{vid}
  </div>
</section>
"""
    related = "".join(f'<a href="/services/{o["slug"]}/">{esc(o["short"])} →</a>' for o in SERVICES if o is not s)
    body = f"""<section class="page-hero">
  <div class="wrap">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a><span aria-hidden="true">/</span><a href="/#services">Services</a><span aria-hidden="true">/</span><span>{esc(s['short'])}</span></nav>
    <span class="eyebrow">{esc(s['brand'])} &bull; Northern Virginia</span>
    <h1>{esc(s['name'])} in Sterling, Ashburn &amp; Northern Virginia</h1>
    <p class="hero__lead">{esc(s['lead'])}</p>
    <div class="cta-row"><a class="btn btn--gold" href="/#contact">Get a Free Quote</a><a class="btn btn--dark" href="tel:{TEL}">Call {PHONE}</a></div>
  </div>
</section>
<section class="band">
  <div class="wrap two-col">
    <div class="panel"><h2>What's included</h2><ul class="checklist">{included}</ul></div>
    <div class="panel"><h2>How we install</h2><ol class="numlist">{steps}</ol></div>
  </div>
</section>
{photos}<section class="band band--alt">
  <div class="wrap">
    <div class="head"><span class="eyebrow">Good to know</span><h2>Advice from our installs</h2></div>
    <div class="prose">{know}</div>
  </div>
</section>
<section class="band">
  <div class="wrap" style="display:grid;gap:22px">
    <div class="head" style="margin-bottom:0"><span class="eyebrow">Service area</span><h2>{esc(s['short'])} installation near you</h2>
    <p>{NAME} is based in Sterling and installs {esc(s['noun'])} for homeowners in {esc(city_line)}, and across Loudoun County, Fairfax County and Northern Virginia.</p></div>
    <div class="cities">{cities}</div>
  </div>
</section>
<section class="band band--alt">
  <div class="wrap faq">
    <div class="head"><span class="eyebrow">FAQ</span><h2>{esc(s['short'])} questions</h2></div>
    <div class="faq__list">{faq_html(s['faq'])}</div>
  </div>
</section>
<section class="band">
  <div class="wrap" style="display:grid;gap:18px"><h2 style="font-size:1.5rem">Other services</h2><div class="related">{related}</div></div>
</section>
{cta_band(parts, 'Get a free quote for ' + s['noun'])}"""
    schema = {"@context": "https://schema.org", "@graph": [
        {"@type": "Service", "name": s["name"], "serviceType": s["name"], "url": SITE + path,
         "description": s["lead"], "provider": {"@type": "HomeAndConstructionBusiness", "@id": BIZ_ID, "name": NAME, "telephone": "+1-571-241-9569"},
         "areaServed": [{"@type": "City", "name": c + ", VA"} for c in CITIES]},
        faq_schema(s["faq"]),
        crumbs_schema([("Home", "/"), ("Services", "/#services"), (s["short"], path)]),
    ]}
    return path, page(parts, path=path, title=title, desc=desc, body=body, schema=schema)


def faq_page(parts):
    path = "/faq/"
    groups = [("General", GENERAL_FAQ)] + [(s["short"], s["faq"]) for s in SERVICES]
    sections = "\n".join(
        f'<div style="display:grid;gap:12px"><h2 style="font-size:1.4rem;color:var(--gold)">{esc(g)}</h2><div class="faq__list">{faq_html(items)}</div></div>'
        for g, items in groups)
    all_items = [qa for _, items in groups for qa in items]
    body = f"""<section class="page-hero">
  <div class="wrap">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a><span aria-hidden="true">/</span><span>FAQ</span></nav>
    <span class="eyebrow">{NAME} FAQ</span>
    <h1>Smart home installation questions, answered</h1>
    <p class="hero__lead">Answers about video doorbells, cameras, Ring Alarm, Nest thermostats, smart locks, Lutron lighting and Wi-Fi from {NAME} in Sterling, Virginia.</p>
  </div>
</section>
<section class="band">
  <div class="wrap faq" style="display:grid;gap:44px">{sections}</div>
</section>
{cta_band(parts, 'Still have a question? Ask us.')}"""
    schema = {"@context": "https://schema.org", "@graph": [faq_schema(all_items), crumbs_schema([("Home", "/"), ("FAQ", path)])]}
    title = f"Smart Home Installation FAQ | {NAME}, Northern Virginia"
    desc = f"Answers to common questions about smart home, camera, doorbell, alarm, thermostat, lock, lighting and Wi-Fi installation from {NAME} in Sterling, VA."
    return path, page(parts, path=path, title=title, desc=desc, body=body, schema=schema)


def main():
    src = (ROOT / "index.html").read_text()
    parts = extract(src)
    (ROOT / "assets").mkdir(exist_ok=True)
    (ROOT / "assets" / "site.css").write_text("/* Generated from index.html by build/build_pages.py. Edit index.html, then rebuild. */\n" + parts["style"].strip() + "\n")
    paths = ["/"]
    for s in SERVICES + [None]:
        path, out = service_page(parts, s) if s else faq_page(parts)
        dest = ROOT / path.strip("/") / "index.html"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(out)
        paths.append(path)
    urls = "\n".join(f"  <url><loc>{SITE}{p}</loc><changefreq>monthly</changefreq><priority>{'1.0' if p == '/' else '0.8'}</priority></url>" for p in paths)
    (ROOT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n</urlset>\n')
    print("built", len(paths) - 1, "pages")


if __name__ == "__main__":
    main()
