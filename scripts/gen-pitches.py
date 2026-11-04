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
  slug='nomad', no='01', city='New York City', name='The Ritz-Carlton New York, NoMad', short='Ritz-Carlton NoMad',
  tagline='A skyline stay, with the whole city a short walk away.',
  hand='golden hour, 50 floors up',
  fonts='Cormorant+Garamond:ital,wght@0,400;0,600;1,400&family=Poppins:wght@300;400;500&family=Caveat:wght@500',
  head="'Cormorant Garamond',Georgia,serif", body="'Poppins',sans-serif",
  c=dict(desk='#0d1120', paper='#f7f1e3', ink='#1a2038', accent='#b8934a', accent2='#1f2a52', soft='#efe5cd'),
  vibe=['Deep navy', 'Champagne gold', 'Warm lamplight'],
  facts=[
   'Oversize windows and gold-link light fixtures in the rooms.',
   'José Andrés restaurants in the hotel.',
   'Nubeluz, a cocktail bar on the 50th floor.',
   'In NoMad, with Madison Square Park, Flatiron, and Chelsea nearby.',
  ],
  why='The most "New York at night" stay on the list. It gives a hotel pitch its strongest opening shot: the window, then the skyline, then a walk that starts right at the lobby.',
  angle=dict(
   hotel='Open on the window view at dusk. Cut to Nubeluz, then a map of the walk to Madison Square Park, Flatiron, and the Chelsea galleries. Close with a hotel dinner.',
   luggage='Packed flat-lay at home, the case on the curb outside the lobby, then the SoHo haul unpacked in the room.',
   airline='Landing into the city lights, then a cab straight to NoMad. Make the skyline the payoff for the flight.'),
  pins=[
   ('stay','Room view and amenities','here','Oversize windows are the opening shot.',False),
   ('eat','José Andrés dinner at the hotel','here','The luxury restaurant payoff.',False),
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
   ('pack','Pack-up flat-lay','here','The luggage "after" shot: bags full of finds.',False),
  ]),
 dict(
  slug='brooklyn', no='02', city='New York City', name='1 Hotel Brooklyn Bridge', short='1 Hotel Brooklyn Bridge',
  tagline='Nature-forward luxury on the Dumbo waterfront.',
  hand='skyline, but make it calm',
  fonts='Fraunces:ital,wght@0,300;0,500;1,300&family=Inter:wght@300;400;500&family=Caveat:wght@500',
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
   hotel='Lead with the skyline across the water, then the spa and rooftop pool. Show the Dumbo walk: bridge park, carousel, cobblestones.',
   luggage='A "weekend away" packing story: skincare, linen outfits, and a market haul in the bag. Show the bag on cobblestones.',
   airline='Short-haul angle: a quick flight into New York, then a slow morning on the waterfront.'),
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
  fonts='Cormorant+Garamond:ital,wght@0,400;0,600;1,400&family=Inter:wght@300;400;500&family=Caveat:wght@500',
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
   hotel='Sunrise on the water, the beach walk, and the lobby-to-sea path. Then a "worth the ride" day in Kakaʻako to show the local side.',
   luggage='Pack for the beach and bring home locally made goods: the bag filled with House of Mana Up and MORI finds.',
   airline='The descent into Honolulu, then arrival and a lei moment. The destination is the whole payoff.'),
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
  fonts='Fraunces:ital,wght@0,300;0,500;1,300&family=Inter:wght@300;400;500&family=Caveat:wght@500',
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
   hotel='Sunset from the room, a walk to Palisades Park, then a ride to Venice for matcha and boutiques.',
   luggage='A "cute LA haul" story: home goods and clothes from Abbot Kinney going into the bag, then unpacked at home.',
   airline='The window view coming in over the coast, then sunset on arrival.'),
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
  fonts='Cormorant+Garamond:ital,wght@0,400;0,600;1,400&family=Inter:wght@300;400;500&family=Caveat:wght@500',
  head="'Cormorant Garamond',Georgia,serif", body="'Inter',sans-serif",
  c=dict(desk='#173a55', paper='#f4f1ea', ink='#1c3447', accent='#3a7ca5', accent2='#9fcbc0', soft='#e3ebea'),
  vibe=['Sea-glass', 'Navy', 'White linen'],
  facts=[
   'Upscale beachfront retreat in Santa Monica with ocean views.',
   'Beach path access toward Venice (confirm walking time).',
   'Near the Santa Monica Pier.',
  ],
  why='The easy, breezy beach option. It pairs well with the luggage pitch: sand, sun, and a bag that goes from the airport to the boardwalk.',
  angle=dict(
   hotel='Wake up to the ocean, walk the beach path, then take a short ride to Venice. Show the stay as a slow coastal morning.',
   luggage='Beach-bag-to-boutique story: swimsuit, sunscreen, and a Malibu Country Mart haul all in one suitcase.',
   airline='The coast from the window, then the first sight of the ocean from the hotel.'),
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
    if (!a) return;
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
          --head:{h['head']}; --body:{h['body']}; --hand:'Caveat',cursive; }}
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
    <div class="kick">Three ways to tell it</div>
    <h2>One trip, three pitches</h2>
    <div class="notes">
      <div class="note"><h3>Hotel POV</h3><p>{esc(ang['hotel'])}</p></div>
      <div class="note"><h3>Luggage POV</h3><p>{esc(ang['luggage'])}</p></div>
      <div class="note"><h3>Airline POV</h3><p>{esc(ang['airline'])}</p></div>
    </div>
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

def hub():
    cards = ''
    for h in HOTELS:
        c = h['c']
        cards += f'''
    <a class="cover-card" href="pitch-{h['slug']}.html" style="--d:{c['desk']};--a:{c['accent']};--b:{c['accent2']};--p:{c['paper']};--hf:{h['head']}">
      <span class="spine"></span>
      <span class="no">{h['no']}</span>
      <span class="city">{esc(h['city'])}</span>
      <span class="nm">{esc(h['short'])}</span>
      <span class="hd">{esc(h['hand'])}</span>
    </a>'''
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="robots" content="noindex">
<title>Pitch center</title>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,wght@0,300;0,500;1,300&family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400&family=Inter:wght@300;400&family=Caveat:wght@500&display=swap" rel="stylesheet">
<style>
  :root {{ --bg:#1b1713; --cream:#f3e9dc; --gold:#c9a66b; }}
  * {{ box-sizing:border-box; }}
  html,body {{ margin:0; background:var(--bg); color:var(--cream); font-family:'Inter',sans-serif; font-weight:300; -webkit-font-smoothing:antialiased; }}
  a {{ color:inherit; text-decoration:none; }}
  .wrap {{ max-width:1080px; margin:0 auto; padding:24px 16px 60px; }}
  .back {{ font-size:13px; letter-spacing:.06em; opacity:.8; }}
  h1 {{ font-family:'Fraunces',Georgia,serif; font-weight:300; font-size:clamp(36px,6vw,64px); margin:28px 0 8px; }}
  .lede {{ max-width:56ch; line-height:1.7; opacity:.85; }}
  .hand {{ font-family:'Caveat',cursive; font-size:24px; color:var(--gold); margin:6px 0 30px; }}
  .shelf {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(210px,1fr)); gap:22px; }}
  .cover-card {{ position:relative; display:flex; flex-direction:column; justify-content:flex-end; aspect-ratio:3/4; padding:20px 18px 18px 34px; border-radius:6px 14px 14px 6px;
     background:linear-gradient(160deg,var(--b),var(--a) 70%,var(--d)); color:#fff; box-shadow:0 14px 28px rgba(0,0,0,.4); transition:transform .25s; }}
  .cover-card:hover {{ transform:translateY(-6px) rotate(-1deg); }}
  .spine {{ position:absolute; left:0; top:0; bottom:0; width:18px; background:rgba(0,0,0,.28); border-radius:6px 0 0 6px; }}
  .no {{ position:absolute; top:16px; right:16px; font-size:12px; letter-spacing:.2em; opacity:.8; }}
  .city {{ font-size:11px; letter-spacing:.18em; text-transform:uppercase; opacity:.85; }}
  .nm {{ font-family:var(--hf); font-size:28px; line-height:1.05; margin:8px 0; }}
  .hd {{ font-family:'Caveat',cursive; font-size:22px; opacity:.9; }}
  .note {{ margin-top:40px; font-size:13px; opacity:.6; line-height:1.7; }}
</style>
</head>
<body>
<div class="wrap">
  <a class="back" href="index.html">&larr; Home</a>
  <h1>Pitch center</h1>
  <p class="lede">A private shelf of travel-guide notebooks, one per stay. Each one is styled to the hotel's own mood and pins the itinerary I'd shoot for a hotel, luggage, or airline pitch.</p>
  <p class="hand">pick a notebook</p>
  <div class="shelf">{cards}
  </div>
  <p class="note">Private page, reached only by typing "pitch". Stops marked "confirm" inside each notebook still need checking.</p>
</div>
{BRIDGE}
</body>
</html>
'''

if __name__ == '__main__':
    with open(os.path.join(ROOT, 'pitches.html'), 'w', encoding='utf-8') as f: f.write(hub())
    for h in HOTELS:
        with open(os.path.join(ROOT, f"pitch-{h['slug']}.html"), 'w', encoding='utf-8') as f: f.write(hotel_page(h))
    print('wrote', 1 + len(HOTELS), 'pages')
