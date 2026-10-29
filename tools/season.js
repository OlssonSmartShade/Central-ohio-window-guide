#!/usr/bin/env node
// Seasonal homepage refresh for centralohiowindowguide.com
// Rewrites the <!--season:*--> blocks in public/index.html for the current
// season (America/New_York). Run daily by .github/workflows/seasonal-update.yml;
// it only commits when the season actually changes.
// Test a date: SEASON_DATE=2027-01-15 node tools/season.js
const fs = require('fs');
const path = require('path');

const FILE = path.join(__dirname, '..', 'public', 'index.html');
const now = process.env.SEASON_DATE ? new Date(process.env.SEASON_DATE + 'T12:00:00Z') : new Date();
const parts = new Intl.DateTimeFormat('en-US', { timeZone: 'America/New_York', year: 'numeric', month: 'numeric' }).formatToParts(now);
const year = +parts.find(p => p.type === 'year').value;
const month = +parts.find(p => p.type === 'month').value;

let key, label;
if (month === 12) { key = 'winter'; label = `Winter ${year}–${String(year + 1).slice(2)}`; }
else if (month <= 2) { key = 'winter'; label = `Winter ${year - 1}–${String(year).slice(2)}`; }
else if (month <= 5) { key = 'spring'; label = `Spring ${year}`; }
else if (month <= 8) { key = 'summer'; label = `Summer ${year}`; }
else { key = 'autumn'; label = `Autumn ${year}`; }

const SEASONS = {
  winter: {
    kicker: 'This winter in Central Ohio',
    h2: 'Short days, cold glass, <em>warmer rooms.</em>',
    p: 'Ohio winters pull heat straight through bare windows. Cellular (honeycomb) shades trap a layer of air at the glass, and motorized shades can close automatically at sunset when the temperature drops. Winter is also the quiet season for installers, so measure-to-install moves faster.',
    links: [['/shades-vs-blinds-vs-shutters-ohio/', 'Which insulates best'], ['/motorized-shades-cost-central-ohio/', 'See 2026 prices']]
  },
  spring: {
    kicker: 'This spring in Central Ohio',
    h2: 'Plan now, <em>before the summer sun.</em>',
    p: 'Custom shades and shutters take several weeks from order to install, so spring is the time to measure if you want west-facing rooms and sunrooms covered before the July heat. It is also when new-construction homes in Powell, Plain City and Delaware close and need privacy fast.',
    links: [['/sunroom-window-treatments-ohio/', 'Sunrooms & tough windows'], ['/window-treatment-cost-calculator/', 'Price my windows']]
  },
  summer: {
    kicker: 'This summer in Central Ohio',
    h2: 'Beat the west sun <em>without the blackout.</em>',
    p: 'Afternoon sun is the hottest light an Ohio house gets. Solar shades cut glare and heat while keeping the view, ceramic window film blocks UV that fades floors and furniture, and motorized shades can lower themselves on schedule while you are at work.',
    links: [['/window-film-for-homes-ohio/', 'Home window film guide'], ['/smart-home-window-automation-central-ohio/', 'Smart shade schedules']]
  },
  autumn: {
    kicker: 'This fall in Central Ohio',
    h2: 'Order now, <em>home for the holidays.</em>',
    p: 'Custom window treatments take several weeks to make, so fall orders are what get installed before family arrives for the holidays. It is also the time to add insulating cellular shades before heating season, and to motorize the tall windows you will not want to reach all winter.',
    links: [['/motorized-shades-cost-central-ohio/', 'Read the cost guide'], ['/shades-vs-blinds-vs-shutters-ohio/', 'Compare your options']]
  }
};

const s = SEASONS[key];
const band =
  `<section class="band stripe" id="this-season"><div class="in"><div class="ix-head center rv">` +
  `<p class="kicker">${s.kicker}</p><h2>${s.h2}</h2><p>${s.p}</p></div>` +
  `<p class="cta-row rv" style="display:flex;justify-content:center;flex-wrap:wrap;gap:12px;margin:0">` +
  `<a class="btn" href="${s.links[0][0]}">${s.links[0][1]} <span class="arr">&rarr;</span></a>` +
  `<a class="btn ghost" href="${s.links[1][0]}">${s.links[1][1]}</a></p></div></section>`;

const blocks = {
  topline: `Updated for ${label}`,
  edition: `The ${label} Edition`,
  band
};

let html = fs.readFileSync(FILE, 'utf8');
const before = html;
for (const [name, value] of Object.entries(blocks)) {
  const re = new RegExp(`<!--season:${name}-->[\\s\\S]*?<!--/season:${name}-->`);
  if (!re.test(html)) { console.error(`Missing marker: season:${name}`); process.exit(1); }
  html = html.replace(re, `<!--season:${name}-->${value}<!--/season:${name}-->`);
}

if (html === before) {
  console.log(`No change — already ${label}.`);
} else {
  fs.writeFileSync(FILE, html);
  console.log(`Homepage updated for ${label}.`);
}
