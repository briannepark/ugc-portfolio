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
 'nomad': ['4:00 pm','5:30 pm','8:30 pm','7:00 am','9:30 am','12:00 pm','2:30 pm','4:30 pm','7:00 pm','8:00 am','10:00 am','1:30 pm','8:00 am','1:00 pm','6:30 pm'],
 'brooklyn': ['8:00 am','10:30 am','2:00 pm','12:30 pm','1:00 pm','6:00 pm','10:00 am','1:30 pm'],
 'maui': ['12:30 pm','6:00 pm','9:30 am','1:30 pm','3:00 pm','9:30 am','11:30 am'],
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
  intro="Picture a trip that feels like yours again: a skyline room, a spa afternoon, the pop-ups you usually miss, and everything baby and the dog need handled, comfortably. This is the long weekend I'd take other moms on, one stop at a time.",
  chapters=[
   ('Day 1 · Settle in','Sleep like you mean it',"I travel with my baby and my dog, so the hotel has to work for all three of us. This is the part of the trip I'd film first: a quiet room, a long nap while the city hums far below, and a soak at the end of the day.",
    [('The bed and the quiet','here','Oversize windows, high above the street. Nap time and bedtime, on the clock. Ask about the bedding and a crib.',True),('Bath time, mom and baby','here','Diptyque bath products and a separate rain shower, with a deep soaking tub in select rooms. Request a tub room: a warm bath for baby, then a long one for me.',True),('Family perks','here','Ritz Kids activities are listed on the hotel site, and adjoining rooms may be possible. Ask what is offered for babies and toddlers.',True),('Dogs welcome','here','Up to two pets, 60 lbs combined, with a per-stay fee (reported anywhere from $250 to $375, so confirm). Bowls are provided in the room.',True)]),
   ('Day 1 · Nightfall','Fifty floors up',"Dinner at the hotel turns into a nightcap, and the nightcap turns into the best view of the trip. Blue hour, every light in Midtown below.",
    [('Bazaar Meat by José Andrés','here','Velvet booths, feather chandeliers, dinner at the hotel.',False),('Nubeluz, 50th floor','here','Skyline at blue hour.',False)]),
   ('Day 2 · Early morning','Gym before the city wakes',"While baby sleeps in, I slip down to the fitness center. It is open around the clock, with Peloton bikes, right next to the spa. Then a matcha to go, and out for the morning stroll.",
    [('Fitness center','here','Open 24 hours, with Peloton bikes. Confirm hours and any age rules.',True)]),
   ('Day 2 · Morning','Madison Square Park, at stroller pace',"First morning, nice and easy: a few blocks from the lobby to Madison Square Park with baby in the stroller and the pup on a leash. Coffee in hand, one slow loop of the lawn, the Flatiron in the frame.",
    [('Madison Square Park and Flatiron','walk','A short, flat stroll with baby and pup. Leashed dogs only; the park also has a dog run. Confirm rules and hours.',True),('Cha Cha Matcha, NoMad','walk','1158 Broadway, about two blocks from the lobby: a matcha to go before the park. Cash is not accepted. Confirm hours.',True),('Matchaful, Flatiron','walk','337 Park Ave South, on the far side of the park. A newer cafe with Japanese matcha. Confirm hours.',True)]),
   ('Day 2 · Afternoon','Petals and frames',"SoHo, but make it dreamy, and doable with a stroller: the trendy shops and pop-ups I usually skip, with an easy ride back for naps. A shop of soft, handmade flowers, a pair of Gentle Monster frames, a sample sale that's gone by Monday, and a pop-up only the locals know about.",
    [('CJ Hendry Flower Market','ride','The plush-flower shop at 172 Prince St. Pick a bloom for $10.',False),('Gentle Monster, SoHo','ride','Installation-style retail.',True),('Kith, SoHo','ride','The all-white sneaker wall and a tiled flagship. Confirm which store and hours.',True),('Sample-sale hunt','ride','Check the 260 Sample Sale list the week you go.',True),('Pop-up of the week','ride','Pop-ups rotate weekly. The kind I usually miss with a baby in tow. Pick one for the feed.',True)]),
   ('Day 2 · The matcha crawl','Three cups, three moods',"A line down the block for the matcha everyone talks about, a café that doubles as an art gallery, and one more cup to compare. This is the matcha chapter.",
    [('12 Matcha','ride','54 Bond St, NoHo. Ceremonial-grade, long line, famous basque cheesecake.',False),('Rhythm Zero','ride','An art-gallery café with a West Village location. Seasonal matcha drinks.',False),('Rok Matcha','ride','Rōk Matcha in New York. Confirm the exact address and hours before we plan around it.',True)]),
   ('Day 2 · Rest hour','Back by four, for a reset',"After a big day out, we're back at the hotel. Baby naps, I take a long bath, and the dog gets a quiet corner. Rest is part of the itinerary, and it makes the evening better.",
    [('Nap and soak','here','The room at its calmest, afternoon light across the skyline.',False),('Spa and steam room','here','A 6,800 sq ft spa with a sauna and steam room. Confirm treatments and age rules.',True)]),
   ('Day 2 · Evening','A bowl worth the ride',"Steam, noodles, a counter seat. Ramen is the cozy beat between the shopping and the next day.",
    [('Ippudo','ride','Hakata-style ramen under a canopy of bamboo. Confirm which location (the storefront photo is #24) and wait times.',True)]),
   ('Day 3 · Early morning','Chelsea gallery streets, pup in tow',"Second morning, west side: the tree-lined blocks of the Chelsea galleries, all at street level so baby and the pup can both come. The High Line runs overhead, and we'll admire it from below (dogs aren't allowed up there, except service dogs). Grab a matcha at Cha Cha Matcha (1158 Broadway) on the way out.",
    [('Chelsea gallery streets','walk','Window-shop the galleries on the W 20s blocks, leashed pup and stroller along. Many galleries may not allow dogs inside, so confirm before going in.',True)]),
   ('Day 3 · Morning','The secret garden',"The city drops away: cherry blossoms in spring, a Japanese hill-and-pond garden, and roses in early summer. This is the quiet chapter.",
    [('Brooklyn Botanical Garden','ride','990 Washington Ave, Prospect Heights. Cherry blossoms in spring, roses in early summer, the Japanese garden and the conservatory year-round. Confirm hours and tickets.',True)]),
   ('Day 3 · Afternoon','Downtown, in one sweep',"Three very different worlds within reach of each other: an immersive art museum, a Parisian department store inside a landmark, and a Chinatown shop where you can get your aura photographed.",
    [('Mercer Labs','ride','21 Dey St. Fifteen immersive rooms; plan 60 to 90 minutes and book ahead.',False),('Printemps, One Wall Street','ride','Café, cocktail bars, and the landmarked Red Room with its mosaics.',False),('Aura reading at Magic Jewelry','ride','238 Canal St, Chinatown. Aura photographs.',False)]),
   ('Day 4 · Early morning','Along the Hudson, one last stroll',"Last morning, flat and unhurried: the riverside greenway on the west edge of the city. Water on one side, the stroller rolls easily, and leashed pups are generally welcome in Hudson River Park.",
    [('Hudson River Greenway','walk','A flat, car-free waterfront path. Confirm dog rules and any dog run hours.',True),('Matchaful, Manhattan West','walk','450 W 33rd St, inside Whole Foods (entrance on 10th Ave). Open 8 am to 7 pm per the building site. A matcha stop on the way toward the river.',True)]),
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
    [('CJ Hendry Flower Market','ride','The plush-flower shop at 172 Prince St. Pick a bloom for $10.',False),('Gentle Monster, SoHo','ride','Cross the bridge for a design stop.',True),('Kith, SoHo','ride','The all-white sneaker wall and a tiled flagship. Confirm which store and hours.',True),('12 Matcha','ride','54 Bond St, NoHo. Ceremonial-grade, long line.',False)]),
   ('Day 2 · Evening','Art-gallery coffee and ramen',"A café that doubles as an art space in Williamsburg, then ramen and a scoop by the water on the way home.",
    [('Rhythm Zero','ride','An art-gallery café with locations in Williamsburg and Greenpoint.',False),('Rok Matcha','ride','Rōk Matcha in New York. Confirm the exact address and hours before we plan around it.',True),('Ippudo','ride','Hakata-style ramen under a canopy of bamboo. Confirm which location and wait times.',True),('Ice cream by the water','ride','A scoop at golden hour.',True)]),
   ('Day 3 · Morning','The secret garden',"The city drops away: cherry blossoms in spring, a Japanese hill-and-pond garden, and roses in early summer.",
    [('Brooklyn Botanical Garden','ride','990 Washington Ave, Prospect Heights. Cherry blossoms in spring, roses in early summer, the Japanese garden and the conservatory year-round. Confirm hours and tickets.',True)]),
   ('Day 3 · Afternoon','Lower Manhattan, in one sweep',"An immersive art museum, a Parisian department store inside a landmark, and a Chinatown shop where you can get your aura photographed. All a short ride across the bridge.",
    [('Mercer Labs','ride','21 Dey St. Fifteen immersive rooms; plan 60 to 90 minutes and book ahead.',False),('Printemps, One Wall Street','ride','Café, cocktail bars, and the landmarked Red Room with its mosaics.',False),('Aura reading at Magic Jewelry','ride','238 Canal St, Chinatown. Aura photographs.',False)]),
  ]),
'maui': dict(
  intro="This is a quick staycation, kept small and kept local. Two nights, a quiet hotel by the water, sunset on Haleakalā, a day in Lahaina as it rebuilds, and good food from the people who live here. Many in Hawaiʻi are weary of tourism that takes more than it gives, so the plan is to take little and spend close to home.",
  chapters=[
   ('Day 1 · Arrival','A short hop, a local plate',"From the airport, the first stops are in Kahului and Wailuku, before the resort. A plate of Hawaiian food, and a gift from a shop that sells ʻōiwi-made goods.",
    [('Poi By The Pound, Kahului','ride','Hawaiian food with locally sourced ingredients. Listed by OHA as Native Hawaiian-owned in 2020; confirm.',True),('Native Intelligence, Wailuku','ride','Fresh lei, ʻōiwi products and gifts. Also on the OHA list; confirm.',True),('Wailea Beach','walk','Shallow and sandy right at the resort, with complimentary beach chairs.',False),('Keiki Pool','here','A waterfall, a slide and pool toys, built for little ones.',False)]),
   ('Day 1 · Evening','Fish from the island',"Dinner is fish that came out of Hawaiian waters, then a slow walk back to the water.",
    [('South Maui Fish Co, Kihei','ride','Fresh fish, poke and fish tacos, described as family-owned and using Hawaiʻi-caught fish. Confirm hours.',True),('Lobby Lounge sunset hula','here','Cocktails and small plates, with a nightly sunset hula show.',True)]),
   ('Day 2 · Morning','Makawao and the makers',"A short drive up the slope of Haleakalā is cooler air and small shops. The point is to meet the people behind the things I would bring home.",
    [("Hui Noʻeau Visual Arts Center",'ride','An art center and gallery on a historic estate in Makawao.',True),('Holoholo Surf and Kūlua, Makawao','ride','Both listed by OHA as Native Hawaiian-owned in 2020; confirm they are still open and who owns them.',True),('Makawao town','ride','Small galleries and boutiques on the main street.',True)]),
   ('Day 2 · Rest hour','Nap before the mountain',"Back at the resort for the part of the day that makes the evening work. Baby naps, I rest, and the car is packed for the cold.",
    [('The quiet room','here','Ask for a room away from the pool for naps.',True),('Pack for the summit','here','Warm layers for everyone, a blanket, and all food, water and gas. Nothing is sold in the park.',False)]),
   ('Day 2 · Sunset','Sunset on Haleakalā',"This is why I want to come to Maui. Above the clouds, the whole sky turns, and the island goes quiet. It is a sacred place, so I would arrive early, stay on the paths, and leave no trace.",
    [('Haleakalā sunset','trip','No reservation is needed for sunset, but cars can be turned around when the park is full. Arrive 2 to 3 hours early (3 in winter). Sunset runs from about 5:47 pm in early December to 7:16 pm in early July.',True),('Haleakalā Visitor Center','trip','One place to watch from, and parking fills up. Have a backup viewing spot.',True)]),
   ('Day 3 · Lahaina','Lahaina, rebuilding',"Lahaina is still healing. Front Street reopened to vehicles on August 1, 2026, and the town is asking visitors to come gently: stay out of fenced areas and active rebuild sites, do not photograph residents' homes, and spend at the places that have reopened.",
    [('Front Street, Lahaina','trip','Reopened to vehicles between Pāpalaua and Shaw streets on August 1, 2026. Some nearby streets are still closed.',True),('ʻUlu o Lele Marketplace','trip','A new marketplace that was getting ready to open with Front Street. Confirm what is open.',True),('Aloha Mixed Plate, Lahaina','trip','A local plate lunch, listed as open on a recent Lahaina guide.',True),('Star Noodle, Lahaina','trip','Another reopened restaurant on the same list.',True)]),
   ('Day 3 · Boat to bowl','From the water to the plate',"A morning on the water with a local captain, then the freshest poke on the island.",
    [('Fishing with a local captain','trip','Ask who owns the boat, whether a baby is welcome aboard, and book early.',True),('Only Fresh Poke, Olowalu','trip','A food trailer partnered with local fishermen, with no middlemen. Open Wednesday to Sunday, 11 to 5, and closes when the fish runs out.',True)]),
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
  .intro.short { padding:120px 24px 90px; }
  .intro.short h2 { font-family:var(--head); font-weight:400; font-style:italic; font-size:clamp(44px,7vw,84px); line-height:1.05; margin:0 0 28px; }
  .tagpill { display:inline-flex; align-items:center; gap:12px; padding:10px 24px; border:1.5px solid var(--accent); border-radius:999px; font-size:clamp(11px,1.4vw,14px); letter-spacing:.24em; text-transform:uppercase; color:var(--accent); font-weight:500; }
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
  .index .gcats { display:grid; grid-template-columns:repeat(auto-fit,minmax(210px,1fr)); gap:34px 40px; text-align:left; margin-top:30px; }
  .index .gcat { align-self:start; }
  .index .gcat summary { list-style:none; cursor:pointer; }
  .index .gcat summary::-webkit-details-marker { display:none; }
  .index .gcat h3::after { content:'+'; margin-left:12px; font-size:16px; letter-spacing:0; }
  .index .gcat[open] h3::after { content:'\2212'; }
  .index .gcat h3 small { margin-left:auto; }
  .index .gcat h3 { display:flex; align-items:baseline; margin:0 0 10px; padding-bottom:9px; border-bottom:1px solid color-mix(in srgb,var(--txt) 24%, transparent); font:500 12px/1 var(--body); letter-spacing:.24em; text-transform:uppercase; color:var(--accent); }
  .index .gcat h3 small { font-size:11px; letter-spacing:.1em; opacity:.6; }
  .index .gcat ul { list-style:none; margin:0; padding:0; }
  .index .gcat li { font-family:var(--head); font-style:italic; font-size:clamp(17px,1.5vw,19px); line-height:1.35; padding:5px 0; opacity:.9; }
  .index { max-width:1040px; }
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

  /* ---- Kith collage scene ---- */
  .kscene { position:relative; width:min(1180px,100%); aspect-ratio:16/9.4; margin:30px auto 20px; }
  .kscene .lyr { position:absolute; margin:0; transform:translateY(var(--py,0px)) rotate(var(--r,0deg)); filter:drop-shadow(0 10px 14px rgba(0,0,0,.4)); will-change:transform; }
  .kscene img.lyr { height:auto; max-width:none; }
  .kscene .print { background:#f4efe3; padding:9px 9px 11px; }
  .kscene .print img { display:block; width:100%; height:auto; }
  .kscene .print figcaption { position:absolute; left:0; right:0; bottom:5px; text-align:center; font-size:clamp(13px,1.5vw,20px); color:#2a2a2a; }
  .kscene .print:has(figcaption) { padding-bottom:30px; }
  .kscene .tape { z-index:5; }
  .kscene .wall { left:3%; top:3%; width:52%; --r:-1.6deg; z-index:1; }
  .kscene .shop { right:5%; top:8%; width:30%; --r:2.4deg; z-index:2; }
  .kscene .shelf { left:50%; top:46%; width:19%; --r:-6deg; z-index:6; }
  .kscene .ped { right:9%; top:50%; width:15%; --r:5deg; z-index:6; }
  .kscene .msg { z-index:7; color:var(--pen); font-size:clamp(14px,2vw,26px); line-height:1.15; filter:none; }
  .kscene .msg.k1 { left:14%; top:84%; --r:-3deg; }
  .kscene .msg.k2 { left:58%; top:78%; --r:-2deg; }
  @media (max-width:820px) {
    .kscene { aspect-ratio:3/5; }
    .kscene .wall { left:3%; top:1%; width:92%; }
    .kscene .shop { right:3%; top:26%; width:66%; }
    .kscene .shelf { left:3%; top:44%; width:40%; }
    .kscene .ped { right:6%; top:56%; width:34%; }
    .kscene .msg { font-size:15px; }
    .kscene .msg.k1 { display:none; }
    .kscene .msg.k2 { left:8%; top:90%; width:60%; }
  }

  /* ---- Aura reading collage scene ---- */
  .ascene { position:relative; width:min(1180px,100%); aspect-ratio:16/7.2; margin:30px auto 20px; }
  .ascene .lyr { position:absolute; margin:0; transform:translateY(var(--py,0px)) rotate(var(--r,0deg)); filter:drop-shadow(0 10px 14px rgba(0,0,0,.4)); will-change:transform; }
  .ascene img.lyr { height:auto; max-width:none; }
  .ascene .print { background:#f4efe3; padding:9px 9px 34px; }
  .ascene .print img { display:block; width:100%; height:auto; }
  .ascene .print figcaption { position:absolute; left:0; right:0; bottom:6px; text-align:center; font-size:clamp(13px,1.5vw,20px); color:#2a2a2a; }
  .ascene .tape { z-index:5; }
  .ascene .cards { left:4%; top:4%; width:46%; --r:-1.6deg; z-index:1; }
  .ascene .blue { left:54%; top:2%; width:17%; --r:-5deg; z-index:5; }
  .ascene .red { left:73%; top:10%; width:16%; --r:4deg; z-index:5; }
  .ascene .msg { z-index:7; color:var(--pen); font-size:clamp(14px,2vw,26px); line-height:1.15; filter:none; }
  .ascene .msg.a1 { left:56%; top:66%; --r:-3deg; }
  .ascene .msg.a2 { left:78%; top:72%; --r:-2deg; }
  @media (max-width:820px) {
    .ascene { aspect-ratio:3/4.6; }
    .ascene .cards { left:3%; top:1%; width:92%; }
    .ascene .blue { left:4%; top:34%; width:44%; }
    .ascene .red { right:4%; left:auto; top:38%; width:42%; }
    .ascene .msg { font-size:15px; }
    .ascene .msg.a1 { left:8%; top:84%; }
    .ascene .msg.a2 { display:none; }
  }

  /* ---- season toggle ---- */
  html[data-season="winter"] [data-s="m"], html[data-season="warm"] [data-s="w"] { display:none; }
  .hud .season { display:flex; gap:0; border:1px solid currentColor; border-radius:99px; overflow:hidden; }
  .hud .season button { font:inherit; letter-spacing:inherit; text-transform:inherit; color:inherit; background:transparent; border:0; padding:6px 12px; cursor:pointer; }
  .hud .season button[aria-pressed="true"] { background:#fff; color:#000; }
  @media (max-width:820px) { .hud .cur { display:none; } .hud { font-size:10.5px; padding:10px 12px; } .hud .season button { padding:6px 9px; } }

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

  /* ---- washi tape: translucent, pale, torn at the ends ---- */
  .tape { position:absolute; width:98px; height:27px; margin:0; top:-9px; left:-30px; right:auto; bottom:auto; transform:rotate(-38deg); z-index:4; pointer-events:none;
          background-color:rgba(214,219,160,.62);
          background-image:repeating-linear-gradient(90deg,rgba(255,255,255,.24) 0 1px,transparent 1px 4px), linear-gradient(180deg,rgba(255,255,255,.4),rgba(255,255,255,0) 45%,rgba(90,90,40,.07));
          box-shadow:0 1px 2px rgba(0,0,0,.25), inset 0 0 0 1px rgba(140,145,80,.2); clip-path:polygon(0% 0%,2% 12%,0% 25%,2% 38%,0% 50%,2% 63%,0% 75%,2% 88%,0% 100%,100% 100%,98% 88%,100% 75%,98% 63%,100% 50%,98% 38%,100% 25%,98% 12%,100% 0%); mix-blend-mode:normal; }
  .cut:nth-child(even) > .tape, figure.print:nth-of-type(even) > .tape { left:auto; right:-30px; transform:rotate(38deg); }
  figure.print:nth-of-type(3n) > .tape, .cut:nth-child(3n) > .tape { top:auto; bottom:-8px; left:-30px; right:auto; transform:rotate(36deg); }
  .cut .snap .tape, .snap .tape { width:58px; height:18px; left:-16px; top:-6px; right:auto; bottom:auto; transform:rotate(-36deg); }
  .note .tape { display:none; }

  /* ---- open binder opener ---- */
  .bopen { position:relative; height:200vh; margin-bottom:-100vh; z-index:30; pointer-events:none; }
  .bstage { position:sticky; top:0; height:100vh; display:flex; align-items:center; justify-content:center; overflow:hidden;
            background:radial-gradient(ellipse at 50% 20%, #f1ebdf, #d8cfbf 80%); will-change:opacity; }
  .bstage .bd-book { --bw:min(780px,94vw); --bh:min(86vh,900px); will-change:transform; }
  .bstage.live .bd-book a { pointer-events:auto; }
  .bk-kick { margin-bottom:18px; }
  .bstage .bd-page > :not(.bk-pol):not(.bk-cue) { max-width:52%; }
  .bk-logo { display:block; max-width:min(260px,60%); max-height:84px; object-fit:contain; margin:0 0 14px; }
  .bk-name { font-family:var(--head); font-weight:400; font-style:italic; font-size:clamp(34px,4.6vw,56px); line-height:1.04; margin:0 0 12px; color:#231c17; }
  .bk-tag { font-family:var(--body); font-size:clamp(14px,1.5vw,17px); line-height:1.6; max-width:30ch; color:#5a4d3e; }
  .bk-hand { font-family:var(--hand); font-size:clamp(22px,2.4vw,28px); color:#7a6850; margin-top:12px; }
  .bk-pol { position:absolute; right:36px; top:0; width:min(33%,225px); margin:0; padding:10px 10px 36px; background:#fbf8f1; box-shadow:0 10px 24px rgba(0,0,0,.35); transform:rotate(3.5deg); }
  .bk-pol .ph { display:block; aspect-ratio:4/5; background:linear-gradient(150deg,var(--accent2),var(--accent)); position:relative; overflow:hidden; }
  .bk-pol img { position:absolute; inset:0; width:100%; height:100%; object-fit:cover; }
  .bk-pol .bd-clip { left:50%; margin-left:-13px; top:-42px; }
  .bstage .bd-page { overflow:visible; padding-top:0; } .bstage .bk-kick { margin-top:96px; }
  .bk-pol figcaption { position:absolute; left:0; right:0; bottom:8px; white-space:nowrap; text-align:center; font-family:var(--hand); font-size:18px; color:#4a3d2c; }
  .bk-cue { position:absolute; left:42px; bottom:30px; font-family:var(--hand); font-size:clamp(20px,2.2vw,26px); color:#7a6850; animation:bob 2s ease-in-out infinite; }
  .bstage .bd-tabs { gap:6px; }
  .bstage .bd-tab { flex:1 1 0; min-height:0; max-height:128px; font-size:17px; }
  @media (max-width:640px) {
    .bstage .bd-page { display:flex; flex-direction:column; } .bk-pol figcaption { font-size:15px; } .bk-pol { position:relative; right:auto; top:auto; order:-1; align-self:center; width:52%; margin:0 0 26px; padding:7px 7px 28px; } .bk-pol .bd-clip { top:-34px; transform:scale(.8); } .bstage .bk-kick { margin-top:0; }
    .bstage .bd-page > :not(.bk-pol):not(.bk-cue) { max-width:100%; } .bk-name { font-size:32px; } .bk-tag { max-width:24ch; } .bk-cue { left:22px; bottom:20px; font-size:20px; } .bstage .bd-tab { font-size:14px; }
  }
  .bk-cue { text-decoration:none; cursor:pointer; }
  .smap { display:grid; grid-template-columns:minmax(150px,230px) 1fr; gap:34px; align-items:center; max-width:640px; margin:46px auto 0; padding:26px 28px; border:1px solid color-mix(in srgb,var(--txt) 18%, transparent); border-radius:4px; }
  .smap svg { width:100%; height:auto; overflow:visible; }
  .smap .sw { fill:color-mix(in srgb,var(--accent) 16%, transparent); }
  .smap .sg line { stroke:var(--txt); stroke-opacity:.12; stroke-width:.5; }
  .smap .sbase { fill:none; stroke:var(--txt); stroke-opacity:.22; stroke-width:1; stroke-linecap:round; }
  .smap .sline { fill:none; stroke:var(--accent); stroke-width:1.6; stroke-linecap:round; stroke-linejoin:round; stroke-dasharray:100; stroke-dashoffset:100; }
  .smap .shotel { fill:var(--accent); } .smap .slab { font:500 7px var(--body); letter-spacing:.18em; text-transform:uppercase; fill:var(--txt); opacity:.6; }
  .smap .sdest { fill:none; stroke:var(--accent); stroke-width:1.2; opacity:0; }
  .smap .sdot { fill:var(--txt); opacity:0; offset-distance:0%; }
  .smap.in .sline { animation:sdraw 3.2s .3s cubic-bezier(.5,0,.3,1) forwards; }
  .smap.in .sdot { animation:smove 3.2s .3s cubic-bezier(.5,0,.3,1) forwards; }
  .smap.in .sdest { animation:sping 1.4s 3.3s ease-out forwards; }
  @keyframes sdraw { to { stroke-dashoffset:0; } }
  @keyframes smove { 0% { opacity:1; offset-distance:0%; } 96% { opacity:1; } 100% { opacity:0; offset-distance:100%; } }
  @keyframes sping { 0% { opacity:.9; r:3; } 100% { opacity:.9; r:6; } }
  .smap .sinfo .stm { font-family:var(--head); font-style:italic; font-size:18px; line-height:1.3; margin:8px 0 12px; }
  .smap ol { margin:0 0 12px; padding-left:20px; font-size:15px; line-height:1.5; opacity:.88; }
  .smap ol li { padding:2px 0; }
  .smap .smatcha { font-family:var(--head); font-style:italic; font-size:16px; margin:0 0 10px; opacity:.92; }
  .smap .spup { font-size:11px; letter-spacing:.16em; text-transform:uppercase; color:var(--accent); }
  @media (max-width:640px) { .smap { grid-template-columns:1fr; gap:20px; padding:22px 20px; } .smap svg { max-width:190px; margin:0 auto; } }
  @media (prefers-reduced-motion:reduce) { .smap .sline { stroke-dashoffset:0; animation:none !important; } .smap .sdest { opacity:.9; animation:none !important; } .smap .sdot { display:none; } }
  .rail { position:fixed; right:6px; top:50%; transform:translateY(-50%); z-index:59; display:flex; flex-direction:column; align-items:flex-end; gap:0; mix-blend-mode:difference; color:#fff; opacity:0; pointer-events:none; transition:opacity .35s; max-height:86vh; }
  .rail.on { opacity:1; pointer-events:auto; }
  .rail a { display:flex; align-items:center; justify-content:flex-end; gap:9px; padding:6px 8px; font-size:10.5px; letter-spacing:.14em; text-transform:uppercase; line-height:1; color:#fff; text-decoration:none; cursor:pointer; }
  .rail a .s, .rail a .f { white-space:nowrap; transition:opacity .2s, transform .2s; opacity:0; transform:translateX(6px); }
  .rail a.day .s { opacity:.8; transform:none; font-weight:500; }
  .rail a.day { margin-top:7px; } .rail a.day:first-child { margin-top:0; }
  .rail a .f { position:absolute; right:30px; }
  .rail a { position:relative; }
  .rail a:hover .f, .rail a:focus-visible .f, .rail a.act .f { opacity:1; transform:none; }
  .rail a:hover .s, .rail a:focus-visible .s, .rail a.act .s { opacity:0; }
  .rail a i { flex:0 0 auto; width:7px; height:7px; border-radius:50%; border:1px solid #fff; opacity:.75; transition:background .2s, transform .2s, opacity .2s; }
  .rail a.day i { width:10px; height:10px; border-width:1.5px; }
  .rail a.act i { background:#fff; opacity:1; transform:scale(1.25); }
  .rail a:hover i { opacity:1; transform:scale(1.3); }
  @media (max-width:820px) { .rail { right:0; } .rail a { padding:5px 7px; } .rail a.act .f, .rail a:hover .f { display:none; } .rail a.act .s { opacity:.8; } .rail a.day .s { display:none; } }
  @media (prefers-reduced-motion: reduce) { .bopen { height:auto; margin:0; } .bstage { position:relative; height:100vh; } .bk-cue { animation:none; } }

  /* ---- lobby note on a leather notepad ---- */
  .lobby { display:flex; flex-direction:column; align-items:center; padding:30px 24px 90px; }
  .lobby .pad { position:relative; width:min(430px,86vw); aspect-ratio:.74; transform:rotate(-3deg); border-radius:14px; padding:7%;
     background-color:#9a5a2b; background-image:%%LEATHER%%, linear-gradient(150deg,#b87340,#7a4220); background-blend-mode:multiply, normal; box-shadow:0 26px 40px rgba(0,0,0,.4), inset 0 0 0 1px rgba(0,0,0,.25); }
  .lobby .pad::before { content:''; position:absolute; inset:9px; border:1.5px dashed rgba(240,215,170,.5); border-radius:9px; pointer-events:none; }
  .lobby .sheet { position:relative; height:100%; background:#fbf8f1; box-shadow:0 2px 6px rgba(0,0,0,.35); padding:9% 9% 7%; display:flex; flex-direction:column; align-items:center; text-align:center; }
  .lobby .lh { font-family:var(--head); font-size:clamp(13px,1.5vw,16px); letter-spacing:.2em; text-transform:uppercase; color:#3b3a44; line-height:1.5; }
  .lobby .lh small { display:block; font-size:.62em; letter-spacing:.34em; opacity:.7; margin-top:2px; }
  .lobby .lh::before { content:''; display:block; width:26px; height:26px; margin:0 auto 8px; border:1.5px solid #3b3a44; border-radius:50% 50% 45% 45%; opacity:.7; }
  .lobby .msg { font-family:var(--hand); font-size:clamp(30px,4.4vw,46px); line-height:1.18; color:#26263a; margin-top:auto; margin-bottom:auto; transform:rotate(-2deg); text-shadow:0 0 .6px currentColor; }
  .lobby .pen { position:absolute; right:-6%; top:6%; width:3.4%; min-width:15px; height:86%; border-radius:99px; transform:rotate(7deg); z-index:3;
     background:linear-gradient(90deg,#0c1230,#25306a 45%,#0a0f26); box-shadow:3px 6px 10px rgba(0,0,0,.45); }
  .lobby .pen::before { content:''; position:absolute; left:-30%; right:-30%; top:10%; height:5%; border-radius:3px; background:linear-gradient(#f2dc9a,#a98240); }
  .lobby .pen::after { content:''; position:absolute; left:-30%; right:-30%; top:19%; height:2.5%; border-radius:3px; background:linear-gradient(#f2dc9a,#a98240); }
  .lobby .cap2 { margin-top:34px; font-family:var(--hand); font-size:clamp(22px,2.4vw,28px); color:var(--pen); text-align:center; }

  .pin { display:inline-flex; align-items:center; gap:6px; width:fit-content; margin-top:6px; font-family:var(--body); font-size:12px; letter-spacing:.05em; color:var(--accent); border-bottom:1px solid currentColor; padding-bottom:1px; pointer-events:auto; position:relative; z-index:6; }
  .pin svg { width:10px; height:13px; fill:currentColor; } .pin:hover { opacity:.7; }
  .stayline { margin-top:16px; font-size:13px; letter-spacing:.04em; display:flex; gap:14px; flex-wrap:wrap; align-items:center; } .stayline a { border-bottom:1px solid rgba(255,255,255,.6); padding-bottom:1px; }
  .bk-addr { margin-top:14px; font-size:12px; letter-spacing:.05em; color:#5a4d3e; display:flex; gap:12px; flex-wrap:wrap; } .bk-addr a { border-bottom:1px solid currentColor; }

  .hl { max-width:1120px; margin:0 auto; padding:90px 24px 40px; }
  .hl h2 { font-family:var(--head); font-weight:400; font-size:clamp(32px,4.6vw,54px); line-height:1.08; margin:8px 0 10px; }
  .hl .lede { max-width:48ch; line-height:1.65; opacity:.8; margin:0 0 34px; font-size:15.5px; }
  .hl h3 { font-family:var(--hand); font-weight:400; font-size:clamp(26px,3vw,32px); color:var(--accent); margin:0 0 6px; }
  .hl .walks { display:flex; flex-wrap:wrap; gap:14px; margin:0 0 12px; }
  .hl .walk { flex:1 1 190px; display:flex; align-items:center; gap:12px; padding:14px 16px; border:1px solid color-mix(in srgb, currentColor 22%, transparent); border-radius:14px; line-height:1.3; font-size:14px; }
  .hl .walk .m { font-family:var(--head); font-style:italic; font-size:38px; line-height:1; } .hl .walk .m small { font-family:var(--body); font-style:normal; font-size:10px; letter-spacing:.16em; text-transform:uppercase; opacity:.7; margin-left:3px; }
  .hl .cf { display:inline-block; margin-left:8px; padding:1px 7px; border:1px dashed currentColor; border-radius:3px; font-size:10px; letter-spacing:.14em; text-transform:uppercase; color:#d98a8a; vertical-align:2px; }
  .hl .card .cf { color:#b5605a; }
  .hl .wn { margin:0 0 44px; font-size:12px; line-height:1.6; opacity:.6; }
  .hl .cards { display:grid; grid-template-columns:repeat(auto-fit,minmax(250px,1fr)); gap:30px 26px; margin-bottom:34px; }
  .hl .card { position:relative; background:var(--paper); color:var(--ink); padding:30px 22px 18px; border-radius:3px; box-shadow:0 14px 26px rgba(0,0,0,.2), 0 2px 4px rgba(0,0,0,.15); transform:rotate(var(--r,0deg)); }
  .hl .card:nth-child(4n+1){--r:-1.2deg} .hl .card:nth-child(4n+2){--r:.9deg} .hl .card:nth-child(4n+3){--r:-.6deg} .hl .card:nth-child(4n){--r:1.1deg}
  .hl .card::before { content:''; position:absolute; top:-12px; left:50%; width:84px; height:26px; margin-left:-42px; transform:rotate(-2deg); background:rgba(214,219,160,.7); box-shadow:0 1px 2px rgba(0,0,0,.18); clip-path:polygon(0 8%,4% 0,8% 10%,12% 0,16% 10%,20% 0,24% 8%,76% 8%,80% 0,84% 10%,88% 0,92% 10%,96% 0,100% 8%,100% 92%,96% 100%,92% 90%,88% 100%,84% 90%,80% 100%,76% 92%,24% 92%,20% 100%,16% 90%,12% 100%,8% 90%,4% 100%,0 92%); }
  .hl ul { list-style:none; margin:0; padding:0; }
  .hl li { border-bottom:1px solid color-mix(in srgb, currentColor 14%, transparent); }
  .hl li:last-child { border-bottom:0; }
  .hl summary { list-style:none; cursor:pointer; padding:10px 24px 10px 0; position:relative; font-size:15px; line-height:1.4; font-weight:500; }
  .hl summary::-webkit-details-marker { display:none; }
  .hl summary::after { content:'+'; position:absolute; right:2px; top:8px; font-size:18px; font-weight:300; opacity:.55; transition:transform .2s; }
  .hl details[open] > summary::after { transform:rotate(45deg); }
  .hl details p { margin:0 0 12px; font-size:14px; line-height:1.65; opacity:.82; }
  .about.solo { grid-template-columns:1fr; }
  .hl .care .card { background:color-mix(in srgb, var(--paper) 92%, var(--accent)); }
  .hl .kick2 { font-size:11px; letter-spacing:.3em; text-transform:uppercase; opacity:.7; margin:6px 0 18px; }
  @media (max-width:760px) { .hl { padding-top:60px; } .hl .cards { grid-template-columns:1fr; } }
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
  var els = document.querySelectorAll('.reveal,.rise,.smap');
  if (!('IntersectionObserver' in window)) { els.forEach(function (e) { e.classList.add('in'); }); }
  else {
    var io = new IntersectionObserver(function (en) { en.forEach(function (x) { if (x.isIntersecting) { x.target.classList.add('in'); io.unobserve(x.target); } }); }, { threshold: .12 });
    els.forEach(function (e) { io.observe(e); });
  }
  var seasonKey = 'pitch-season';
  function setSeason(v, save) {
    document.documentElement.setAttribute('data-season', v);
    Array.prototype.forEach.call(document.querySelectorAll('.hud .season button'), function (b) { b.setAttribute('aria-pressed', b.getAttribute('data-v') === v ? 'true' : 'false'); });
    if (save) { try { localStorage.setItem(seasonKey, v); } catch (e) {} try { window.name = 'season:' + v; } catch (e) {} }
  }
  var saved = null; try { saved = localStorage.getItem(seasonKey); } catch (e) {}
  if (!saved) { try { if (/^season:/.test(window.name)) saved = window.name.slice(7); } catch (e) {} }
  if (saved === 'warm' || saved === 'winter') setSeason(saved, false);
  Array.prototype.forEach.call(document.querySelectorAll('.hud .season button'), function (b) { b.addEventListener('click', function () { setSeason(b.getAttribute('data-v'), true); }); });
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
  var bo = document.querySelector('.bopen'), bst = bo && bo.querySelector('.bstage'), bbk = bst && bst.querySelector('.bd-book');
  function opener() {
    if (!bo || reduce) return;
    var p = Math.max(0, Math.min(1, (window.pageYOffset || document.documentElement.scrollTop) / (window.innerHeight * .5)));
    bst.style.opacity = Math.max(0, Math.min(1, 1.5 - p * 1.5)).toFixed(3);
    bbk.style.transform = 'scale(' + (1 + p * .85).toFixed(3) + ')';
    bst.classList.toggle('live', p < .5); bst.style.visibility = p >= 1 ? 'hidden' : 'visible';
  }
  var rail = document.querySelector('.rail'), rlinks = rail ? Array.prototype.slice.call(rail.querySelectorAll('a')) : [];
  function railUpdate() {
    if (!rail) return;
    var vh = window.innerHeight, st = window.pageYOffset || document.documentElement.scrollTop, act = null;
    rail.classList.toggle('on', st > vh * .55);
    Array.prototype.forEach.call(document.querySelectorAll('.chapter[id]'), function (c) { if (c.getBoundingClientRect().top < vh * .5) act = c.id; });
    rlinks.forEach(function (a) { a.classList.toggle('act', a.getAttribute('data-t') === act); });
  }
  document.addEventListener('click', function (e) {
    var a = e.target && e.target.closest ? e.target.closest('a[href^="#"]') : null;
    if (!a) return;
    var id = a.getAttribute('href').slice(1), t = id && document.getElementById(id);
    if (!t) return;
    e.preventDefault();
    t.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'start' });
  });
  function onScroll() { railUpdate(); opener(); if (!ticking) { ticking = true; requestAnimationFrame(frame); } }
  window.addEventListener('scroll', onScroll, { passive: true }); window.addEventListener('resize', onScroll); frame(); opener(); railUpdate();
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

ADDR = {'cj-hendry-flower-market': '172 Prince St', '12-matcha': '54 Bond St', 'mercer-labs': '21 Dey St', 'aura-reading-at-magic-jewelry': '238 Canal St', 'brooklyn-botanical-garden': '990 Washington Ave'}
NOPIN = {'sample-sale-hunt', 'pop-up-of-the-week', 'room-and-amenities', 'room-view-and-amenities', 'last-look-and-checkout'}
import urllib.parse as _up

def pin(h, name, key, tag):
    if key in NOPIN: return ''
    if tag == 'here' and h.get('addr'):
        q = h['name'] + ', ' + h['addr']; label = h['addr'].split(',')[0]
    else:
        q = name + ', ' + h['city']; label = ADDR.get(key, 'Map &amp; address')
    href = 'https://www.google.com/maps/search/?api=1&query=' + _up.quote(q)
    return f'<a class="pin" href="{href}" target="_blank" rel="noopener"><svg viewBox="0 0 16 20" aria-hidden="true"><path d="M8 1a6 6 0 0 0-6 6c0 4.5 6 12 6 12s6-7.500 6-12a6 6 0 0 0-6-6zm0 8.200A2.200 2.200 0 1 1 8 4.800a2.200 2.200 0 0 1 0 4.400z"/></svg>{label}</a>'


SNAPS = {('nomad', 'nubeluz-50th-floor'): [('nubeluz-50th-floor-day', 'by day', 's1'), ('nubeluz-50th-floor-night', 'by night', 's2')]}

def snaps(slug_h, key):
    out = ''
    for n, (img, label, cls) in enumerate(SNAPS.get((slug_h, key), [])):
        out += f'<span class="snap {cls}"><span class="tape"></span><img src="{CDN}{slug_h}/{img}.jpg" alt="{label}" loading="lazy" onerror="this.parentNode.remove()"><em class="hand">{label}</em></span>'
    return out

def aura_scene(slug_h, cap_html):
    M = CDN + 'shared/aura/'
    return f'''
        <div class="scene-col">
          <div class="ascene reveal">
            <figure class="lyr print cards" data-speed="0.015"><div class="tape"></div><img src="{M}cards.jpg" alt="Two aura photographs" loading="lazy"><figcaption class="hand">my aura, then and now</figcaption></figure>
            <img class="lyr blue" data-speed="0.04" src="{M}cut-card-blue.png" alt="" loading="lazy">
            <img class="lyr red" data-speed="-0.04" src="{M}cut-card-red.png" alt="" loading="lazy">
            <div class="lyr msg a1 hand" data-speed="0.01">what color<br>are you?</div>
            <div class="lyr msg a2 hand" data-speed="0.02">a tiny Canal St<br>detour</div>
          </div>
          {cap_html}
        </div>'''

def kith_scene(slug_h, cap_html):
    M = CDN + 'shared/kith/'
    return f'''
        <div class="scene-col">
          <div class="kscene reveal">
            <figure class="lyr print wall" data-speed="0.015"><div class="tape"></div><img src="{M}wall.jpg" alt="A glass wall of sneakers" loading="lazy"><figcaption class="hand">a wall of sneakers</figcaption></figure>
            <figure class="lyr print shop" data-speed="-0.03"><div class="tape"></div><img src="{M}shop.jpg" alt="The Kith shop floor" loading="lazy"></figure>
            <img class="lyr shelf" data-speed="0.04" src="{M}cut-shelf.png" alt="" loading="lazy">
            <img class="lyr ped" data-speed="-0.04" src="{M}cut-pedestal.png" alt="" loading="lazy">
            <div class="lyr msg k1 hand" data-speed="0.01">all white,<br>all sneakers</div>
            <div class="lyr msg k2 hand" data-speed="0.02">a store that<br>looks like a gallery</div>
          </div>
          {cap_html}
        </div>'''

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

# ---- seasons: the source copy above is the spring/summer version; winter is the default view ----
WINTER_STOP = {   # warm name -> (winter name, winter note); a None keeps the warm one
  'Brooklyn Botanical Garden': (None, '990 Washington Ave, Prospect Heights. The glass conservatory stays green and warm in winter, and the Japanese garden is quiet under frost. Confirm winter hours and tickets.'),
  'Dumbo ice cream and bridge shot': ('Dumbo hot chocolate and bridge shot', 'Something warm in hand, then the bridge frame at dusk.'),
  'Ice cream by the water': ('Hot chocolate by the water', 'Something warm at dusk.'),
  'Malibu Country Mart': (None, 'Cozy outdoor shopping and cafes. Bring a layer for the ocean breeze.'),
}
WINTER_TEXT = {   # warm sentence -> winter sentence (titles, stories, intros)
  'The secret garden': 'The quiet garden',
  'The city drops away: cherry blossoms in spring, a Japanese hill-and-pond garden, and roses in early summer. This is the quiet chapter.': 'The city drops away: a Japanese hill-and-pond garden, and a glass conservatory of greenhouse blooms. This is the quiet chapter.',
  'The city drops away: cherry blossoms in spring, a Japanese hill-and-pond garden, and roses in early summer.': 'The city drops away: a Japanese hill-and-pond garden, and a glass conservatory of greenhouse blooms.',
  'A scoop of ice cream, the bridge in the frame, and one last dinner that earns its place in the story.': 'A hot chocolate, the bridge in the frame, and one last dinner that earns its place in the story.',
  'Soft light over the skyline, a coffee on the rooftop deck, and nowhere to be. The calm opening shot of the trip.': 'Soft winter light over the skyline, a hot coffee by the window, and nowhere to be. The calm opening shot of the trip.',
  'A café that doubles as an art space in Williamsburg, then ramen and a scoop by the water on the way home.': 'A café that doubles as an art space in Williamsburg, then ramen and a hot chocolate by the water on the way home.',
  "Picture a slower New York. The skyline is right across the water, the bridge is outside your window, and there's a rooftop pool above it all. This is the stay for people who want the city without the rush.": "Picture a slower New York. The skyline is right across the water, the bridge is outside your window, and the city glitters in the cold. This is the stay for people who want the city without the rush.",
}

def sv(warm, winter=None):
    """Escaped text with a winter/warm pair of spans when a winter variant exists."""
    w = winter if winter is not None else WINTER_TEXT.get(warm)
    if not w or w == warm: return esc(warm)
    return f'<span data-s="w">{esc(w)}</span><span data-s="m">{esc(warm)}</span>'

STROLLS = {
 'Madison Square Park, at stroller pace': dict(
   mode='walk', time='About 6 minutes, flat the whole way (est.)',
   path='M 104 78 L 126 78 L 126 112 L 176 112 L 176 190 L 126 190 L 126 112',
   dest=(151, 150), dlabel='Madison Square Park',
   steps=['Out the lobby and east on W 28th St toward Fifth Ave.','South on Fifth Ave, about three blocks.','Enter at the Fifth Ave and 26th St corner, then loop the lawn.'],
   matcha='Matcha: Cha Cha Matcha, 1158 Broadway, on the way.',
   pup='Leashed pup welcome. Confirm park rules.'),
 'Chelsea gallery streets, pup in tow': dict(
   mode='ride', time='A short cab or subway ride west (est. 15 min)',
   path='M 104 78 L 44 78 L 44 175 L 30 175',
   dest=(30, 175), dlabel='Chelsea gallery streets',
   steps=['Ride or cab west to W 22nd St and 10th Ave.','Stroll the gallery blocks on the W 20s, between 10th and 11th Ave.','Look up: the High Line runs overhead. Peek from below, no dogs up top.'],
   matcha='Matcha: Cha Cha Matcha, 1158 Broadway, before you ride.',
   pup='All street level, leashed pup welcome.'),
 'Along the Hudson, one last stroll': dict(
   mode='walk', time='About 25 minutes on foot, or a short ride (est.)',
   path='M 104 78 L 18 78 L 8 78 L 8 248',
   dest=(8, 248), dlabel='Hudson River Greenway',
   steps=['West on W 28th St all the way to the river.','Join the greenway along 11th/12th Ave.','Stroll south with the water on your right.'],
   matcha='Matcha: Matchaful, 450 W 33rd St, a detour toward the river.',
   pup='Leashed pup welcome. Confirm rules.'),
}

def stroll_html(title):
    d = STROLLS.get(title)
    if not d: return ''
    vh = max(d['dest'][1], 190) + 30
    gx = ''.join(f'<line x1="{x}" y1="14" x2="{x}" y2="{vh-14}"/>' for x in (24, 44, 84, 126, 176))
    gy = ''.join(f'<line x1="2" y1="{y}" x2="196" y2="{y}"/>' for y in (78, 112, 150, 190, 248, 292))
    dash = ' stroke-dasharray="1 5"' if d['mode'] == 'ride' else ''
    steps = ''.join(f'<li>{esc(x)}</li>' for x in d['steps'])
    dx, dy = d['dest']
    return f'''
      <div class="smap rise">
        <svg viewBox="0 0 200 {vh}" role="img" aria-label="Route from the hotel to {esc(d['dlabel'])}">
          <path class="sw" d="M 0 0 H 12 V {vh} H 0 Z"/>
          <g class="sg">{gx}{gy}</g>
          <path class="sbase"{dash} d="{d['path']}" pathLength="100"/>
          <path class="sline" d="{d['path']}" pathLength="100"/>
          <circle class="shotel" cx="104" cy="78" r="4"/><text class="slab" x="112" y="68">hotel</text>
          <circle class="sdest" cx="{dx}" cy="{dy}" r="5"/>
          <circle class="sdot" r="3" style="offset-path:path('{d['path']}')"/>
        </svg>
        <div class="sinfo"><div class="kick">How to get there</div><div class="stm">{esc(d['time'])}</div><ol>{steps}</ol><div class="smatcha">{esc(d['matcha'])}</div><div class="spup">{esc(d['pup'])}</div></div>
      </div>'''

def render(h):
    S = STORY[h['slug']]; c = h['c']; slug_h = h['slug']
    dark = slug_h == 'nomad'
    css = (CSS.replace('%%BG%%', c['desk'] if dark else c['paper']).replace('%%TXT%%', '#f3ead6' if dark else c['ink'])
              .replace('%%PAPER%%', c['paper']).replace('%%INK%%', c['ink']).replace('%%ACCENT%%', c['accent'])
              .replace('%%ACCENT2%%', c['accent2']).replace('%%SOFT%%', c['soft'] if not dark else '#1d2547')
              .replace('%%HEAD%%', h['head']).replace('%%BODY%%', h['body']).replace('%%DESK%%', c['desk']).replace('%%PEN%%', '#efe5cc' if dark else '#1d2a4a').replace('%%RED%%', '#ff8a7a' if dark else '#b3362b').replace('%%PAPER_TEX%%', paper_tex(dark)).replace('%%MUTE%%', '#2b3048' if dark else '#d8d0bf').replace('%%PHC%%', 'rgba(240,234,214,.7)' if dark else 'rgba(28,34,51,.55)')).replace('%%LEATHER%%', gp.LEATHER) + gp.BINDER_CSS
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
          <figcaption class="cap"><span class="nm">{sv(name, WINTER_STOP.get(name, (None, None))[0])}</span><span class="row"><span class="tg {cls}">{label}</span>{stamp}</span><span class="nt"><svg class="dd up" viewBox="0 0 40 30"><use href="#d-up"/></svg>{sv(note, WINTER_STOP.get(name, (None, None))[1])}</span>{pin(h, name, key, tag)}</figcaption>{snaps(slug_h, key)}
        </figure>'''
            if key == 'aura-reading-at-magic-jewelry':
                cap = re.search(r'<figcaption.*?</figcaption>', frames[_before:], re.S).group(0)
                frames = frames[:_before] + aura_scene(slug_h, cap)
            if key == 'kith-soho':
                cap = re.search(r'<figcaption.*?</figcaption>', frames[_before:], re.S).group(0)
                frames = frames[:_before] + kith_scene(slug_h, cap)
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
            if slug_h == 'nomad' and key == 'chelsea-gallery-streets':
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
        <div class="rise"><div class="kick">{esc(kick)}</div><h2>{sv(title)}</h2><svg class="dd under" viewBox="0 0 300 14"><use href="#d-under"/></svg></div>
        <div class="note rise"><div class="tape"></div>{sv(story)}<svg class="dd pt" viewBox="0 0 140 70"><use href="#d-arrow"/></svg></div>
      </div>
      <div class="collage n{min(n,4)} {'rev' if i % 2 else ''}">{frames}
      </div>
      {stroll_html(title) if slug_h == 'nomad' else ''}
      <img class="cutout" src="{CDN}{slug_h}/ch{i+1+off}-cutout.png" alt="" onerror="this.remove()">
    </div>
  </section>'''
    walk = [s for s in allstops if s[1] in ('here', 'walk')]
    far = [s for s in allstops if s[1] in ('ride', 'trip')]
    li = lambda arr: ''.join(f'<li>{esc(s[0])}{" <em>(confirm)</em>" if s[3] else ""}</li>' for s in arr)
    def _cat(name, tag):
        lo = name.lower()
        has = lambda *ks: any(k in lo for k in ks)
        if has('bazaar', 'nubeluz', 'lobby lounge'): return 'Hotel'
        if has('matcha', 'rhythm zero'): return 'Matcha'
        if has('sample'): return 'Sample sale'
        if has('pop-up', 'cj hendry'): return 'Pop-ups'
        if has('bazaar', 'nubeluz', 'lobby lounge', 'the bar', 'ippudo', 'nobu', 'ice cream', 'printemps', 'poi by', 'fish co', 'mixed plate', 'star noodle', 'poke', 'breakfast', 'ferraro', 'duo', 'dinner', 'coffee'): return 'Food'
        if has('gentle monster', 'kith', 'intelligence', 'marketplace', 'holoholo', 'kūlua', 'makawao town', 'shops at', 'paʻia town'): return 'Shops'
        if tag == 'here': return 'Hotel'
        return 'Activities'
    _order = ['Hotel', 'Matcha', 'Food', 'Shops', 'Activities', 'Sample sale', 'Pop-ups']
    _g = {k: [] for k in _order}
    _skip = {'lobby and lounge','room view at dusk','the bed and the quiet','bath time, mom and baby','family perks','dogs welcome','fitness center','nap and soak','spa and steam room','last look and checkout'}
    for _s in allstops:
        if _s[0].lower() in _skip: continue
        _g[_cat(_s[0], _s[1])].append(_s[0])
    ticker = '<div class="gcats">' + ''.join(f'<details class="gcat"><summary><h3>{k}<small>{len(v)}</small></h3></summary><ul>' + ''.join(f'<li>{esc(x)}</li>' for x in v) + '</ul></details>' for k, v in _g.items() if v) + '</div>'
    _fl = [('a','c1','g0',2,'4/5',.04),('b','c2','g1',-2,'1/1',-.03),('c','c3','g2',1,'3/4',.02)]
    floats = ''.join(f'<figure class="cut float {a} {c} {gg}" style="--r:{r}deg" data-speed="{sp}"><div class="img" style="--ar:{ar}"><span class="ph"></span><img src="{CDN}{slug_h}/cover-{n+1}.jpg" alt="" onerror="this.remove()"></div></figure>' for n, (a, c, gg, r, ar, sp) in enumerate(_fl) if os.path.exists(os.path.join(ROOT, 'media', 'pitches', slug_h, f'cover-{n+1}.jpg')))
    hotel_line = ''
    if h.get('addr'):
        _mp = 'https://www.google.com/maps/search/?api=1&query=' + _up.quote(h['name'] + ', ' + h['addr'])
        hotel_line = f'<a href="{_mp}" target="_blank" rel="noopener">{esc(h["addr"])}</a><a href="{h["site"]}" target="_blank" rel="noopener">{esc(_up.urlparse(h["site"]).netloc.replace("www.",""))}</a>'
    facts = ''.join(f'<li>{esc(f)}</li>' for f in h['facts'])
    hlsec = ''
    if h.get('hl'):
        H = h['hl']
        _cf = '<span class="cf">confirm</span>'
        def _li(items):
            return ''.join(f'<li><b>{esc(a)}</b> {esc(b)}{_cf if c else ""}</li>' for a, b, c in items)
        def _w(items):
            out = ''
            for m_, nm_, q_, est_ in items:
                href_ = 'https://www.google.com/maps/search/?api=1&query=' + _up.quote(q_)
                out += f'<li class="w"><span class="m">{m_}<small>min</small></span><span><a class="pin" href="{href_}" target="_blank" rel="noopener" style="margin:0">{esc(nm_)}</a>{"<span class=cf>est.</span>" if est_ else ""}</span></li>'
            return out
        def _det(items, strip=True):
            out = ''
            for a_, b_, c_ in items:
                lead = a_.rstrip(':') if strip else a_
                out += f'<li><details><summary>{esc(lead)}{_cf if c_ else ""}</summary><p>{esc(b_[:1].upper() + b_[1:])}</p></details></li>'
            return out
        def _card(title, items, extra=''):
            return f'<div class="card"><h3>{esc(title)}</h3><ul>{_det(items)}</ul>{extra}</div>'
        walks_h = ''.join(f'<a class="walk pin" href="https://www.google.com/maps/search/?api=1&query={_up.quote(q_)}" target="_blank" rel="noopener" style="margin:0;text-decoration:none"><span class="m">{m_}<small>min</small></span><span>{esc(nm_)}{"<span class=cf>est.</span>" if est_ else ""}</span></a>' for m_, nm_, q_, est_ in H['walks'])
        care_h = ('<div class="care"><div class="kick2">' + esc(H['care_title']) + '</div><div class="cards">' + _card('A short stay', H['care']) + '</div></div>') if H.get('care') else ''
        hlsec = (f'<section class="hl rise"><div class="kick">Highlights</div><h2>{esc(H["title"])}</h2><p class="lede">{esc(H["lede"])}</p>'
                 f'<div class="walks">{walks_h}</div><p class="wn">{esc(H["walknote"])}</p>{care_h}'
                 f'<div class="cards">{_card("For baby", H["baby"])}{_card("For the dog", H["dog"])}{_card("For mom", H["mom"])}{_card("At the hotel", [(a_, b_, c_) for a_, b_, c_ in H["given"]])}</div></section>')
    intro_h = ('<section class="intro short rise"><h2>for moms&hellip;</h2><span class="tagpill">a guide to vacation with baby + puppy</span></section>' if slug_h == 'nomad' else f'<section class="intro rise"><div class="kick">The trip</div><p>{sv(S["intro"])}</p></section>')
    lobby = ('''<section class="lobby rise"><div class="pad"><div class="sheet"><div class="lh">The Ritz-Carlton<small>NoMad</small></div><div class="msg">meet you in the lobby at 4PM?</div></div><span class="pen"></span></div><div class="cap2">scroll for the guide &darr;</div></section>''' if slug_h == 'nomad' else '')
    tabs_raw = ([('ch1', S['walk']['kick'])] if 'walk' in S else []) + [(f'ch{i+1+off}', c[0]) for i, c in enumerate(S['chapters'])]
    tabs_l = []
    for tid, kk in tabs_raw:
        m_ = re.match(r'(Day \d+)', kk); lab = m_.group(1) if m_ else kk
        if not tabs_l or tabs_l[-1][1] != lab: tabs_l.append((tid, lab))
    tabs_h = ''.join(f'<a class="bd-tab" href="#{i}">{esc(t)}</a>' for i, t in tabs_l)
    rail_h = ''
    _seen = set()
    for _i, (_tid, _kk) in enumerate(tabs_raw):
        _m = re.match(r'(Day \d+)\s*·\s*(.*)', _kk); _day = _m.group(1) if _m else None
        _first = bool(_day) and _day not in _seen
        if _day: _seen.add(_day)
        _full = _m.group(2) if _m else _kk
        rail_h += f'<a href="#{_tid}" class="{"day" if _first else ""}" data-t="{_tid}"><span class="s">{esc(_day) if _first else ""}</span><span class="f">{esc((_day + " · " if _day else "") + _full)}</span><i></i></a>'
    opener = f'''<section class="bopen" aria-label="Pitch binder"><div class="bstage live"><div class="bd-book" style="--lea:#9a6b47;--lea2:#6d4529;--deb:rgba(38,20,8,.62);--debs:0 1px 0 rgba(255,228,196,.3), 0 -1px 1px rgba(0,0,0,.32)">
      <div class="bd-page">
        <div class="bd-kick bk-kick">Travel &middot; Pitch {h['no']} &middot; {esc(h['city'])}</div>
        <img class="bk-logo" src="{CDN}{slug_h}/logo.png" alt="{esc(h['short'])} logo" onerror="this.remove()">
        <h1 class="bk-name">{esc(h['name'])}</h1>
        <div class="bk-tag">{esc(h['tagline'])}</div>
        <div class="bk-hand">&mdash; {esc(h['hand'])}</div>
        <div class="bk-addr">{hotel_line}</div>
        <figure class="bk-pol">{gp.CLIP}<span class="ph"><img src="{CDN}{slug_h}/walk-room.jpg" alt="" onerror="this.remove()"></span><figcaption>a pitch by Brianne</figcaption></figure>
        <a class="bk-cue" href="#{tabs_l[0][0] if tabs_l else 'ch1'}">scroll to open the itinerary &darr;</a>
      </div>
      <nav class="bd-tabs">{tabs_h}</nav>
      <div class="bd-rings">{'<span class="bd-ring"></span>' * 6}</div>
    </div></div></section>'''
    chips = ''.join(f'<span class="chip"><i></i>{esc(v)}</span>' for v in h['vibe'])
    return f'''<!doctype html>
<html lang="en" data-season="winter">
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
<div class="hud"><a href="pitches.html#travel">&larr; All pitches</a><span class="cur">Intro</span><div class="season" role="group" aria-label="Season"><button type="button" data-v="winter" aria-pressed="true">Winter</button><button type="button" data-v="warm" aria-pressed="false">Spring &amp; Summer</button></div><span class="bar"></span></div>
<nav class="rail" aria-label="Timeline">{rail_h}</nav>

{opener}
{lobby}
{intro_h}
<div class="index"><div class="kick">In this guide</div>{ticker}</div>
{chapters}
{hlsec}

<section class="about{' solo' if h.get('hl') else ''}">
  <div class="rise"><div class="kick">Why this stay</div><h2>{esc(h.get('why_title', "The feeling I'd film"))}</h2><p>{esc(h['why'])}</p><div class="chips">{chips}</div></div>
  {'' if h.get('hl') else f'<div class="rise"><div class="kick">Highlights</div><ul class="clean">{facts}</ul></div>'}
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
