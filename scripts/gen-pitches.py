#!/usr/bin/env python3
"""Generates site/pitches.html (the hub) and one notebook-style page per hotel.

Run: python3 scripts/gen-pitches.py   (then node scripts/build-app.mjs)

Each hotel gets its own palette + fonts so the page feels like a travel-guide
notebook made *for* that hotel's vibe. Nothing here uses a hotel's logo or
claims to be from the hotel — these are Brianne's own pitch drafts.
Items flagged confirm=True show a "confirm" stamp: they still need checking.
"""
import html, os

ROOT = os.path.join(os.path.dirname(__file__), '..', 'site')
CDN = 'https://cdn.jsdelivr.net/gh/briannepark/ugc-portfolio@main/site/media/pitches/'

TAGS = {
    'here': ('At the hotel', 'here'),
    'walk': ('Walkable', 'walk'),
    'ride': ('Short ride', 'ride'),
    'trip': ('Worth the trip', 'trip'),
}

HOTELS = [
 dict(
  slug='nomad', no='01', city='New York City', name='The Ritz-Carlton, NoMad', short='Ritz-Carlton NoMad', addr='25 W 28th St, New York, NY 10001', site='https://www.ritzcarlton.com/en/hotels/new-york/nomad',
  tagline='A skyline stay, with the whole city a short walk away.',
  hand='golden hour, 50 floors up',
  fonts='Cormorant+Garamond:ital,wght@0,400;0,600;1,400&family=Poppins:wght@300;400;500&family=Nothing+You+Could+Do',
  head="'Cormorant Garamond',Georgia,serif", body="'Poppins',sans-serif",
  c=dict(desk='#0d1120', paper='#f7f1e3', ink='#1a2038', accent='#b8934a', accent2='#1f2a52', soft='#efe5cd'),
  vibe=['Deep navy', 'Champagne gold', 'Warm lamplight'],
  facts=[
   'Oversize windows and gold-link light fixtures in the rooms.',
   'Bazaar Meat by José Andrés, in the hotel.',
   'Nubeluz, a cocktail bar on the 50th floor.',
   'In NoMad, with Madison Square Park, Flatiron, and Chelsea nearby.',
   'Diptyque bath products and separate rain showers, with deep soaking tubs in some rooms.',
   'A fitness center open 24 hours, with Peloton bikes, next to a 6,800 sq ft spa.',
   'Ritz Kids activities, and pets welcome: up to two, 60 lbs combined, with a per-stay fee.',
  ],
  why='The most "New York at night" stay on the list. It gives a hotel pitch its strongest opening shot: the window, then the skyline, then a walk that starts right at the lobby. It also works for a family: quiet rooms for naps, soaking tubs for bath time, a gym downstairs, and a dog-friendly policy.',
  angle=dict(
   hotel='Open on the window view at dusk. Cut to Nubeluz, then a map of the walk to Madison Square Park, Flatiron, and the Chelsea galleries. Close with a hotel dinner.'),
  pins=[
   ('stay','Room view and amenities','here','Oversize windows are the opening shot.',False),
   ('eat','Bazaar Meat by José Andrés','here','Velvet booths, feather chandeliers, dinner at the hotel.',False),
   ('night','Nubeluz, 50th floor','here','Skyline at blue hour.',False),
   ('walk','Madison Square Park and Flatiron','walk','Morning walk, coffee in hand.',True),
   ('art','Chelsea galleries and the start of the High Line','walk','Local artists, one gallery per hour.',True),
   ('sale','Sample-sale hunt','ride','Check the 260 Sample Sale list the week you go.',True),
   ('matcha','Matcha in SoHo or NoLita','ride','Cha Cha Matcha is the photogenic pick.',True),
   ('shop','Gentle Monster, SoHo','ride','Installation-style retail.',True),
   ('pop','Pop-up of the week','ride','Pop-ups rotate weekly. Pick one for the feed.',True),
   ('eat','Ramen: Ippudo or Ivan Ramen','ride','East Village or Lower East Side.',True),
   ('sweet','Dumbo ice cream and bridge shot','trip','Van Leeuwen or similar, then the bridge frame.',True),
   ('eat','Nobu Downtown dinner','trip','The big dinner moment.',True),
   ('pack','Last look and checkout','here','One last lobby and window moment.',False),
  ]),
 dict(
  slug='brooklyn', no='02', city='New York City', name='1 Hotel Brooklyn Bridge', short='1 Hotel Brooklyn Bridge',
  tagline='Nature-forward luxury on the Dumbo waterfront.',
  hand='skyline, but make it calm',
  fonts='Fraunces:ital,wght@0,300;0,500;1,300&family=Inter:wght@300;400;500&family=Nothing+You+Could+Do',
  head="'Fraunces',Georgia,serif", body="'Inter',sans-serif",
  c=dict(desk='#2b3326', paper='#efe6d2', ink='#2a3324', accent='#6f8a52', accent2='#a8743f', soft='#e2d6bb'),
  vibe=['Moss green', 'Kraft paper', 'Warm timber'],
  facts=[
   'Anchors the Dumbo waterfront with views of the Lower Manhattan skyline.',
   'Rooftop pool deck.',
   'Bamford Wellness Spa.',
  ],
  why='The calmer, greener pick. It suits your own values (sustainable, ingredient-conscious) and lets you tell a skincare-and-spa story, like your Alastin journey, inside a luxury stay.',
  angle=dict(
   hotel='Lead with the skyline across the water, then the spa and rooftop pool. Show the Dumbo walk: bridge park, carousel, cobblestones.'),
  pins=[
   ('stay','Room and skyline view','here','Morning light across the water.',False),
   ('night','Rooftop pool deck','here','Skyline from the pool.',False),
   ('spa','Bamford Wellness Spa','here','A skin-ritual moment for the skincare audience.',False),
   ('walk','Brooklyn Bridge Park walk','walk','Slow waterfront loop.',True),
   ('walk','Washington Street bridge shot','walk','The classic Dumbo frame.',True),
   ('fun',"Jane's Carousel",'walk','Quick, charming b-roll.',True),
   ('eat','Time Out Market','walk','Lunch with local vendors.',True),
   ('art','Dumbo gallery stop','walk','Local artists nearby.',True),
   ('matcha','Matcha in Williamsburg','ride','Pick a spot the week you go.',True),
   ('shop','Gentle Monster, SoHo','ride','Cross the bridge for a design stop.',True),
   ('eat','Ramen in the East Village','ride','Local favorite pick.',True),
   ('sweet','Ice cream by the water','ride','A scoop at golden hour.',True),
  ]),
 dict(
  slug='halekulani', no='03', city="Hawaiʻi (Oʻahu)", name='Halekulani', short='Halekulani',
  tagline='Oceanfront Waikiki, with local Hawaiian makers close by.',
  hand='mahalo, Waikiki',
  fonts='Cormorant+Garamond:ital,wght@0,400;0,600;1,400&family=Inter:wght@300;400;500&family=Nothing+You+Could+Do',
  head="'Cormorant Garamond',Georgia,serif", body="'Inter',sans-serif",
  c=dict(desk='#1d4c52', paper='#f8f1e1', ink='#27393c', accent='#7b5a8c', accent2='#2f8089', soft='#eddfc3'),
  vibe=['Ocean teal', 'Orchid', 'Warm sand'],
  facts=[
   'Oceanfront in Waikiki (confirm room views and categories).',
   'Known for classic, quiet luxury (confirm current dining and spa).',
   'A short ride from Kakaʻako, a walkable neighborhood of murals and local shops.',
  ],
  why='Your strongest story. A proud Kanaka showing Hawaiian-owned makers and neighborhoods beats a generic beach feed, and the hotel gives the pitch a refined, grounded base.',
  angle=dict(
   hotel='Sunrise on the water, the beach walk, and the lobby-to-sea path. Then a "worth the ride" day in Kakaʻako to show the local side.'),
  pins=[
   ('stay','Oceanfront room and lanai view','here','Confirm room categories.',True),
   ('night','Sunrise on the beach','here','Soft light, no filter.',False),
   ('eat','Sunset dinner at the hotel','here','Confirm the restaurant and hours.',True),
   ('shop','Waikiki shops','walk','A quick browse before the beach.',True),
   ('art','Kakaʻako murals walk','ride','Colorful neighborhood, easy to wander.',False),
   ('shop','House of Mana Up','ride','Hawaiian entrepreneurs, beauty and local foods.',False),
   ('shop','MORI by Art+Flea','ride','Goods by Hawaiian artists.',False),
   ('shop','always a.line and Salvage Public','ride','Hawaiian-inspired prints and surf graphic tees.',False),
   ('sweet','Black Sheep Cream Company','ride','Rotating ice cream flavors.',False),
   ('eat',"Merriman's Honolulu",'ride','Farm-to-table dinner.',False),
   ('sweet',"Lin's Hawaiian Snacks",'ride','Shave ice, open since the 1980s.',False),
   ('matcha','Local matcha stop','ride','Pick one the week you go.',True),
   ('art','Honolulu Museum of Art','trip','Local artists and a quiet gallery moment.',True),
  ]),
 dict(
  slug='proper', no='04', city='Los Angeles', name='Santa Monica Proper', short='Santa Monica Proper',
  tagline='Sunset over the Pacific, with Venice and the Westside around it.',
  hand='golden hour on Wilshire',
  fonts='Fraunces:ital,wght@0,300;0,500;1,300&family=Inter:wght@300;400;500&family=Nothing+You+Could+Do',
  head="'Fraunces',Georgia,serif", body="'Inter',sans-serif",
  c=dict(desk='#5a2f22', paper='#f6ead6', ink='#43281f', accent='#b5573a', accent2='#d9a441', soft='#ecd9b7'),
  vibe=['Terracotta', 'Ochre', 'Warm cream'],
  facts=[
   'Luxury lifestyle hotel on Wilshire Boulevard.',
   'Sunset views over the Pacific.',
   'Near Palisades Park, Main Street, and Santa Monica shops.',
  ],
  why='The most "cute and trendy" stay on the list. It sits in the middle of your LA wish list: matcha in Venice, markets, boutiques, and a golden-hour finish.',
  angle=dict(
   hotel='Sunset from the room, a walk to Palisades Park, then a ride to Venice for matcha and boutiques.'),
  pins=[
   ('stay','Room and sunset view','here','Pacific light through the window.',False),
   ('night','Rooftop or lounge sunset','here','Confirm what the hotel offers.',True),
   ('walk','Palisades Park clifftop walk','walk','Ocean views, easy golden-hour stroll.',False),
   ('shop','Main Street shops','ride','A boutique stroll.',False),
   ('shop','Montana Avenue boutiques','ride','Pretty window shopping.',False),
   ('matcha','Shuhari Matcha Café, Venice','ride','Your matcha stop.',False),
   ('shop','Abbot Kinney Boulevard','ride','Shops and cafes in one strip.',False),
   ('eat','Gjusta bakery','ride','Breakfast or a pastry.',False),
   ('sweet','Salt & Straw','ride','A scoop on the boulevard.',False),
   ('eat','Elephante rooftop dinner','walk','Rooftop views. Confirm distance.',True),
   ('eat','Din Tai Fung','ride','Confirm the nearest location.',True),
   ('home','Goodies LA','trip','Home-goods hunt. Confirm location and hours.',True),
   ('shop','Gentle Monster flagship, Broadway','trip','The kinetic-sculpture store downtown.',False),
   ('art','The Getty or the Hammer Museum','trip','Art day.',False),
   ('sale','Sample sale check','trip','Dates change. Confirm the week you go.',True),
  ]),
 dict(
  slug='shutters', no='05', city='Los Angeles', name='Shutters on the Beach', short='Shutters on the Beach',
  tagline='A beachfront stay: ocean views, bike paths, and Venice down the shore.',
  hand='salt air, soft light',
  fonts='Cormorant+Garamond:ital,wght@0,400;0,600;1,400&family=Inter:wght@300;400;500&family=Nothing+You+Could+Do',
  head="'Cormorant Garamond',Georgia,serif", body="'Inter',sans-serif",
  c=dict(desk='#173a55', paper='#f4f1ea', ink='#1c3447', accent='#3a7ca5', accent2='#9fcbc0', soft='#e3ebea'),
  vibe=['Sea-glass', 'Navy', 'White linen'],
  facts=[
   'Upscale beachfront retreat in Santa Monica with ocean views.',
   'Beach path access toward Venice (confirm walking time).',
   'Near the Santa Monica Pier.',
  ],
  why='The easy, breezy beach option. It is the slow-morning stay: ocean light, a beach path, and an easy ride to Venice.',
  angle=dict(
   hotel='Wake up to the ocean, walk the beach path, then take a short ride to Venice. Show the stay as a slow coastal morning.'),
  pins=[
   ('stay','Ocean-view room and balcony','here','Morning light on the water.',False),
   ('walk','Beach path walk','here','Straight out the door.',True),
   ('fun','Santa Monica Pier','walk','Confirm distance and crowds.',True),
   ('art','Venice Canals','ride','Pretty, calm, easy to film.',False),
   ('matcha','Shuhari Matcha Café, Venice','ride','Matcha with a beach walk.',False),
   ('shop','Abbot Kinney Boulevard','ride','Shops and cafes.',False),
   ('sweet','Erewhon smoothie','ride','Venice or Santa Monica location.',False),
   ('eat','Tartine Bakery','ride','Pastry stop in Santa Monica.',False),
   ('eat','Malibu Farm on the pier','trip','Ocean dinner on the Malibu Pier.',False),
   ('shop','Malibu Country Mart','trip','Outdoor shopping and cafes.',False),
   ('eat','Nobu Malibu','trip','Confirm availability.',True),
   ('home','Goodies LA','trip','Home goods. Confirm location.',True),
   ('shop','Gentle Monster flagship, Broadway','trip','Downtown design stop.',False),
  ]),
]

CAT = {'stay':'Stay','eat':'Eat','night':'View','walk':'Walk','art':'Art','sale':'Sample sale','matcha':'Matcha','shop':'Shop',
       'pop':'Pop-up','sweet':'Sweet','fun':'Fun','spa':'Spa','pack':'Pack','home':'Home goods'}

def esc(s): return html.escape(s, quote=True)

BRIDGE = """
<script>
(function () {
  document.addEventListener('click', function (e) {
    var a = e.target && e.target.closest ? e.target.closest('a[href]') : null;
    if (!a || window.parent === window) return;
    var href = a.getAttribute('href');
    var m = href && href.match(/^(index|pitches|contact|pitch-[a-z]+)\\.html(#.*)?$/);
    if (!m) return;
    e.preventDefault();
    var page = m[1] === 'index' ? 'home' : m[1];
    window.parent.postMessage({ type: 'ugc-nav', page: page, hash: m[2] || '' }, '*');
  });
  window.addEventListener('message', function (e) {
    var d = e.data;
    if (d && d.type === 'ugc-scroll' && d.hash) {
      var el = document.getElementById(d.hash.replace('#', ''));
      if (el) el.scrollIntoView();
    }
  });
})();
</script>
"""

def hotel_page(h):
    c = h['c']
    pins_html = ''
    for i, (cat, title, tag, note, confirm) in enumerate(h['pins']):
        label, cls = TAGS[tag]
        stamp = '<span class="stamp">confirm</span>' if confirm else ''
        pins_html += f'''
      <article class="pin t{i % 5}">
        <div class="shot c-{cat}"><span>{esc(CAT[cat])}</span></div>
        <div class="pin-body">
          <div class="pin-top"><span class="num">{i+1:02d}</span><span class="tag {cls}">{label}</span>{stamp}</div>
          <h3>{esc(title)}</h3>
          <p class="hand">{esc(note)}</p>
        </div>
      </article>'''
    walk = [p for p in h['pins'] if p[2] in ('here', 'walk')]
    far = [p for p in h['pins'] if p[2] in ('ride', 'trip')]
    li = lambda arr: ''.join(f'<li>{esc(p[1])}{" <em>(confirm)</em>" if p[4] else ""}</li>' for p in arr)
    facts = ''.join(f'<li>{esc(f)}</li>' for f in h['facts'])
    chips = ''.join(f'<span class="chip"><i></i>{esc(v)}</span>' for v in h['vibe'])
    ang = h['angle']
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="robots" content="noindex">
<title>Pitch: {esc(h['short'])}</title>
<link href="https://fonts.googleapis.com/css2?family={h['fonts']}&display=swap" rel="stylesheet">
<style>
  :root {{ --desk:{c['desk']}; --paper:{c['paper']}; --ink:{c['ink']}; --accent:{c['accent']}; --accent2:{c['accent2']}; --soft:{c['soft']};
          --head:{h['head']}; --body:{h['body']}; --hand:'Nothing You Could Do',cursive; }}
  * {{ box-sizing:border-box; }}
  html,body {{ margin:0; background:var(--desk); color:var(--ink); font-family:var(--body); font-weight:300; -webkit-font-smoothing:antialiased; }}
  a {{ color:inherit; text-decoration:none; }}
  .top {{ max-width:1080px; margin:0 auto; padding:20px 16px 0; display:flex; justify-content:space-between; font-size:13px; letter-spacing:.06em; }}
  .top a {{ color:#fff; opacity:.8; }} .top a:hover {{ opacity:1; }}
  .notebook {{ max-width:1080px; margin:14px auto 40px; padding:0 16px; }}
  .sheet {{ position:relative; background:var(--paper); border-radius:6px 16px 16px 6px; padding:44px 40px 44px 76px; margin-bottom:22px;
           box-shadow:0 18px 40px rgba(0,0,0,.28); overflow:hidden;
           background-image:repeating-linear-gradient(transparent 0 31px, rgba(0,0,0,.06) 31px 32px); }}
  .sheet::before {{ content:''; position:absolute; left:0; top:0; bottom:0; width:48px; background:rgba(0,0,0,.14);
           background-image:radial-gradient(circle at 24px 20px, var(--desk) 7px, transparent 8px); background-size:48px 44px; }}
  .sheet::after {{ content:''; position:absolute; left:58px; top:0; bottom:0; width:2px; background:var(--accent); opacity:.35; }}
  .kick {{ font-size:12px; letter-spacing:.2em; text-transform:uppercase; color:var(--accent); font-weight:500; }}
  h1,h2,h3 {{ font-family:var(--head); font-weight:400; margin:0; line-height:1.08; }}
  h1 {{ font-size:clamp(34px,6vw,64px); margin:12px 0 10px; }}
  h2 {{ font-size:clamp(26px,3.6vw,38px); margin:6px 0 16px; }}
  .hand {{ font-family:var(--hand); font-size:22px; line-height:1.15; color:var(--accent); margin:0; font-weight:500; }}
  p {{ line-height:1.7; }}
  .cover {{ min-height:340px; display:grid; grid-template-columns:1.2fr .8fr; gap:28px; align-items:center; }}
  .cover .lede {{ font-size:18px; max-width:46ch; }}
  .photo {{ position:relative; aspect-ratio:4/5; border-radius:12px; transform:rotate(2.5deg); border:10px solid #fff; box-shadow:0 10px 24px rgba(0,0,0,.25);
           background:linear-gradient(160deg,var(--accent2),var(--accent)); overflow:hidden; display:flex; align-items:flex-end; }}
  .photo span {{ position:relative; z-index:1; color:#fff; font-family:var(--hand); font-size:22px; padding:12px; }}
  .photo img {{ position:absolute; inset:0; width:100%; height:100%; object-fit:cover; z-index:2; }}
  .tape {{ position:absolute; width:90px; height:26px; background:rgba(255,255,255,.55); top:-4px; left:50%; margin-left:-45px; transform:rotate(-4deg); z-index:3; }}
  .signed {{ margin-top:18px; }}
  .two {{ display:grid; grid-template-columns:1.1fr .9fr; gap:32px; }}
  ul.clean {{ margin:0; padding-left:18px; line-height:1.9; }}
  .chips {{ display:flex; flex-wrap:wrap; gap:8px; margin-top:12px; }}
  .chip {{ display:inline-flex; align-items:center; gap:8px; padding:6px 12px; border:1px solid rgba(0,0,0,.15); border-radius:999px; background:rgba(255,255,255,.6); font-size:13px; }}
  .chip i {{ width:14px; height:14px; border-radius:50%; background:var(--accent); display:inline-block; }}
  .chip:nth-child(2) i {{ background:var(--accent2); }} .chip:nth-child(3) i {{ background:var(--soft); border:1px solid rgba(0,0,0,.2); }}
  .board {{ column-count:3; column-gap:18px; margin-top:8px; }}
  .pin {{ break-inside:avoid; margin:0 0 18px; background:#fff; border-radius:12px; box-shadow:0 6px 16px rgba(0,0,0,.14); overflow:hidden; position:relative; }}
  .pin.t0 {{ transform:rotate(-1.2deg); }} .pin.t1 {{ transform:rotate(.9deg); }} .pin.t2 {{ transform:rotate(-.4deg); }} .pin.t3 {{ transform:rotate(1.3deg); }} .pin.t4 {{ transform:rotate(-.9deg); }}
  .pin::before {{ content:''; position:absolute; top:8px; left:50%; width:12px; height:12px; margin-left:-6px; border-radius:50%; background:var(--accent); box-shadow:0 2px 3px rgba(0,0,0,.35); z-index:2; }}
  .shot {{ height:92px; display:flex; align-items:flex-end; padding:10px 12px; background:linear-gradient(135deg,var(--accent2),var(--accent)); color:#fff; font-family:var(--hand); font-size:22px; }}
  .pin:nth-child(3n+2) .shot {{ height:128px; }} .pin:nth-child(4n) .shot {{ height:70px; }}
  .c-eat .shot, .shot.c-eat {{ background:linear-gradient(135deg,var(--accent),var(--accent2)); }}
  .c-sweet, .c-matcha {{ filter:saturate(1.1); }}
  .pin-body {{ padding:12px 14px 16px; }}
  .pin-top {{ display:flex; gap:8px; align-items:center; flex-wrap:wrap; margin-bottom:6px; }}
  .num {{ font-size:11px; letter-spacing:.14em; color:#888; }}
  .tag {{ font-size:10px; letter-spacing:.1em; text-transform:uppercase; padding:3px 8px; border-radius:999px; font-weight:500; }}
  .tag.here, .tag.walk {{ background:var(--accent); color:#fff; }} .tag.ride {{ background:var(--soft); color:var(--ink); }} .tag.trip {{ background:var(--ink); color:#fff; }}
  .stamp {{ font-size:10px; letter-spacing:.1em; text-transform:uppercase; border:1px dashed #b34; color:#b34; padding:2px 6px; border-radius:4px; transform:rotate(-3deg); }}
  .pin h3 {{ font-size:20px; margin-bottom:6px; }}
  .pin .hand {{ font-size:19px; color:var(--ink); opacity:.75; }}
  .notes {{ display:grid; grid-template-columns:repeat(3,1fr); gap:18px; }}
  .notes.one {{ grid-template-columns:minmax(0,640px); }}
  .note {{ background:var(--soft); padding:20px 18px; border-radius:4px; box-shadow:0 6px 14px rgba(0,0,0,.12); }}
  .note:nth-child(1) {{ transform:rotate(-1deg); }} .note:nth-child(2) {{ transform:rotate(.8deg); }} .note:nth-child(3) {{ transform:rotate(-.6deg); }}
  .note h3 {{ font-size:22px; margin-bottom:8px; }} .note p {{ margin:0; font-size:15px; }}
  .cta {{ text-align:center; padding:56px 40px 56px 76px; }}
  .btn {{ display:inline-block; margin-top:14px; padding:14px 26px; border-radius:999px; background:var(--ink); color:#fff; font-size:14px; letter-spacing:.06em; }}
  .fine {{ color:#fff; opacity:.6; font-size:12px; text-align:center; padding-bottom:30px; }}
  @media (max-width:820px) {{
    .sheet {{ padding:34px 20px 34px 62px; }} .cover,.two,.notes {{ grid-template-columns:1fr; }} .board {{ column-count:2; }} .cta {{ padding:40px 20px 40px 62px; }}
  }}
  @media (max-width:520px) {{ .board {{ column-count:1; }} .sheet::before {{ width:36px; background-size:36px 44px; background-image:radial-gradient(circle at 18px 20px, var(--desk) 6px, transparent 7px); }} .sheet::after {{ left:44px; }} .sheet {{ padding-left:56px; }} }}
</style>
</head>
<body>
<div class="top"><a href="pitches.html">&larr; All pitches</a><a href="index.html">Home</a></div>
<main class="notebook">
  <section class="sheet cover">
    <div>
      <div class="kick">Pitch {h['no']} &middot; {esc(h['city'])}</div>
      <h1>{esc(h['name'])}</h1>
      <p class="lede">{esc(h['tagline'])}</p>
      <p class="hand signed">&mdash; a travel guide by Brianne</p>
    </div>
    <div class="photo"><div class="tape"></div><span>{esc(h['hand'])}</span>
      <img src="{CDN}{h['slug']}-hero.jpg" alt="" onerror="this.remove()">
    </div>
  </section>

  <section class="sheet">
    <div class="two">
      <div>
        <div class="kick">Why this stay</div>
        <h2>The feeling I'd film</h2>
        <p>{esc(h['why'])}</p>
        <div class="chips">{chips}</div>
      </div>
      <div>
        <div class="kick">What it's known for</div>
        <ul class="clean">{facts}</ul>
      </div>
    </div>
  </section>

  <section class="sheet" id="itinerary">
    <div class="kick">The itinerary board</div>
    <h2>Pinned, in the order I'd shoot it</h2>
    <p class="hand">Stops tagged "confirm" still need checking before we book.</p>
    <div class="board">{pins_html}
    </div>
  </section>

  <section class="sheet">
    <div class="kick">How I'd tell it</div>
    <h2>The stay, start to finish</h2>
    <div class="notes one"><div class="note"><h3>Hotel POV</h3><p>{esc(ang['hotel'])}</p></div></div>
  </section>

  <section class="sheet">
    <div class="two">
      <div><div class="kick">Walkable from the hotel</div><h2>Out the door</h2><ul class="clean">{li(walk)}</ul></div>
      <div><div class="kick">Worth the ride</div><h2>A little farther</h2><ul class="clean">{li(far)}</ul></div>
    </div>
  </section>

  <section class="sheet cta">
    <div class="kick">Let's make it real</div>
    <h2>Stay with me, and I'll tell the story.</h2>
    <p class="hand">Reels, photos, and a guide like this one.</p>
    <a class="btn" href="contact.html">Say hello</a>
  </section>
</main>
<div class="fine">Draft pitch for {esc(h['short'])}. Not affiliated with or endorsed by the hotel.</div>
{BRIDGE}
</body>
</html>
'''

import urllib.parse
def _uri(svg):
    return 'url("data:image/svg+xml;utf8,' + urllib.parse.quote(svg, safe="/:=,'()* ").replace('"', '%22') + '")'

LEATHER = _uri("<svg xmlns='http://www.w3.org/2000/svg' width='260' height='260'><filter id='l' x='0' y='0' width='100%' height='100%'><feTurbulence type='fractalNoise' baseFrequency='.6' numOctaves='3' seed='7' stitchTiles='stitch' result='n'/><feDiffuseLighting in='n' surfaceScale='1.8' diffuseConstant='1' lighting-color='#ffffff'><feDistantLight azimuth='50' elevation='62'/></feDiffuseLighting></filter><rect width='260' height='260' filter='url(#l)'/></svg>")
PAPERN = _uri("<svg xmlns='http://www.w3.org/2000/svg' width='200' height='200'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.8' numOctaves='2' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 .3 0 0 0 0 .25 0 0 0 0 .2 0 0 0 .09 0'/></filter><rect width='100%' height='100%' filter='url(#n)'/></svg>")

# Shared by the hub's open binder and the opener on each pitch page.
BINDER_CSS = r"""
  .bd-book { position:relative; width:var(--bw,min(760px,94vw)); height:var(--bh,min(84vh,860px)); border-radius:18px; color:#2a2420;
     background-color:var(--lea,#4a2621); background-image:%%LEATHER%%, radial-gradient(ellipse at 28% 18%, rgba(255,255,255,.2), transparent 55%), linear-gradient(150deg,var(--lea,#4a2621),var(--lea2,#2a110d));
     background-blend-mode:multiply, soft-light, normal; box-shadow:0 40px 80px rgba(0,0,0,.55), 0 0 0 1px rgba(0,0,0,.45), inset 0 0 0 1px rgba(255,235,200,.08); }
  .bd-book::after { content:''; position:absolute; inset:11px; border:1.5px dashed rgba(235,215,170,.4); border-radius:11px; pointer-events:none; }
  .bd-page { position:absolute; left:68px; right:48px; top:28px; bottom:28px; background-color:#f2ecdf; background-image:%%PAPERN%%; border-radius:3px 8px 8px 3px; padding:34px 40px 24px 42px; overflow:hidden;
     box-shadow:0 1px 0 #ddd5c1, 0 2px 0 #f2ecdf, 0 3px 0 #cfc6b0, 0 4px 6px rgba(0,0,0,.45), inset 14px 0 20px -14px rgba(0,0,0,.3); z-index:2; }
  .bd-rings { position:absolute; left:22px; top:9%; bottom:9%; width:84px; z-index:4; display:flex; flex-direction:column; justify-content:space-between; pointer-events:none; }
  .bd-ring { position:relative; width:84px; height:20px; border-radius:12px; background:linear-gradient(#fbfbfb,#b6b9bd 42%,#eceded 56%,#74777c); box-shadow:0 3px 5px rgba(0,0,0,.5), inset 0 0 0 1px rgba(0,0,0,.18); }
  .bd-ring::after { content:''; position:absolute; right:10px; top:3px; width:14px; height:14px; border-radius:50%; background:#17110e; box-shadow:inset 0 1px 3px #000; }
  .bd-tabs { position:absolute; right:20px; top:44px; bottom:44px; width:52px; z-index:3; display:flex; flex-direction:column; gap:7px; }
  .bd-tab { flex:0 0 auto; width:44px; min-height:92px; padding:12px 0; writing-mode:vertical-rl; text-align:center; font-family:'Nothing You Could Do',cursive; font-size:19px; line-height:1; color:#2b2420; background:#e8dfcb; background-image:%%PAPERN%%;
     border-radius:0 9px 9px 0; box-shadow:2px 2px 5px rgba(0,0,0,.35); transition:transform .25s, background-color .25s; cursor:pointer; display:flex; align-items:center; justify-content:center; }
  .bd-tab:nth-child(2n) { background-color:#ddd2ba; } .bd-tab:nth-child(3n) { background-color:#efe7d6; }
  .bd-tab:hover,.bd-tab:focus-visible { transform:translateX(9px); outline:none; background-color:#fff8e6; }
  .bd-tab.ghost { background:transparent; box-shadow:none; border:1.5px dashed rgba(235,215,170,.5); border-left:0; color:rgba(235,215,170,.7); cursor:default; }
  .bd-tab.ghost:hover { transform:none; background:transparent; }
  .bd-clip { position:absolute; width:26px; height:76px; z-index:5; filter:drop-shadow(1px 2px 1px rgba(0,0,0,.35)); }
  .bd-kick { font:500 11px/1 'Inter',sans-serif; letter-spacing:.32em; text-transform:uppercase; color:#8a7a62; }
  .bd-foil { background:linear-gradient(115deg,#f6e4b0,#c39b55 45%,#f1d98f 62%,#a98240); -webkit-background-clip:text; background-clip:text; color:transparent; text-shadow:none; }
  @media (max-width:640px) {
    .bd-page { left:50px; right:34px; top:20px; bottom:20px; padding:24px 20px 16px 22px; }
    .bd-rings { left:14px; width:68px; } .bd-ring { width:68px; height:17px; } .bd-ring::after { width:12px; height:12px; right:8px; top:2px; }
    .bd-tabs { right:8px; width:38px; top:34px; } .bd-tab { width:32px; min-height:70px; font-size:15px; padding:9px 0; }
  }
""".replace('%%LEATHER%%', LEATHER).replace('%%PAPERN%%', PAPERN)

CLIP = '<svg class="bd-clip" viewBox="0 0 26 76" aria-hidden="true"><path d="M5 52V15a8 8 0 0 1 16 0v47a11 11 0 0 1-22 0V22" transform="translate(2 0)" fill="none" stroke="#a8acb2" stroke-width="2.4" stroke-linecap="round"/></svg>'

HUB_CSS = r"""
  :root { --foil:#d9bb7e; }
  * { box-sizing:border-box; }
  html,body { margin:0; min-height:100%; color:#efe4d0; font-family:'Inter',sans-serif; font-weight:300; -webkit-font-smoothing:antialiased;
     background:#1b1410; background-image:radial-gradient(ellipse at 50% 30%, rgba(120,80,50,.28), transparent 65%), %%PAPERN%%; }
  a { color:inherit; text-decoration:none; } button { font:inherit; color:inherit; }
  .hand { font-family:'Nothing You Could Do',cursive; font-weight:400; }
  .back { position:fixed; top:14px; left:18px; z-index:20; font-size:12px; letter-spacing:.14em; text-transform:uppercase; opacity:.75; }
  .room { max-width:1060px; margin:0 auto; padding:64px 18px 60px; text-align:center; }
  .eyebrow { font-size:11px; letter-spacing:.34em; text-transform:uppercase; color:var(--foil); margin:0; }
  h1 { font-family:'Cormorant Garamond',Georgia,serif; font-style:italic; font-weight:400; font-size:clamp(44px,7vw,84px); margin:10px 0 0; line-height:1; }
  .pick { font-size:24px; color:var(--foil); margin:8px 0 26px; }
  .note { margin:34px auto 0; max-width:60ch; font-size:12px; line-height:1.7; opacity:.5; }
  /* cabinet */
  .cab { position:relative; background:linear-gradient(#4a4540,#34302c); border-radius:14px; padding:22px 22px 18px; box-shadow:0 40px 70px rgba(0,0,0,.55), inset 0 1px 0 rgba(255,255,255,.12), inset 0 0 0 1px rgba(0,0,0,.4);
     background-image:repeating-linear-gradient(90deg, rgba(255,255,255,.035) 0 1px, transparent 1px 3px), linear-gradient(#4a4540,#34302c); }
  .open { position:relative; height:clamp(330px,56vh,500px); background:linear-gradient(#0d0907,#1d1511); border-radius:8px 8px 0 0; box-shadow:inset 0 22px 40px rgba(0,0,0,.85), inset 0 0 0 2px rgba(0,0,0,.6); overflow:hidden; }
  .binders { position:absolute; inset:0; display:flex; align-items:flex-end; justify-content:center; gap:clamp(6px,1.2vw,14px); padding:0 3%; }
  .spine { position:relative; flex:0 1 clamp(78px,17vw,168px); height:var(--h,90%); border:0; padding:0; cursor:pointer; border-radius:7px 7px 0 0;
     background-color:var(--lea); background-image:%%LEATHER%%, linear-gradient(90deg, rgba(0,0,0,.45), rgba(255,255,255,.1) 22%, rgba(255,255,255,.04) 60%, rgba(0,0,0,.5)), linear-gradient(var(--lea),var(--lea2));
     background-blend-mode:multiply, normal, normal; box-shadow:0 0 0 1px rgba(0,0,0,.6), 6px 0 14px rgba(0,0,0,.5); transition:transform .3s cubic-bezier(.2,.8,.2,1); display:flex; flex-direction:column; align-items:center; justify-content:flex-start; gap:0; }
  .spine:hover,.spine:focus-visible { transform:translateY(-20px); outline:none; }
  .spine .band { display:block; width:100%; height:26px; margin-top:34px; border-block:1.5px solid rgba(217,187,126,.55); background:repeating-linear-gradient(0deg, transparent 0 6px, rgba(217,187,126,.28) 6px 7px); }
  .spine .band.bt { margin-top:auto; margin-bottom:96px; }
  .spine .lbl { position:absolute; left:50%; top:23%; transform:translateX(-50%); width:54%; min-height:46%; padding:16px 0; background:#efe6d3; background-image:%%PAPERN%%; color:#2a211a; border-radius:3px; box-shadow:0 1px 3px rgba(0,0,0,.6), inset 0 0 0 3px #efe6d3, inset 0 0 0 4px rgba(120,95,60,.45);
     display:flex; flex-direction:column; align-items:center; justify-content:center; gap:14px; writing-mode:vertical-rl; }
  .spine .lbl b { font-family:'Cormorant Garamond',serif; font-weight:600; font-size:clamp(14px,1.75vw,21px); letter-spacing:.16em; text-transform:uppercase; }
  .spine .lbl i { font-style:normal; font-size:10px; letter-spacing:.22em; text-transform:uppercase; opacity:.6; }
  .spine .num { position:absolute; bottom:104px; left:0; right:0; text-align:center; font-family:'Cormorant Garamond',serif; font-size:16px; color:var(--foil); opacity:.85; letter-spacing:.12em; }
  .front { position:relative; z-index:5; height:clamp(86px,13vh,120px); margin:-86px -22px 0; padding:0 22px; background:linear-gradient(#58524b,#3b3732); border-radius:4px; box-shadow:0 -8px 18px rgba(0,0,0,.45), inset 0 1px 0 rgba(255,255,255,.18), inset 0 -2px 0 rgba(0,0,0,.35); display:flex; align-items:center; justify-content:center; }
  .front { margin-top:calc(-1 * clamp(86px,13vh,120px) + 34px); }
  .front.low { margin:12px 0 0; z-index:1; box-shadow:inset 0 1px 0 rgba(255,255,255,.14), inset 0 -2px 0 rgba(0,0,0,.35), 0 2px 0 #28251f; }
  .plate { position:absolute; left:50%; top:16px; transform:translateX(-50%); padding:5px 20px; background:#d6b977; background-image:linear-gradient(#e6cf95,#b8964f); border-radius:3px; box-shadow:0 1px 2px rgba(0,0,0,.5); }
  .plate i { display:block; font-style:normal; font-size:10px; letter-spacing:.32em; text-transform:uppercase; background:#efe6d3; color:#2a211a; padding:4px 14px; }
  .pull { position:absolute; left:50%; bottom:14px; transform:translateX(-50%); width:120px; height:10px; border-radius:6px; background:linear-gradient(#f0dca0,#a98240); box-shadow:0 3px 5px rgba(0,0,0,.55); }
  .front.low { height:clamp(66px,9vh,84px); } .front.low .plate { top:10px; } .front.low .pull { bottom:10px; }
  /* open binder overlay */
  .ob { position:fixed; inset:0; z-index:100; display:flex; align-items:center; justify-content:center; background:rgba(12,7,5,.82); backdrop-filter:blur(3px); opacity:0; pointer-events:none; transition:opacity .4s; }
  .ob.show { opacity:1; pointer-events:auto; }
  .ob .x { position:absolute; top:14px; left:16px; background:none; border:0; cursor:pointer; font-size:12px; letter-spacing:.14em; text-transform:uppercase; opacity:.8; z-index:5; }
  .ob .stage { perspective:2200px; }
  .ob .bd-book { transform:translateY(46px) scale(.9); transition:transform .7s cubic-bezier(.2,.8,.2,1), opacity .6s; }
  .ob.show .bd-book { transform:none; }
  .ob.leaving .bd-book { transform:scale(1.9); opacity:0; }
  .ob .cov { position:absolute; inset:0; z-index:8; border-radius:18px; transform-origin:left center; transition:transform 1.3s cubic-bezier(.6,.05,.2,1), opacity .3s 1s; backface-visibility:hidden; display:flex; align-items:center; justify-content:center; text-align:center;
     background-color:var(--lea); background-image:%%LEATHER%%, radial-gradient(ellipse at 28% 18%, rgba(255,255,255,.2), transparent 55%), linear-gradient(150deg,var(--lea),var(--lea2)); background-blend-mode:multiply, soft-light, normal; box-shadow:inset 0 0 0 11px transparent, inset 0 0 0 1.5px rgba(235,215,170,.35); }
  .ob .cov::before { content:''; position:absolute; inset:11px; border:1.5px dashed rgba(235,215,170,.4); border-radius:11px; }
  .ob .cov .in { display:flex; flex-direction:column; gap:14px; align-items:center; }
  .ob .cov .t { font-family:'Cormorant Garamond',serif; font-style:italic; font-size:clamp(54px,9vw,104px); line-height:1; padding:0 .1em; }
  .ob .cov .hand { font-size:22px; color:rgba(235,215,170,.85); } .ob .cov .cn { font-size:11px; letter-spacing:.3em; text-transform:uppercase; color:rgba(235,215,170,.55); }
  .ob.opened .cov { transform:rotateY(-168deg); opacity:0; pointer-events:none; }
  .bd-page h2 { font-family:'Cormorant Garamond',serif; font-style:italic; font-weight:400; font-size:clamp(54px,8vw,92px); line-height:1; margin:14px 0 4px; }
  .bd-page .sub { font-size:23px; color:#6b5a44; margin-bottom:26px; }
  .idx { list-style:none; margin:0; padding:0; }
  .row { display:grid; grid-template-columns:1fr auto; align-items:center; gap:2px 10px; border-bottom:1px solid rgba(60,45,30,.2); padding:11px 0; }
  .row .go { display:grid; grid-template-columns:34px 1fr auto; align-items:baseline; gap:8px; }
  .row .go b { font-family:'Cormorant Garamond',serif; font-weight:500; font-size:15px; color:#9a8660; }
  .row .n { font-family:'Cormorant Garamond',serif; font-weight:600; font-size:clamp(20px,2.4vw,27px); line-height:1.1; }
  .row .c { font-size:10px; letter-spacing:.2em; text-transform:uppercase; color:#8a7a62; }
  .row .go:hover .n { text-decoration:underline; text-decoration-thickness:1px; text-underline-offset:4px; }
  .row .cp { background:none; border:1px solid rgba(60,45,30,.35); border-radius:99px; padding:4px 11px; font-size:10px; letter-spacing:.14em; text-transform:uppercase; cursor:pointer; color:#4a3d2c; }
  .row .cp:hover { background:#2a211a; color:#f2ecdf; }
  .row .lk { display:none; grid-column:1/-1; width:100%; border:1px dashed rgba(60,45,30,.4); background:rgba(255,255,255,.4); font:12px/1.4 'Inter',sans-serif; padding:6px 8px; color:#2a211a; }
  .row.showlink .lk { display:block; }
  .hnote { font-family:'Nothing You Could Do',cursive; font-size:19px; color:#7a6850; margin:18px 0 0; }
  .soon { padding-top:10px; } .soon .big { font-size:46px; color:#6b5a44; transform:rotate(-3deg); margin:6px 0 6px; } .soon p { max-width:34ch; line-height:1.7; font-size:14px; color:#6b5a44; }
  .ruled { margin-top:26px; } .ruled i { display:block; height:34px; border-bottom:1px solid rgba(60,45,30,.18); }
  @media (max-width:640px) {
    .room { padding-top:56px; } .spine .band { height:18px; margin-top:22px; } .spine .band.bt { margin-bottom:84px; } .spine .num { bottom:92px; }
    .row .go { grid-template-columns:26px 1fr; } .row .c { grid-column:2; } .bd-page h2 { font-size:54px; }
    .bd-book { --bw:94vw; --bh:86vh; }
  }
  @media (prefers-reduced-motion: reduce) { .ob .cov,.ob .bd-book,.spine { transition:none; } }
""".replace('%%LEATHER%%', LEATHER).replace('%%PAPERN%%', PAPERN)

HUB_JS = r"""
(function () {
  var inFrame = window.parent && window.parent !== window;
  function go(href) {
    var m = href.match(/^(index|pitches|contact|pitch-[a-z]+)\.html(#.*)?$/); if (!m) return;
    var page = m[1] === 'index' ? 'home' : m[1];
    if (inFrame) window.parent.postMessage({ type: 'ugc-nav', page: page, hash: m[2] || '' }, '*'); else window.location.href = href;
  }
  var cur = null, reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  function openB(id) {
    var ob = document.getElementById('ob-' + id); if (!ob) return; cur = ob;
    ob.classList.remove('leaving', 'opened'); ob.classList.add('show'); ob.setAttribute('aria-hidden', 'false');
    setTimeout(function () { ob.classList.add('opened'); }, reduce ? 0 : 620);
    var x = ob.querySelector('.x'); if (x) x.focus({ preventScroll: true });
  }
  function closeB() { if (!cur) return; cur.classList.remove('show', 'opened', 'leaving'); cur.setAttribute('aria-hidden', 'true'); cur = null; }
  Array.prototype.forEach.call(document.querySelectorAll('.spine'), function (b) { b.addEventListener('click', function () { openB(b.getAttribute('data-open')); }); });
  Array.prototype.forEach.call(document.querySelectorAll('.ob'), function (ob) {
    ob.querySelector('.x').addEventListener('click', closeB);
    ob.addEventListener('click', function (e) { if (e.target === ob || e.target.classList.contains('stage')) closeB(); });
  });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeB(); });
  function linkFor(page) {
    try { var u = new URL(window.parent.location.href); if (u.protocol === 'http:' || u.protocol === 'https:') { u.hash = ''; u.searchParams.set('page', page); return u.toString(); } } catch (e) {}
    return '?page=' + page;
  }
  Array.prototype.forEach.call(document.querySelectorAll('.row .cp'), function (btn) {
    btn.addEventListener('click', function () {
      var row = btn.closest('.row'), inp = row.querySelector('.lk'), url = linkFor(row.getAttribute('data-page'));
      inp.value = url; row.classList.add('showlink'); inp.focus(); inp.select();
      var ok = false; try { ok = document.execCommand('copy'); } catch (e) {}
      btn.textContent = ok ? 'copied' : 'copy below';
      setTimeout(function () { btn.textContent = 'copy link'; }, 1800);
    });
  });
  // tabs and rows: the binder zooms away, then we go to the pitch
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('.ob a[href]'); if (!a) return;
    e.preventDefault(); e.stopPropagation();
    var href = a.getAttribute('href');
    if (cur && !reduce) { cur.classList.add('leaving'); setTimeout(function () { go(href); }, 550); } else go(href);
  }, true);
  window.addEventListener('message', function (e) { var d = e.data; if (d && d.type === 'ugc-scroll' && d.hash) openB(d.hash.replace('#', '')); });
  if (location.hash && location.hash.length > 1) openB(location.hash.slice(1));
})();
"""

BINDERS = [
 dict(id='travel', no='01', title='Travel', sub='hotel & destination pitches', lea='#4a2621', lea2='#2a110d',
      pitches=[('nomad', 'NoMad'), ('brooklyn', '1 Hotel'), ('halekulani', 'Halekulani'), ('proper', 'Proper'), ('shutters', 'Shutters')]),
 dict(id='skincare', no='02', title='Skincare', sub='routines & rituals', lea='#3b2a22', lea2='#1f130e', pitches=[]),
 dict(id='homegoods', no='03', title='Homegoods', sub='rooms & rituals at home', lea='#403a24', lea2='#1f1b0e', pitches=[]),
 dict(id='fashion', no='04', title='Fashion', sub='wardrobe & style pitches', lea='#211c1b', lea2='#0c0908', pitches=[]),
]


PUBLIC = {'nomad': 'pitch-ritz-carlton-nomad-nyc'}  # public address names (internal page key stays pitch-nomad)


def hub():
    by = {h['slug']: h for h in HOTELS}
    spines = ''
    books = ''
    for k, b in enumerate(BINDERS):
        n = len(b['pitches'])
        cnt = f'{n} pitches' if n else 'coming soon'
        hgt = [93, 88, 91, 86][k % 4]
        spines += f'''
      <button class="spine" type="button" data-open="{b['id']}" style="--lea:{b['lea']};--lea2:{b['lea2']};--h:{hgt}%" aria-label="Open the {b['title']} binder">
        <span class="band"></span>
        <span class="lbl"><b>{b['title']}</b><i>{cnt}</i></span>
        <span class="band bt"></span>
      </button>'''
        if n:
            rows = ''
            tabs = ''
            for sl, tab in b['pitches']:
                h = by[sl]
                rows += f'''
          <li class="row" data-page="{PUBLIC.get(sl, 'pitch-' + sl)}">
            <a class="go" href="pitch-{sl}.html"><b>{h['no']}</b><span class="n">{esc(h['short'])}</span><span class="c">{esc(h['city'])}</span></a>
            <button class="cp" type="button">copy link</button>
            <input class="lk" readonly aria-label="Direct link">
          </li>'''
                tabs += f'<a class="bd-tab" href="pitch-{sl}.html" title="{esc(h["short"])}">{esc(tab)}</a>'
            page = f'<ol class="idx">{rows}\n        </ol><p class="hnote">tap a tab, or any line, to open that pitch</p>'
        else:
            tabs = '<span class="bd-tab ghost">soon</span><span class="bd-tab ghost">soon</span>'
            page = '<div class="soon"><div class="hand big">coming soon</div><p>Nothing filed here yet. This binder will hold the next set of pitches.</p><div class="ruled"><i></i><i></i><i></i><i></i></div></div>'
        rings = '<span class="bd-ring"></span>' * 6
        clip = CLIP.replace('class="bd-clip"', 'class="bd-clip" style="right:70px;top:-14px"')
        books += f'''
  <div class="ob" id="ob-{b['id']}" aria-hidden="true">
    <button class="x" type="button">&larr; back to the cabinet</button>
    <div class="stage"><div class="bd-book" style="--lea:{b['lea']};--lea2:{b['lea2']}">
      <div class="bd-page">
        {clip}
        <div class="bd-kick">Binder {b['no']}</div>
        <h2>{b['title']}</h2>
        <div class="hand sub">{esc(b['sub'])}</div>
        {page}
      </div>
      <nav class="bd-tabs">{tabs}</nav>
      <div class="bd-rings">{rings}</div>
      <div class="cov"><div class="in"><span class="bd-kick" style="color:rgba(235,215,170,.7)">Binder {b['no']}</span><span class="t bd-foil">{b['title']}</span><span class="hand">{esc(b['sub'])}</span><span class="cn">{cnt}</span></div></div>
    </div></div>
  </div>'''
    css = HUB_CSS
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="robots" content="noindex">
<title>Pitch center</title>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,wght@0,300;0,500;1,300&family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Inter:wght@300;400;500&family=Nothing+You+Could+Do&display=swap" rel="stylesheet">
<style>{css}{BINDER_CSS}</style>
</head>
<body>
<a class="back" href="index.html">&larr; Home</a>
<main class="room">
  <p class="eyebrow">Pitch center</p>
  <h1>The filing cabinet</h1>
  <p class="hand pick">pick a binder</p>
  <div class="cab">
    <div class="open"><div class="binders">{spines}
    </div></div>
    <div class="front"><span class="plate"><i>Pitches</i></span><span class="pull"></span></div>
    <div class="front low"><span class="plate"><i>Archive</i></span><span class="pull"></span></div>
  </div>
  <p class="note">Private. Reached only by typing "pitch", or by a direct link to one pitch. Stops marked "confirm" inside each pitch still need checking.</p>
</main>
{books}
{BRIDGE}
<script>{HUB_JS}</script>
</body>
</html>
'''

if __name__ == '__main__':
    with open(os.path.join(ROOT, 'pitches.html'), 'w', encoding='utf-8') as f: f.write(hub())
    for h in HOTELS:
        with open(os.path.join(ROOT, f"pitch-{h['slug']}.html"), 'w', encoding='utf-8') as f: f.write(hotel_page(h))
    print('wrote', 1 + len(HOTELS), 'pages')
