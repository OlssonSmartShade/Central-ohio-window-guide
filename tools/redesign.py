"""One-time editorial redesign of Central Ohio Window Guide (Oct 2026).

Rewraps every page in public/ with the new masthead, article layout and footer,
keeping each page's title, meta, canonical, schema, GA tag and body copy.
Also writes the new homepage. Run from the repo root:  python3 tools/redesign.py
New articles should copy the markup of any existing article page afterwards.
"""
import json, re, math, html
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString

PUB = Path(__file__).resolve().parent.parent / "public"
SITE = "https://centralohiowindowguide.com"
IMG = "/images/editorial/"
CREDIT = "Photo: Norman Window Fashions"

GUIDES = [
  # slug, kicker, short title, blurb, image, alt
  ("smart-home-window-automation-central-ohio", "Smart Home", "The Complete Guide to Smart Home Window Automation",
   "Matter-over-Thread, voice control, scheduling, power options, and retrofitting an existing home without opening walls.",
   "norman-smartdrape-shades-living-room-49.webp", "Motorized sheer vertical shades across a wall of living room windows"),
  ("motorized-shades-cost-central-ohio", "Cost Guide", "What Motorized & Custom Shades Really Cost",
   "2026 installed price ranges for motorized, roller, solar and cellular shades, blinds and shutters, plus whole-house examples.",
   "norman-soluna-roller-shades-living-room-26.webp", "Light-filtering roller shades on large living room windows"),
  ("plantation-shutters-cost-columbus-ohio", "Cost Guide", "How Much Plantation Shutters Cost in Columbus",
   "Installed prices for composite and hardwood shutters, patio doors, arches and whole-house budgets.",
   "norman-normandy-hardwood-plantation-shutters-living-room-with-arched-windows-59.webp", "Stained hardwood plantation shutters with an arched top over French doors"),
  ("shades-vs-blinds-vs-shutters-ohio", "Buyer's Guide", "Shades vs. Blinds vs. Shutters for Ohio Homes",
   "Insulation, light control, durability, resale value and cost compared, with a pick for every room.",
   "norman-woodlore-composite-plantation-shutters-living-room-31.webp", "White composite plantation shutters in a bright living room"),
  ("window-treatment-cost-calculator", "Tool", "Window Treatment Cost Calculator",
   "Choose products, window count and sizes for an installed price range for your Central Ohio home in seconds.",
   "norman-centerpiece-roman-shades-dining-room-27.webp", "Fabric Roman shades above a dining table and kitchen windows"),
  ("child-pet-safe-cordless-window-treatments", "Safety", "Child- and Pet-Safe Cordless Window Treatments",
   "Why cordless and motorized treatments are the safe choice for families and pets, and which styles last.",
   "norman-portrait-honeycomb-cellular-shades-bedroom-15.webp", "Cordless cellular shades in a calm primary bedroom"),
  ("sunroom-window-treatments-ohio", "Room by Room", "Sunrooms & Hard-to-Cover Windows",
   "Solar shades, motorization, specialty shapes and window film for sunrooms, high windows and arches.",
   "norman-perfectsheer-shades-living-room-89.webp", "Sheer shades softening light across a corner of tall windows"),
  ("window-film-for-homes-ohio", "Window Film", "Home Window Tinting in Central Ohio",
   "Ceramic heat control, UV protection, frosted privacy and security film, with glass safety and cost per square foot.",
   "norman-soluna-roller-shades-home-office-90.webp", "Sunlit home office with roller shades on paned windows"),
]
CITIES = [
  ("columbus", "Columbus", "Every neighborhood", "norman-soluna-roller-shades-kitchen-24.webp"),
  ("dublin", "Dublin", "Muirfield to Bridge Park", "norman-brightwood-plantation-shutters-great-room-with-specialty-shape-windows-72.webp"),
  ("upper-arlington", "Upper Arlington", "Classic homes, modern control", "norman-normandy-hardwood-plantation-shutters-great-room-17.webp"),
  ("new-albany", "New Albany", "Georgian estates", "norman-smartdrape-shades-living-room-53.webp"),
  ("powell", "Powell", "New builds & great rooms", "norman-woodlore-composite-plantation-shutters-great-room-36.webp"),
  ("westerville", "Westerville", "Uptown to the suburbs", "norman-synchrony-blinds-living-room-41.webp"),
  ("worthington", "Worthington", "Historic & classic homes", "norman-normandy-hardwood-plantation-shutters-living-room-21.webp"),
  ("bexley", "Bexley", "Historic & older homes", "norman-normandy-wood-blinds-living-room-16.webp"),
  ("hilliard", "Hilliard", "New & existing homes", "norman-portrait-honeycomb-cellular-shades-living-room-79.webp"),
  ("gahanna", "Gahanna", "Energy-saving picks", "norman-portrait-honeycomb-cellular-shades-dining-room-4.webp"),
  ("plain-city", "Plain City", "Farmhouse to new build", "norman-woodlore-composite-plantation-shutters-living-room-32.webp"),
  ("delaware", "Delaware", "New & historic homes", "norman-normandy-hardwood-plantation-shutters-kitchen-with-arched-windows-19.webp"),
  ("lewis-center", "Lewis Center", "Open plans & tall glass", "norman-smartfold-shades-living-room-57.webp"),
  ("lancaster", "Lancaster", "Fairfield County homes", "norman-smartdrape-shades-dining-room-52.webp"),
]
CITY_ALT = "Custom window treatments in a {} area home (manufacturer photo)"

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500&family=Jost:wght@400;500&display=swap">'
         '<link rel="stylesheet" href="/style.css?v=2">'
         '<meta name="theme-color" content="#faf7f0">'
         '<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 64 64%27%3E%3Crect width=%2764%27 height=%2764%27 fill=%27%231f1b17%27/%3E%3Ctext x=%2732%27 y=%2745%27 text-anchor=%27middle%27 font-family=%27Georgia%27 font-size=%2738%27 fill=%27%23e7c97f%27%3EW%3C/text%3E%3C/svg%3E">'
         '<script>document.documentElement.classList.add("js")</script>')

def nav(current=""):
    items = [("/motorized-shades-cost-central-ohio/", "Costs"), ("/smart-home-window-automation-central-ohio/", "Smart Home"),
             ("/plantation-shutters-cost-columbus-ohio/", "Shutters"), ("/shades-vs-blinds-vs-shutters-ohio/", "Compare"),
             ("/window-film-for-homes-ohio/", "Window Film"), ("/#neighborhoods", "Neighborhoods"),
             ("/window-treatment-cost-calculator/", "Calculator"), ("/about/", "About")]
    cur = ' aria-current="page"'
    links = "".join(f'<a href="{h}"{cur if h == current else ""}>{t}</a>' for h, t in items)
    return ('<a class="skip" href="#content">Skip to content</a>'
            '<div class="topline"><div class="in"><span><span class="hide-xs">A homeowner resource for </span>Columbus &amp; Central Ohio</span>'
            '<span class="hide-sm">Prices updated October 2026</span></div></div>'
            '<header class="masthead"><div class="in"><a class="brand" href="/" aria-label="Central Ohio Window Guide, home">'
            '<span class="pre">CENTRAL OHIO</span><span class="name">Window <i>Guide</i></span></a>'
            f'<nav class="sections" aria-label="Sections">{links}</nav></div></header>')

def footer():
    g = "".join(f'<li><a href="/{s}/">{t}</a></li>' for s, k, t, *_ in GUIDES[:6])
    c = "".join(f'<li><a href="/motorized-shades-{s}-ohio/">{n}</a></li>' for s, n, *_ in CITIES[:8])
    return ('<footer class="foot"><div class="in"><div class="top"><div><a class="brand" href="/"><span class="pre">CENTRAL OHIO</span>'
            '<span class="name">Window <i>Guide</i></span></a><p class="about">Plain-spoken guides to smart shades, shutters and window '
            'treatments, written for the homes of Columbus and Central Ohio.</p></div>'
            f'<div><h4>Guides</h4><ul>{g}</ul></div><div><h4>Neighborhoods</h4><ul>{c}<li><a href="/#neighborhoods">All areas</a></li></ul></div>'
            '<div><h4>The Guide</h4><ul><li><a href="/about/">About &amp; disclosure</a></li><li><a href="/window-treatment-cost-calculator/">Cost calculator</a></li>'
            '<li><a href="https://olssonss.com">Olsson Smart Shades</a></li><li><a href="tel:+16149070976">(614) 907-0976</a></li></ul></div></div>'
            '<div class="bottom"><span>&copy; 2026 Central Ohio Window Guide</span>'
            '<p class="disclosure">Published by Olsson Smart Shades, a local Central Ohio installer.</p></div></div></footer>'
            '<script src="/site.js?v=2" defer></script>')

def tile(href, img, alt, cat, title, blurb, extra="", delay=0):
    return (f'<a class="tile rv d{delay}" href="{href}"><div class="ph"><img src="{IMG}{img}" alt="{html.escape(alt)}" width="1300" height="735" loading="lazy"></div>'
            f'<p class="cat">{cat}</p><h3>{title}</h3><p>{blurb}</p>{extra}</a>')

def read_minutes(text):
    return max(2, math.ceil(len(text.split()) / 230))

def fix_head(soup, img_url, desc):
    head = soup.head
    for l in head.find_all("link", rel="stylesheet"):
        l.decompose()
    can = head.find("link", rel="canonical")
    title = soup.title.get_text()
    extra = BeautifulSoup(FONTS +
        f'<meta property="og:type" content="article"><meta property="og:site_name" content="Central Ohio Window Guide">'
        f'<meta property="og:title" content="{html.escape(title)}"><meta property="og:description" content="{html.escape(desc)}">'
        f'<meta property="og:url" content="{can["href"]}"><meta property="og:image" content="{img_url}">'
        '<meta name="twitter:card" content="summary_large_image">', "html.parser")
    can.insert_after(extra)
    # add image to Article schema
    for sc in head.find_all("script", type="application/ld+json"):
        try:
            data = json.loads(sc.string)
        except Exception:
            continue
        items = data if isinstance(data, list) else [data]
        for it in items:
            if it.get("@type") == "Article":
                it["image"] = img_url
                it["dateModified"] = "2026-10-22"
        sc.string = json.dumps(data, ensure_ascii=False, separators=(",", ":"))

def related_for(slug):
    slugs = [g[0] for g in GUIDES]
    if slug in slugs:
        i = slugs.index(slug)
        picks = [GUIDES[(i + k) % len(GUIDES)] for k in (1, 2, 3)]
        return [(f"/{g[0]}/", g[4], g[5], g[1], g[2], g[3]) for g in picks]
    city_slugs = [c[0] for c in CITIES]
    out = [(f"/{GUIDES[1][0]}/", GUIDES[1][4], GUIDES[1][5], GUIDES[1][1], GUIDES[1][2], GUIDES[1][3])]
    i = city_slugs.index(slug) if slug in city_slugs else 0
    for k in (1, 2):
        c = CITIES[(i + k) % len(CITIES)]
        out.append((f"/motorized-shades-{c[0]}-ohio/", c[3], CITY_ALT.format(c[1]), "Neighborhood Guide", c[1], c[2]))
    return out

CALC_CSS = """
.calc{background:var(--paper);border:1px solid var(--hair);border-top:2px solid var(--gold);padding:clamp(20px,4vw,34px);margin:28px 0 36px;font-family:var(--sans);font-size:.95rem;line-height:1.5}
.calc label{display:block;font-size:.64rem;font-weight:500;letter-spacing:.22em;text-transform:uppercase;color:var(--gold-deep);margin:0 0 8px}
.calc select,.calc input{width:100%;font:inherit;font-size:1rem;color:var(--ink);padding:12px 12px;border:1px solid var(--hair);border-radius:0;background:var(--ground);-webkit-appearance:none;appearance:none}
.calc select{background-image:linear-gradient(45deg,transparent 50%,var(--gold) 50%),linear-gradient(135deg,var(--gold) 50%,transparent 50%);background-position:calc(100% - 18px) 52%,calc(100% - 13px) 52%;background-size:5px 5px;background-repeat:no-repeat;padding-right:34px}
.calc select:focus,.calc input:focus{outline:none;border-color:var(--gold)}
.row{display:grid;grid-template-columns:2fr 1fr 1.3fr auto;gap:12px;align-items:end;margin-bottom:14px}
.rm{background:none;border:1px solid var(--hair);padding:11px 14px;cursor:pointer;color:var(--mute);font:inherit}
.rm:hover{border-color:var(--ink);color:var(--ink)}
.add{background:none;border:0;border-bottom:1px solid var(--gold);color:var(--gold-deep);padding:6px 0;cursor:pointer;font:inherit;font-size:.72rem;letter-spacing:.18em;text-transform:uppercase;margin-top:6px}
.result{margin-top:26px;background:var(--night);color:#d9cfbc;padding:26px 28px}
.result>div:first-child{font-size:.64rem;letter-spacing:.26em;text-transform:uppercase;color:#e7c97f}
.result .big{font-family:var(--serif);font-size:clamp(2.2rem,5vw,3rem);color:#fff;line-height:1.15;margin:8px 0 4px}
.result p{margin:6px 0 0;color:#b9ad97;font-size:.92rem}
.result a.btn{margin-top:18px}
@media(max-width:600px){.row{grid-template-columns:1fr 1fr}.row .p{grid-column:1/-1}}
"""

def transform(path):
    slug = path.parent.name
    soup = BeautifulSoup(path.read_text(), "html.parser")
    desc = soup.find("meta", attrs={"name": "description"})["content"]
    art = soup.find("article")
    h1 = art.find("h1")
    meta = art.find("p", class_="meta")

    g = next((x for x in GUIDES if x[0] == slug), None)
    city = next((c for c in CITIES if slug == f"motorized-shades-{c[0]}-ohio"), None)
    if g:
        kicker, img, alt = g[1], g[4], g[5]
    elif city:
        kicker, img, alt = f"Neighborhood Guide &middot; {city[1]}", city[3], CITY_ALT.format(city[1])
    else:  # about
        kicker, img, alt = "About the Guide", "norman-soluna-roller-shades-bedroom-7.webp", "Light-filtering roller shades in a serene bedroom"
    img_url = SITE + IMG + img

    # body nodes after h1/meta
    nodes = [n for n in art.contents if not (isinstance(n, NavigableString) and not n.strip())]
    nodes = [n for n in nodes if n is not h1 and n is not meta]
    dek_html = None
    if nodes and getattr(nodes[0], "name", None) == "p" and not nodes[0].get("class"):
        dek_html = nodes[0].decode_contents()
        nodes = nodes[1:]
    if dek_html is None:
        dek_html = html.escape(desc)
    words = h1.get_text() + " " + " ".join(n.get_text(" ") if hasattr(n, "get_text") else str(n) for n in nodes)
    mins = read_minutes(words)

    body = "".join(str(n) for n in nodes)
    prose = BeautifulSoup(f'<article class="prose" id="content">{body}</article>', "html.parser")
    pr = prose.article
    for h2 in pr.find_all("h2", recursive=False):
        if h2.get_text().strip().lower().startswith(("quick answer", "the short answer")):
            box = prose.new_tag("div", attrs={"class": "answer"})
            nxt = h2.find_next_sibling()
            h2.wrap(box)
            if nxt is not None and nxt.name == "p":
                box.append(nxt.extract())
            break
    first_p = pr.find(recursive=False)
    if first_p is not None and first_p.name == "p" and not first_p.get("class"):
        first_p["class"] = "lead"

    rel = related_for(city[0] if city else slug)
    rel_html = "".join(tile(h, i, a, c, t, b, delay=k + 1) for k, (h, i, a, c, t, b) in enumerate(rel))

    new_body = (
        '<body><div class="progress" aria-hidden="true"></div>' + nav("/" + slug + "/") +
        '<main><header class="story-head">'
        f'<p class="kicker">{kicker}</p><h1>{h1.decode_contents()}</h1><p class="dek">{dek_html}</p>'
        f'<p class="byline"><span>Central Ohio Window Guide</span><span>Updated October 2026</span><span>{mins} min read</span></p></header>'
        f'<figure class="story-hero"><div class="frame"><img src="{IMG}{img}" alt="{html.escape(alt)}" width="1300" height="735" fetchpriority="high"></div>'
        f'<figcaption>{CREDIT}</figcaption></figure>'
        '<div class="story-body"><aside class="toc" aria-label="In this guide"><p>In this guide</p><ol></ol></aside>'
        f'{prose}</div>'
        f'<section class="related"><div class="in"><p class="kicker center" style="text-align:center">Keep reading</p>'
        f'<h2>More from the <em>Guide</em></h2><div class="grid">{rel_html}</div></div></section></main>'
        + footer())

    # keep trailing page scripts (calculator)
    scripts = [str(s) for s in soup.body.find_all("script", recursive=False)]
    new_body = new_body.replace("</main>", "</main>", 1)
    tail = "".join(scripts)
    new_body += tail + "</body>"

    fix_head(soup, img_url, desc)
    st = soup.head.find("style")
    if st is not None and ".calc" in st.get_text():
        st.string = CALC_CSS
    out = "<!doctype html>\n" + str(soup.html).split("<body", 1)[0] + new_body + "</html>\n"
    out = out.replace('<html lang="en">', '<html lang="en">', 1)
    path.write_text(out)

def home():
    soup = BeautifulSoup((PUB / "index.html").read_text(), "html.parser")
    desc = soup.find("meta", attrs={"name": "description"})["content"]
    hero = "norman-normandy-hardwood-plantation-shutters-living-room-with-arched-windows-59.webp"
    fix_head(soup, SITE + IMG + hero, desc)
    soup.head.find("meta", property="og:type")["content"] = "website"
    f = GUIDES[0]
    essentials = [GUIDES[i] for i in (1, 2, 3, 4)]
    tiles = "".join(tile(f"/{g[0]}/", g[4], g[5], g[1], g[2], g[3], delay=(k % 3) + 1) for k, g in enumerate(essentials[:3]))
    idx = "".join(
        f'<li class="rv"><a href="/{g[0]}/"><span class="no">{k:02d}</span><span class="t">{g[2]}<small>{g[3]}</small></span><span class="c">{g[1]}</span></a></li>'
        for k, g in enumerate(GUIDES, 1))
    towns = "".join(f'<a href="/motorized-shades-{c[0]}-ohio/"><span class="n">{c[1]}</span><span class="d">{c[2]}</span></a>' for c in CITIES)
    towns += '<a class="more-town" href="/motorized-shades-cost-central-ohio/"><span class="n">Elsewhere nearby?</span><span class="d">Start with the cost guide &rarr;</span></a>'
    prices = [("Faux wood blinds", "$125–500"), ("Cordless cellular shades", "$175–750"), ("Manual roller shades", "$175–650"),
              ("Motorized roller shades", "$450–1,300"), ("Composite shutters", "$275–1,600")]
    price_html = "".join(f'<div class="rv d{(k % 3) + 1}"><p class="lbl">{l}</p><p class="v">{v}</p><p class="u">per window, installed</p></div>' for k, (l, v) in enumerate(prices))

    body = (
        '<body>' + nav("/") +
        '<main id="content">'
        f'<section class="cover"><div class="bg"><img src="{IMG}{hero}" alt="Stained hardwood plantation shutters with an arched top in a light-filled living room" width="1300" height="735" fetchpriority="high"></div>'
        '<div class="in"><p class="issue">The Autumn 2026 Edition &middot; Columbus &amp; Central Ohio</p>'
        '<h1>Window treatments &amp; smart shades in Central Ohio, <em>explained.</em></h1>'
        '<p class="lede">Honest local guides to smart window automation, motorized shades, shutters and what it all really costs, written for the homes of Columbus.</p>'
        '<p class="cta-row"><a class="btn" href="/motorized-shades-cost-central-ohio/">Read the cost guide <span class="arr">&rarr;</span></a>'
        '<a class="btn light" href="/window-treatment-cost-calculator/">Price my windows</a></p></div></section>'
        '<div class="ledger"><div class="in"><span><b>8</b>In-depth guides</span><span><b>14</b>Neighborhood guides</span>'
        '<span><b>2026</b>Installed prices</span><span><b>Free</b>Cost calculator</span></div></div>'

        '<section class="band"><div class="in"><div class="sec-head rv"><h2>The <em>cover</em> story</h2>'
        '<p>The future-proof home starts at the window. Here is how smart shades actually work in Ohio houses.</p></div>'
        f'<a class="feature rv" href="/{f[0]}/"><div class="ph"><img src="{IMG}{f[4]}" alt="{f[5]}" width="1300" height="735" loading="lazy"></div>'
        f'<div><p class="kicker">{f[1]} &middot; 5 min read</p><h3>{f[2]}</h3><p>{f[3]}</p><span class="more">Read the guide</span></div></a></div></section>'

        '<section class="band paper"><div class="in"><div class="sec-head rv"><h2>The <em>essentials</em></h2>'
        '<p>Start here if you are pricing a project, choosing between styles, or planning a whole house.</p></div>'
        f'<div class="grid">{tiles}</div></div></section>'

        '<section class="band night"><div class="in"><div class="sec-head rv"><h2>The 2026 <em>price index</em></h2>'
        '<p>Typical installed prices per window in Central Ohio, measuring and installation included.</p></div>'
        f'<div class="prices">{price_html}</div>'
        '<p class="note rv">Ranges reflect window size, fabric and options. <a href="/motorized-shades-cost-central-ohio/" style="color:#e7c97f">See the full cost guide</a> or '
        '<a href="/window-treatment-cost-calculator/" style="color:#e7c97f">price your own windows</a>.</p></div></section>'

        '<section class="band"><div class="in"><div class="sec-head rv"><h2>Every guide, <em>in one place</em></h2>'
        '<p>Eight long-form guides, updated for 2026.</p></div>'
        f'<ol class="index">{idx}</ol></div></section>'

        '<section class="band paper" id="neighborhoods"><div class="in"><div class="sec-head rv"><h2>Neighborhood <em>guides</em></h2>'
        '<p>What works for the windows, light and housing styles of each Central Ohio community.</p></div>'
        f'<div class="towns rv">{towns}</div></div></section>'

        '<section class="band quote-band"><div class="in"><blockquote class="rv">The right window treatment is the one that fits how you live in a room, '
        'the light it gets, and the windows it actually has.</blockquote></div></section>'

        '<section class="band stripe"><div class="in"><div class="publisher">'
        f'<div class="ph rv"><img src="{IMG}norman-soluna-roller-shades-bedroom-7.webp" alt="Light-filtering roller shades in a serene bedroom" width="1300" height="735" loading="lazy"></div>'
        '<div class="rv d1"><p class="kicker">From the publisher</p><h2>Need a <em>local installer?</em></h2>'
        '<p>This guide is published by <a href="https://olssonss.com">Olsson Smart Shades</a>, which designs and installs custom and motorized '
        'window treatments across Columbus and Central Ohio. Free in-home consultations, real samples in your own light, and a written quote before anything is ordered.</p>'
        '<p class="cta-row"><a class="btn" href="https://olssonss.com/quote">Book a free consultation <span class="arr">&rarr;</span></a>'
        '<a class="btn ghost" href="tel:+16149070976">(614) 907-0976</a></p></div></div></div></section>'
        '</main>' + footer() + '</body>')
    out = "<!doctype html>\n" + str(soup.html).split("<body", 1)[0] + body + "</html>\n"
    (PUB / "index.html").write_text(out)

if __name__ == "__main__":
    for p in sorted(PUB.glob("*/index.html")):
        transform(p)
        print("ok", p.parent.name)
    home()
    print("ok home")
