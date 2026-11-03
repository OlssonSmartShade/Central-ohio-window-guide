"""One-off content additions for AI-visibility pass (Nov 2026).
Adds new sections + FAQs (visible and in FAQPage schema) to thin guides and Dublin page.
Run: python3 tools/add_content.py  (idempotent: skips a page that already has its marker)."""
import json, re, html, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent / 'public'
TODAY = '2026-11-03'

def faq_html(faqs, heading=True):
    out = '<h2>Frequently asked questions</h2>' if heading else ''
    for q, a in faqs:
        out += f'<h3>{html.escape(q)}</h3><p>{a}</p>'
    return out

def strip(a):
    return html.unescape(re.sub(r'<[^>]+>', '', a))

def patch(slug, marker, body_html, faqs, include_existing_faqs, insert_before='<div class="cta">', title=None, wpm_bump=0):
    f = ROOT / slug / 'index.html'
    t = f.read_text(encoding='utf-8')
    if marker in t:
        print('skip', slug); return
    # schema
    existing = []
    def fix(m):
        d = json.loads(m.group(2))
        items = d if isinstance(d, list) else [d]
        for o in items:
            if o.get('@type') == 'FAQPage':
                existing.extend((q['name'], q['acceptedAnswer']['text']) for q in o['mainEntity'])
                for q, a in faqs:
                    o['mainEntity'].append({'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': strip(a)}})
            if o.get('@type') == 'Article':
                o['dateModified'] = TODAY
        return m.group(1) + json.dumps(d, ensure_ascii=False, separators=(',', ':')) + m.group(3)
    t = re.sub(r'(<script type="application/ld\+json">)(.*?)(</script>)', fix, t, flags=re.S)
    visible = list(existing) if include_existing_faqs else []
    visible += faqs
    block = f'<!--{marker}-->' + body_html + faq_html(visible, heading=include_existing_faqs)
    assert t.count(insert_before) == 1, (slug, insert_before)
    t = t.replace(insert_before, block + insert_before)
    t = t.replace('Updated October 2026', 'Updated November 2026')
    if title:
        t = re.sub(r'<title>.*?</title>', f'<title>{html.escape(title)}</title>', t, count=1)
        t = re.sub(r'<meta content="[^"]*" property="og:title"/>', f'<meta content="{html.escape(title)}" property="og:title"/>', t, count=1)
    f.write_text(t, encoding='utf-8')
    print('patched', slug)

# ---------------- Child & pet safe ----------------
patch('child-pet-safe-cordless-window-treatments', 'ai-pass-nov26', '''
<h2>What changed in 2018, and what it means for older blinds</h2>
<p>At the end of 2018 a new U.S. industry safety standard, ANSI/WCMA A100.1-2018, took effect. It requires stock window coverings, the ready-made blinds and shades sold off the shelf, to be cordless or to have cords that are short or out of reach. Custom, made-to-measure products can still be ordered with cords, so the safest choice in a custom order is to ask for cordless or motorized operation from the start.</p>
<p>Many Central Ohio homes still have blinds that were installed before that change. If your blinds have long pull cords, looped beaded chains, or inner cords you can pull out between the slats, they were made to an older standard. Replacing them in children's rooms and the rooms where kids play is the single biggest safety upgrade you can make at the window.</p>
<h2>Cordless options compared</h2>
<table><thead><tr><th>Option</th><th>How it works</th><th>Best for</th></tr></thead><tbody>
<tr><td>Cordless lift</td><td>Push up or pull down the bottom rail by hand</td><td>Bedrooms, nurseries, most standard windows</td></tr>
<tr><td>Motorized</td><td>Remote, phone app, voice, or a schedule</td><td>Large, high, or hard-to-reach windows, and whole-home safety</td></tr>
<tr><td>Wand tilt</td><td>A rigid wand turns the slats instead of a cord</td><td>Faux wood and wood blinds</td></tr>
<tr><td>Plantation shutters</td><td>Hinged panels with a tilt rod, no cords at all</td><td>Living areas and rooms where pets watch the window</td></tr>
</tbody></table>
<p>Cordless cellular shades typically run about $175 to $750 per window installed in Central Ohio, and rechargeable motorized roller shades about $450 to $1,300, depending on size. Use the <a href="/window-treatment-cost-calculator/">cost calculator</a> for your own windows.</p>
''', [
    ('Are custom blinds still sold with cords?', 'Yes. The 2018 safety standard made stock, off-the-shelf blinds cordless, but custom products can still be ordered with cords. For homes with children or pets, ask for cordless lift or motorized operation when you order.'),
    ('Are motorized shades safe for pets?', 'Yes. Motorized shades have no cords or chains, and the motor stops when the shade reaches its set limit. Many families also set a schedule so the shades raise and lower on their own, which keeps pets from pulling at the bottom rail.'),
    ('How do I make my existing corded blinds safer?', 'Until you replace them, keep cords wrapped up high on a cleat, move cribs, beds and furniture away from windows, and remove looped cords. Replacing them with cordless or motorized products is the permanent fix.'),
], include_existing_faqs=True)

# ---------------- Sunroom ----------------
patch('sunroom-window-treatments-ohio', 'ai-pass-nov26', '''
<h2>Heat, glare and fading in an Ohio sunroom</h2>
<p>A sunroom has far more glass than any other room, so it heats up fastest in summer, loses heat fastest in winter, and lets in the most UV. That UV is what fades flooring, rugs and furniture over time. The goal in most Central Ohio sunrooms is to cut glare and heat in the afternoon while keeping the view of the yard, then add some insulation for winter.</p>
<h2>Solar shade openness, explained</h2>
<p>Solar shades are rated by openness, the percentage of the fabric that is open weave. The lower the number, the more glare, heat and UV the shade blocks, and the less of the view you see.</p>
<table><thead><tr><th>Openness</th><th>View</th><th>Glare and heat control</th><th>Good for</th></tr></thead><tbody>
<tr><td>1%</td><td>Softest view</td><td>Highest</td><td>West-facing glass and rooms with TVs or screens</td></tr>
<tr><td>3%</td><td>Clear view</td><td>High</td><td>Most sunrooms and family rooms, a common balance</td></tr>
<tr><td>5% to 10%</td><td>Clearest view</td><td>Moderate</td><td>Shaded or north-facing windows where the view comes first</td></tr>
</tbody></table>
<p>Darker fabric colors generally give a clearer view out than light colors at the same openness. Bring samples into the room and look at them in your own afternoon light before you decide. Solar shades do not give privacy at night when the lights are on inside; for that, pair them with a light-filtering or blackout layer, or choose dual roller shades.</p>
''', [
    ('Do solar shades give privacy at night?', 'No. Solar shades give daytime privacy, but at night with the lights on inside, people outside can see in. For night privacy, use dual roller shades that pair a solar fabric with a light-filtering or blackout fabric, or add a second treatment.'),
    ('What solar shade openness is best for a sunroom?', 'Three percent is a common balance for Central Ohio sunrooms: a clear view with strong glare and heat control. One percent suits hot west-facing glass, and five to ten percent suits shaded windows where the view matters most.'),
    ('Should I motorize sunroom shades?', 'For a wall of windows or any glass you cannot reach easily, yes. Motorized shades can lower together with one tap or on a schedule, such as every afternoon when the sun reaches the glass.'),
], include_existing_faqs=True)

# ---------------- Shades vs blinds vs shutters ----------------
patch('shades-vs-blinds-vs-shutters-ohio', 'ai-pass-nov26', '''
<h2>Lifespan and upkeep</h2>
<table><thead><tr><th></th><th>Shades</th><th>Blinds</th><th>Plantation shutters</th></tr></thead><tbody>
<tr><td>What wears first</td><td>Fabric and lift parts</td><td>Slats and cords</td><td>Very little; panels are built into the window frame</td></tr>
<tr><td>Typical life</td><td>Many years</td><td>Many years</td><td>Decades</td></tr>
<tr><td>Cleaning</td><td>Vacuum with a soft brush; spot clean</td><td>Dust slats; faux wood wipes clean</td><td>Dust or wipe the louvers</td></tr>
<tr><td>Kitchens and baths</td><td>Choose moisture-resistant roller fabrics</td><td>Faux wood handles humidity; real wood does not</td><td>Composite handles humidity; hardwood is better in dry rooms</td></tr>
</tbody></table>
<h2>When to mix them</h2>
<p>Most Central Ohio homes end up with more than one type. A common plan is shutters on the street-facing front rooms for a uniform look from outside, blackout cellular or roller shades in bedrooms, faux wood blinds or composite shutters in kitchens and baths where moisture matters, and motorized solar shades on big west-facing glass. Keeping colors consistent from room to room makes a mix look intentional.</p>
''', [
    ('Which is cheapest: shades, blinds or shutters?', 'Blinds are usually the least expensive, at about $150 to $600 per window installed in Central Ohio. Manual shades start around $175, and plantation shutters cost the most, from about $275 for a small window to $1,950 for a large opening or patio door.'),
    ('Which lasts the longest?', 'Plantation shutters. They are mounted to the window frame, have no fabric or cords to wear out, and commonly last for decades. Shades and blinds last many years but are usually replaced sooner.'),
], include_existing_faqs=True)

# ---------------- Dublin ----------------
patch('motorized-shades-dublin-ohio', 'ai-pass-nov26', '', [
    ('How much do window treatments cost in Dublin, Ohio?', 'Installed, custom faux wood blinds run about $150 to $500 per window, cordless cellular shades $175 to $750, rechargeable motorized roller shades $450 to $1,300, and composite plantation shutters $275 to $1,950, depending on size and options. Whole-home projects are priced room by room after an in-home measurement.'),
    ('Can I get a free window treatment consultation in Dublin?', 'Yes. <a href="https://www.olssonss.com/quote">Olsson Smart Shades</a> offers free in-home consultations in Dublin: they bring real samples, measure every window, and send a written quote the same day. Call <a href="tel:+16149070976">(614) 907-0976</a>.'),
    ('What are automated blinds and motorized window coverings?', 'They are blinds and shades moved by a small motor and controlled by remote, phone app, voice assistant, or schedule. Most use rechargeable battery motors, so they can be added to existing Dublin homes without opening walls; hardwired motors are an option in new builds.'),
], include_existing_faqs=False, insert_before='<h2>Nearby guides</h2>',
   title='Dublin, OH Window Treatments: Blinds & Motorized Shades')
