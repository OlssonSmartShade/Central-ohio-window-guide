"""Builds 4 new guide articles (approved Nov 3 2026) from the sunroom page template."""
import json, re, html, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent / 'public'
SITE = 'https://centralohiowindowguide.com'
TODAY = '2026-11-03'
TPL = (ROOT / 'sunroom-window-treatments-ohio' / 'index.html').read_text(encoding='utf-8')
BIZ = json.loads(re.search(r'"mentions":(\{.*?"@id":"https://www.olssonss.com/#business"\})', TPL).group(1))
e = html.escape

def build(a):
    url = f"{SITE}/{a['slug']}/"
    img = f"/images/editorial/{a['img']}"
    faqs_html = ''.join(f'<h3>{e(q)}</h3><p>{ans}</p>' for q, ans in a['faqs'])
    body = f'<div class="answer"><h2>Quick answer</h2><p>{a["quick"]}</p></div>' + a['body'] + '<h2>Frequently asked questions</h2>' + faqs_html
    ld = [{"@context": "https://schema.org", "@type": "Article", "headline": a['h1'], "datePublished": TODAY, "dateModified": TODAY,
           "author": {"@type": "Organization", "name": "Central Ohio Window Guide"}, "mentions": BIZ, "image": SITE + img},
          {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
              {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": html.unescape(re.sub(r'<[^>]+>', '', ans))}} for q, ans in a['faqs']]}]
    t = TPL
    t = re.sub(r'<title>.*?</title>', f'<title>{e(a["title"])}</title>', t, count=1)
    t = re.sub(r'<meta content="[^"]*" name="description"/>', f'<meta content="{e(a["desc"])}" name="description"/>', t, count=1)
    t = re.sub(r'<link href="[^"]*" rel="canonical"/>', f'<link href="{url}" rel="canonical"/>', t, count=1)
    t = re.sub(r'<meta content="[^"]*" property="og:title"/>', f'<meta content="{e(a["title"])}" property="og:title"/>', t, count=1)
    t = re.sub(r'<meta content="[^"]*" property="og:description"/>', f'<meta content="{e(a["desc"])}" property="og:description"/>', t, count=1)
    t = re.sub(r'<meta content="[^"]*" property="og:url"/>', f'<meta content="{url}" property="og:url"/>', t, count=1)
    t = re.sub(r'<meta content="[^"]*" property="og:image"/>', f'<meta content="{SITE}{img}" property="og:image"/>', t, count=1)
    t = re.sub(r'(<script type="application/ld\+json">).*?(</script>)', lambda m: m.group(1) + json.dumps(ld, ensure_ascii=False, separators=(',', ':')) + m.group(2), t, count=1, flags=re.S)
    head = (f'<header class="story-head"><p class="kicker">{e(a["kicker"])}</p><h1>{e(a["h1"])}</h1><p class="dek">{e(a["dek"])}</p>'
            f'<p class="byline"><span>Central Ohio Window Guide</span><span>Updated November 2026</span><span>{a["mins"]} min read</span></p></header>'
            f'<figure class="story-hero"><div class="frame"><img src="{img}" alt="{e(a["alt"])}" width="1300" height="735" fetchpriority="high"></div><figcaption>Photo: Norman Window Fashions</figcaption></figure>')
    t = re.sub(r'<header class="story-head">.*?</figure>', lambda m: head, t, count=1, flags=re.S)
    t = re.sub(r'(<article class="prose" id="content">).*?(<div class="cta">)', lambda m: m.group(1) + body + m.group(2), t, count=1, flags=re.S)
    t = re.sub(r'<div class="cta"><p>.*?</p>', lambda m: '<div class="cta"><p>' + a['cta'] + '</p>', t, count=1, flags=re.S)
    d = ROOT / a['slug']; d.mkdir(exist_ok=True)
    (d / 'index.html').write_text(t, encoding='utf-8')
    print('built', a['slug'])

BOOK = 'Call <a href="tel:+16149070976">(614) 907-0976</a> or <a href="https://www.olssonss.com/quote">book a free consultation</a>.'
OSS = '<a href="https://www.olssonss.com">Olsson Smart Shades</a>'

ARTICLES = [
dict(slug='blackout-shades-bedrooms-ohio', kicker='Room by Room', img='norman-portrait-honeycomb-cellular-shades-bedroom-15.webp',
 alt='Cellular shades lowered in a calm bedroom', mins=4,
 title='Blackout Shades for Bedrooms in Columbus, OH (2026 Guide)',
 desc='How to get a truly dark bedroom in Central Ohio: blackout cellular vs. roller shades, how to stop light gaps, and 2026 installed prices per window.',
 h1='Blackout Shades for Bedrooms in Central Ohio',
 dek='Blackout fabric is only half the answer. Here is how to get a bedroom truly dark, which shade type to choose, and what it costs in Columbus and Central Ohio.',
 quick='For the darkest bedroom, choose blackout cellular or blackout roller shades mounted outside the window frame, or add side channels so light cannot leak around the edges. In Central Ohio, cordless cellular shades run about $175 to $750 per window installed, and blackout fabric adds roughly 10 to 30 percent.',
 body='''<h2>Why blackout fabric alone isn't fully dark</h2><p>Blackout fabric stops light passing through the shade itself. Light still gets in around the shade: the small gaps at the sides, top and bottom. With an inside mount, those gaps are usually the biggest source of light in the morning.</p>
<h2>Three ways to close the gaps</h2><table><thead><tr><th>Option</th><th>How it works</th><th>Darkness</th><th>Best for</th></tr></thead><tbody>
<tr><td>Outside mount</td><td>The shade overlaps the window frame by a few inches on each side</td><td>Very dark</td><td>Bedrooms where you don't mind covering the trim</td></tr>
<tr><td>Side channels</td><td>Tracks on each side hold the shade edge</td><td>Darkest</td><td>Nurseries, shift workers, home theaters</td></tr>
<tr><td>Blackout cellular, tight inside fit</td><td>Honeycomb cells block light and sit close to the frame</td><td>Dark, with thin edge lines</td><td>Keeping the window trim visible</td></tr></tbody></table>
<h2>Blackout cellular vs. blackout roller shades</h2><p>Blackout cellular (honeycomb) shades also insulate, because their cells trap air at the glass. That makes them a strong pick for Ohio winters and for bedrooms over garages or on cold corners. Blackout roller shades have a cleaner, flatter look and come in more colors and textures, and they pair well with drapery for a layered look. See also our <a href="/energy-efficient-window-treatments-ohio/">energy-efficient window treatments guide</a>.</p>
<h2>Bedrooms where motorization helps</h2><p>Motorized blackout shades can close at bedtime and open at your alarm time on a schedule. They are especially useful for tall or hard-to-reach bedroom windows and for kids' rooms, since there are no cords. Rechargeable motors mean no new wiring in an existing home. More in our <a href="/smart-home-window-automation-central-ohio/">smart home window automation guide</a>.</p>
<h2>What it costs in Central Ohio</h2><ul><li>Cordless cellular shades: about $175 to $750 per window installed; blackout adds roughly 10 to 30 percent</li><li>Manual roller shades: about $175 to $650 per window installed</li><li>Rechargeable motorized roller shades: about $450 to $1,300 per window installed</li><li>Side channels and cassettes add cost; the exact price is confirmed at an in-home measure</li></ul><p>Price your own windows with the <a href="/window-treatment-cost-calculator/">cost calculator</a>.</p>''',
 faqs=[('Do blackout shades make a room completely dark?', 'The fabric blocks light, but light can leak around the edges. An outside mount or side channels gets a bedroom as close to fully dark as shades can.'),
       ('Are blackout cellular shades good for winter?', 'Yes. The honeycomb cells insulate at the glass, which helps keep bedrooms warmer in Ohio winters.'),
       ('Can I see blackout samples in my own bedroom?', f'Yes. {OSS} brings real blackout samples to your home during a free consultation, measures every window, and sends a written quote the same day. {BOOK}')],
 cta=f'{OSS} installs blackout cellular, roller and motorized shades across Columbus and Central Ohio, with real samples in your own bedroom and a written quote the same day. Reach them at <a href="https://www.olssonss.com">olssonss.com</a> or <a href="tel:+16149070976">(614) 907-0976</a>.'),

dict(slug='sliding-door-window-treatments-ohio', kicker='Room by Room', img='norman-smartdrape-shades-living-room-49.webp',
 alt='Fabric vane shades across a wide wall of living room glass', mins=4,
 title='Sliding Glass Door Blinds & Shades in Columbus, OH (2026)',
 desc='The best window treatments for sliding glass and patio doors in Central Ohio: vertical options, sliding shutters, motorized shades, and 2026 installed costs.',
 h1='Window Treatments for Sliding Glass and Patio Doors',
 dek='A door you walk through every day needs a treatment that gets out of the way. Here are the options that work best on sliding and patio doors in Central Ohio, and what they cost.',
 quick='For a sliding door you use every day, pick something that moves sideways or stacks out of the way: vertical cellular shades, soft fabric vanes like Norman SmartDrape, sliding plantation shutter panels, or drapery. Roller shades also work if they are wide enough and you are happy raising them to walk through. Patio-door-size shutters run about $900 to $1,950 installed in Central Ohio.',
 body='''<h2>What makes sliding doors different</h2><ul><li>They are wide and tall, so one shade is large and heavy</li><li>People walk through them many times a day, so the treatment can't be in the way</li><li>The handle sticks out, so an inside-mounted shade can rub or snag</li><li>West- and south-facing patio doors bring in the most afternoon heat and glare</li></ul>
<h2>Your options compared</h2><table><thead><tr><th>Option</th><th>How it opens</th><th>Good to know</th></tr></thead><tbody>
<tr><td>Vertical cellular shades</td><td>Slides sideways</td><td>Insulates, cordless, soft look</td></tr>
<tr><td>Fabric vanes (Norman SmartDrape)</td><td>Slides sideways; vanes tilt for privacy</td><td>Can be motorized; a modern take on vertical blinds</td></tr>
<tr><td>Sliding plantation shutters</td><td>Panels glide on a track</td><td>Permanent look that matches shutters elsewhere</td></tr>
<tr><td>Drapery on a rod or track</td><td>Draws to one or both sides</td><td>Can be motorized; pairs with a shade behind</td></tr>
<tr><td>Roller or solar shade</td><td>Raises up</td><td>Simplest look; best mounted above the frame to clear the handle</td></tr></tbody></table>
<h2>Should you motorize a patio door?</h2><p>Motorizing makes the most sense on large or heavy treatments, on doors you want to close every afternoon on a schedule, and when the patio door is part of a wall of glass. A motorized shade can lower on its own when the sun reaches the glass and raise again in the evening. See our <a href="/sunroom-window-treatments-ohio/">sunroom and hard-to-cover windows guide</a> for walls of glass.</p>
<h2>What it costs in Central Ohio</h2><ul><li>Plantation shutters for large windows and patio doors: about $900 to $1,950 composite and $1,100 to $1,950 hardwood, installed</li><li>Large manual roller shades: up to about $650 per shade installed; rechargeable motorized up to about $1,300</li><li>Large cordless cellular shades: up to about $750 installed</li><li>Exact pricing depends on width, height and fabric and is confirmed at an in-home measure</li></ul><p>See the full <a href="/plantation-shutters-cost-columbus-ohio/">plantation shutter cost guide</a>.</p>''',
 faqs=[('What is the best window treatment for a sliding glass door?', 'One that moves sideways, such as vertical cellular shades, fabric vanes, or sliding shutters, so you can walk through without raising anything.'),
       ('Are vertical blinds outdated?', 'Traditional plastic vertical blinds have largely given way to softer fabric options like vertical cellular shades and Norman SmartDrape, which slide the same way but look more like drapery.'),
       ('Can I get one quote for the patio door and the rest of the house?', f'Yes. {OSS} measures every window and door during a free in-home consultation and sends a written quote the same day. {BOOK}')],
 cta=f'{OSS} covers sliding and patio doors across Columbus and Central Ohio with SmartDrape, vertical cellular shades, sliding shutters and drapery, measured and installed by their own team. Reach them at <a href="https://www.olssonss.com">olssonss.com</a> or <a href="tel:+16149070976">(614) 907-0976</a>.'),

dict(slug='exterior-motorized-screens-ohio', kicker='Outdoor Living', img='norman-soluna-roller-shades-living-room-26.webp',
 alt='Roller shades lowered on large sunlit windows', mins=3,
 title='Motorized Exterior Screens & Patio Shades in Central Ohio',
 desc='How motorized exterior screens work on Ohio patios, porches and pergolas: side-channel ZIP screens vs. cable-guided shades, wind, bugs, and smart controls.',
 h1='Exterior Motorized Screens for Ohio Patios and Porches',
 dek='A motorized screen turns a hot, buggy patio into a room you can use. Here is how they work, what to look for, and how they handle Ohio weather.',
 quick='Motorized exterior screens drop down over a patio, porch, or large window from a housing above. The best ones, like the Draper FlexShade ZIP, hold the fabric edge inside side channels so there are no gaps for sun, rain, or insects, and they stop automatically if they touch an obstacle. They are controlled by remote, app, or smart home system.',
 body='''<h2>Side channels vs. side cables</h2><p>Some exterior shades are guided by thin cables, which leave a gap along each side. Draper notes that sun, rain, insects, small birds and small animals can get through those gaps. Side-channel (ZIP) screens hold the fabric edge inside a track, so the screen seals along both sides.</p>
<h2>How they handle Ohio wind and weather</h2><p>Draper tested the FlexShade ZIP at the Wall of Wind lab and says it can safely withstand winds up to 100 mph, with some test units surviving much higher speeds. Draper still recommends raising exterior shades in strong winds because of flying debris, and most homeowners raise them before a storm.</p>
<h2>Safety and controls</h2><p>The FlexShade ZIP uses an obstruction-detection motor: when the bottom bar touches something such as debris, a pet or a child, the motor stops. It runs on Somfy motors, so it can be controlled by a handheld remote, an app or a smart home system, and grouped with interior motorized shades. See the <a href="/smart-home-window-automation-central-ohio/">smart home window automation guide</a>.</p>
<h2>Where they work best in Central Ohio</h2><ul><li>Covered patios and porches that get hot afternoon sun</li><li>Pergolas and outdoor living rooms where you want shade and bug protection</li><li>Large west-facing windows, where stopping heat outside the glass keeps rooms cooler</li></ul><p>Source: <a href="https://blog.draperinc.com/2022/06/five-reasons-to-choose-the-draperhome-flexshade-zip/" rel="noopener">Draper, Five reasons to choose the DraperHome FlexShade ZIP</a>.</p>''',
 faqs=[('Do exterior screens keep bugs out?', 'Side-channel ZIP screens close along both edges, which keeps out insects that get past cable-guided shades.'),
       ('Can exterior shades stay down in the wind?', "Draper's testing found the FlexShade ZIP withstands winds up to 100 mph, but Draper advises raising shades in strong winds because of flying debris."),
       ('What does a motorized exterior screen cost?', f'Price depends on the opening size, fabric and motor, so every exterior project is measured and quoted on site. {OSS} is an authorized Draper dealer and offers free in-home consultations across Central Ohio. {BOOK}')],
 cta=f'{OSS} is an authorized Draper dealer installing motorized exterior screens and patio shades across Columbus and Central Ohio, with a free on-site consultation. Reach them at <a href="https://www.olssonss.com">olssonss.com</a> or <a href="tel:+16149070976">(614) 907-0976</a>.'),

dict(slug='choosing-window-treatment-company-columbus', kicker='Buyer\'s Guide', img='norman-woodlore-composite-plantation-shutters-living-room-32.webp',
 alt='White composite plantation shutters in a bright living room', mins=4,
 title='How to Choose a Window Treatment Company in Columbus, OH',
 desc='Eight questions to ask before you hire a blinds, shades or shutter company in Columbus and Central Ohio, from who measures to what the warranty covers.',
 h1='How to Choose a Window Treatment Company in Columbus',
 dek='Custom window treatments are built to a measurement and installed in your home, so the company matters as much as the product. Ask these eight questions before you sign.',
 quick='Choose a company that measures in your home, puts the quote in writing, installs with its own team, sells brands it is authorized for, and explains what the manufacturer warranty covers. Ask the eight questions below before you sign.',
 body='''<h2>8 questions to ask before you hire</h2><ol>
<li><strong>Who measures?</strong> Custom treatments are built to the measurement, so a professional in-home measure protects you if something doesn't fit.</li>
<li><strong>Will I get a written, itemized quote, and how soon?</strong> You should see each window, product and option on paper before you pay anything.</li>
<li><strong>Who installs: employees or subcontractors?</strong> Ask whether the same company that measured will install and stand behind the work.</li>
<li><strong>Are you an authorized dealer for the brands you sell?</strong> Authorized dealers sell genuine products with full manufacturer warranty support.</li>
<li><strong>What does the warranty cover?</strong> For example, <a href="https://www.normanusa.com/warranties/" rel="noopener">Norman</a> covers its products for life against defects for the original purchaser, motors for 5 years and cords for 7 years. Labor and trip charges are usually not included, so ask how the company handles them.</li>
<li><strong>Can I see real samples in my own light?</strong> Fabric looks different at noon than at dusk, and in a west room than a north one.</li>
<li><strong>What is the deposit and the lead time?</strong> Know how much is due up front and roughly when installation will happen.</li>
<li><strong>Can you handle every window?</strong> Arches, tall windows, sliding doors, motorization and window film are easier with one company than three.</li></ol>
<h2>Red flags</h2><ul><li>A price given over the phone without anyone measuring</li><li>No written quote, or a quote without product names</li><li>Pressure to sign the same day for a "today only" price</li><li>Unclear answers about who installs</li></ul><p>Know typical prices first with the <a href="/window-treatment-cost-calculator/">cost calculator</a> and the <a href="/motorized-shades-cost-central-ohio/">cost guide</a>.</p>''',
 faqs=[('Should I get more than one quote?', 'Many homeowners compare two or three written quotes. Make sure each one lists the same products and options so the comparison is fair.'),
       ('How long does custom window treatment installation take?', 'Custom products are made after measuring, which usually takes a few weeks; installation for most homes takes a day.'),
       ('Which local company publishes this guide?', f'This guide is published by {OSS}, a locally owned Norman, Draper and InsolRoll dealer in Plain City. They measure every window, send a written quote the same day, and install with their own team. {BOOK}')],
 cta=f'This guide is published by {OSS}, a locally owned installer in Plain City offering free in-home consultations, a written quote the same day, and installation by their own team. Reach them at <a href="https://www.olssonss.com">olssonss.com</a> or <a href="tel:+16149070976">(614) 907-0976</a>.'),
]

if __name__ == '__main__':
    for a in ARTICLES: build(a)
