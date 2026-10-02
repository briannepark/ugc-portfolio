import * as wmill from 'windmill-client';

// "Auto-fill" for the brand tracker: given just a name + website, fetches the
// site (and a likely contact/press/partnerships subpage, best effort), then
// asks an AI model — with Anthropic's native web_search tool enabled — to
// suggest a few category tags and find the best contact email for UGC/brand
// partnership outreach. A lot of retail sites don't list a partnerships email
// on their own pages, so the model can also search the web (press kits,
// "work with us"/influencer program pages, link-in-bio pages, etc.) when the
// site itself comes up empty.
//
// To keep this trustworthy, the model is never simply taken at its word: every
// email address is harvested independently — from the fetched page(s) AND
// from the raw content of the model's own response (which includes its search
// results) — and the model's final pick is only accepted if it's literally
// present in that harvested set. It can never invent/guess an address.
//
// Requires a Windmill Variable at exactly u/brianne/anthropic_api_key (an
// Anthropic API key, from console.anthropic.com — set as a secret). This is
// separate from the dashboard password and incurs a small per-use API cost
// (a bit more than before now that web search may run).
const PASSWORD_VARIABLE = 'u/brianne/brand_crm_password';
const ANTHROPIC_KEY_VARIABLE = 'u/brianne/anthropic_api_key';
const ANTHROPIC_MODEL = 'claude-haiku-4-5-20251001';

type Result =
  | { ok: true; tags: string[]; contactEmail: string; note?: string }
  | { ok: false; error: string; detail?: string };

const clean = (s: unknown, max: number) => String(s ?? '').trim().slice(0, max);

async function checkPassword(password: string): Promise<string | null> {
  const expected = String((await wmill.getVariable(PASSWORD_VARIABLE)) ?? '').trim();
  if (!expected) return "The dashboard password hasn't been set up yet — add a Windmill variable at u/brianne/brand_crm_password.";
  if (String(password ?? '').trim() !== expected) return 'Incorrect password.';
  return null;
}

function normalizeUrl(input: string): string {
  const v = input.trim();
  if (!v) return '';
  return /^https?:\/\//i.test(v) ? v : `https://${v}`;
}

async function fetchText(url: string, timeoutMs = 10000): Promise<string> {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);
  try {
    const res = await fetch(url, {
      signal: controller.signal,
      redirect: 'follow',
      headers: { 'user-agent': 'Mozilla/5.0 (compatible; brand-tracker-bot/1.0)' },
    });
    if (!res.ok) throw new Error(`${url} responded ${res.status}`);
    return await res.text();
  } finally {
    clearTimeout(timer);
  }
}

function stripHtml(html: string): string {
  return html
    .replace(/<script[\s\S]*?<\/script>/gi, ' ')
    .replace(/<style[\s\S]*?<\/style>/gi, ' ')
    .replace(/<!--[\s\S]*?-->/g, ' ')
    .replace(/<[^>]+>/g, ' ')
    .replace(/&nbsp;/g, ' ')
    .replace(/&amp;/g, '&')
    .replace(/\s+/g, ' ')
    .trim();
}

function harvestEmails(...texts: string[]): string[] {
  const found = new Set<string>();
  for (const t of texts) {
    if (!t) continue;
    const mailtoRe = /mailto:([^"'?\s>\\]+)/gi;
    let m: RegExpExecArray | null;
    while ((m = mailtoRe.exec(t))) found.add(m[1].toLowerCase());
    const emailRe = /[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}/gi;
    while ((m = emailRe.exec(t))) found.add(m[0].toLowerCase());
  }
  return Array.from(found).filter((e) => !/\.(png|jpe?g|gif|svg|webp)$/i.test(e));
}

function findContactLink(html: string, baseUrl: string): string | null {
  const hrefRe = /href=["']([^"']+)["']/gi;
  const candidates: string[] = [];
  let m: RegExpExecArray | null;
  while ((m = hrefRe.exec(html))) candidates.push(m[1]);
  const keywords = ['contact', 'partnership', 'collab', 'press', 'influencer', 'brand', 'pr-inquir', 'work-with'];
  const hit = candidates.find((href) => keywords.some((k) => href.toLowerCase().includes(k)));
  if (!hit) return null;
  try {
    return new URL(hit, baseUrl).toString();
  } catch {
    return null;
  }
}

function extractJson(text: string): any {
  const match = text.match(/\{[\s\S]*\}/);
  if (!match) throw new Error('Model response had no JSON object.');
  return JSON.parse(match[0]);
}

export async function main(password: string, name: string, website: string): Promise<Result> {
  const authError = await checkPassword(password);
  if (authError) return { ok: false, error: authError };

  const brandName = clean(name, 150);
  const url = normalizeUrl(clean(website, 300));
  if (!brandName) return { ok: false, error: 'Add a brand name first.' };
  if (!url) return { ok: false, error: 'Add a website first.' };

  const apiKey = String((await wmill.getVariable(ANTHROPIC_KEY_VARIABLE)) ?? '').trim();
  if (!apiKey) {
    return {
      ok: false,
      error: "Auto-fill isn't set up yet — add a Windmill variable at u/brianne/anthropic_api_key (your Anthropic API key).",
    };
  }

  let current = 'Fetch homepage';
  let combinedText = '';
  let combinedHtml = '';
  try {
    const homeHtml = await fetchText(url);
    combinedHtml += homeHtml;
    combinedText += stripHtml(homeHtml).slice(0, 6000);

    current = 'Fetch contact page';
    const contactUrl = findContactLink(homeHtml, url);
    if (contactUrl && contactUrl !== url) {
      try {
        const contactHtml = await fetchText(contactUrl);
        combinedHtml += ' ' + contactHtml;
        combinedText += '\n\n[Contact page]\n' + stripHtml(contactHtml).slice(0, 4000);
      } catch {
        // Best effort — fine if the guessed contact page doesn't exist.
      }
    }
  } catch (err: any) {
    return {
      ok: false,
      error: "Couldn't reach that website. Double-check the URL, or fill in tags/email yourself.",
      detail: String(err?.message ?? err).slice(0, 300),
    };
  }

  const pageEmails = harvestEmails(combinedHtml, combinedText).slice(0, 15);

  current = 'Ask AI model';
  try {
    const prompt = `You're helping categorize a brand for a UGC (user-generated content) creator's partnership tracker.

Brand name: ${brandName}
Website: ${url}

Page content already fetched (homepage, and a contact page if one was found):
"""
${combinedText.slice(0, 9000)}
"""

Email addresses already found on that page content: ${pageEmails.length ? pageEmails.join(', ') : '(none found)'}

If a good brand-partnerships/UGC/influencer contact email isn't among those, use the web_search tool to look for one — try the brand's press kit, an "ambassador"/"influencer program"/"work with us" page, or their Instagram/TikTok bio link page (e.g. a linktr.ee or similar), searching things like "${brandName} influencer partnerships contact" or "${brandName} UGC creator program email". Only do this if needed — if a good email is already in the list above, don't bother searching.

Once you're done, respond with ONLY a JSON object as your final answer, no other text, in this exact shape:
{"tags": ["tag1", "tag2"], "contactEmail": "the best address you found, or null", "note": "one short sentence, or null"}

Rules:
- tags: 2-5 short lowercase category/niche words for this brand (e.g. "skincare", "fitness", "home decor", "pet", "recurring"). Base them only on what the page actually describes.
- contactEmail: must be an email address you ACTUALLY SAW written somewhere (on the fetched page, or in a search result) — never invent, guess, or construct one from a pattern (like "info@" + domain) unless you saw that exact address written out. Prefer one that sounds right for brand partnerships/UGC/influencer outreach (containing words like partnerships, pr, marketing, collab, influencer, brand, hello, press) over a personal-looking one. If you found nothing suitable, return null.
- note: a short one-sentence explanation of where the email came from (e.g. "found on their press kit page"), or null if contactEmail is null.`;

    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), 45000);
    let res: Response;
    try {
      res = await fetch('https://api.anthropic.com/v1/messages', {
        method: 'POST',
        signal: controller.signal,
        headers: {
          'content-type': 'application/json',
          'x-api-key': apiKey,
          'anthropic-version': '2023-06-01',
        },
        body: JSON.stringify({
          model: ANTHROPIC_MODEL,
          max_tokens: 1500,
          messages: [{ role: 'user', content: prompt }],
          tools: [{ type: 'web_search_20250305', name: 'web_search', max_uses: 4 }],
        }),
      });
    } finally {
      clearTimeout(timer);
    }

    if (!res.ok) {
      const bodyText = await res.text().catch(() => '');
      throw new Error(`Anthropic API responded ${res.status}: ${bodyText.slice(0, 300)}`);
    }

    const data: any = await res.json();
    const contentBlocks: any[] = Array.isArray(data?.content) ? data.content : [];
    // The final JSON answer is in the last text block; everything in the
    // response (including search results) is fair game for harvesting real
    // email addresses to validate that answer against.
    const textBlocks = contentBlocks.filter((b) => b?.type === 'text').map((b) => b.text ?? '');
    const lastText = textBlocks[textBlocks.length - 1] ?? '';
    const parsed = extractJson(lastText);

    const searchEmails = harvestEmails(JSON.stringify(contentBlocks));
    const allowedEmails = new Set([...pageEmails, ...searchEmails]);

    const tags = Array.isArray(parsed.tags)
      ? parsed.tags.map((t: unknown) => clean(t, 40)).filter(Boolean).slice(0, 5)
      : [];
    let contactEmail = clean(parsed.contactEmail, 200).toLowerCase();
    // Defense in depth: only ever accept an email that was actually seen
    // somewhere (fetched page or search results), regardless of what the
    // model's final answer claims.
    if (contactEmail && !allowedEmails.has(contactEmail)) contactEmail = '';
    const note = clean(parsed.note, 300);

    return { ok: true, tags, contactEmail, note: note || undefined };
  } catch (err: any) {
    return {
      ok: false,
      error: `Could not auto-fill from that website (${current.toLowerCase()} failed). Please fill in tags/email yourself.`,
      detail: String(err?.message ?? err).slice(0, 300),
    };
  }
}
