#!/usr/bin/env python3
"""Scroll-story version of the hotel pitch pages.

Run: python3 scripts/gen-pitch-stories.py   (then node scripts/build-app.mjs)

Reuses the hotel palettes/fonts/facts from gen-pitches.py, adds a story
(chapters = the itinerary) and renders each page as a scroll-driven collage:
torn-edge photo cut-outs, handwritten notes, doodles, parallax.

Photo slots (all optional; a designed placeholder shows until the file exists):
  site/media/pitches/<hotel>-hero.jpg          full-bleed cover background
  site/media/pitches/<hotel>/cover-1..3.jpg    floating cover cut-outs
  site/media/pitches/<hotel>/<stop>.jpg        one per stop (see STOPS.md)
  site/media/pitches/<hotel>/ch<N>-cutout.png  optional transparent PNG that floats in chapter N
"""
import importlib.util, os, re, html

HERE = os.path.dirname(__file__)
spec = importlib.util.spec_from_file_location('gp', os.path.join(HERE, 'gen-pitches.py'))
gp = importlib.util.module_from_spec(spec); spec.loader.exec_module(gp)
ROOT = gp.ROOT
CDN = gp.CDN
esc = gp.esc
TAGS = gp.TAGS

def slug(t): return re.sub(r'[^a-z0-9]+', '-', t.lower()).strip('-')

TIMES = {
 'nomad': ['4:00 pm','8:30 pm','9:30 am','12:00 pm','2:30 pm','7:00 pm','10:00 am','1:30 pm','1:00 pm','6:30 pm'],
 'brooklyn': ['8:00 am','10:30 am','2:00 pm','12:30 pm','1:00 pm','6:00 pm','10:00 am','1:30 pm'],
 'halekulani': ['4:00 pm','6:30 pm','10:00 am','2:30 pm','9:30 am'],
 'proper': ['5:00 pm','7:00 pm','10:30 am','2:00 pm','11:00 am'],
 'shutters': ['8:00 am','1:00 pm','10:30 am','11:00 am','4:30 pm'],
}

def tm(slug_h, n):
    t = TIMES[slug_h][n]
    return t.replace(' ', '<small>', 1) + '</small>' if False else t

# (kicker, title, story, [(stop, tag, note, confirm)])
STORY = {
'nomad': dict(
  walk=dict(kick='Day 1 · Arrival', title='Through the doors',
    story="Walk in with me. Past the sheer curtains, toward the glow of the bar, and then up to a window with the whole city lit below. This is how I'd open the trip: moving through the hotel, one room at a time.",
    scenes=[
      ('Lobby','Step through the doors.','Sheer curtains, floor-to-ceiling windows, and a sculptural chandelier over the lounge.'),
      ('Lounge','Past the lounge, toward the bar.','Green velvet, brass, and a wall of hanging greenery behind the bottles.'),
      ('Room','Then up, to the view.','Dusk over the downtown skyline, with every light just switching on.')]),
  intro="Picture this. You land in New York, ride into NoMad, and step into a room where the window is so wide the skyline feels hung just for you. This is the long weekend I'd take you on, one stop at a time.",
  chapters=[
   ('Day 1 · Nightfall','Fifty floors up',"Dinner at the hotel turns into a nightcap, and the nightcap turns into the best view of the trip. Blue hour, every light in Midtown below.",
    [('Bazaar Meat by José Andrés','here','Velvet booths, feather chandeliers, dinner at the hotel.',False),('Nubeluz, 50th floor','here','Skyline at blue hour.',False)]),
   ('Day 2 · Morning','Coffee in hand, on foot',"Out the lobby and into the neighborhood. Everything good around here is a walk away: the park, the Flatiron, the galleries of Chelsea.",
    [('Madison Square Park and Flatiron','walk','Morning walk, coffee in hand.',True),('Chelsea galleries and the start of the High Line','walk','Local artists, one gallery per hour.',True)]),
   ('Day 2 · Afternoon','Petals and frames',"SoHo, but make it dreamy. A shop of soft, handmade flowers, a pair of Gentle Monster frames, a sample sale that's gone by Monday, and a pop-up only the locals know about.",
    [('CJ Hendry Flower Market','ride','The plush-flower shop at 172 Prince St. Pick a bloom for $10.',False),('Gentle Monster, SoHo','ride','Installation-style retail.',True),('Sample-sale hunt','ride','Check the 260 Sample Sale list the week you go.',True),('Pop-up of the week','ride','Pop-ups rotate weekly. Pick one for the feed.',True)]),
   ('Day 2 · The matcha crawl','Three cups, three moods',"A line down the block for the matcha everyone talks about, a café that doubles as an art gallery, and one more cup to compare. This is the matcha chapter.",
    [('12 Matcha','ride','54 Bond St, NoHo. Ceremonial-grade, long line, famous basque cheesecake.',False),('Rhythm Zero','ride','An art-gallery café with a West Village location. Seasonal matcha drinks.',False),('Rok Matcha','ride','Rōk Matcha in New York. Confirm the exact address and hours before we plan around it.',True)]),
   ('Day 2 · Evening','A bowl worth the ride',"Steam, noodles, a counter seat. Ramen is the cozy beat between the shopping and the next day.",
    [('Ippudo','ride','Hakata-style ramen under a canopy of bamboo. Confirm which location (the storefront photo is #24) and wait times.',True)]),
   ('Day 3 · Morning','The secret garden',"A quick train up the Hudson and the city drops away: stone terraces, a long reflecting pool, and the river below. This is the quiet chapter.",
    [('Untermyer Gardens','trip','Metro-North from Grand Central to Greystone, about 40 minutes, then a short ride or walk. Free; closes at dusk.',False)]),
   ('Day 3 · Afternoon','Downtown, in one sweep',"Three very different worlds within reach of each other: an immersive art museum, a Parisian department store inside a landmark, and a Chinatown shop where you can get your aura photographed.",
    [('Mercer Labs','ride','21 Dey St. Fifteen immersive rooms; plan 60 to 90 minutes and book ahead.',False),('Printemps, One Wall Street','ride','Café, cocktail bars, and the landmarked Red Room with its mosaics.',False),('Aura reading at Magic Jewelry','ride','238 Canal St, Chinatown. Aura photographs.',False)]),
   ('Day 4 · Across the bridge','Brooklyn, then the big dinner',"A scoop of ice cream, the bridge in the frame, and one last dinner that earns its place in the story.",
    [('Dumbo ice cream and bridge shot','trip','Van Leeuwen or similar, then the bridge frame.',True),('Nobu Downtown dinner','trip','The big dinner moment.',True)]),
   ('Day 4 · Goodbye','One last look',"Back to the window for a final look, because you'll want to come back.",
    [('Last look and checkout','here','One last lobby and window moment.',False)]),
  ]),
'brooklyn': dict(
  intro="Picture a slower New York. The skyline is right across the water, the bridge is outside your window, and there's a rooftop pool above it all. This is the stay for people who want the city without the rush.",
  chapters=[
   ('Day 1 · Morning','Wake up to the water',"Soft light over the skyline, a coffee on the rooftop deck, and nowhere to be. The calm opening shot of the trip.",
    [('Room and skyline view','here','Morning light across the water.',False),('Rooftop pool deck','here','Skyline from the pool.',False)]),
   ('Day 1 · Reset','A ritual, not a rush',"A spa stop for the slow kind of self-care: the kind you build over weeks and notice in the mirror. This is where I'd tell that story.",
    [('Bamford Wellness Spa','here','A skin-ritual moment for the skincare audience.',False)]),
   ('Day 1 · Afternoon','Cobblestones and bridge light',"Walk the waterfront park, find the famous bridge frame, and stop for the carousel. Everything is close, and everything is pretty.",
    [('Brooklyn Bridge Park walk','walk','Slow waterfront loop.',True),('Washington Street bridge shot','walk','The classic Dumbo frame.',True),("Jane's Carousel",'walk','Quick, charming b-roll.',True)]),
   ('Day 2 · Local','Eat, browse, repeat',"Lunch from a dozen local vendors and a gallery stop for local artists. All within a short walk of the hotel.",
    [('Time Out Market','walk','Lunch with local vendors.',True),('Dumbo gallery stop','walk','Local artists nearby.',True)]),
   ('Day 2 · Across the bridge','Petals, frames, and matcha',"Cross the bridge to SoHo for the plush-flower shop and the Gentle Monster store, then a matcha crawl through NoHo and the villages.",
    [('CJ Hendry Flower Market','ride','The plush-flower shop at 172 Prince St. Pick a bloom for $10.',False),('Gentle Monster, SoHo','ride','Cross the bridge for a design stop.',True),('12 Matcha','ride','54 Bond St, NoHo. Ceremonial-grade, long line.',False)]),
   ('Day 2 · Evening','Art-gallery coffee and ramen',"A café that doubles as an art space in Williamsburg, then ramen and a scoop by the water on the way home.",
    [('Rhythm Zero','ride','An art-gallery café with locations in Williamsburg and Greenpoint.',False),('Rok Matcha','ride','Rōk Matcha in New York. Confirm the exact address and hours before we plan around it.',True),('Ippudo','ride','Hakata-style ramen under a canopy of bamboo. Confirm which location and wait times.',True),('Ice cream by the water','ride','A scoop at golden hour.',True)]),
   ('Day 3 · Morning','The secret garden',"A quick train up the Hudson and the city drops away: stone terraces, a long reflecting pool, and the river below.",
    [('Untermyer Gardens','trip','Metro-North from Grand Central to Greystone, about 40 minutes, then a short ride or walk. Free; closes at dusk.',False)]),
   ('Day 3 · Afternoon','Lower Manhattan, in one sweep',"An immersive art museum, a Parisian department store inside a landmark, and a Chinatown shop where you can get your aura photographed. All a short ride across the bridge.",
    [('Mercer Labs','ride','21 Dey St. Fifteen immersive rooms; plan 60 to 90 minutes and book ahead.',False),('Printemps, One Wall Street','ride','Café, cocktail bars, and the landmarked Red Room with its mosaics.',False),('Aura reading at Magic Jewelry','ride','238 Canal St, Chinatown. Aura photographs.',False)]),
  ]),
'halekulani': dict(
  intro="Picture waking up to the Pacific in Waikiki, then spending a day with the people who make Hawaiʻi's best things. This is a stay with ocean in front of it and a story behind it.",
  chapters=[
   ('Day 1 · Arrival','Ocean first',"Open the door, hear the water, and watch the light change over the beach. I'd start every morning here.",
    [('Oceanfront room and lanai view','here','Confirm room categories.',True),('Sunrise on the beach','here','Soft light, no filter.',False)]),
   ('Day 1 · Golden hour','Dinner as the sun goes down',"A slow walk through Waikiki, then dinner as the sky turns gold.",
    [('Waikiki shops','walk','A quick browse before the beach.',True),('Sunset dinner at the hotel','here','Confirm the restaurant and hours.',True)]),
   ('Day 2 · Kakaʻako','Meet the makers',"A short ride from the hotel is a neighborhood full of murals and Hawaiian-owned shops. I'd spend a whole day here, meeting the people behind the things I'd bring home.",
    [('Kakaʻako murals walk','ride','Colorful neighborhood, easy to wander.',False),('House of Mana Up','ride','Hawaiian entrepreneurs, beauty and local foods.',False),('MORI by Art+Flea','ride','Goods by Hawaiian artists.',False),('always a.line and Salvage Public','ride','Hawaiian-inspired prints and surf graphic tees.',False)]),
   ('Day 2 · Sweet','Ice cream, shave ice, and a good dinner',"Between the shops, something cold. After, a farm-to-table dinner to close the day.",
    [('Black Sheep Cream Company','ride','Rotating ice cream flavors.',False),("Lin's Hawaiian Snacks",'ride','Shave ice, open since the 1980s.',False),('Local matcha stop','ride','Pick one the week you go.',True),("Merriman's Honolulu",'ride','Farm-to-table dinner.',False)]),
   ('Day 3 · Culture','A quiet gallery morning',"One last slow morning with Hawaiian art before the flight home.",
    [('Honolulu Museum of Art','trip','Local artists and a quiet gallery moment.',True)]),
  ]),
'proper': dict(
  intro="Picture golden hour over the Pacific, a matcha in Venice, a cart of finds from the best boutiques in town. This is Los Angeles, the cute and trendy way.",
  chapters=[
   ('Day 1 · Arrival','Sunset from the room',"The Pacific light comes through the window and everything turns warm. This is the first shot, and the setup for the whole trip.",
    [('Room and sunset view','here','Pacific light through the window.',False),('Rooftop or lounge sunset','here','Confirm what the hotel offers.',True)]),
   ('Day 1 · Evening','The cliffside walk',"A stroll along the clifftop park, then dinner on a rooftop as the sky goes pink.",
    [('Palisades Park clifftop walk','walk','Ocean views, easy golden-hour stroll.',False),('Elephante rooftop dinner','walk','Rooftop views. Confirm distance.',True)]),
   ('Day 2 · Venice','Matcha, pastries, boutiques',"A short ride south: the matcha I came for, a pastry from the bakery everyone talks about, a scoop on the boulevard, and a whole street of shops.",
    [('Shuhari Matcha Café, Venice','ride','Your matcha stop.',False),('Abbot Kinney Boulevard','ride','Shops and cafes in one strip.',False),('Gjusta bakery','ride','Breakfast or a pastry.',False),('Salt & Straw','ride','A scoop on the boulevard.',False)]),
   ('Day 2 · Afternoon','Window shopping, Santa Monica style',"Boutiques on Main Street and Montana Avenue, then dumplings for dinner.",
    [('Main Street shops','ride','A boutique stroll.',False),('Montana Avenue boutiques','ride','Pretty window shopping.',False),('Din Tai Fung','ride','Confirm the nearest location.',True)]),
   ('Day 3 · Worth the drive','Home goods, frames, and art',"The things worth leaving the coast for: a home-goods hunt, the Gentle Monster flagship, a museum day, and a sample sale if the timing works.",
    [('Goodies LA','trip','Home-goods hunt. Confirm location and hours.',True),('Rok Matcha, Koreatown','trip','Rōk Coffee & Tea, 3060 W Olympic Blvd. Confirm hours.',False),('Gentle Monster flagship, Broadway','trip','The kinetic-sculpture store downtown.',False),('The Getty or the Hammer Museum','trip','Art day.',False),('Sample sale check','trip','Dates change. Confirm the week you go.',True)]),
  ]),
'shutters': dict(
  intro="Picture a hotel that opens right onto the beach: ocean from the balcony, a path along the sand, Venice down the shore. This is Los Angeles at its easiest.",
  chapters=[
   ('Day 1 · Morning','Wake up to the ocean',"Open the balcony door to the sound of waves and walk straight onto the beach path. No plan, just salt air.",
    [('Ocean-view room and balcony','here','Morning light on the water.',False),('Beach path walk','here','Straight out the door.',True)]),
   ('Day 1 · Afternoon','The pier and the canals',"The pier for a classic coastal moment, then a ride to Venice's quiet canals.",
    [('Santa Monica Pier','walk','Confirm distance and crowds.',True),('Venice Canals','ride','Pretty, calm, easy to film.',False)]),
   ('Day 2 · Venice','Sips and shops',"Matcha, a smoothie, a pastry, and a boulevard of boutiques. The easy, sunny day.",
    [('Shuhari Matcha Café, Venice','ride','Matcha with a beach walk.',False),('Abbot Kinney Boulevard','ride','Shops and cafes.',False),('Erewhon smoothie','ride','Venice or Santa Monica location.',False),('Tartine Bakery','ride','Pastry stop in Santa Monica.',False)]),
   ('Day 3 · Malibu','A day up the coast',"Drive north for dinner on the pier and a day at the country mart. The ocean is the whole backdrop.",
    [('Malibu Farm on the pier','trip','Ocean dinner on the Malibu Pier.',False),('Malibu Country Mart','trip','Outdoor shopping and cafes.',False),('Nobu Malibu','trip','Confirm availability.',True)]),
   ('Day 3 · Downtown','Matcha, frames, and home goods',"One city stop before heading home: the flagship store everyone's seen, and a home-goods hunt for the suitcase.",
    [('Rok Matcha, Koreatown','trip','Rōk Coffee & Tea, 3060 W Olympic Blvd. Confirm hours.',False),('Gentle Monster flagship, Broadway','trip','Downtown design stop.',False),('Goodies LA','trip','Home goods. Confirm location.',True)]),
  ]),
}

CSS = r"""
  :root { --bg:%%BG%%; --txt:%%TXT%%; --paper:%%PAPER%%; --ink:%%INK%%; --accent:%%ACCENT%%; --accent2:%%ACCENT2%%; --soft:%%SOFT%%;
          --head:%%HEAD%%; --body:%%BODY%%; --hand:'Nothing You Could Do',cursive; --pen:%%PEN%%;
          --grain:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='220' height='220'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='2' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 .5 0'/></filter><rect width='100%25' height='100%25' filter='url(%23n)'/></svg>"); }
  * { box-sizing:border-box; }
  html { scroll-behavior:smooth; }
  html,body { margin:0; background-color:var(--bg); background-image:%%PAPER_TEX%%; color:var(--txt); font-family:var(--body); font-weight:300; -webkit-font-smoothing:antialiased; }
  a { color:inherit; text-decoration:none; }
  h1,h2,h3 { font-family:var(--head); font-weight:400; margin:0; line-height:1.04; }
  .hand { font-family:var(--hand); font-weight:400; }
  .kick { font-size:12px; letter-spacing:.22em; text-transform:uppercase; color:var(--accent); font-weight:500; }

  /* HUD */
  .hud { position:fixed; top:0; left:0; right:0; z-index:60; display:flex; justify-content:space-between; align-items:center; padding:12px 18px; font-size:12px; letter-spacing:.12em; text-transform:uppercase; color:#fff; mix-blend-mode:difference; }
  .hud .bar { position:absolute; left:0; bottom:0; height:2px; width:0; background:#fff; }
  .hud .cur { opacity:.9; }

  /* cover */
  .cover { position:relative; min-height:100vh; display:flex; align-items:flex-end; overflow:hidden; color:#fff;
           background:linear-gradient(165deg,var(--accent2),var(--accent) 70%,%%DESK%%); }
  .cover > img.bg { position:absolute; inset:0; width:100%; height:100%; object-fit:cover; }
  .cover::after { content:''; position:absolute; inset:0; background:linear-gradient(0deg,rgba(0,0,0,.6),rgba(0,0,0,.05) 55%,rgba(0,0,0,.25)); }
  .cover .in { position:relative; z-index:3; max-width:1100px; width:100%; margin:0 auto; padding:0 24px 12vh; }
  .cover h1 { font-size:clamp(46px,9vw,120px); max-width:11ch; margin:10px 0 14px; text-shadow:0 4px 30px rgba(0,0,0,.35); }
  .cover .tag { font-size:clamp(20px,2.4vw,30px); max-width:34ch; opacity:.95; margin:0 0 20px; }
  .cover .hand { font-size:clamp(22px,2.6vw,32px); }
  .cover .kick { color:#fff; opacity:.85; }
  .scroll { margin-top:30px; font-size:12px; letter-spacing:.2em; text-transform:uppercase; opacity:.8; animation:bob 2s ease-in-out infinite; }
  @keyframes bob { 50% { transform:translateY(8px); } }
  .cover .float { position:absolute; z-index:2; width:clamp(120px,17vw,250px); }
  .cover .float.a { top:12%; right:6%; --r:5deg; } .cover .float.b { top:36%; right:22%; width:clamp(100px,13vw,190px); --r:-6deg; } .cover .float.c { top:14%; right:30%; width:clamp(90px,10vw,150px); --r:3deg; }

  /* cut-outs */
  .cut { position:relative; margin:0; transform:translateY(var(--py,0px)) rotate(var(--r,0deg)); filter:drop-shadow(0 12px 20px rgba(0,0,0,.28)); }
  .cut .img { position:relative; aspect-ratio:var(--ar,4/5); overflow:hidden; background:var(--g); display:flex; align-items:center; justify-content:center; text-align:center; padding:18px;
              clip-path:var(--clip); }
  .cut .img::before { content:''; position:absolute; inset:0; background-image:var(--grain); opacity:.35; mix-blend-mode:multiply; }
  .cut .img img { position:absolute; inset:0; width:100%; height:100%; object-fit:cover; z-index:2; }
  .cut .ph { position:relative; z-index:1; font-family:var(--head); font-size:clamp(20px,2.4vw,30px); color:rgba(255,255,255,.92); line-height:1.1; }
  .cut.paper .img { border:0; }
  .tape { position:absolute; top:-12px; left:50%; width:84px; height:24px; margin-left:-42px; background:rgba(255,255,255,.55); transform:rotate(-3deg); z-index:4; }
  .c1 { --clip:polygon(2% 3%,12% 0,26% 2%,41% 0,58% 3%,74% 1%,90% 3%,100% 1%,98% 18%,100% 36%,97% 55%,100% 72%,98% 90%,100% 100%,84% 97%,66% 100%,47% 98%,30% 100%,14% 98%,0 100%,2% 82%,0 63%,3% 44%,0 26%); }
  .c2 { --clip:polygon(0 2%,16% 0,33% 3%,52% 0,71% 2%,88% 0,100% 3%,98% 24%,100% 47%,97% 69%,100% 92%,86% 100%,67% 97%,48% 100%,27% 98%,9% 100%,0 96%,3% 74%,0 52%,2% 28%); }
  .c3 { --clip:polygon(3% 0,22% 3%,40% 0,60% 2%,80% 0,100% 2%,97% 22%,100% 41%,98% 63%,100% 85%,96% 100%,76% 98%,55% 100%,34% 97%,15% 100%,0 97%,3% 75%,0 52%,3% 30%,0 12%); }
  .c4 { --clip:polygon(0 0,100% 3%,98% 100%,3% 97%); }
  .g0 { --g:linear-gradient(150deg,var(--accent2),var(--accent)); } .g1 { --g:linear-gradient(150deg,var(--accent),var(--soft)); }
  .g2 { --g:linear-gradient(150deg,var(--ink),var(--accent2)); } .g3 { --g:linear-gradient(150deg,var(--soft),var(--accent2)); }
  .cap { margin-top:14px; display:flex; flex-direction:column; gap:4px; color:var(--txt); }
  .cap .nm { font-family:var(--hand); font-size:clamp(20px,2vw,25px); line-height:1.15; }
  .cap .row { display:flex; align-items:center; gap:8px; flex-wrap:wrap; }
  .cap .nt { font-size:13px; opacity:.75; line-height:1.5; }
  .tg { font-size:10px; letter-spacing:.12em; text-transform:uppercase; padding:3px 9px; border-radius:999px; font-weight:500; }
  .tg.here,.tg.walk { background:var(--accent); color:#fff; } .tg.ride { background:var(--soft); color:var(--txt); border:1px solid color-mix(in srgb, var(--txt) 25%, transparent); } .tg.trip { background:var(--txt); color:var(--bg); }
  .stamp { font-size:10px; letter-spacing:.1em; text-transform:uppercase; border:1px dashed currentColor; color:#c0392b; padding:2px 6px; border-radius:4px; transform:rotate(-3deg); }

  /* intro + marquee */
  .intro { max-width:760px; margin:0 auto; padding:110px 24px 70px; text-align:center; }
  .intro p { font-family:var(--head); font-size:clamp(24px,3.4vw,38px); line-height:1.3; margin:18px 0 0; }
  .marq { overflow:hidden; border-block:1px solid color-mix(in srgb, var(--txt) 25%, transparent); padding:14px 0; white-space:nowrap; }
  .marq div { display:inline-block; animation:mq 40s linear infinite; font-family:var(--head); font-style:italic; font-size:22px; letter-spacing:.04em; color:var(--accent); }
  .marq span { margin:0 22px; }
  @keyframes mq { to { transform:translateX(-50%); } }

  /* chapters */
  .chapter { position:relative; padding:120px 0 40px; }
  .chapter:nth-of-type(even) { background:color-mix(in srgb, var(--soft) 35%, transparent); }
  .wrap { max-width:1100px; margin:0 auto; padding:0 24px; position:relative; }
  .ch-head { display:grid; grid-template-columns:1fr 1fr; gap:40px; align-items:end; margin-bottom:60px; padding-top:70px; }
  .num { position:absolute; top:-70px; left:10px; font-family:var(--head); font-size:clamp(72px,11vw,150px); white-space:nowrap; line-height:1; color:transparent; -webkit-text-stroke:1.5px color-mix(in srgb, var(--accent) 55%, transparent); z-index:0; pointer-events:none; }
  .ch-head > * { position:relative; z-index:1; }
  .ch-head h2 { font-size:clamp(34px,5.2vw,68px); margin-top:10px; }
  .note { background:var(--paper); color:var(--ink); padding:22px 24px 30px; font-family:var(--hand); font-size:clamp(20px,2vw,25px); line-height:1.4; position:relative; transform:rotate(1.2deg);
          box-shadow:0 10px 22px rgba(0,0,0,.22); clip-path:polygon(0 0,100% 0,100% 94%,94% 100%,80% 96%,64% 100%,46% 97%,30% 100%,14% 97%,0 100%); }
  .note .tape { top:-12px; }
  .doodle { position:absolute; width:90px; height:60px; color:var(--accent); fill:none; stroke:currentColor; stroke-width:3; stroke-linecap:round; stroke-linejoin:round; }
  .note .doodle { right:-40px; bottom:-38px; transform:rotate(18deg); z-index:3; }
  .collage { display:flex; flex-wrap:wrap; gap:96px 3%; align-items:flex-start; }
  .chapter:nth-of-type(odd) .collage.rev { flex-direction:row-reverse; }
  .collage .cut { flex:0 0 auto; }
  .n1 .cut { width:56%; margin-left:auto; margin-right:auto; --ar:5/4; }
  .n2 .cut { width:46%; } .n2 .cut:nth-child(2) { margin-top:80px; } .n2 .cut:nth-child(1) { --ar:4/5; } .n2 .cut:nth-child(2) { --ar:1/1; }
  .n3 .cut:nth-child(1) { width:54%; --ar:4/3; } .n3 .cut:nth-child(2) { width:40%; margin-top:70px; --ar:4/5; } .n3 .cut:nth-child(3) { width:44%; margin-left:8%; --ar:1/1; }
  .n4 .cut { width:47%; } .n4 .cut:nth-child(1) { --ar:4/5; } .n4 .cut:nth-child(2) { margin-top:70px; --ar:1/1; } .n4 .cut:nth-child(3) { --ar:1/1; } .n4 .cut:nth-child(4) { margin-top:50px; --ar:4/5; }
  .cutout { position:absolute; right:2%; bottom:-30px; width:min(24vw,260px); z-index:5; filter:drop-shadow(0 14px 18px rgba(0,0,0,.35)); transform:rotate(4deg); }


  /* walk-through */
  .walkthru { position:relative; height:440vh; }
  .walkthru .stick { position:sticky; top:0; height:100vh; overflow:hidden; background:#06080f; }
  .walkthru .scene { position:absolute; inset:0; opacity:0; will-change:transform,opacity; }
  .walkthru .s1 img { width:100%; height:100%; object-fit:cover; object-position:50% 40%; transform-origin:50% 38%; }
  .walkthru .s2 .blur { position:absolute; inset:-30px; background-size:cover; background-position:center; filter:blur(28px) brightness(.55); }
  .walkthru .s2 img { position:absolute; left:50%; top:50%; height:min(100vh,120vw*1.78); max-width:100%; transform:translate(-50%,-50%); object-fit:cover; box-shadow:0 30px 80px rgba(0,0,0,.6); aspect-ratio:9/16; }
  .walkthru .s3 { background:radial-gradient(ellipse at 50% 60%,#1b2347,#05070d 70%); display:flex; align-items:center; justify-content:center; }
  .walkthru .s3 .frame { margin-top:-12vh; width:min(86vw,1040px); aspect-ratio:3/2; overflow:hidden; border:8px solid rgba(255,255,255,.9); box-shadow:0 30px 90px rgba(0,0,0,.7); border-radius:4px; }
  .walkthru .s3 img { width:100%; height:100%; object-fit:cover; transform-origin:50% 55%; }
  .walkthru .vig { position:absolute; inset:0; pointer-events:none; background:radial-gradient(ellipse at center,transparent 45%,rgba(0,0,0,.55)), linear-gradient(0deg,rgba(0,0,0,.6),transparent 40%); }
  .wcaps { position:absolute; left:0; right:0; bottom:9vh; padding:0 24px; max-width:1100px; margin:0 auto; color:#fff; }
  .wcap { position:absolute; left:24px; right:24px; bottom:0; opacity:0; transform:translateY(16px); transition:opacity .5s, transform .5s; }
  .wcap.on { opacity:1; transform:none; }
  .wcap .hand { font-size:clamp(28px,4.2vw,54px); line-height:1.1; display:block; color:#fff; text-shadow:0 3px 20px rgba(0,0,0,.6); }
  .wcap p { margin:10px 0 0; max-width:46ch; font-size:clamp(14px,1.5vw,18px); opacity:.9; line-height:1.6; text-shadow:0 2px 12px rgba(0,0,0,.6); }
  .floors { position:absolute; top:90px; right:24px; display:flex; flex-direction:column; align-items:flex-end; gap:10px; color:#fff; font-size:12px; letter-spacing:.2em; text-transform:uppercase; }
  .floors .f { opacity:.4; transition:opacity .4s; padding-right:16px; position:relative; } .floors .f::after { content:''; position:absolute; right:0; top:50%; width:6px; height:6px; margin-top:-3px; border-radius:50%; background:#fff; opacity:.6; }
  .floors .f.on { opacity:1; } .floors .f.on::after { background:var(--accent); opacity:1; box-shadow:0 0 0 4px rgba(255,255,255,.2); }
  .floors i { display:none; }
  .walkintro { padding-bottom:20px; }
  @media (prefers-reduced-motion: reduce) { .walkthru { height:auto; } .walkthru .stick { position:relative; height:auto; } .walkthru .scene { position:relative; opacity:1 !important; height:70vh; } .wcap { position:relative; opacity:1; transform:none; left:0; right:0; margin-bottom:20px; } .wcaps { position:relative; bottom:auto; padding:20px 24px; } .floors { display:none; } }

  .reveal { opacity:0; transition:opacity .8s ease; } .reveal.in { opacity:1; }
  .reveal .img { transform:translateY(34px) scale(.96); transition:transform .9s cubic-bezier(.2,.7,.2,1); } .reveal.in .img { transform:none; }
  .rise { opacity:0; transform:translateY(26px); transition:all .8s ease; } .rise.in { opacity:1; transform:none; }

  /* ---- realistic board: prints, index cards, restrained motion ---- */
  .cut { filter:none; background:none; padding:0; box-shadow:none; }
  .cut .img { clip-path:none; padding:14px; border:10px solid #fbf8f1; box-shadow:0 1px 2px rgba(0,0,0,.28), 0 14px 30px rgba(0,0,0,.2); }
  .cut .img::before { opacity:.22; }
  .cut .ph { font-size:clamp(15px,1.5vw,19px); color:%%PHC%%; font-style:italic; }
  .g0 { --g:linear-gradient(150deg,color-mix(in srgb,var(--accent2) 40%,%%MUTE%%),color-mix(in srgb,var(--accent) 35%,%%MUTE%%)); }
  .g1 { --g:linear-gradient(150deg,color-mix(in srgb,var(--accent) 30%,%%MUTE%%),color-mix(in srgb,var(--soft) 60%,%%MUTE%%)); }
  .g2 { --g:linear-gradient(150deg,color-mix(in srgb,var(--ink) 25%,%%MUTE%%),color-mix(in srgb,var(--accent2) 35%,%%MUTE%%)); }
  .g3 { --g:linear-gradient(150deg,color-mix(in srgb,var(--soft) 70%,%%MUTE%%),color-mix(in srgb,var(--accent2) 30%,%%MUTE%%)); }
  .tape { width:72px; height:20px; margin-left:-36px; top:-11px; background:rgba(236,228,205,.62); box-shadow:0 1px 1px rgba(0,0,0,.18); transform:rotate(-2deg); }
  .cap { margin:0; padding:16px 2px 0; gap:6px; color:var(--txt); }
  .cap .nm { font-family:var(--head); font-size:clamp(18px,1.7vw,22px); line-height:1.15; }
  .cap .nt { font-family:var(--hand); font-size:clamp(18px,1.7vw,21px); line-height:1.4; opacity:1; color:var(--pen); text-shadow:0 0 .5px currentColor; }
  .stamp { color:%%RED%%; }
  .note { background:none; box-shadow:none; clip-path:none; padding:0; color:var(--pen); position:relative; transform:rotate(-.8deg);
          font-size:clamp(21px,2.1vw,27px); line-height:1.42; text-shadow:0 0 .6px currentColor; }
  .note .tape { display:none; }
  .dd { fill:none; stroke:var(--pen); stroke-width:2.2; stroke-linecap:round; stroke-linejoin:round; overflow:visible; }
  .dd.under { display:block; width:min(260px,70%); height:14px; stroke:var(--accent); margin-top:10px; }
  .dd.pt { position:absolute; width:130px; height:64px; right:6px; bottom:-76px; transform:rotate(12deg); }
  .dd.up { display:inline-block; width:26px; height:20px; vertical-align:-4px; margin-right:6px; }
  .num { position:static; display:block; font-family:var(--body); font-size:12px; letter-spacing:.32em; text-transform:uppercase; color:var(--accent); -webkit-text-stroke:0; line-height:1; margin-bottom:8px; font-weight:500; }
  .ch-head { padding-top:0; }
  .reveal .img { transform:none; transition:none; } .reveal { transition:opacity 1s ease; }
  .scroll { animation:none; }
  .wcap .hand { font-family:var(--head); font-style:italic; font-size:clamp(30px,4.4vw,58px); line-height:1.05; }
  .cover .hand, .end .hand { font-family:var(--head); font-style:italic; }
  .index { max-width:860px; margin:0 auto; padding:34px 24px; text-align:center; border-block:1px solid color-mix(in srgb,var(--txt) 22%, transparent); }
  .index p { font-family:var(--head); font-style:italic; font-size:clamp(16px,1.6vw,19px); line-height:1.9; margin:8px 0 0; color:var(--txt); opacity:.85; }
  .index p span { white-space:nowrap; } .index p span::after { content:'  ·  '; opacity:.5; white-space:pre; } .index p span:last-child::after { content:''; }

  /* ---- smooth flow + layout variety ---- */
  .chapter:nth-of-type(even) { background:none; }
  .chapter { padding:100px 0 10px; }
  .chapter::after { content:''; display:block; height:150px; margin:36px auto 0; width:min(420px,60%); background:var(--accent); opacity:.5;
    -webkit-mask:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 200 150'><path d='M100 0 C 40 30, 160 60, 100 90 S 60 130, 100 150' fill='none' stroke='black' stroke-width='3' stroke-dasharray='2 9' stroke-linecap='round'/></svg>") center/contain no-repeat;
            mask:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 200 150'><path d='M100 0 C 40 30, 160 60, 100 90 S 60 130, 100 150' fill='none' stroke='black' stroke-width='3' stroke-dasharray='2 9' stroke-linecap='round'/></svg>") center/contain no-repeat; }
  .chapter:nth-of-type(even)::after { transform:scaleX(-1); }
  .index { border:0; }
  .cover { -webkit-mask-image:linear-gradient(#000 80%, transparent); mask-image:linear-gradient(#000 80%, transparent); }
  .walkthru { -webkit-mask-image:linear-gradient(transparent, #000 10vh, #000 calc(100% - 10vh), transparent); mask-image:linear-gradient(transparent, #000 10vh, #000 calc(100% - 10vh), transparent); }
  .num { position:absolute; top:-70px; left:10px; display:block; font-family:var(--head); font-size:clamp(72px,11vw,150px); white-space:nowrap; line-height:1; color:transparent; -webkit-text-stroke:1.5px color-mix(in srgb, var(--accent) 55%, transparent); letter-spacing:0; text-transform:none; margin:0; font-weight:400; z-index:0; pointer-events:none; }
  .ch-head { padding-top:70px; }
  .ch-head .kick { font-size:clamp(15px,1.5vw,19px); letter-spacing:.2em; font-weight:600; }
  .ch-head h2 { font-size:clamp(40px,6vw,88px); }
  @media (max-width:820px) { .num { top:-42px; font-size:76px; } .ch-head { padding-top:50px; } .chapter::after { height:100px; } }
  @media (min-width:821px) {
    .L-side .wrap { display:grid; grid-template-columns:.85fr 1.15fr; gap:0 64px; align-items:start; }
    .L-side .ch-head { grid-column:1; grid-template-columns:1fr; gap:26px; position:sticky; top:90px; margin-bottom:0; align-self:start; }
    .L-side .collage { grid-column:2; grid-row:1 / span 3; display:block; }
    .L-side .collage .cut { width:86% !important; margin:0 0 90px 0 !important; --ar:4/5; }
    .L-side .collage .cut:nth-child(even) { margin-left:14% !important; --ar:1/1; }
    .L-side .note .dd.pt { display:none; }
    .L-center .ch-head { grid-template-columns:1fr; justify-items:center; text-align:center; gap:26px; }
    .L-center .ch-head .dd.under { margin-left:auto; margin-right:auto; }
    .L-center .note { max-width:640px; }
    .L-center .note .dd.pt { right:-60px; bottom:-70px; }
    .L-center .collage { display:block; }
    .L-center .collage .cut { width:46% !important; margin:0 0 80px 4% !important; }
    .L-center .collage .cut:nth-child(even) { margin-left:auto !important; margin-right:4% !important; margin-top:-30px !important; }
    .L-hero .collage { display:flex; flex-wrap:wrap; gap:80px 4%; }
    .L-hero .collage .cut:nth-child(1) { width:100% !important; --ar:16/8 !important; margin:0 !important; }
    .L-hero .collage .cut:nth-child(n+2) { width:30% !important; margin:0 !important; --ar:4/5; }
    .L-hero .collage .cut:nth-child(3n) { margin-top:50px !important; }
    .L-hero .collage.n2 .cut:nth-child(2) { width:46% !important; margin-left:auto !important; }
    .L-mason .ch-head { grid-template-columns:1fr; gap:26px; }
    .L-mason .note { max-width:700px; }
    .L-mason .collage { display:block; column-count:2; column-gap:6%; }
    .L-mason .collage .cut { width:100% !important; margin:0 0 80px !important; break-inside:avoid; }
    .L-mason .collage .cut:nth-child(odd) { --ar:4/5; } .L-mason .collage .cut:nth-child(even) { --ar:1/1; }
    .L-mason .collage.n1 { column-count:1; }
  }

  /* ---- Madison Square Park collage scene ---- */
  .scene-col { flex:0 0 100%; width:100%; }
  .mscene { position:relative; width:min(1180px,100%); aspect-ratio:16/11.2; margin:30px auto 20px; }
  .mscene .lyr { position:absolute; margin:0; transform:translateY(var(--py,0px)) rotate(var(--r,0deg)); filter:drop-shadow(0 10px 14px rgba(0,0,0,.4)); will-change:transform; }
  .mscene img.lyr { height:auto; max-width:none; }
  .mscene .print { background:#f4efe3; padding:10px 10px 12px; box-shadow:0 1px 0 rgba(255,255,255,.4) inset; filter:drop-shadow(0 12px 16px rgba(0,0,0,.45)); }
  .mscene .print img { display:block; width:100%; height:auto; }
  .mscene .print.wide { left:7%; top:3%; width:63%; --r:-1.6deg; z-index:1; }
  .mscene .print.tall { right:3%; top:0%; width:25%; --r:2.6deg; z-index:2; padding-bottom:34px; }
  .mscene .print.tall figcaption { position:absolute; left:0; right:0; bottom:6px; text-align:center; font-size:clamp(14px,1.7vw,22px); color:#2a2a2a; }
  .mscene .tape { z-index:5; }
  .mscene .tree.tl { left:-6%; top:12%; width:31%; --r:-2deg; z-index:4; }
  .mscene .tree.tr { right:-5%; bottom:4%; width:30%; --r:3deg; z-index:4; }
  .mscene .tower { left:57%; top:25%; width:14.5%; --r:2deg; z-index:3; }
  .mscene .fount { left:21%; bottom:-1%; width:47%; --r:-2.5deg; z-index:5; }
  .mscene .circ { left:3%; bottom:3%; width:16%; --r:-5deg; z-index:6; }
  .mscene .msg { z-index:7; color:var(--pen); font-size:clamp(14px,2vw,26px); line-height:1.15; filter:none; }
  .mscene .msg.m1 { left:6%; top:62%; --r:-4deg; }
  .mscene .msg.m2 { left:56.5%; top:59%; --r:2deg; width:16%; z-index:7; }
  .mscene .msg.m3 { right:9%; bottom:-3%; --r:-3deg; width:22%; }
  .mscene .dd.a1 { left:21%; top:73%; width:11%; --r:-20deg; z-index:7; filter:none; }
  .mscene .dd.a2 { display:none; }
  .mscene .dd.u1 { display:none; }
  @media (max-width:820px) {
    .mscene { aspect-ratio:3/5.7; }
    .mscene .print.wide { left:3%; top:1%; width:90%; }
    .mscene .print.tall { right:2%; top:25%; width:52%; }
    .mscene .tree.tl { left:-9%; top:29%; width:38%; }
    .mscene .tower { display:none; }
    .mscene .fount { left:3%; top:73%; bottom:auto; width:80%; }
    .mscene .circ { left:auto; right:3%; top:57%; width:30%; }
    .mscene .tree.tr { right:-9%; top:83%; bottom:auto; width:40%; }
    .mscene .msg { font-size:15px; }
    .mscene .msg.m1 { left:4%; top:63%; width:50%; }
    .mscene .msg.m2 { left:4%; top:53%; width:36%; }
    .mscene .msg.m3 { left:4%; right:auto; top:auto; bottom:1%; width:46%; }
    .mscene .dd { display:none; }
  }

  /* ---- extra snapshots on a stop ---- */
  .cut .snap { position:absolute; width:46%; background:#f4efe3; padding:7px 7px 24px; box-shadow:0 10px 18px rgba(0,0,0,.4); z-index:3; }
  .cut .snap img { display:block; width:100%; aspect-ratio:4/5; object-fit:cover; }
  .cut .snap em { position:absolute; left:0; right:0; bottom:3px; text-align:center; font-style:normal; font-size:15px; color:#2a2a2a; }
  .cut .snap .tape { width:50px; height:15px; margin-left:-25px; top:-8px; }
  .cut .snap.s1 { right:-13%; top:30%; transform:rotate(5deg); width:40%; }
  .cut .snap.s2 { left:-32%; top:26%; transform:rotate(-4deg); width:36%; }
  @media (max-width:820px) { .cut .snap { width:34% !important; } .cut .snap.s1 { right:-3%; top:24%; } .cut .snap.s2 { left:-3%; top:32%; } }

  /* ---- Chelsea galleries collage scene ---- */
  .cscene { position:relative; width:min(1180px,100%); aspect-ratio:16/12.6; margin:30px auto 20px; }
  .cscene .lyr { position:absolute; margin:0; transform:translateY(var(--py,0px)) rotate(var(--r,0deg)); filter:drop-shadow(0 10px 14px rgba(0,0,0,.4)); will-change:transform; }
  .cscene img.lyr { height:auto; max-width:none; }
  .cscene .print { background:#f4efe3; padding:9px 9px 11px; }
  .cscene .print img { display:block; width:100%; height:auto; }
  .cscene .print figcaption { position:absolute; left:0; right:0; bottom:5px; text-align:center; font-size:clamp(13px,1.5vw,20px); color:#2a2a2a; }
  .cscene .print:has(figcaption) { padding-bottom:30px; }
  .cscene .tape { z-index:5; }
  .cscene .ext { left:2%; top:2%; width:47%; --r:-1.6deg; z-index:1; }
  .cscene .night { right:3%; top:0%; width:32%; --r:2.4deg; z-index:2; }
  .cscene .eve { right:19%; top:30%; width:22%; --r:-3deg; z-index:4; }
  .cscene .branches { left:30%; top:43%; width:35%; --r:1.4deg; z-index:2; }
  .cscene .paint { right:3%; top:49%; width:25%; --r:-2.2deg; z-index:3; }
  .cscene .kawsroom { left:1%; top:58%; width:27%; --r:-3deg; z-index:3; }
  .cscene .koons { left:44%; top:13%; width:10%; --r:-6deg; z-index:6; }
  .cscene .kaws { left:62%; top:50%; width:10%; --r:5deg; z-index:6; }
  .cscene .msg { z-index:7; color:var(--pen); font-size:clamp(14px,2vw,26px); line-height:1.15; filter:none; }
  .cscene .msg.c1 { left:54%; top:3%; width:9%; --r:-3deg; z-index:7; }
  .cscene .msg.c2 { left:33%; top:88%; --r:-3deg; }
  .cscene .msg.c3 { right:3%; top:88%; --r:-2deg; }
  @media (max-width:820px) {
    .cscene { aspect-ratio:3/6.4; }
    .cscene .ext { left:3%; top:1%; width:92%; }
    .cscene .night { right:2%; top:22%; width:56%; }
    .cscene .eve { left:2%; top:30%; width:40%; }
    .cscene .branches { left:3%; top:44%; width:70%; }
    .cscene .paint { right:2%; top:57%; width:56%; }
    .cscene .kawsroom { left:3%; top:70%; width:52%; }
    .cscene .koons { left:72%; top:41.5%; width:18%; }
    .cscene .kaws { left:60%; top:74%; width:19%; }
    .cscene .msg { font-size:15px; }
    .cscene .msg.c1, .cscene .msg.c2 { display:none; }
    .cscene .msg.c3 { left:30%; right:auto; bottom:1%; width:60%; }
  }

  /* ---- CJ Hendry Flower Market collage scene ---- */
  .fscene { position:relative; width:min(1180px,100%); aspect-ratio:16/10.4; margin:30px auto 20px; }
  .fscene .lyr { position:absolute; margin:0; transform:translateY(var(--py,0px)) rotate(var(--r,0deg)); filter:drop-shadow(0 10px 14px rgba(0,0,0,.35)); will-change:transform; }
  .fscene img.lyr { height:auto; max-width:none; }
  .fscene .print { background:#f4efe3; padding:9px 9px 11px; }
  .fscene .print img { display:block; width:100%; height:auto; }
  .fscene .print figcaption { position:absolute; left:0; right:0; bottom:5px; text-align:center; font-size:clamp(13px,1.5vw,20px); color:#2a2a2a; }
  .fscene .print:has(figcaption) { padding-bottom:30px; }
  .fscene .tape { z-index:5; }
  .fscene .tent { left:2%; top:2%; width:57%; --r:-1.4deg; z-index:1; }
  .fscene .tiers { right:3%; top:4%; width:35%; --r:2.4deg; z-index:2; }
  .fscene .close { left:36%; top:50%; width:26%; --r:-3deg; z-index:3; }
  .fscene .bq1 { left:7%; top:44%; width:25%; --r:-9deg; z-index:6; }
  .fscene .bq2 { right:4%; top:44%; width:20%; --r:8deg; z-index:6; }
  .fscene .msg { z-index:7; color:var(--pen); font-size:clamp(14px,2vw,26px); line-height:1.15; filter:none; }
  .fscene .msg.f1 { left:64%; top:56%; --r:-3deg; width:12%; }
  .fscene .msg.f2 { left:22%; top:90%; --r:-2deg; }
  .fscene .dd.a1 { left:35%; top:90%; width:9%; --r:-8deg; z-index:7; filter:none; }
  @media (max-width:820px) {
    .fscene { aspect-ratio:3/6; }
    .fscene .tent { left:3%; top:1%; width:92%; }
    .fscene .tiers { right:2%; top:22%; width:62%; }
    .fscene .close { left:3%; top:50%; width:46%; }
    .fscene .bq1 { left:4%; top:30%; width:34%; }
    .fscene .bq2 { right:4%; top:56%; width:30%; }
    .fscene .msg { font-size:15px; }
    .fscene .msg.f1 { display:none; }
    .fscene .msg.f2 { left:8%; top:90%; width:50%; }
    .fscene .dd { display:none; }
  }

  /* ---- Gentle Monster collage scene ---- */
  .gscene { position:relative; width:min(1180px,100%); aspect-ratio:16/11; margin:30px auto 20px; }
  .gscene .lyr { position:absolute; margin:0; transform:translateY(var(--py,0px)) rotate(var(--r,0deg)); filter:drop-shadow(0 10px 14px rgba(0,0,0,.35)); will-change:transform; }
  .gscene img.lyr { height:auto; max-width:none; }
  .gscene .print { background:#f4efe3; padding:9px 9px 11px; }
  .gscene .print img { display:block; width:100%; height:auto; }
  .gscene .print figcaption { position:absolute; left:0; right:0; bottom:5px; text-align:center; font-size:clamp(13px,1.5vw,20px); color:#2a2a2a; }
  .gscene .print:has(figcaption) { padding-bottom:30px; }
  .gscene .tape { z-index:5; }
  .gscene .shop { left:2%; top:2%; width:54%; --r:-1.4deg; z-index:1; }
  .gscene .door { right:5%; top:3%; width:18%; --r:3deg; z-index:2; }
  .gscene .coral { left:34%; top:44%; width:34%; --r:1.8deg; z-index:3; }
  .gscene .bison { left:4%; top:56%; width:28%; --r:-3deg; z-index:3; }
  .gscene .faces { right:3%; top:38%; width:22%; --r:5deg; z-index:6; }
  .gscene .msg { z-index:7; color:var(--pen); font-size:clamp(14px,2vw,26px); line-height:1.15; filter:none; }
  .gscene .msg.g1 { left:58%; top:10%; --r:-3deg; width:16%; }
  .gscene .msg.g2 { left:72%; top:84%; --r:-2deg; }
  .gscene .dd.a1 { left:55%; top:26%; width:8%; --r:25deg; z-index:7; filter:none; }
  @media (max-width:820px) {
    .gscene { aspect-ratio:3/6.2; }
    .gscene .shop { left:3%; top:1%; width:92%; }
    .gscene .door { right:3%; top:22%; width:38%; }
    .gscene .coral { left:3%; top:30%; width:62%; }
    .gscene .bison { left:30%; top:56%; width:66%; }
    .gscene .faces { left:2%; top:64%; width:40%; right:auto; }
    .gscene .msg { font-size:15px; }
    .gscene .msg.g1 { display:none; }
    .gscene .msg.g2 { left:6%; top:92%; width:70%; }
    .gscene .dd { display:none; }
  }

  /* ---- Mercer Labs collage scene ---- */
  .mlscene { position:relative; width:min(1180px,100%); aspect-ratio:16/11.2; margin:30px auto 20px; }
  .mlscene .lyr { position:absolute; margin:0; transform:translateY(var(--py,0px)) rotate(var(--r,0deg)); filter:drop-shadow(0 10px 14px rgba(0,0,0,.4)); will-change:transform; }
  .mlscene img.lyr { height:auto; max-width:none; }
  .mlscene .print { background:#f4efe3; padding:9px 9px 11px; }
  .mlscene .print img { display:block; width:100%; height:auto; }
  .mlscene .print figcaption { position:absolute; left:0; right:0; bottom:5px; text-align:center; font-size:clamp(13px,1.5vw,20px); color:#2a2a2a; }
  .mlscene .print:has(figcaption) { padding-bottom:30px; }
  .mlscene .tape { z-index:5; }
  .mlscene .room { left:3%; top:2%; width:30%; --r:-2deg; z-index:1; }
  .mlscene .cave { left:31%; top:8%; width:24%; --r:2.5deg; z-index:2; }
  .mlscene .robot { right:4%; top:2%; width:26%; --r:-2.4deg; z-index:2; }
  .mlscene .ext { left:56%; top:40%; width:21%; --r:4deg; z-index:5; }
  .mlscene .neon { left:6%; top:62%; width:24%; --r:-6deg; z-index:5; }
  .mlscene .tun { left:33%; top:61%; width:22%; --r:5deg; z-index:5; }
  .mlscene .msg { z-index:7; color:var(--pen); font-size:clamp(14px,2vw,26px); line-height:1.15; filter:none; }
  .mlscene .msg.l1 { left:57%; top:12%; --r:-3deg; width:13%; }
  .mlscene .msg.l2 { left:68%; top:78%; --r:-2deg; }
  .mlscene .dd.a1 { left:30%; top:48%; width:8%; --r:60deg; z-index:7; filter:none; display:none; }
  @media (max-width:820px) {
    .mlscene { aspect-ratio:3/7; }
    .mlscene .room { left:3%; top:1%; width:62%; }
    .mlscene .cave { right:3%; top:12%; width:50%; left:auto; }
    .mlscene .robot { left:3%; top:34%; width:52%; right:auto; }
    .mlscene .ext { left:auto; right:3%; top:38%; width:40%; }
    .mlscene .neon { left:3%; top:64%; width:44%; }
    .mlscene .tun { left:auto; right:4%; top:62%; width:40%; }
    .mlscene .msg { font-size:15px; }
    .mlscene .msg.l1 { display:none; }
    .mlscene .msg.l2 { left:8%; top:92%; width:60%; }
    .mlscene .dd { display:none; }
  }

  /* ---- 12 Matcha collage scene ---- */
  .tscene { position:relative; width:min(1180px,100%); aspect-ratio:16/10.2; margin:30px auto 20px; }
  .tscene .lyr { position:absolute; margin:0; transform:translateY(var(--py,0px)) rotate(var(--r,0deg)); filter:drop-shadow(0 10px 14px rgba(0,0,0,.35)); will-change:transform; }
  .tscene img.lyr { height:auto; max-width:none; }
  .tscene .print { background:#f4efe3; padding:9px 9px 11px; }
  .tscene .print img { display:block; width:100%; height:auto; }
  .tscene .print figcaption { position:absolute; left:0; right:0; bottom:5px; text-align:center; font-size:clamp(13px,1.5vw,20px); color:#2a2a2a; }
  .tscene .print:has(figcaption) { padding-bottom:30px; }
  .tscene .tape { z-index:5; }
  .tscene .bar { left:3%; top:2%; width:55%; --r:-1.5deg; z-index:1; }
  .tscene .room { right:3%; top:6%; width:36%; --r:2.2deg; z-index:2; }
  .tscene .cup { left:50%; top:36%; width:13%; --r:6deg; z-index:6; }
  .tscene .cups { left:8%; top:58%; width:20%; --r:-6deg; z-index:5; }
  .tscene .jars { left:29%; top:62%; width:20%; --r:4deg; z-index:5; }
  .tscene .msg { z-index:7; color:var(--pen); font-size:clamp(14px,2vw,26px); line-height:1.15; filter:none; }
  .tscene .msg.t1 { left:66%; top:44%; --r:-3deg; }
  .tscene .msg.t2 { left:64%; top:70%; --r:-2deg; }
  .tscene .dd.a1 { left:64%; top:56%; width:8%; --r:200deg; z-index:7; filter:none; }
  @media (max-width:820px) {
    .tscene { aspect-ratio:3/6; }
    .tscene .bar { left:3%; top:1%; width:92%; }
    .tscene .room { right:3%; top:20%; width:70%; }
    .tscene .cup { left:3%; top:34%; width:26%; }
    .tscene .cups { left:3%; top:58%; width:42%; }
    .tscene .jars { left:auto; right:3%; top:56%; width:44%; }
    .tscene .msg { font-size:15px; }
    .tscene .msg.t1 { display:none; }
    .tscene .msg.t2 { left:8%; top:90%; width:60%; }
    .tscene .dd { display:none; }
  }

  /* collage scenes always span the full chapter width, whatever the layout */
  .collage .scene-col { column-span:all; -webkit-column-span:all; }
  @media (min-width:821px) { .L-side .collage:has(.scene-col) { grid-column:1 / -1; grid-row:auto; } .L-side:has(.scene-col) .ch-head { position:static; } }

  /* ---- Rok Matcha collage scene ---- */
  .rscene { position:relative; width:min(1180px,100%); aspect-ratio:16/9; margin:30px auto 20px; }
  .rscene .lyr { position:absolute; margin:0; transform:translateY(var(--py,0px)) rotate(var(--r,0deg)); filter:drop-shadow(0 10px 14px rgba(0,0,0,.35)); will-change:transform; }
  .rscene img.lyr { height:auto; max-width:none; }
  .rscene .print { background:#f4efe3; padding:9px 9px 34px; }
  .rscene .print img { display:block; width:100%; height:auto; }
  .rscene .print figcaption { position:absolute; left:0; right:0; bottom:6px; text-align:center; font-size:clamp(13px,1.5vw,20px); color:#2a2a2a; }
  .rscene .tape { z-index:5; }
  .rscene .store { left:4%; top:4%; width:58%; --r:-1.6deg; z-index:1; }
  .rscene .cup { right:12%; top:2%; width:17%; --r:4deg; z-index:6; }
  .rscene .door { left:44%; top:52%; width:19%; --r:-5deg; z-index:5; }
  .rscene .msg { z-index:7; color:var(--pen); font-size:clamp(14px,2vw,26px); line-height:1.15; filter:none; }
  .rscene .msg.r1 { left:75%; top:50%; --r:-3deg; width:16%; }
  .rscene .msg.r2 { left:66%; top:73%; --r:-2deg; }
  .rscene .dd.a1 { left:73%; top:42%; width:6%; --r:-30deg; z-index:7; filter:none; display:none; }
  @media (max-width:820px) {
    .rscene { aspect-ratio:3/4.4; }
    .rscene .store { left:3%; top:1%; width:92%; }
    .rscene .cup { right:6%; top:26%; width:42%; }
    .rscene .door { left:3%; top:34%; width:46%; }
    .rscene .msg { font-size:15px; }
    .rscene .msg.r1 { display:none; }
    .rscene .msg.r2 { left:8%; top:90%; width:60%; }
    .rscene .dd { display:none; }
  }

  /* ---- Rhythm Zero collage scene ---- */
  .zscene { position:relative; width:min(1180px,100%); aspect-ratio:16/8; margin:30px auto 20px; }
  .zscene .lyr { position:absolute; margin:0; transform:translateY(var(--py,0px)) rotate(var(--r,0deg)); filter:drop-shadow(0 10px 14px rgba(0,0,0,.35)); will-change:transform; }
  .zscene img.lyr { height:auto; max-width:none; }
  .zscene .print { background:#f4efe3; padding:9px 9px 34px; }
  .zscene .print img { display:block; width:100%; height:auto; }
  .zscene .print figcaption { position:absolute; left:0; right:0; bottom:6px; text-align:center; font-size:clamp(13px,1.5vw,20px); color:#2a2a2a; }
  .zscene .tape { z-index:5; }
  .zscene .store { left:8%; top:8%; width:40%; --r:-2deg; z-index:1; }
  .zscene .cup { left:44%; top:2%; width:15%; --r:5deg; z-index:6; }
  .zscene .msg { z-index:7; color:var(--pen); font-size:clamp(14px,2vw,26px); line-height:1.15; filter:none; }
  .zscene .msg.z1 { left:62%; top:22%; --r:-3deg; }
  .zscene .msg.z2 { left:20%; top:80%; --r:-2deg; }
  @media (max-width:820px) {
    .zscene { aspect-ratio:3/3.8; }
    .zscene .store { left:3%; top:2%; width:80%; }
    .zscene .cup { right:4%; left:auto; top:36%; width:42%; }
    .zscene .msg { font-size:15px; }
    .zscene .msg.z1 { left:6%; top:62%; width:46%; }
    .zscene .msg.z2 { left:6%; top:86%; }
  }

  .rscene.nyc { aspect-ratio:16/6; }
  .rscene.nyc .cup { left:30%; top:4%; width:15%; }
  .rscene.nyc .msg.r1 { left:48%; top:30%; }
  .rscene.nyc .msg.r2 { left:34%; top:78%; }
  @media (max-width:820px) { .rscene.nyc { aspect-ratio:3/3; } .rscene.nyc .cup { left:8%; right:auto; top:4%; width:40%; } .rscene.nyc .msg.r1 { display:block; left:52%; top:30%; width:44%; } .rscene.nyc .msg.r2 { left:8%; top:86%; } }

  /* ---- Ippudo collage scene ---- */
  .iscene { position:relative; width:min(1180px,100%); aspect-ratio:16/10.6; margin:30px auto 20px; }
  .iscene .lyr { position:absolute; margin:0; transform:translateY(var(--py,0px)) rotate(var(--r,0deg)); filter:drop-shadow(0 10px 14px rgba(0,0,0,.4)); will-change:transform; }
  .iscene img.lyr { height:auto; max-width:none; }
  .iscene .print { background:#f4efe3; padding:9px 9px 11px; }
  .iscene .print img { display:block; width:100%; height:auto; }
  .iscene .print figcaption { position:absolute; left:0; right:0; bottom:5px; text-align:center; font-size:clamp(13px,1.5vw,20px); color:#2a2a2a; }
  .iscene .print:has(figcaption) { padding-bottom:30px; }
  .iscene .tape { z-index:5; }
  .iscene .room1 { left:3%; top:3%; width:47%; --r:-1.6deg; z-index:1; }
  .iscene .store { right:4%; top:2%; width:33%; --r:2.4deg; z-index:2; }
  .iscene .room2 { left:6%; top:52%; width:34%; --r:2deg; z-index:2; }
  .iscene .bowl1 { left:38%; top:40%; width:25%; --r:-6deg; z-index:6; }
  .iscene .bowl2 { left:58%; top:56%; width:21%; --r:7deg; z-index:6; }
  .iscene .msg { z-index:7; color:var(--pen); font-size:clamp(14px,2vw,26px); line-height:1.15; filter:none; }
  .iscene .msg.i1 { left:78%; top:48%; --r:-3deg; width:16%; }
  .iscene .msg.i2 { left:80%; top:78%; --r:-2deg; }
  @media (max-width:820px) {
    .iscene { aspect-ratio:3/6.2; }
    .iscene .room1 { left:3%; top:1%; width:92%; }
    .iscene .store { right:3%; top:20%; width:62%; }
    .iscene .room2 { left:3%; top:44%; width:62%; }
    .iscene .bowl1 { right:2%; top:42%; width:52%; left:auto; }
    .iscene .bowl2 { left:6%; top:68%; width:50%; }
    .iscene .msg { font-size:15px; }
    .iscene .msg.i1 { display:none; }
    .iscene .msg.i2 { left:8%; top:92%; width:60%; }
  }

  /* ---- Printemps collage scene ---- */
  .pscene { position:relative; width:min(1180px,100%); aspect-ratio:16/11.6; margin:30px auto 20px; }
  .pscene .lyr { position:absolute; margin:0; transform:translateY(var(--py,0px)) rotate(var(--r,0deg)); filter:drop-shadow(0 10px 14px rgba(0,0,0,.4)); will-change:transform; }
  .pscene img.lyr { height:auto; max-width:none; }
  .pscene .print { background:#f4efe3; padding:9px 9px 11px; }
  .pscene .print img { display:block; width:100%; height:auto; }
  .pscene .print figcaption { position:absolute; left:0; right:0; bottom:5px; text-align:center; font-size:clamp(13px,1.5vw,20px); color:#2a2a2a; }
  .pscene .print:has(figcaption) { padding-bottom:30px; }
  .pscene .tape { z-index:5; }
  .pscene .hall { left:3%; top:2%; width:42%; --r:-1.8deg; z-index:1; }
  .pscene .lounge { left:42%; top:8%; width:19%; --r:3deg; z-index:2; }
  .pscene .beauty { right:3%; top:2%; width:32%; --r:2deg; z-index:2; }
  .pscene .door { left:8%; top:52%; width:20%; --r:-4deg; z-index:5; }
  .pscene .lamp { left:31%; top:52%; width:19%; --r:5deg; z-index:5; }
  .pscene .pedestal { right:16%; top:50%; width:16%; --r:-5deg; z-index:5; }
  .pscene .msg { z-index:7; color:var(--pen); font-size:clamp(14px,2vw,26px); line-height:1.15; filter:none; }
  .pscene .msg.p1 { left:54%; top:68%; --r:-3deg; }
  .pscene .msg.p2 { left:48%; top:48%; --r:-4deg; display:none; }
  @media (max-width:820px) {
    .pscene { aspect-ratio:3/7; }
    .pscene .hall { left:3%; top:1%; width:92%; }
    .pscene .lounge { left:3%; top:22%; width:44%; }
    .pscene .beauty { right:3%; top:25%; width:50%; }
    .pscene .door { left:4%; top:46%; width:42%; }
    .pscene .lamp { right:4%; left:auto; top:46%; width:40%; }
    .pscene .pedestal { left:30%; top:66%; width:40%; right:auto; }
    .pscene .msg { font-size:15px; }
    .pscene .msg.p1 { left:8%; top:90%; width:60%; }
  }

  /* ending */
  .about { max-width:1100px; margin:0 auto; padding:110px 24px 40px; display:grid; grid-template-columns:1.1fr .9fr; gap:40px; }
  .about h2 { font-size:clamp(30px,4vw,50px); margin:8px 0 14px; } .about p { line-height:1.8; max-width:52ch; }
  .chips { display:flex; flex-wrap:wrap; gap:8px; margin-top:14px; }
  .chip { display:inline-flex; align-items:center; gap:8px; padding:6px 12px; border:1px solid color-mix(in srgb, var(--txt) 30%, transparent); border-radius:999px; font-size:13px; }
  .chip i { width:14px; height:14px; border-radius:50%; background:var(--accent); } .chip:nth-child(2) i { background:var(--accent2); } .chip:nth-child(3) i { background:var(--soft); border:1px solid rgba(0,0,0,.2); }
  ul.clean { margin:10px 0 0; padding-left:18px; line-height:1.9; }
  .lists { max-width:1100px; margin:0 auto; padding:30px 24px 80px; display:grid; grid-template-columns:1fr 1fr; gap:40px; }
  .lists h3 { font-size:30px; margin-bottom:6px; }
  .lists em, .about em { opacity:.65; }
  .end { text-align:center; padding:120px 24px 130px; background:linear-gradient(180deg,transparent,color-mix(in srgb, var(--accent) 22%, transparent)); }
  .end h2 { font-size:clamp(38px,6.5vw,88px); max-width:14ch; margin:12px auto 10px; }
  .end .hand { font-size:26px; color:var(--accent); }
  .btn { display:inline-block; margin-top:26px; padding:16px 32px; border-radius:999px; background:var(--txt); color:var(--bg); font-size:14px; letter-spacing:.08em; }
  .fine { text-align:center; opacity:.55; font-size:12px; padding:0 20px 40px; }

  @media (max-width:820px) {
    .ch-head,.about,.lists { grid-template-columns:1fr; }
    .collage { gap:70px 4%; }
    .ch-head { margin-bottom:40px; }
    .n1 .cut,.n2 .cut,.n3 .cut:nth-child(n),.n4 .cut { width:100% !important; margin-left:0 !important; margin-top:0 !important; }
    .cut:nth-child(even) { width:84% !important; margin-left:auto !important; }
    .float.b,.cover .float.c { display:none; } .cover .float.a { top:10%; right:5%; width:34vw; }
    .chapter { padding-top:90px; } .dd.pt { display:none; }
  }
  @media (prefers-reduced-motion: reduce) { .reveal,.rise { opacity:1; transform:none; transition:none; } .reveal .img { transform:none; } .marq div,.scroll { animation:none; } }
"""

DOODLES = """<svg width="0" height="0" style="position:absolute"><defs>
<symbol id="d-arrow" viewBox="0 0 140 70"><path d="M6 12 C 34 2, 68 8, 94 30 S 120 54, 130 57"/><path d="M113 44 L131 58 L108 63"/></symbol>
<symbol id="d-under" viewBox="0 0 300 14"><path d="M3 9 C 60 3, 120 12, 180 6 S 260 4, 297 8"/><path d="M30 12.5 C 100 8, 170 13, 250 10"/></symbol>
<symbol id="d-up" viewBox="0 0 40 30"><path d="M4 26 C 14 25, 24 15, 31 4"/><path d="M22 6 L32 3 L34 13"/></symbol>
</defs></svg>"""

JS = r"""
<script>
(function () {
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var els = document.querySelectorAll('.reveal,.rise');
  if (!('IntersectionObserver' in window)) { els.forEach(function (e) { e.classList.add('in'); }); }
  else {
    var io = new IntersectionObserver(function (en) { en.forEach(function (x) { if (x.isIntersecting) { x.target.classList.add('in'); io.unobserve(x.target); } }); }, { threshold: .12 });
    els.forEach(function (e) { io.observe(e); });
  }
  var cur = document.querySelector('.hud .cur'), bar = document.querySelector('.hud .bar');
  var chs = document.querySelectorAll('.chapter,.walkthru');
  var cuts = Array.prototype.slice.call(document.querySelectorAll('.cut[data-speed],.lyr[data-speed]'));
  var walk = document.querySelector('.walkthru'), ticking = false, s1, s2, s3, wcaps = [], floors = [];
  if (walk) { s1 = walk.querySelector('.s1'); s2 = walk.querySelector('.s2'); s3 = walk.querySelector('.s3');
    wcaps = Array.prototype.slice.call(walk.querySelectorAll('.wcap')); floors = Array.prototype.slice.call(walk.querySelectorAll('.floors .f')); }
  function frame() {
    ticking = false;
    var h = document.documentElement, st = window.pageYOffset || h.scrollTop, max = h.scrollHeight - window.innerHeight;
    if (bar && max > 0) bar.style.width = Math.min(100, st / max * 100) + '%';
    var vh = window.innerHeight, label = 'Intro';
    chs.forEach(function (c) { var r = c.getBoundingClientRect(); if (r.top < vh * .5) label = c.getAttribute('data-label'); });
    if (cur && cur.textContent !== label) cur.textContent = label;
    if (walk && !reduce) {
      var wr = walk.getBoundingClientRect(), p = Math.max(0, Math.min(1, -wr.top / (wr.height - vh)));
      var ramp = function (a, b, x) { return Math.max(0, Math.min(1, (x - a) / (b - a))); };
      var o1 = 1 - ramp(.28, .40, p), o2 = ramp(.28, .40, p) * (1 - ramp(.62, .74, p)), o3 = ramp(.62, .74, p);
      s1.style.opacity = o1; s2.style.opacity = o2; s3.style.opacity = o3;
      s1.firstElementChild.style.transform = 'scale(' + (1 + .55 * ramp(0, .4, p)).toFixed(3) + ')';
      s2.querySelector('img').style.transform = 'translate(-50%,-50%) scale(' + (1.02 + .14 * ramp(.3, .72, p)).toFixed(3) + ')';
      s3.querySelector('img').style.transform = 'scale(' + (1 + .12 * ramp(.62, 1, p)).toFixed(3) + ')';
      var step = p < .34 ? 0 : (p < .68 ? 1 : 2);
      wcaps.forEach(function (c, i) { c.classList.toggle('on', i === step); });
      floors.forEach(function (f, i) { f.classList.toggle('on', i === step); });
    }
    if (!reduce && window.innerWidth > 820) cuts.forEach(function (c) {
      var r = c.getBoundingClientRect();
      if (r.bottom < -200 || r.top > vh + 200) return;
      var d = (r.top + r.height / 2 - vh / 2) * parseFloat(c.getAttribute('data-speed'));
      c.style.setProperty('--py', d.toFixed(1) + 'px');
    });
  }
  function onScroll() { if (!ticking) { ticking = true; requestAnimationFrame(frame); } }
  window.addEventListener('scroll', onScroll, { passive: true }); window.addEventListener('resize', onScroll); frame();
})();
</script>
"""


def paper_tex(dark):
    import urllib.parse
    def uri(svg): return "url(\"data:image/svg+xml;utf8," + urllib.parse.quote(svg, safe="/:=,'()* ") .replace('"', "%22") + "\")"
    if dark:
        mottle = "<svg xmlns='http://www.w3.org/2000/svg' width='700' height='700'><filter id='m'><feTurbulence type='fractalNoise' baseFrequency='.012 .02' numOctaves='3' seed='4' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 .55  0 0 0 0 .6  0 0 0 0 .8  0 0 0 .22 -.05'/></filter><rect width='100%' height='100%' filter='url(#m)'/></svg>"
        fiber = "<svg xmlns='http://www.w3.org/2000/svg' width='400' height='400'><filter id='f'><feTurbulence type='fractalNoise' baseFrequency='.9 .05' numOctaves='2' seed='9' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 .8  0 0 0 0 .8  0 0 0 0 .9  0 0 0 .18 -.08'/></filter><rect width='100%' height='100%' filter='url(#f)'/></svg>"
        grain = "<svg xmlns='http://www.w3.org/2000/svg' width='220' height='220'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='2' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 .22 -.04'/></filter><rect width='100%' height='100%' filter='url(#n)'/></svg>"
    else:
        mottle = "<svg xmlns='http://www.w3.org/2000/svg' width='700' height='700'><filter id='m'><feTurbulence type='fractalNoise' baseFrequency='.012 .02' numOctaves='3' seed='4' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 .55  0 0 0 0 .42  0 0 0 0 .25  0 0 0 .32 -.08'/></filter><rect width='100%' height='100%' filter='url(#m)'/></svg>"
        fiber = "<svg xmlns='http://www.w3.org/2000/svg' width='400' height='400'><filter id='f'><feTurbulence type='fractalNoise' baseFrequency='.9 .05' numOctaves='2' seed='9' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 .45  0 0 0 0 .35  0 0 0 0 .2  0 0 0 .22 -.09'/></filter><rect width='100%' height='100%' filter='url(#f)'/></svg>"
        grain = "<svg xmlns='http://www.w3.org/2000/svg' width='220' height='220'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='2' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 .2  0 0 0 0 .15  0 0 0 0 .1  0 0 0 .32 -.06'/></filter><rect width='100%' height='100%' filter='url(#n)'/></svg>"
    return ", ".join(uri(x) for x in (grain, fiber, mottle))

SNAPS = {('nomad', 'nubeluz-50th-floor'): [('nubeluz-50th-floor-day', 'by day', 's1'), ('nubeluz-50th-floor-night', 'by night', 's2')]}

def snaps(slug_h, key):
    out = ''
    for n, (img, label, cls) in enumerate(SNAPS.get((slug_h, key), [])):
        out += f'<span class="snap {cls}"><span class="tape"></span><img src="{CDN}{slug_h}/{img}.jpg" alt="{label}" loading="lazy" onerror="this.parentNode.remove()"><em class="hand">{label}</em></span>'
    return out

def printemps_scene(slug_h, cap_html):
    M = CDN + 'shared/printemps/'
    P = lambda cls, src, alt, cap='', sp=0.02: f'<figure class="lyr print {cls}" data-speed="{sp}"><div class="tape"></div><img src="{M}{src}" alt="{alt}" loading="lazy">' + (f'<figcaption class="hand">{cap}</figcaption>' if cap else '') + '</figure>'
    C = lambda cls, src, sp: f'<img class="lyr {cls}" data-speed="{sp}" src="{M}{src}" alt="" loading="lazy">'
    return f'''
        <div class="scene-col">
          <div class="pscene reveal">
            {P('hall', 'hall.jpg', 'The gilded main hall', 'the gold room', 0.015)}
            {P('lounge', 'lounge.jpg', 'The red lounge', 'the Red Room', -0.03)}
            {P('beauty', 'beauty.jpg', 'The white beauty hall', 'upstairs, all cream', 0.025)}
            {C('door', 'cut-door.png', 0.04)}
            {C('lamp', 'cut-lamp.png', -0.04)}
            {C('pedestal', 'cut-beauty.png', 0.03)}
            <div class="lyr msg p1 hand" data-speed="0.01">Paris, inside<br>an Art Deco tower</div>
            <div class="lyr msg p2 hand" data-speed="0.02">look up</div>
          </div>
          {cap_html}
        </div>'''

def ippudo_scene(slug_h, cap_html):
    M = CDN + 'shared/ippudo/'
    P = lambda cls, src, alt, cap='', sp=0.02: f'<figure class="lyr print {cls}" data-speed="{sp}"><div class="tape"></div><img src="{M}{src}" alt="{alt}" loading="lazy">' + (f'<figcaption class="hand">{cap}</figcaption>' if cap else '') + '</figure>'
    C = lambda cls, src, sp: f'<img class="lyr {cls}" data-speed="{sp}" src="{M}{src}" alt="" loading="lazy">'
    return f'''
        <div class="scene-col">
          <div class="iscene reveal">
            {P('room1', 'room1.jpg', 'The bamboo-canopy dining room', 'under the bamboo', 0.015)}
            {P('store', 'store.jpg', 'Ippudo storefront', 'the front door', -0.03)}
            {P('room2', 'room2.jpg', 'The long communal tables', '', 0.025)}
            {C('bowl1', 'cut-bowl-black.png', 0.045)}
            {C('bowl2', 'cut-bowl-red.png', -0.04)}
            <div class="lyr msg i1 hand" data-speed="0.01">steam, noodles,<br>a counter seat</div>
            <div class="lyr msg i2 hand" data-speed="0.02">the cozy beat<br>of the day</div>
          </div>
          {cap_html}
        </div>'''

def rz_scene(slug_h, cap_html):
    M = CDN + 'shared/rz/'
    return f'''
        <div class="scene-col">
          <div class="zscene reveal">
            <figure class="lyr print store" data-speed="0.015"><div class="tape"></div><img src="{M}store.jpg" alt="Rhythm Zero storefront" loading="lazy"><figcaption class="hand">art-gallery café</figcaption></figure>
            <img class="lyr cup" data-speed="0.04" src="{M}cut-cup.png" alt="" loading="lazy">
            <div class="lyr msg z1 hand" data-speed="0.01">blueberry matcha,<br>pink on the bottom</div>
            <div class="lyr msg z2 hand" data-speed="0.02">sit, sip, people-watch</div>
          </div>
          {cap_html}
        </div>'''

def rok_nyc_scene(slug_h, cap_html):
    M = CDN + 'shared/rok/'
    return f'''
        <div class="scene-col">
          <div class="rscene nyc reveal">
            <img class="lyr cup" data-speed="0.04" src="{M}cut-cup.png" alt="" loading="lazy">
            <div class="lyr msg r1 hand" data-speed="0.01">watch the whisk<br>drip</div>
            <div class="lyr msg r2 hand" data-speed="0.02">matcha crawl, cup three</div>
          </div>
          {cap_html}
        </div>'''

def rok_scene(slug_h, cap_html):
    M = CDN + 'shared/rok/'
    P = lambda cls, src, alt, cap='', sp=0.02: f'<figure class="lyr print {cls}" data-speed="{sp}"><div class="tape"></div><img src="{M}{src}" alt="{alt}" loading="lazy">' + (f'<figcaption class="hand">{cap}</figcaption>' if cap else '') + '</figure>'
    C = lambda cls, src, sp: f'<img class="lyr {cls}" data-speed="{sp}" src="{M}{src}" alt="" loading="lazy">'
    return f'''
        <div class="scene-col">
          <div class="rscene reveal">
            {P('store', 'store.jpg', 'Rok Coffee and Tea storefront', 'Koreatown, 3060 W Olympic', 0.015)}
            {C('cup', 'cut-cup.png', 0.04)}
            {C('door', 'cut-door.png', -0.035)}
            <div class="lyr msg r1 hand" data-speed="0.01">watch the whisk<br>drip</div>
            <div class="lyr msg r2 hand" data-speed="0.02">a matcha detour<br>in Koreatown</div>
            <svg class="lyr dd a1" viewBox="0 0 140 70" data-speed="0.01"><use href="#d-arrow"/></svg>
          </div>
          {cap_html}
        </div>'''

def matcha12_scene(slug_h, cap_html):
    M = CDN + 'shared/matcha12/'
    P = lambda cls, src, alt, cap='', sp=0.02: f'<figure class="lyr print {cls}" data-speed="{sp}"><div class="tape"></div><img src="{M}{src}" alt="{alt}" loading="lazy">' + (f'<figcaption class="hand">{cap}</figcaption>' if cap else '') + '</figure>'
    C = lambda cls, src, sp: f'<img class="lyr {cls}" data-speed="{sp}" src="{M}{src}" alt="" loading="lazy">'
    return f'''
        <div class="scene-col">
          <div class="tscene reveal">
            {P('bar', 'bar.jpg', 'The matcha bar and menu wall', 'the menu wall', 0.015)}
            {P('room', 'room.jpg', 'A sunny room with tall windows', 'grab a window seat', -0.03)}
            {C('cup', 'cut-cup.png', 0.04)}
            {C('cups', 'cut-cups.png', -0.035)}
            {C('jars', 'cut-jars.png', 0.03)}
            <div class="lyr msg t1 hand" data-speed="0.01">green on green</div>
            <div class="lyr msg t2 hand" data-speed="0.02">order the one<br>with the 12 on it</div>
            <svg class="lyr dd a1" viewBox="0 0 140 70" data-speed="0.01"><use href="#d-arrow"/></svg>
          </div>
          {cap_html}
        </div>'''

def mercer_scene(slug_h, cap_html):
    M = CDN + 'shared/mercer/'
    P = lambda cls, src, alt, cap='', sp=0.02: f'<figure class="lyr print {cls}" data-speed="{sp}"><div class="tape"></div><img src="{M}{src}" alt="{alt}" loading="lazy">' + (f'<figcaption class="hand">{cap}</figcaption>' if cap else '') + '</figure>'
    C = lambda cls, src, sp: f'<img class="lyr {cls}" data-speed="{sp}" src="{M}{src}" alt="" loading="lazy">'
    return f'''
        <div class="scene-col">
          <div class="mlscene reveal">
            {P('room', 'room.jpg', 'A room of projected flowers', 'step inside the garden', 0.015)}
            {P('cave', 'cave.jpg', 'A tunnel of flowers', '', -0.03)}
            {P('robot', 'robot.jpg', 'A robotic instrument in a glowing room', '', 0.025)}
            {C('ext', 'cut-exterior.png', 0.04)}
            {C('neon', 'cut-neon.png', -0.04)}
            {C('tun', 'cut-tunnel.png', 0.03)}
            <div class="lyr msg l1 hand" data-speed="0.01">a museum you<br>can step inside</div>
            <div class="lyr msg l2 hand" data-speed="0.02">bring a friend,<br>stay a while</div>
            <svg class="lyr dd a1" viewBox="0 0 140 70" data-speed="0.01"><use href="#d-arrow"/></svg>
          </div>
          {cap_html}
        </div>'''

def gm_scene(slug_h, cap_html):
    M = CDN + 'shared/gm/'
    P = lambda cls, src, alt, cap='', sp=0.02: f'<figure class="lyr print {cls}" data-speed="{sp}"><div class="tape"></div><img src="{M}{src}" alt="{alt}" loading="lazy">' + (f'<figcaption class="hand">{cap}</figcaption>' if cap else '') + '</figure>'
    C = lambda cls, src, sp: f'<img class="lyr {cls}" data-speed="{sp}" src="{M}{src}" alt="" loading="lazy">'
    return f'''
        <div class="scene-col">
          <div class="gscene reveal">
            {P('shop', 'shop.jpg', 'Mirrored eyewear gallery', '', 0.015)}
            {P('door', 'door.jpg', 'Looking through the store entrance', '', -0.03)}
            {P('coral', 'coral.jpg', 'A woven sculpture installation', 'a whole new installation', 0.025)}
            {P('bison', 'bison.jpg', 'White bison installation', '', -0.02)}
            {C('faces', 'cut-faces.png', 0.045)}
            <div class="lyr msg g1 hand" data-speed="0.01">shopping that feels<br>like a gallery</div>
            <div class="lyr msg g2 hand" data-speed="0.02">art you can<br>walk right past</div>
            <svg class="lyr dd a1" viewBox="0 0 140 70" data-speed="0.01"><use href="#d-arrow"/></svg>
          </div>
          {cap_html}
        </div>'''

def flower_scene(slug_h, cap_html):
    M = CDN + 'shared/cj/'
    P = lambda cls, src, alt, cap='', sp=0.02: f'<figure class="lyr print {cls}" data-speed="{sp}"><div class="tape"></div><img src="{M}{src}" alt="{alt}" loading="lazy">' + (f'<figcaption class="hand">{cap}</figcaption>' if cap else '') + '</figure>'
    C = lambda cls, src, sp: f'<img class="lyr {cls}" data-speed="{sp}" src="{M}{src}" alt="" loading="lazy">'
    return f'''
        <div class="scene-col">
          <div class="fscene reveal">
            {P('tent', 'tent.jpg', 'Rows of flowers under a white tent', '', 0.015)}
            {P('tiers', 'tiers.jpg', 'Flowers stacked in tiers', 'every color, stacked', -0.03)}
            {P('close', 'close.jpg', 'A close-up of velvet flowers', '', 0.03)}
            {C('bq1', 'cut-bouquet-plush.png', 0.045)}
            {C('bq2', 'cut-bouquet-hand.png', -0.04)}
            <div class="lyr msg f1 hand" data-speed="0.01">rows and rows<br>of blooms</div>
            <div class="lyr msg f2 hand" data-speed="0.02">pick your own<br>bouquet</div>
            <svg class="lyr dd a1" viewBox="0 0 140 70" data-speed="0.01"><use href="#d-arrow"/></svg>
          </div>
          {cap_html}
        </div>'''

def chelsea_scene(slug_h, cap_html):
    M = CDN + slug_h + '/chelsea/'
    P = lambda cls, src, alt, cap='', sp=0.02: f'<figure class="lyr print {cls}" data-speed="{sp}"><div class="tape"></div><img src="{M}{src}" alt="{alt}" loading="lazy">' + (f'<figcaption class="hand">{cap}</figcaption>' if cap else '') + '</figure>'
    C = lambda cls, src, sp: f'<img class="lyr {cls}" data-speed="{sp}" src="{M}{src}" alt="" loading="lazy">'
    return f'''
        <div class="scene-col">
          <div class="cscene reveal">
            {P('ext', 'ext.jpg', 'A gallery entrance under the High Line', 'under the High Line', 0.015)}
            {P('night', 'night.jpg', 'The High Line at blue hour', 'High Line, blue hour', -0.03)}
            {P('eve', 'eve.jpg', 'Dinner under the High Line stairs', 'dinner nearby', 0.03)}
            {P('branches', 'branches.jpg', 'A gallery of hanging sculptures', '', 0.02)}
            {P('paint', 'paint.jpg', 'Paintings in a gallery', '', -0.02)}
            {P('kawsroom', 'kaws.jpg', 'A big gallery with a yellow figure', '', 0.025)}
            {C('koons', 'cut-koons.png', 0.045)}
            {C('kaws', 'cut-kaws.png', -0.04)}
            <div class="lyr msg c1 hand" data-speed="0.01">one gallery<br>per hour</div>
            <div class="lyr msg c2 hand" data-speed="0.02">art you can<br>walk right into</div>
            <div class="lyr msg c3 hand" data-speed="0.02">then the High Line<br>at golden hour &rarr;</div>
          </div>
          {cap_html}
        </div>'''

def madison_scene(slug_h, cap_html):
    M = CDN + slug_h + '/madison/'
    L = lambda cls, src, speed, extra='': f'<img class="lyr {cls}" data-speed="{speed}" src="{M}{src}" alt="" loading="lazy" {extra}>'
    return f'''
        <div class="scene-col">
          <div class="mscene reveal">
            <figure class="lyr print wide" data-speed="0.015"><div class="tape"></div><img src="{M}wide.jpg" alt="Madison Square Park from above" loading="lazy"></figure>
            {L('tree tl', 'cut-tree-left.png', -0.02)}
            {L('tower', 'cut-tower.png', 0.035)}
            <figure class="lyr print tall" data-speed="-0.025"><div class="tape"></div><img src="{M}tall.jpg" alt="The fountain, sun through the trees" loading="lazy"><figcaption class="hand">sun through the trees</figcaption></figure>
            {L('fount', 'cut-fountain.png', 0.045)}
            {L('tree tr', 'cut-tree-right.png', -0.03)}
            {L('circ', 'cut-circle.png', 0.02)}
            <div class="lyr msg m1 hand" data-speed="0.01">coffee on a green bench,<br>fountain in the corner of my eye</div>
            <div class="lyr msg m2 hand" data-speed="0.02">&uarr; the Flatiron,<br>a few blocks away</div>
            <div class="lyr msg m3 hand" data-speed="0.02">golden hour = best light</div>
            <svg class="lyr dd a1" viewBox="0 0 140 70" data-speed="0.01"><use href="#d-arrow"/></svg>
            <svg class="lyr dd a2" viewBox="0 0 140 70" data-speed="0.01"><use href="#d-arrow"/></svg>
            <svg class="lyr dd u1" viewBox="0 0 300 14" data-speed="0"><use href="#d-under"/></svg>
          </div>
          {cap_html}
        </div>'''

LAYOUTS = ['', 'L-side', 'L-center', 'L-hero', 'L-mason']

def render(h):
    S = STORY[h['slug']]; c = h['c']; slug_h = h['slug']
    dark = slug_h == 'nomad'
    css = (CSS.replace('%%BG%%', c['desk'] if dark else c['paper']).replace('%%TXT%%', '#f3ead6' if dark else c['ink'])
              .replace('%%PAPER%%', c['paper']).replace('%%INK%%', c['ink']).replace('%%ACCENT%%', c['accent'])
              .replace('%%ACCENT2%%', c['accent2']).replace('%%SOFT%%', c['soft'] if not dark else '#1d2547')
              .replace('%%HEAD%%', h['head']).replace('%%BODY%%', h['body']).replace('%%DESK%%', c['desk']).replace('%%PEN%%', '#efe5cc' if dark else '#1d2a4a').replace('%%RED%%', '#ff8a7a' if dark else '#b3362b').replace('%%PAPER_TEX%%', paper_tex(dark)).replace('%%MUTE%%', '#2b3048' if dark else '#d8d0bf').replace('%%PHC%%', 'rgba(240,234,214,.7)' if dark else 'rgba(28,34,51,.55)'))
    clips = ['c1', 'c2', 'c3', 'c4']
    chapters = ''
    allstops = []
    k = 0
    off = 0
    if 'walk' in S:
        off = 1
        W = S['walk']
        sc = W['scenes']
        chapters += f'''
  <section class="chapter walkintro" id="ch1" data-label="{esc(W['kick'])}">
    <div class="wrap">
      <div class="num">{tm(slug_h,0)}</div>
      <div class="ch-head">
        <div class="rise"><div class="kick">{esc(W['kick'])}</div><h2>{esc(W['title'])}</h2><svg class="dd under" viewBox="0 0 300 14"><use href="#d-under"/></svg></div>
        <div class="note rise"><div class="tape"></div>{esc(W['story'])}<svg class="dd pt" viewBox="0 0 140 70"><use href="#d-arrow"/></svg></div>
      </div>
    </div>
  </section>
  <section class="walkthru" data-label="{esc(W['kick'])}">
    <div class="stick">
      <div class="scene s1"><img src="{CDN}{slug_h}/walk-lobby.jpg" alt="The lobby lounge"></div>
      <div class="scene s2"><div class="blur" style="background-image:url({CDN}{slug_h}/walk-bar.jpg)"></div><img src="{CDN}{slug_h}/walk-bar.jpg" alt="The bar"></div>
      <div class="scene s3"><div class="frame"><img src="{CDN}{slug_h}/walk-room.jpg" alt="The room view at dusk"></div></div>
      <div class="vig"></div>
      <div class="wcaps">
        <div class="wcap w1"><span class="hand">{esc(sc[0][1])}</span><p>{esc(sc[0][2])}</p></div>
        <div class="wcap w2"><span class="hand">{esc(sc[1][1])}</span><p>{esc(sc[1][2])}</p></div>
        <div class="wcap w3"><span class="hand">{esc(sc[2][1])}</span><p>{esc(sc[2][2])}</p></div>
      </div>
      <div class="floors"><span class="f f1">{esc(sc[0][0])}</span><span class="f f2">{esc(sc[1][0])}</span><span class="f f3">{esc(sc[2][0])}</span><i></i></div>
    </div>
  </section>'''
        allstops += [('Lobby and lounge','here','',False,'walk-lobby'),('The bar','here','',False,'walk-bar'),('Room view at dusk','here','',False,'walk-room')]
    for i, (kick, title, story, stops) in enumerate(S['chapters']):
        n = len(stops)
        frames = ''
        for j, (name, tag, note, confirm) in enumerate(stops):
            key = slug(name); allstops.append((name, tag, note, confirm, key))
            label, cls = TAGS[tag]
            stamp = '<span class="stamp">confirm</span>' if confirm else ''
            rot = [-.7, .5, -.3, .8][(i + j) % 4]
            speed = [0.025, -0.02, 0.03, -0.025][(i + j) % 4]
            _before = len(frames)
            frames += f'''
        <figure class="cut reveal {clips[(i + j) % 4]} g{(i + j) % 4}" style="--r:{rot}deg" data-speed="{speed}">
          <div class="tape"></div>
          <div class="img"><span class="ph">{esc(name)}</span><img src="{CDN}{slug_h}/{key}.jpg" alt="{esc(name)}" loading="lazy" onerror="this.remove()"></div>
          <figcaption class="cap"><span class="nm">{esc(name)}</span><span class="row"><span class="tg {cls}">{label}</span>{stamp}</span><span class="nt"><svg class="dd up" viewBox="0 0 40 30"><use href="#d-up"/></svg>{esc(note)}</span></figcaption>{snaps(slug_h, key)}
        </figure>'''
            if key == 'printemps-one-wall-street':
                cap = re.search(r'<figcaption.*?</figcaption>', frames[_before:], re.S).group(0)
                frames = frames[:_before] + printemps_scene(slug_h, cap)
            if key == 'ippudo':
                cap = re.search(r'<figcaption.*?</figcaption>', frames[_before:], re.S).group(0)
                frames = frames[:_before] + ippudo_scene(slug_h, cap)
            if key == 'rhythm-zero':
                cap = re.search(r'<figcaption.*?</figcaption>', frames[_before:], re.S).group(0)
                frames = frames[:_before] + rz_scene(slug_h, cap)
            if key == 'rok-matcha':
                cap = re.search(r'<figcaption.*?</figcaption>', frames[_before:], re.S).group(0)
                frames = frames[:_before] + rok_nyc_scene(slug_h, cap)
            if key == 'rok-matcha-koreatown':
                cap = re.search(r'<figcaption.*?</figcaption>', frames[_before:], re.S).group(0)
                frames = frames[:_before] + rok_scene(slug_h, cap)
            if key == '12-matcha':
                cap = re.search(r'<figcaption.*?</figcaption>', frames[_before:], re.S).group(0)
                frames = frames[:_before] + matcha12_scene(slug_h, cap)
            if key == 'mercer-labs':
                cap = re.search(r'<figcaption.*?</figcaption>', frames[_before:], re.S).group(0)
                frames = frames[:_before] + mercer_scene(slug_h, cap)
            if key == 'gentle-monster-soho':
                cap = re.search(r'<figcaption.*?</figcaption>', frames[_before:], re.S).group(0)
                frames = frames[:_before] + gm_scene(slug_h, cap)
            if key == 'cj-hendry-flower-market':
                cap = re.search(r'<figcaption.*?</figcaption>', frames[_before:], re.S).group(0)
                frames = frames[:_before] + flower_scene(slug_h, cap)
            if slug_h == 'nomad' and key == 'chelsea-galleries-and-the-start-of-the-high-line':
                cap = re.search(r'<figcaption.*?</figcaption>', frames[_before:], re.S).group(0)
                frames = frames[:_before] + chelsea_scene(slug_h, cap)
            if slug_h == 'nomad' and key == 'madison-square-park-and-flatiron':
                cap = re.search(r'<figcaption.*?</figcaption>', frames[_before:], re.S).group(0)
                frames = frames[:_before] + madison_scene(slug_h, cap)
        k += 1
        chapters += f'''
  <section class="chapter {LAYOUTS[(i + off) % 5]}" id="ch{i+1+off}" data-label="{esc(kick)}">
    <div class="wrap">
      <div class="num">{tm(slug_h,i+off)}</div>
      <div class="ch-head">
        <div class="rise"><div class="kick">{esc(kick)}</div><h2>{esc(title)}</h2><svg class="dd under" viewBox="0 0 300 14"><use href="#d-under"/></svg></div>
        <div class="note rise"><div class="tape"></div>{esc(story)}<svg class="dd pt" viewBox="0 0 140 70"><use href="#d-arrow"/></svg></div>
      </div>
      <div class="collage n{min(n,4)} {'rev' if i % 2 else ''}">{frames}
      </div>
      <img class="cutout" src="{CDN}{slug_h}/ch{i+1+off}-cutout.png" alt="" onerror="this.remove()">
    </div>
  </section>'''
    walk = [s for s in allstops if s[1] in ('here', 'walk')]
    far = [s for s in allstops if s[1] in ('ride', 'trip')]
    li = lambda arr: ''.join(f'<li>{esc(s[0])}{" <em>(confirm)</em>" if s[3] else ""}</li>' for s in arr)
    ticker = ' '.join(f'<span>{esc(s[0])}</span>' for s in allstops)
    facts = ''.join(f'<li>{esc(f)}</li>' for f in h['facts'])
    chips = ''.join(f'<span class="chip"><i></i>{esc(v)}</span>' for v in h['vibe'])
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="robots" content="noindex">
<title>Pitch: {esc(h['short'])}</title>
<link href="https://fonts.googleapis.com/css2?family={h['fonts']}&display=swap" rel="stylesheet">
<style>{css}</style>
</head>
<body>
{DOODLES}
<div class="hud"><a href="pitches.html">&larr; All pitches</a><span class="cur">Intro</span><span class="bar"></span></div>

<header class="cover">
  <img class="bg" src="{CDN}{slug_h}-hero.jpg" alt="" onerror="this.remove()">
  <figure class="cut float a c1 g0" style="--r:2deg" data-speed="0.04"><div class="img" style="--ar:4/5"><span class="ph"></span><img src="{CDN}{slug_h}/cover-1.jpg" alt="" onerror="this.remove()"></div></figure>
  <figure class="cut float b c2 g1" style="--r:-2deg" data-speed="-0.03"><div class="img" style="--ar:1/1"><span class="ph"></span><img src="{CDN}{slug_h}/cover-2.jpg" alt="" onerror="this.remove()"></div></figure>
  <figure class="cut float c c3 g2" style="--r:1deg" data-speed="0.02"><div class="img" style="--ar:3/4"><span class="ph"></span><img src="{CDN}{slug_h}/cover-3.jpg" alt="" onerror="this.remove()"></div></figure>
  <div class="in">
    <div class="kick">Pitch {h['no']} &middot; {esc(h['city'])}</div>
    <h1>{esc(h['name'])}</h1>
    <p class="tag">{esc(h['tagline'])}</p>
    <div class="hand">&mdash; {esc(h['hand'])}</div>
    <div class="scroll">Scroll the story &darr;</div>
  </div>
</header>

<section class="intro rise"><div class="kick">The trip</div><p>{esc(S['intro'])}</p></section>
<div class="index"><div class="kick">In this guide</div><p>{ticker}</p></div>
{chapters}

<section class="about">
  <div class="rise"><div class="kick">Why this stay</div><h2>The feeling I'd film</h2><p>{esc(h['why'])}</p><div class="chips">{chips}</div></div>
  <div class="rise"><div class="kick">What it's known for</div><ul class="clean">{facts}</ul></div>
</section>
<section class="lists">
  <div class="rise"><div class="kick">Walkable from the hotel</div><h3>Out the door</h3><ul class="clean">{li(walk)}</ul></div>
  <div class="rise"><div class="kick">Worth the ride</div><h3>A little farther</h3><ul class="clean">{li(far)}</ul></div>
</section>

<section class="end">
  <div class="kick">Let's make it real</div>
  <h2 class="rise">Come with me, and I'll bring you the whole story.</h2>
  <div class="hand">Reels, photos, and a guide like this one.</div>
  <a class="btn" href="contact.html">Say hello</a>
</section>
<div class="fine">Draft pitch for {esc(h['short'])}. Not affiliated with or endorsed by the hotel. Stops marked "confirm" still need checking.</div>
{gp.BRIDGE}
{JS}
</body>
</html>
'''

def stops_md():
    out = ['# Photo slots for the pitch stories', '',
           'Drop a JPG at each path below (under `site/media/pitches/`). Until a file exists the page shows a designed placeholder.',
           'Optional: `<hotel>/ch<N>-cutout.png` is a transparent PNG that floats beside chapter N.', '']
    for h in gp.HOTELS:
        out += [f"## {h['short']}  (`{h['slug']}`)", '', f"- `{h['slug']}-hero.jpg` (full-bleed cover background)",
                f"- `{h['slug']}/cover-1.jpg`, `cover-2.jpg`, `cover-3.jpg` (floating cover cut-outs)"]
        for kick, title, story, stops in STORY[h['slug']]['chapters']:
            for s in stops:
                out.append(f"- `{h['slug']}/{slug(s[0])}.jpg`: {s[0]}")
        out.append('')
    return '\n'.join(out)

if __name__ == '__main__':
    for h in gp.HOTELS:
        with open(os.path.join(ROOT, f"pitch-{h['slug']}.html"), 'w', encoding='utf-8') as f: f.write(render(h))
    with open(os.path.join(ROOT, 'pitches.html'), 'w', encoding='utf-8') as f: f.write(gp.hub())
    os.makedirs(os.path.join(ROOT, 'media', 'pitches'), exist_ok=True)
    with open(os.path.join(ROOT, 'media', 'pitches', 'STOPS.md'), 'w', encoding='utf-8') as f: f.write(stops_md())
    print('wrote', len(gp.HOTELS), 'story pages + hub')
