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
   'Oversize windows with the skyline in every frame.',
   'Bazaar Meat by José Andrés and Nubeluz on the 50th floor, without leaving the building.',
   'Bath time for baby, then for mom: Diptyque products, rain showers, and deep soaking tubs in some rooms.',
   'A fitness center open 24 hours, with Peloton bikes, next to a 6,800 sq ft spa.',
   'Ritz Kids activities, and pets welcome: up to two, 60 lbs combined, with a per-stay fee.',
   'In NoMad, with Madison Square Park, Flatiron, Chelsea, and SoHo pop-ups within easy reach.',
  ],
  hl=dict(
   title='Luxury, made easy for the whole family',
   lede="A beautiful hotel is only worth it if it works for the people I travel with. Here is what makes this one easy with a baby and a dog.",
   walks=[
    ('4','National Museum of Mathematics','National Museum of Mathematics, New York',False),
    ('5','Madison Square Park and Jemmy\'s Dog Run','Madison Square Park Dog Run, New York',True),
    ('6','LEGO Store, Fifth Avenue','LEGO Store, 5th Avenue, New York',False),
    ('8','Harry Potter New York','Harry Potter New York flagship store',False),
    ('8','Flatiron Building','Flatiron Building, New York',True),
   ],
   walknote='Times at about 20 minutes per mile. Museum, LEGO and Harry Potter distances are from the hotel\'s own listing; the park and Flatiron are estimates. Confirm on the day.',
   baby=[
    ('Cribs, extra beds, adjoining rooms and kids\' bath products','are part of Ritz-Carlton\'s family offering. Ask for each when booking.',True),
    ('Bath time:','deep soaking tubs in select rooms. Request a tub room for the baby\'s bath.',True),
    ('24-hour in-room dining,','so bottle and snack times never depend on a restaurant\'s hours.',False),
    ('Childcare:','the concierge can arrange it for an evening out.',True),
    ('Ritz Kids','is for ages 4 to 12, and Nubeluz has kids\' options at weekend high tea (Sat and Sun, 11 to 3). Ask about this season\'s Ritz Kids tea.',True),
   ],
   dog=[
    ('Pets welcome:','up to two, 60 lbs combined, no breed restrictions.',True),
    ('Pet beds, bowls and treats','are provided, subject to availability.',True),
    ('Morning and afternoon walks:','Madison Square Park is a few minutes away, with Jemmy\'s Dog Run: separate small and large dog areas, open with the park (around 6 am to 11 pm), waste bags provided.',True),
    ('Relief break:','the front desk can point to the closest grassy spot for a quick potty walk.',True),
    ('The fee','is per stay and reported anywhere from $250 to $375.',True),
   ],
   given=[
    ('In the hotel','Zaytinya, an all-day Mediterranean restaurant from José Andrés. Bazaar Meat by José Andrés, on Level 2. Nubeluz, the rooftop bar with 270-degree skyline views. The Lobby Lounge, for pastries and coffee in the morning and cocktails at night.',False),
    ('Views of the city','Oversize windows in the rooms, with views from the Empire State Building down to the Statue of Liberty.',False),
   ],
   mom=[
    ('Fitness center','open 24 hours, with Peloton bikes, right by the spa.',False),
    ('Spa:','a 6,800 sq ft spa with a sauna and steam room.',True),
    ('Bath and rain shower:','Diptyque products in every room.',False),
    ('Nubeluz and Bazaar Meat','are in the building, so a date night is an elevator ride.',False),
   ],
  ),
  why_title="What I'd show other moms",
  why="I'm a mom who travels with a baby and a dog, and I want other moms to see what's possible. Pampering and excitement belong back in the picture, without giving up anything baby or the dog needs. This stay makes that real: quiet rooms for naps, soaking tubs for bath time, a gym downstairs, a skyline bar for the night, and the trendy pop-ups I usually miss a short ride away.",
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

LEATHER = _uri("<svg xmlns='http://www.w3.org/2000/svg' width='320' height='320'><filter id='g' x='0' y='0' width='100%' height='100%'><feTurbulence type='fractalNoise' baseFrequency='1.7' numOctaves='4' seed='9' stitchTiles='stitch'/><feColorMatrix type='saturate' values='0'/><feComponentTransfer><feFuncR type='linear' slope='.55' intercept='.56'/><feFuncG type='linear' slope='.55' intercept='.56'/><feFuncB type='linear' slope='.55' intercept='.56'/></feComponentTransfer></filter><filter id='lt' x='0' y='0' width='100%' height='100%'><feTurbulence type='fractalNoise' baseFrequency='1.15 1.4' numOctaves='2' seed='21' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 1 0 0 0 0 1 0 0 0 0 1 5.5 0 0 0 -3.55'/></filter><filter id='dk' x='0' y='0' width='100%' height='100%'><feTurbulence type='fractalNoise' baseFrequency='1.3 1.1' numOctaves='2' seed='33' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 5 0 0 0 -3.3'/></filter><filter id='mo' x='0' y='0' width='100%' height='100%'><feTurbulence type='fractalNoise' baseFrequency='.018 .03' numOctaves='3' seed='6' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 .08 0 0 0 0 .04 0 0 0 0 0 .5 0 0 0 -.15'/></filter><filter id='sw' x='0' y='0' width='100%' height='100%'><feTurbulence type='fractalNoise' baseFrequency='.06 .5' numOctaves='2' seed='14' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 1 0 0 0 0 1 0 0 0 0 1 1.6 0 0 0 -.95'/></filter><rect width='320' height='320' filter='url(#g)'/><rect width='320' height='320' filter='url(#sw)' opacity='.35'/><rect width='320' height='320' filter='url(#lt)' opacity='.55'/><rect width='320' height='320' filter='url(#dk)' opacity='.45'/><rect width='320' height='320' filter='url(#mo)' opacity='.5'/></svg>")
PAPERT = _uri("<svg xmlns='http://www.w3.org/2000/svg' width='300' height='300'><filter id='t' x='0' y='0' width='100%' height='100%'><feTurbulence type='fractalNoise' baseFrequency='.75' numOctaves='4' seed='2' stitchTiles='stitch' result='n'/><feDiffuseLighting in='n' surfaceScale='.55' diffuseConstant='1' lighting-color='#ffffff'><feDistantLight azimuth='225' elevation='72'/></feDiffuseLighting></filter><filter id='f1' x='0' y='0' width='100%' height='100%'><feTurbulence type='fractalNoise' baseFrequency='.9 .07' numOctaves='2' seed='5' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 .35 0 0 0 0 .3 0 0 0 0 .22 0 0 0 1.2 -.62'/></filter><filter id='f2' x='0' y='0' width='100%' height='100%'><feTurbulence type='fractalNoise' baseFrequency='.07 .9' numOctaves='2' seed='8' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 .35 0 0 0 0 .3 0 0 0 0 .22 0 0 0 1.2 -.64'/></filter><filter id='cl' x='0' y='0' width='100%' height='100%'><feTurbulence type='fractalNoise' baseFrequency='.012' numOctaves='3' seed='3' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 .5 0 0 0 0 .42 0 0 0 0 .3 .35 0 0 0 -.1'/></filter><rect width='300' height='300' filter='url(#t)'/><rect width='300' height='300' filter='url(#f1)' opacity='.12'/><rect width='300' height='300' filter='url(#f2)' opacity='.1'/><rect width='300' height='300' filter='url(#cl)' opacity='.35'/></svg>")
CLOTH = _uri("<svg xmlns='http://www.w3.org/2000/svg' width='160' height='160'><filter id='a' x='0' y='0' width='100%' height='100%'><feTurbulence type='fractalNoise' baseFrequency='1.1 .1' numOctaves='2' seed='4' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1.1 0 0 0 -.38'/></filter><filter id='b' x='0' y='0' width='100%' height='100%'><feTurbulence type='fractalNoise' baseFrequency='.1 1.1' numOctaves='2' seed='7' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 1 0 0 0 0 1 0 0 0 0 1 .9 0 0 0 -.4'/></filter><rect width='160' height='160' filter='url(#a)' opacity='.55'/><rect width='160' height='160' filter='url(#b)' opacity='.4'/></svg>")
WOODH = _uri("<svg xmlns='http://www.w3.org/2000/svg' width='600' height='160'><filter id='w' x='0' y='0' width='100%' height='100%'><feTurbulence type='fractalNoise' baseFrequency='.006 .45' numOctaves='4' seed='5' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 .32 0 0 0 0 .2 0 0 0 0 .09 1.15 0 0 0 -.42'/></filter><filter id='t' x='0' y='0' width='100%' height='100%'><feTurbulence type='fractalNoise' baseFrequency='.004 .06' numOctaves='3' seed='12' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 .25 0 0 0 0 .14 0 0 0 0 .05 .9 0 0 0 -.3'/></filter><rect width='600' height='160' filter='url(#t)'/><rect width='600' height='160' filter='url(#w)'/></svg>")
WOODV = _uri("<svg xmlns='http://www.w3.org/2000/svg' width='160' height='600'><filter id='w' x='0' y='0' width='100%' height='100%'><feTurbulence type='fractalNoise' baseFrequency='.45 .006' numOctaves='4' seed='8' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 .32 0 0 0 0 .2 0 0 0 0 .09 1.15 0 0 0 -.42'/></filter><filter id='t' x='0' y='0' width='100%' height='100%'><feTurbulence type='fractalNoise' baseFrequency='.06 .004' numOctaves='3' seed='12' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 .25 0 0 0 0 .14 0 0 0 0 .05 .9 0 0 0 -.3'/></filter><rect width='160' height='600' filter='url(#t)'/><rect width='160' height='600' filter='url(#w)'/></svg>")
PAPERN = _uri("<svg xmlns='http://www.w3.org/2000/svg' width='200' height='200'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.8' numOctaves='2' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 .3 0 0 0 0 .25 0 0 0 0 .2 0 0 0 .09 0'/></filter><rect width='100%' height='100%' filter='url(#n)'/></svg>")

# Shared by the hub's open binder and the opener on each pitch page.
BINDER_CSS = r"""
  .bd-book { position:relative; width:var(--bw,min(760px,94vw)); height:var(--bh,min(84vh,860px)); border-radius:12px; color:#2a2420;
     background-color:var(--lea,#4a2621); background-image:%%LEATHER%%, radial-gradient(ellipse at 28% 18%, rgba(255,255,255,.2), transparent 55%), linear-gradient(150deg,var(--lea,#4a2621),var(--lea2,#2a110d));
     background-blend-mode:multiply, soft-light, normal; box-shadow:0 34px 60px rgba(40,26,14,.38), 0 3px 8px rgba(40,26,14,.25); }
  .bd-book::after { content:''; position:absolute; inset:11px; border:1px solid var(--stitch,rgba(255,255,255,.14)); border-radius:7px; pointer-events:none; }
  .bd-page { position:absolute; left:68px; right:48px; top:28px; bottom:28px; background-color:#f1ebdd; background-image:%%PAPERT%%; border-radius:2px 6px 6px 2px; padding:34px 40px 24px 42px; overflow:hidden;
     box-shadow:0 1px 0 #ddd5c1, 0 2px 0 #f2ecdf, 0 3px 0 #cfc6b0, 0 4px 6px rgba(0,0,0,.45), inset 14px 0 20px -14px rgba(0,0,0,.3); z-index:2; }
  .bd-rings { position:absolute; left:22px; top:9%; bottom:9%; width:84px; z-index:4; display:flex; flex-direction:column; justify-content:space-between; pointer-events:none; }
  .bd-ring { position:relative; width:84px; height:20px; border-radius:12px; background:linear-gradient(180deg,#7b7e82 0,#f6f7f8 16%,#cfd2d4 38%,#6d7074 62%,#c3c6c8 84%,#85888c 100%); box-shadow:0 5px 7px rgba(0,0,0,.45), 0 1px 1px rgba(0,0,0,.5), inset 0 0 0 1px rgba(0,0,0,.14); }
  .bd-ring::after { content:''; position:absolute; right:10px; top:3px; width:14px; height:14px; border-radius:50%; background:#17110e; box-shadow:inset 0 1px 3px #000; }
  .bd-tabs { position:absolute; right:20px; top:44px; bottom:44px; width:52px; z-index:3; display:flex; flex-direction:column; gap:7px; }
  .bd-tab { flex:0 0 auto; width:44px; min-height:92px; padding:12px 0; writing-mode:vertical-rl; text-align:center; font-family:'Nothing You Could Do',cursive; font-size:19px; line-height:1; color:#2b2420; background:#e8dfcb; background-image:%%PAPERT%%;
     border-radius:0 9px 9px 0; box-shadow:2px 2px 5px rgba(0,0,0,.35); transition:transform .25s, background-color .25s; cursor:pointer; display:flex; align-items:center; justify-content:center; }
  .bd-tab:nth-child(2n) { background-color:#ddd2ba; } .bd-tab:nth-child(3n) { background-color:#efe7d6; }
  .bd-tab:hover,.bd-tab:focus-visible { transform:translateX(9px); outline:none; background-color:#fff8e6; }
  .bd-tab.ghost { background:transparent; box-shadow:none; border:1px dashed rgba(255,255,255,.35); border-left:0; color:rgba(255,255,255,.6); cursor:default; }
  .bd-tab.ghost:hover { transform:none; background:transparent; }
  .bd-clip { position:absolute; width:26px; height:76px; z-index:5; filter:drop-shadow(1px 2px 1px rgba(0,0,0,.35)); }
  .bd-kick { font:500 11px/1 'Inter',sans-serif; letter-spacing:.32em; text-transform:uppercase; color:#8a7a62; }
  .bd-foil { color:var(--deb,rgba(0,0,0,.5)); text-shadow:var(--debs,0 1px 0 rgba(255,255,255,.25)); }
  @media (max-width:640px) {
    .bd-page { left:50px; right:34px; top:20px; bottom:20px; padding:24px 20px 16px 22px; }
    .bd-rings { left:14px; width:68px; } .bd-ring { width:68px; height:17px; } .bd-ring::after { width:12px; height:12px; right:8px; top:2px; }
    .bd-tabs { right:8px; width:38px; top:34px; } .bd-tab { width:32px; min-height:70px; font-size:15px; padding:9px 0; }
  }
""".replace('%%LEATHER%%', LEATHER).replace('%%PAPERT%%', PAPERT).replace('%%PAPERN%%', PAPERN)

CLIP = '<svg class="bd-clip" viewBox="0 0 26 76" aria-hidden="true"><path d="M5 52V15a8 8 0 0 1 16 0v47a11 11 0 0 1-22 0V22" transform="translate(2 0)" fill="none" stroke="#a8acb2" stroke-width="2.4" stroke-linecap="round"/></svg>'

HUB_CSS = r"""
  * { box-sizing:border-box; }
  html,body { margin:0; min-height:100%; color:#2b2520; font-family:'Inter',sans-serif; font-weight:300; -webkit-font-smoothing:antialiased;
     background:#e4ddd0; background-image:%%PAPERN%%, radial-gradient(ellipse at 50% -10%, #f6f1e8, #e1d9ca 72%); }
  a { color:inherit; text-decoration:none; } button { font:inherit; color:inherit; }
  .hand { font-family:'Nothing You Could Do',cursive; font-weight:400; }
  .back { position:fixed; top:14px; left:18px; z-index:20; font-size:11px; letter-spacing:.16em; text-transform:uppercase; opacity:.6; }
  .room { max-width:1060px; margin:0 auto; padding:64px 18px 60px; text-align:center; }
  .eyebrow { font-size:11px; letter-spacing:.34em; text-transform:uppercase; color:#8a7a64; margin:0; }
  h1 { font-family:'Fraunces',Georgia,serif; font-weight:300; font-size:clamp(40px,6vw,72px); letter-spacing:-.01em; margin:12px 0 0; line-height:1.05; }
  .pick { font-size:21px; color:#8a7a64; margin:10px 0 34px; }
  .note { margin:38px auto 0; max-width:60ch; font-size:12px; line-height:1.7; opacity:.5; }
  .unit { position:relative; display:grid; grid-template-columns:clamp(16px,2.6vw,30px) 1fr clamp(16px,2.6vw,30px); box-shadow:0 46px 50px -26px rgba(50,32,16,.5), 0 6px 10px rgba(50,32,16,.25); }
  .side { background-color:#b98e5e; background-image:%%WOODV%%, linear-gradient(90deg,rgba(255,255,255,.18),rgba(0,0,0,.12) 55%,rgba(0,0,0,.22)); box-shadow:inset 0 0 0 1px rgba(60,36,14,.35); }
  .side:last-child { background-image:%%WOODV%%, linear-gradient(270deg,rgba(255,255,255,.18),rgba(0,0,0,.12) 55%,rgba(0,0,0,.22)); }
  .bay { position:relative; background-color:#a77f55; background-image:%%WOODV%%, linear-gradient(180deg,rgba(0,0,0,.42),rgba(0,0,0,.08) 30%,rgba(0,0,0,.18)); box-shadow:inset 0 18px 26px rgba(30,16,4,.5), inset 14px 0 22px -8px rgba(30,16,4,.45), inset -14px 0 22px -8px rgba(30,16,4,.45); }
  .shelfrow { position:relative; display:flex; align-items:flex-end; justify-content:center; padding:0 4%; }
  .shelfrow.one { height:clamp(310px,52vh,450px); gap:2px; }
  .shelfrow.two { height:clamp(140px,21vh,190px); justify-content:space-between; padding:0 8%; }
  .board { height:clamp(16px,2.6vw,24px); position:relative; z-index:3; background-color:#c9a171; background-image:%%WOODH%%, linear-gradient(180deg,rgba(255,255,255,.34),rgba(255,255,255,0) 22%,rgba(0,0,0,.0) 60%,rgba(0,0,0,.28));
     box-shadow:0 1px 0 rgba(60,34,12,.55), 0 14px 18px -4px rgba(25,12,2,.55), inset 0 -2px 0 rgba(60,34,12,.3); }
  .shelfrow::after { content:''; position:absolute; left:0; right:0; bottom:0; height:14px; background:linear-gradient(180deg,rgba(20,10,2,0),rgba(20,10,2,.42)); pointer-events:none; }
  .binders { display:contents; }
  .spine { position:relative; flex:0 1 clamp(62px,12vw,118px); height:var(--h,90%); border:0; padding:0; cursor:pointer; border-radius:4px 4px 0 0; z-index:2;
     background-color:var(--lea);
     background-image:%%LEATHER%%, linear-gradient(90deg, rgba(0,0,0,.34) 0, rgba(255,255,255,.2) 5%, rgba(255,255,255,.06) 14%, rgba(0,0,0,0) 40%, rgba(0,0,0,.12) 78%, rgba(0,0,0,.4) 100%), linear-gradient(180deg, rgba(255,255,255,.12), rgba(0,0,0,0) 8%, rgba(0,0,0,0) 94%, rgba(0,0,0,.22));
     background-blend-mode:multiply, normal, normal; box-shadow:2px 0 3px rgba(20,10,2,.35), 7px 0 14px rgba(20,10,2,.3); transition:transform .25s ease, box-shadow .25s ease; }
  .spine::before, .spine::after { content:''; position:absolute; top:0; bottom:0; width:2px; }
  .spine::before { left:10px; background:linear-gradient(90deg,rgba(0,0,0,.32),rgba(255,255,255,.1)); }
  .spine::after { right:10px; background:linear-gradient(90deg,rgba(255,255,255,.08),rgba(0,0,0,.28)); }
  .spine:hover,.spine:focus-visible { transform:translateY(-14px); box-shadow:2px 0 3px rgba(20,10,2,.35), 10px 16px 20px rgba(20,10,2,.35); outline:none; }
  .spine .lbl { position:absolute; left:50%; top:13%; transform:translateX(-50%); width:50%; padding:14px 0; display:flex; flex-direction:row; align-items:center; justify-content:center; gap:14px; writing-mode:vertical-rl; z-index:1;
     color:var(--deb); text-shadow:var(--debs); border:1.5px solid var(--deb); border-radius:2px; box-shadow:0 1px 0 rgba(255,255,255,.18), inset 0 1px 1px rgba(0,0,0,.18); }
  .spine .lbl b { font:600 clamp(14px,1.8vw,19px)/1 'Fraunces',Georgia,serif; letter-spacing:.3em; text-transform:uppercase; }
  .spine .lbl i { font:500 9px/1 'Inter',sans-serif; font-style:normal; letter-spacing:.22em; text-transform:uppercase; opacity:.8; }
  .spine .no { position:absolute; left:0; right:0; bottom:18px; text-align:center; font:500 11px/1 'Inter',sans-serif; letter-spacing:.2em; color:var(--deb); text-shadow:var(--debs); z-index:1; }
  .spine .rule { position:absolute; left:14px; right:14px; height:2px; background:var(--deb); opacity:.45; box-shadow:0 1px 0 rgba(255,255,255,.25); border-radius:1px; }
  .spine .rule.a { top:7%; } .spine .rule.b { bottom:46px; }
  /* lower shelf: standing books, lying stack, ceramic vase with branches */
  .bshelf { display:flex; align-items:flex-end; gap:0; height:86%; }
  .bv { display:block; width:var(--w,18px); height:var(--h,80%); position:relative; transform:rotate(var(--r,0deg)); transform-origin:bottom left; margin-right:var(--m,0); border-radius:2px 2px 0 0 / 3px 3px 0 0;
     background-color:var(--c); background-image:%%CLOTH%%, linear-gradient(90deg,rgba(0,0,0,.38) 0,rgba(255,255,255,.14) 9%,rgba(0,0,0,0) 30%,rgba(0,0,0,.12) 74%,rgba(0,0,0,.45) 100%), linear-gradient(180deg,rgba(255,255,255,.1),rgba(0,0,0,0) 10%,rgba(0,0,0,.12)); box-shadow:1px 0 2px rgba(15,8,2,.55), 4px 0 8px rgba(15,8,2,.25); }
  .bv::before { content:''; position:absolute; left:3px; right:3px; top:10%; height:5px; border-top:1px solid var(--g,rgba(230,205,150,.7)); border-bottom:1px solid var(--g,rgba(230,205,150,.7)); opacity:.85; }
  .bv::after { content:''; position:absolute; left:34%; right:34%; top:26%; bottom:18%; background:repeating-linear-gradient(180deg, var(--g,rgba(230,205,150,.62)) 0 1.5px, transparent 1.5px 7px); opacity:.7; }
  .bv.plain::after { display:none; }
  .lying { display:flex; flex-direction:column; justify-content:flex-end; width:clamp(110px,20vw,210px); margin-left:14px; }
  .bk { display:block; height:var(--t,22px); width:var(--w,100%); margin-left:var(--ml,0); position:relative; border-radius:1px 3px 3px 1px;
     background:repeating-linear-gradient(180deg,#efe8d6 0 1px,#d6ccb4 1px 2px); border-left:8px solid var(--c); box-shadow:0 2px 3px rgba(15,8,2,.5), inset -3px 0 4px rgba(90,70,40,.35); }
  .bk::before,.bk::after { content:''; position:absolute; left:-8px; right:-1px; height:4px; background-color:var(--c); background-image:%%CLOTH%%; }
  .bk::before { top:-1px; border-radius:1px 3px 0 0; } .bk::after { bottom:-1px; border-radius:0 0 3px 1px; }
  .plant { position:relative; width:clamp(90px,17vw,160px); height:100%; align-self:flex-end; }
  .plant svg { position:absolute; left:50%; bottom:-1px; transform:translateX(-50%); height:112%; width:auto; max-width:none; overflow:visible; filter:drop-shadow(4px 6px 5px rgba(15,8,2,.4)); }
  .bay::after { content:''; position:absolute; inset:0; z-index:4; pointer-events:none;
     background:radial-gradient(ellipse at 22% -6%, rgba(255,238,205,.30), rgba(255,238,205,0) 55%), radial-gradient(ellipse at 50% 55%, rgba(0,0,0,0) 55%, rgba(20,10,2,.28) 100%), %%PAPERN%%; mix-blend-mode:soft-light; }
  .ob { position:fixed; inset:0; z-index:100; display:flex; align-items:center; justify-content:center; background:rgba(34,26,20,.55); backdrop-filter:blur(6px); opacity:0; pointer-events:none; transition:opacity .3s; }
  .ob.show { opacity:1; pointer-events:auto; }
  .ob .x { position:absolute; top:14px; left:16px; background:none; border:0; cursor:pointer; font-size:11px; letter-spacing:.16em; text-transform:uppercase; color:#fff; opacity:.85; z-index:5; }
  .ob .stage { perspective:2400px; }
  .ob .bd-book { transform:translateY(24px) scale(.96); transition:transform .5s ease, opacity .45s; }
  .ob.show .bd-book { transform:none; }
  .ob.leaving .bd-book { transform:scale(1.5); opacity:0; }
  .ob .cov { position:absolute; inset:0; z-index:8; border-radius:12px; transform-origin:left center; transition:transform .95s cubic-bezier(.55,.05,.25,1), opacity .25s .75s; backface-visibility:hidden; display:flex; align-items:center; justify-content:center; text-align:center;
     background-color:var(--lea); background-image:%%LEATHER%%, linear-gradient(135deg, rgba(255,255,255,.12), rgba(255,255,255,0) 50%, rgba(0,0,0,.16)); background-blend-mode:multiply, normal; }
  .ob .cov::before { content:''; position:absolute; inset:11px; border:1px solid var(--stitch,rgba(255,255,255,.14)); border-radius:7px; }
  .ob .cov .in { display:flex; flex-direction:column; gap:16px; align-items:center; color:var(--deb); }
  .ob .cov .t { font-family:'Fraunces',serif; font-weight:300; font-size:clamp(44px,8vw,88px); line-height:1; letter-spacing:.01em; }
  .ob .cov .kk, .ob .cov .cn { font:400 11px/1 'Inter',sans-serif; letter-spacing:.32em; text-transform:uppercase; opacity:.85; text-shadow:var(--debs); }
  .ob.opened .cov { transform:rotateY(-168deg); opacity:0; pointer-events:none; }
  .bd-page h2 { font-family:'Fraunces',serif; font-weight:300; font-size:clamp(46px,7vw,80px); line-height:1; margin:14px 0 4px; letter-spacing:-.01em; }
  .bd-page .sub { font-size:22px; color:#7a6a54; margin-bottom:26px; }
  .idx { list-style:none; margin:0; padding:0; }
  .row { display:grid; grid-template-columns:1fr auto; align-items:center; gap:2px 10px; border-bottom:1px solid rgba(60,45,30,.16); padding:11px 0; }
  .row .go { display:grid; grid-template-columns:34px 1fr auto; align-items:baseline; gap:8px; }
  .row .go b { font:400 12px/1 'Inter',sans-serif; color:#9a8660; letter-spacing:.1em; }
  .row .n { font-family:'Fraunces',serif; font-weight:400; font-size:clamp(18px,2.2vw,24px); line-height:1.15; }
  .row .c { font-size:10px; letter-spacing:.2em; text-transform:uppercase; color:#8a7a62; }
  .row .go:hover .n { text-decoration:underline; text-decoration-thickness:1px; text-underline-offset:4px; }
  .row .cp { background:none; border:1px solid rgba(60,45,30,.3); border-radius:99px; padding:4px 11px; font-size:10px; letter-spacing:.14em; text-transform:uppercase; cursor:pointer; color:#4a3d2c; }
  .row .cp:hover { background:#2a211a; color:#f2ecdf; }
  .row .lk { display:none; grid-column:1/-1; width:100%; border:1px dashed rgba(60,45,30,.4); background:rgba(255,255,255,.4); font:12px/1.4 'Inter',sans-serif; padding:6px 8px; color:#2a211a; }
  .row.showlink .lk { display:block; }
  .hnote { font-family:'Nothing You Could Do',cursive; font-size:18px; color:#7a6850; margin:18px 0 0; }
  .soon { padding-top:10px; } .soon .big { font-size:42px; color:#6b5a44; transform:rotate(-3deg); margin:6px 0 6px; } .soon p { max-width:34ch; line-height:1.7; font-size:14px; color:#6b5a44; }
  .ruled { margin-top:26px; } .ruled i { display:block; height:34px; border-bottom:1px solid rgba(60,45,30,.16); }
  @media (max-width:640px) {
    .room { padding-top:56px; } .spine::before { left:6px; } .spine::after { right:6px; } .spine .rule { left:11px; right:11px; } .spine .lbl { width:62%; }
    .row .go { grid-template-columns:26px 1fr; } .row .c { grid-column:2; } .bd-page h2 { font-size:48px; }
    .bd-book { --bw:94vw; --bh:86vh; }
    .shelfrow.two { padding:0 6%; }
  }
  @media (prefers-reduced-motion: reduce) { .ob .cov,.ob .bd-book,.spine { transition:none; } }
""".replace('%%LEATHER%%', LEATHER).replace('%%CLOTH%%', CLOTH).replace('%%PAPERN%%', PAPERN).replace('%%WOODH%%', WOODH).replace('%%WOODV%%', WOODV)

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
 dict(id='travel', no='01', title='Travel', sub='hotel & destination pitches', lea='#9a6b47', lea2='#6d4529', deb='rgba(38,20,8,.62)', debs='0 1px 0 rgba(255,228,196,.3), 0 -1px 1px rgba(0,0,0,.32)',
      pitches=[('nomad', 'NoMad'), ('brooklyn', '1 Hotel'), ('halekulani', 'Halekulani'), ('proper', 'Proper'), ('shutters', 'Shutters')]),
 dict(id='skincare', no='02', title='Skincare', sub='routines & rituals', lea='#d3b2a4', lea2='#b9917f', deb='rgba(88,52,40,.6)', debs='0 1px 0 rgba(255,255,255,.38), 0 -1px 1px rgba(60,30,20,.25)', pitches=[]),
 dict(id='homegoods', no='03', title='Homegoods', sub='rooms & rituals at home', lea='#8b9479', lea2='#667057', deb='rgba(25,32,18,.6)', debs='0 1px 0 rgba(255,255,255,.22), 0 -1px 1px rgba(10,16,6,.35)', pitches=[]),
 dict(id='fashion', no='04', title='Fashion', sub='wardrobe & style pitches', lea='#3d3a38', lea2='#252322', deb='rgba(0,0,0,.7)', debs='0 1px 0 rgba(255,255,255,.14), 0 -1px 1px rgba(0,0,0,.6)', pitches=[]),
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
      <button class="spine" type="button" data-open="{b['id']}" style="--lea:{b['lea']};--lea2:{b['lea2']};--deb:{b['deb']};--debs:{b['debs']};--h:{hgt}%" aria-label="Open the {b['title']} binder">
        <span class="rule a"></span>
        <span class="lbl"><b>{b['title']}</b><i>{cnt}</i></span>
        <span class="rule b"></span>
        <span class="no">{b['no']}</span>
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
    <button class="x" type="button">&larr; back to the shelf</button>
    <div class="stage"><div class="bd-book" style="--lea:{b['lea']};--lea2:{b['lea2']};--deb:{b['deb']};--debs:{b['debs']}">
      <div class="bd-page">
        {clip}
        <div class="bd-kick">Binder {b['no']}</div>
        <h2>{b['title']}</h2>
        <div class="hand sub">{esc(b['sub'])}</div>
        {page}
      </div>
      <nav class="bd-tabs">{tabs}</nav>
      <div class="bd-rings">{rings}</div>
      <div class="cov"><div class="in"><span class="kk">Binder {b['no']}</span><span class="t bd-foil">{b['title']}</span><span class="cn">{esc(b['sub'])}</span></div></div>
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
  <h1>The pitch library</h1>
  <p class="hand pick">choose a binder</p>
  <div class="unit">
    <div class="side"></div>
    <div class="bay">
      <div class="shelfrow one"><div class="binders">{spines}
      </div></div>
      <div class="board"></div>
      <div class="shelfrow two">
        <div class="bshelf">
          <span class="bv" style="--w:21px;--h:80%;--c:#4b5a4d"></span><span class="bv" style="--w:27px;--h:92%;--c:#7a3f36;--g:rgba(225,195,140,.7)"></span><span class="bv plain" style="--w:17px;--h:72%;--c:#d4c9b2"></span><span class="bv" style="--w:23px;--h:86%;--c:#34495c"></span><span class="bv plain" style="--w:15px;--h:66%;--c:#9a8461"></span><span class="bv" style="--w:25px;--h:90%;--c:#5b4c3f;--m:3px"></span><span class="bv plain" style="--w:19px;--h:82%;--c:#b3a384;--r:7deg;--m:12px"></span>
          <div class="lying"><span class="bk" style="--t:25px;--c:#35435a"></span><span class="bk" style="--t:20px;--c:#8e5a40;--w:91%;--ml:5%"></span><span class="bk" style="--t:27px;--c:#4a5946;--w:97%;--ml:1%"></span></div>
        </div>
        <div class="plant"><svg viewBox="0 0 160 262" aria-hidden="true"><defs>
<linearGradient id="lg1" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#8da57a"/><stop offset="1" stop-color="#52703f"/></linearGradient>
<linearGradient id="lg2" x1="0" y1="1" x2="1" y2="0"><stop offset="0" stop-color="#6d8a5c"/><stop offset="1" stop-color="#9bb08a"/></linearGradient>
<linearGradient id="lg3" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#7a9566"/><stop offset="1" stop-color="#3f5c36"/></linearGradient>
<linearGradient id="vz" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#9d9484"/><stop offset=".22" stop-color="#efe9dc"/><stop offset=".5" stop-color="#ddd5c4"/><stop offset=".82" stop-color="#a79e8c"/><stop offset="1" stop-color="#6f6758"/></linearGradient>
<filter id="spk" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="1.2" numOctaves="2" seed="3"/><feColorMatrix values="0 0 0 0 .3 0 0 0 0 .24 0 0 0 0 .18 0 0 0 3 -1.85"/><feComposite in2="SourceGraphic" operator="in"/></filter>
<clipPath id="vc"><path d="M52 186 C46 200 40 232 46 252 C47 258 52 260 58 260 L102 260 C108 260 113 258 114 252 C120 232 114 200 108 186Z"/></clipPath></defs>
<path d="M80 176 Q72 150 46 40" stroke="#5a4a32" stroke-width="1.7" fill="none" stroke-linecap="round"/><path d="M80 176 Q82 120 88 16" stroke="#5a4a32" stroke-width="1.7" fill="none" stroke-linecap="round"/><path d="M80 176 Q92 150 128 52" stroke="#5a4a32" stroke-width="1.7" fill="none" stroke-linecap="round"/><path d="M80 176 Q78 150 26 96" stroke="#5a4a32" stroke-width="1.7" fill="none" stroke-linecap="round"/><path d="M80 176 Q88 140 138 108" stroke="#5a4a32" stroke-width="1.7" fill="none" stroke-linecap="round"/><g transform="translate(74.1 154.9) rotate(-57.7)"><path d="M0 0 C3.9 -6.5 13.9 -6.8 19.4 0 C13.9 6.8 3.9 6.5 0 0Z" fill="url(#lg2)" stroke="rgba(30,45,25,.45)" stroke-width=".5"/><path d="M0 0 L17.4 0" stroke="rgba(235,240,215,.35)" stroke-width=".6"/></g><g transform="translate(72.3 148.0) rotate(-151.5)"><path d="M0 0 C4.2 -5.8 15.3 -6.1 21.2 0 C15.3 6.1 4.2 5.8 0 0Z" fill="url(#lg3)" stroke="rgba(30,45,25,.45)" stroke-width=".5"/><path d="M0 0 L19.1 0" stroke="rgba(235,240,215,.35)" stroke-width=".6"/></g><g transform="translate(70.4 140.4) rotate(-56.8)"><path d="M0 0 C3.9 -5.3 13.9 -5.6 19.3 0 C13.9 5.6 3.9 5.3 0 0Z" fill="url(#lg2)" stroke="rgba(30,45,25,.45)" stroke-width=".5"/><path d="M0 0 L17.3 0" stroke="rgba(235,240,215,.35)" stroke-width=".6"/></g><g transform="translate(68.3 132.2) rotate(-148.2)"><path d="M0 0 C3.1 -5.0 11.1 -5.3 15.4 0 C11.1 5.3 3.1 5.0 0 0Z" fill="url(#lg3)" stroke="rgba(30,45,25,.45)" stroke-width=".5"/><path d="M0 0 L13.9 0" stroke="rgba(235,240,215,.35)" stroke-width=".6"/></g><g transform="translate(66.0 123.2) rotate(-53.3)"><path d="M0 0 C3.7 -5.4 13.4 -5.7 18.6 0 C13.4 5.7 3.7 5.4 0 0Z" fill="url(#lg2)" stroke="rgba(30,45,25,.45)" stroke-width=".5"/><path d="M0 0 L16.8 0" stroke="rgba(235,240,215,.35)" stroke-width=".6"/></g><g transform="translate(63.6 113.4) rotate(-154.9)"><path d="M0 0 C3.7 -5.0 13.3 -5.3 18.5 0 C13.3 5.3 3.7 5.0 0 0Z" fill="url(#lg1)" stroke="rgba(30,45,25,.45)" stroke-width=".5"/><path d="M0 0 L16.7 0" stroke="rgba(235,240,215,.35)" stroke-width=".6"/></g><g transform="translate(61.1 103.0) rotate(-49.1)"><path d="M0 0 C2.9 -3.8 10.5 -4.0 14.6 0 C10.5 4.0 2.9 3.8 0 0Z" fill="url(#lg1)" stroke="rgba(30,45,25,.45)" stroke-width=".5"/><path d="M0 0 L13.1 0" stroke="rgba(235,240,215,.35)" stroke-width=".6"/></g><g transform="translate(58.4 91.8) rotate(-153.6)"><path d="M0 0 C3.8 -5.5 13.7 -5.7 19.1 0 C13.7 5.7 3.8 5.5 0 0Z" fill="url(#lg3)" stroke="rgba(30,45,25,.45)" stroke-width=".5"/><path d="M0 0 L17.2 0" stroke="rgba(235,240,215,.35)" stroke-width=".6"/></g><g transform="translate(55.5 80.0) rotate(-48.7)"><path d="M0 0 C3.4 -5.3 12.3 -5.6 17.1 0 C12.3 5.6 3.4 5.3 0 0Z" fill="url(#lg2)" stroke="rgba(30,45,25,.45)" stroke-width=".5"/><path d="M0 0 L15.4 0" stroke="rgba(235,240,215,.35)" stroke-width=".6"/></g><g transform="translate(52.5 67.4) rotate(-141.5)"><path d="M0 0 C2.8 -4.4 10.2 -4.6 14.1 0 C10.2 4.6 2.8 4.4 0 0Z" fill="url(#lg2)" stroke="rgba(30,45,25,.45)" stroke-width=".5"/><path d="M0 0 L12.7 0" stroke="rgba(235,240,215,.35)" stroke-width=".6"/></g><g transform="translate(49.3 54.0) rotate(-45.4)"><path d="M0 0 C3.9 -6.4 14.1 -6.7 19.6 0 C14.1 6.7 3.9 6.4 0 0Z" fill="url(#lg3)" stroke="rgba(30,45,25,.45)" stroke-width=".5"/><path d="M0 0 L17.7 0" stroke="rgba(235,240,215,.35)" stroke-width=".6"/></g><g transform="translate(46.0 40.0) rotate(-146.4)"><path d="M0 0 C3.6 -5.4 12.9 -5.6 17.9 0 C12.9 5.6 3.6 5.4 0 0Z" fill="url(#lg1)" stroke="rgba(30,45,25,.45)" stroke-width=".5"/><path d="M0 0 L16.1 0" stroke="rgba(235,240,215,.35)" stroke-width=".6"/></g><g transform="translate(81.4 140.9) rotate(-48.0)"><path d="M0 0 C4.2 -6.1 15.0 -6.4 20.9 0 C15.0 6.4 4.2 6.1 0 0Z" fill="url(#lg2)" stroke="rgba(30,45,25,.45)" stroke-width=".5"/><path d="M0 0 L18.8 0" stroke="rgba(235,240,215,.35)" stroke-width=".6"/></g><g transform="translate(81.8 132.4) rotate(-133.1)"><path d="M0 0 C4.4 -7.2 15.8 -7.6 22.0 0 C15.8 7.6 4.4 7.2 0 0Z" fill="url(#lg1)" stroke="rgba(30,45,25,.45)" stroke-width=".5"/><path d="M0 0 L19.8 0" stroke="rgba(235,240,215,.35)" stroke-width=".6"/></g><g transform="translate(82.2 123.5) rotate(-45.0)"><path d="M0 0 C4.3 -5.7 15.5 -6.0 21.5 0 C15.5 6.0 4.3 5.7 0 0Z" fill="url(#lg2)" stroke="rgba(30,45,25,.45)" stroke-width=".5"/><path d="M0 0 L19.3 0" stroke="rgba(235,240,215,.35)" stroke-width=".6"/></g><g transform="translate(82.7 114.3) rotate(-144.8)"><path d="M0 0 C3.5 -4.7 12.6 -4.9 17.6 0 C12.6 4.9 3.5 4.7 0 0Z" fill="url(#lg3)" stroke="rgba(30,45,25,.45)" stroke-width=".5"/><path d="M0 0 L15.8 0" stroke="rgba(235,240,215,.35)" stroke-width=".6"/></g><g transform="translate(83.2 104.8) rotate(-45.1)"><path d="M0 0 C3.9 -5.5 13.9 -5.8 19.3 0 C13.9 5.8 3.9 5.5 0 0Z" fill="url(#lg2)" stroke="rgba(30,45,25,.45)" stroke-width=".5"/><path d="M0 0 L17.3 0" stroke="rgba(235,240,215,.35)" stroke-width=".6"/></g><g transform="translate(83.7 94.9) rotate(-131.7)"><path d="M0 0 C4.2 -6.7 15.1 -7.1 21.0 0 C15.1 7.1 4.2 6.7 0 0Z" fill="url(#lg1)" stroke="rgba(30,45,25,.45)" stroke-width=".5"/><path d="M0 0 L18.9 0" stroke="rgba(235,240,215,.35)" stroke-width=".6"/></g><g transform="translate(84.2 84.7) rotate(-46.3)"><path d="M0 0 C3.8 -5.0 13.7 -5.2 19.0 0 C13.7 5.2 3.8 5.0 0 0Z" fill="url(#lg2)" stroke="rgba(30,45,25,.45)" stroke-width=".5"/><path d="M0 0 L17.1 0" stroke="rgba(235,240,215,.35)" stroke-width=".6"/></g><g transform="translate(84.8 74.1) rotate(-140.9)"><path d="M0 0 C3.1 -4.7 11.0 -4.9 15.3 0 C11.0 4.9 3.1 4.7 0 0Z" fill="url(#lg2)" stroke="rgba(30,45,25,.45)" stroke-width=".5"/><path d="M0 0 L13.7 0" stroke="rgba(235,240,215,.35)" stroke-width=".6"/></g><g transform="translate(85.4 63.2) rotate(-38.7)"><path d="M0 0 C4.1 -6.5 14.6 -6.9 20.3 0 C14.6 6.9 4.1 6.5 0 0Z" fill="url(#lg2)" stroke="rgba(30,45,25,.45)" stroke-width=".5"/><path d="M0 0 L18.3 0" stroke="rgba(235,240,215,.35)" stroke-width=".6"/></g><g transform="translate(86.0 51.9) rotate(-137.7)"><path d="M0 0 C2.9 -4.3 10.4 -4.5 14.5 0 C10.4 4.5 2.9 4.3 0 0Z" fill="url(#lg1)" stroke="rgba(30,45,25,.45)" stroke-width=".5"/><path d="M0 0 L13.0 0" stroke="rgba(235,240,215,.35)" stroke-width=".6"/></g><g transform="translate(86.6 40.3) rotate(-48.8)"><path d="M0 0 C3.8 -6.4 13.7 -6.8 19.0 0 C13.7 6.8 3.8 6.4 0 0Z" fill="url(#lg3)" stroke="rgba(30,45,25,.45)" stroke-width=".5"/><path d="M0 0 L17.1 0" stroke="rgba(235,240,215,.35)" stroke-width=".6"/></g><g transform="translate(87.3 28.3) rotate(-130.8)"><path d="M0 0 C3.8 -5.2 13.6 -5.5 18.9 0 C13.6 5.5 3.8 5.2 0 0Z" fill="url(#lg2)" stroke="rgba(30,45,25,.45)" stroke-width=".5"/><path d="M0 0 L17.0 0" stroke="rgba(235,240,215,.35)" stroke-width=".6"/></g><g transform="translate(88.0 16.0) rotate(-28.8)"><path d="M0 0 C3.4 -5.2 12.2 -5.4 16.9 0 C12.2 5.4 3.4 5.2 0 0Z" fill="url(#lg1)" stroke="rgba(30,45,25,.45)" stroke-width=".5"/><path d="M0 0 L15.2 0" stroke="rgba(235,240,215,.35)" stroke-width=".6"/></g><g transform="translate(88.6 155.8) rotate(-10.1)"><path d="M0 0 C3.4 -4.7 12.2 -5.0 16.9 0 C12.2 5.0 3.4 4.7 0 0Z" fill="url(#lg3)" stroke="rgba(30,45,25,.45)" stroke-width=".5"/><path d="M0 0 L15.2 0" stroke="rgba(235,240,215,.35)" stroke-width=".6"/></g><g transform="translate(91.4 148.8) rotate(-112.9)"><path d="M0 0 C3.4 -4.6 12.4 -4.8 17.2 0 C12.4 4.8 3.4 4.6 0 0Z" fill="url(#lg1)" stroke="rgba(30,45,25,.45)" stroke-width=".5"/><path d="M0 0 L15.5 0" stroke="rgba(235,240,215,.35)" stroke-width=".6"/></g><g transform="translate(94.5 141.0) rotate(-26.4)"><path d="M0 0 C3.9 -5.1 13.9 -5.3 19.4 0 C13.9 5.3 3.9 5.1 0 0Z" fill="url(#lg2)" stroke="rgba(30,45,25,.45)" stroke-width=".5"/><path d="M0 0 L17.4 0" stroke="rgba(235,240,215,.35)" stroke-width=".6"/></g><g transform="translate(97.8 132.5) rotate(-114.3)"><path d="M0 0 C3.6 -6.0 12.8 -6.3 17.8 0 C12.8 6.3 3.6 6.0 0 0Z" fill="url(#lg2)" stroke="rgba(30,45,25,.45)" stroke-width=".5"/><path d="M0 0 L16.0 0" stroke="rgba(235,240,215,.35)" stroke-width=".6"/></g><g transform="translate(101.4 123.2) rotate(-14.4)"><path d="M0 0 C3.1 -4.5 11.1 -4.7 15.4 0 C11.1 4.7 3.1 4.5 0 0Z" fill="url(#lg3)" stroke="rgba(30,45,25,.45)" stroke-width=".5"/><path d="M0 0 L13.9 0" stroke="rgba(235,240,215,.35)" stroke-width=".6"/></g><g transform="translate(105.2 113.2) rotate(-110.3)"><path d="M0 0 C4.1 -6.6 14.6 -6.9 20.3 0 C14.6 6.9 4.1 6.6 0 0Z" fill="url(#lg1)" stroke="rgba(30,45,25,.45)" stroke-width=".5"/><path d="M0 0 L18.3 0" stroke="rgba(235,240,215,.35)" stroke-width=".6"/></g><g transform="translate(109.3 102.5) rotate(-16.9)"><path d="M0 0 C3.0 -4.7 10.9 -4.9 15.1 0 C10.9 4.9 3.0 4.7 0 0Z" fill="url(#lg3)" stroke="rgba(30,45,25,.45)" stroke-width=".5"/><path d="M0 0 L13.6 0" stroke="rgba(235,240,215,.35)" stroke-width=".6"/></g><g transform="translate(113.6 91.0) rotate(-111.4)"><path d="M0 0 C4.0 -6.6 14.4 -6.9 20.0 0 C14.4 6.9 4.0 6.6 0 0Z" fill="url(#lg3)" stroke="rgba(30,45,25,.45)" stroke-width=".5"/><path d="M0 0 L18.0 0" stroke="rgba(235,240,215,.35)" stroke-width=".6"/></g><g transform="translate(118.1 78.7) rotate(-30.1)"><path d="M0 0 C2.8 -3.7 10.0 -3.9 13.9 0 C10.0 3.9 2.8 3.7 0 0Z" fill="url(#lg3)" stroke="rgba(30,45,25,.45)" stroke-width=".5"/><path d="M0 0 L12.5 0" stroke="rgba(235,240,215,.35)" stroke-width=".6"/></g><g transform="translate(122.9 65.7) rotate(-127.0)"><path d="M0 0 C3.0 -4.7 10.7 -5.0 14.9 0 C10.7 5.0 3.0 4.7 0 0Z" fill="url(#lg2)" stroke="rgba(30,45,25,.45)" stroke-width=".5"/><path d="M0 0 L13.4 0" stroke="rgba(235,240,215,.35)" stroke-width=".6"/></g><g transform="translate(128.0 52.0) rotate(-23.4)"><path d="M0 0 C3.8 -5.6 13.5 -5.9 18.8 0 C13.5 5.9 3.8 5.6 0 0Z" fill="url(#lg3)" stroke="rgba(30,45,25,.45)" stroke-width=".5"/><path d="M0 0 L16.9 0" stroke="rgba(235,240,215,.35)" stroke-width=".6"/></g><g transform="translate(75.0 159.2) rotate(-73.8)"><path d="M0 0 C4.1 -5.4 14.8 -5.7 20.5 0 C14.8 5.7 4.1 5.4 0 0Z" fill="url(#lg1)" stroke="rgba(30,45,25,.45)" stroke-width=".5"/><path d="M0 0 L18.5 0" stroke="rgba(235,240,215,.35)" stroke-width=".6"/></g><g transform="translate(71.1 152.0) rotate(-167.5)"><path d="M0 0 C3.9 -6.1 14.1 -6.4 19.6 0 C14.1 6.4 3.9 6.1 0 0Z" fill="url(#lg1)" stroke="rgba(30,45,25,.45)" stroke-width=".5"/><path d="M0 0 L17.7 0" stroke="rgba(235,240,215,.35)" stroke-width=".6"/></g><g transform="translate(66.3 144.1) rotate(-80.0)"><path d="M0 0 C4.2 -5.8 15.2 -6.1 21.1 0 C15.2 6.1 4.2 5.8 0 0Z" fill="url(#lg1)" stroke="rgba(30,45,25,.45)" stroke-width=".5"/><path d="M0 0 L18.9 0" stroke="rgba(235,240,215,.35)" stroke-width=".6"/></g><g transform="translate(60.3 135.7) rotate(-165.9)"><path d="M0 0 C3.4 -4.8 12.4 -5.1 17.2 0 C12.4 5.1 3.4 4.8 0 0Z" fill="url(#lg1)" stroke="rgba(30,45,25,.45)" stroke-width=".5"/><path d="M0 0 L15.5 0" stroke="rgba(235,240,215,.35)" stroke-width=".6"/></g><g transform="translate(53.3 126.7) rotate(-87.4)"><path d="M0 0 C3.3 -5.1 11.9 -5.3 16.6 0 C11.9 5.3 3.3 5.1 0 0Z" fill="url(#lg1)" stroke="rgba(30,45,25,.45)" stroke-width=".5"/><path d="M0 0 L14.9 0" stroke="rgba(235,240,215,.35)" stroke-width=".6"/></g><g transform="translate(45.3 117.0) rotate(-170.7)"><path d="M0 0 C2.9 -4.4 10.6 -4.6 14.7 0 C10.6 4.6 2.9 4.4 0 0Z" fill="url(#lg2)" stroke="rgba(30,45,25,.45)" stroke-width=".5"/><path d="M0 0 L13.2 0" stroke="rgba(235,240,215,.35)" stroke-width=".6"/></g><g transform="translate(36.2 106.8) rotate(-81.4)"><path d="M0 0 C3.6 -5.5 12.9 -5.8 17.9 0 C12.9 5.8 3.6 5.5 0 0Z" fill="url(#lg1)" stroke="rgba(30,45,25,.45)" stroke-width=".5"/><path d="M0 0 L16.1 0" stroke="rgba(235,240,215,.35)" stroke-width=".6"/></g><g transform="translate(26.0 96.0) rotate(-183.7)"><path d="M0 0 C3.8 -5.6 13.6 -5.9 18.9 0 C13.6 5.9 3.8 5.6 0 0Z" fill="url(#lg2)" stroke="rgba(30,45,25,.45)" stroke-width=".5"/><path d="M0 0 L17.0 0" stroke="rgba(235,240,215,.35)" stroke-width=".6"/></g><g transform="translate(87.8 156.2) rotate(-8.4)"><path d="M0 0 C4.5 -5.8 16.0 -6.1 22.3 0 C16.0 6.1 4.5 5.8 0 0Z" fill="url(#lg3)" stroke="rgba(30,45,25,.45)" stroke-width=".5"/><path d="M0 0 L20.0 0" stroke="rgba(235,240,215,.35)" stroke-width=".6"/></g><g transform="translate(92.3 149.0) rotate(-94.6)"><path d="M0 0 C3.1 -4.4 11.2 -4.6 15.5 0 C11.2 4.6 3.1 4.4 0 0Z" fill="url(#lg1)" stroke="rgba(30,45,25,.45)" stroke-width=".5"/><path d="M0 0 L14.0 0" stroke="rgba(235,240,215,.35)" stroke-width=".6"/></g><g transform="translate(97.7 142.0) rotate(7.8)"><path d="M0 0 C3.1 -4.6 11.0 -4.9 15.3 0 C11.0 4.9 3.1 4.6 0 0Z" fill="url(#lg3)" stroke="rgba(30,45,25,.45)" stroke-width=".5"/><path d="M0 0 L13.7 0" stroke="rgba(235,240,215,.35)" stroke-width=".6"/></g><g transform="translate(104.0 135.0) rotate(-84.7)"><path d="M0 0 C4.1 -6.6 14.9 -6.9 20.7 0 C14.9 6.9 4.1 6.6 0 0Z" fill="url(#lg1)" stroke="rgba(30,45,25,.45)" stroke-width=".5"/><path d="M0 0 L18.7 0" stroke="rgba(235,240,215,.35)" stroke-width=".6"/></g><g transform="translate(111.1 128.1) rotate(12.0)"><path d="M0 0 C4.0 -5.8 14.5 -6.1 20.2 0 C14.5 6.1 4.0 5.8 0 0Z" fill="url(#lg3)" stroke="rgba(30,45,25,.45)" stroke-width=".5"/><path d="M0 0 L18.1 0" stroke="rgba(235,240,215,.35)" stroke-width=".6"/></g><g transform="translate(119.2 121.3) rotate(-85.9)"><path d="M0 0 C2.9 -4.7 10.3 -4.9 14.3 0 C10.3 4.9 2.9 4.7 0 0Z" fill="url(#lg1)" stroke="rgba(30,45,25,.45)" stroke-width=".5"/><path d="M0 0 L12.9 0" stroke="rgba(235,240,215,.35)" stroke-width=".6"/></g><g transform="translate(128.2 114.6) rotate(19.9)"><path d="M0 0 C3.4 -5.3 12.3 -5.6 17.1 0 C12.3 5.6 3.4 5.3 0 0Z" fill="url(#lg2)" stroke="rgba(30,45,25,.45)" stroke-width=".5"/><path d="M0 0 L15.4 0" stroke="rgba(235,240,215,.35)" stroke-width=".6"/></g><g transform="translate(138.0 108.0) rotate(-78.2)"><path d="M0 0 C2.7 -3.5 9.6 -3.7 13.3 0 C9.6 3.7 2.7 3.5 0 0Z" fill="url(#lg1)" stroke="rgba(30,45,25,.45)" stroke-width=".5"/><path d="M0 0 L11.9 0" stroke="rgba(235,240,215,.35)" stroke-width=".6"/></g>
<path d="M52 186 C46 200 40 232 46 252 C47 258 52 260 58 260 L102 260 C108 260 113 258 114 252 C120 232 114 200 108 186Z" fill="url(#vz)"/>
<rect x="40" y="170" width="84" height="92" fill="#fff" filter="url(#spk)" clip-path="url(#vc)" opacity=".7"/>
<ellipse cx="80" cy="186" rx="28" ry="6" fill="#3a2e20"/><ellipse cx="80" cy="185" rx="28" ry="5.5" fill="none" stroke="rgba(255,255,255,.55)" stroke-width="1.4"/></svg></div>
      </div>
      <div class="board"></div>
    </div>
    <div class="side"></div>
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
