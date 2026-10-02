import * as wmill from 'windmill-client';

const PASSWORD_VARIABLE = 'u/brianne/brand_crm_password';
const BRANDS_STORE = 'u/brianne/brand_crm_brands';
const STATUSES = ['not_contacted', 'contacted', 'responded', 'negotiating', 'deal', 'passed'];

type Brand = {
  id: string;
  name: string;
  website: string;
  contactEmail: string;
  tags: string[];
  status: string;
  rate: string;
  notes: string;
  history: { at: string; type: string; text: string }[];
  createdAt: string;
  updatedAt: string;
};

type Input = {
  id?: string;
  name?: string;
  website?: string;
  contactEmail?: string;
  tags?: string[];
  status?: string;
  rate?: string;
  notes?: string;
  // Optional free-text note appended to the history timeline for this edit
  // (e.g. "Replied — interested, wants a rate quote").
  historyNote?: string;
};

const clean = (s: unknown, max: number) => String(s ?? '').trim().slice(0, max);
const isEmail = (s: string) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(s);

async function checkPassword(password: string): Promise<string | null> {
  const expected = String((await wmill.getVariable(PASSWORD_VARIABLE)) ?? '').trim();
  if (!expected) return "The dashboard password hasn't been set up yet — add a Windmill variable at u/brianne/brand_crm_password.";
  if (String(password ?? '').trim() !== expected) return 'Incorrect password.';
  return null;
}

async function readAll(): Promise<Brand[]> {
  const stored = await wmill.getState(BRANDS_STORE);
  const list: any[] = Array.isArray(stored?.brands) ? stored.brands : [];
  return list;
}

export async function main(
  password: string,
  brand: Input,
): Promise<{ ok: true; brand: Brand; brands: Brand[] } | { ok: false; error: string }> {
  const authError = await checkPassword(password);
  if (authError) return { ok: false, error: authError };

  const name = clean(brand?.name, 150);
  if (!name) return { ok: false, error: 'Please add a brand name.' };

  const contactEmail = clean(brand?.contactEmail, 200);
  if (contactEmail && !isEmail(contactEmail)) return { ok: false, error: "That contact email doesn't look valid." };

  const status = STATUSES.includes(String(brand?.status)) ? String(brand?.status) : undefined;
  const tags = Array.isArray(brand?.tags)
    ? brand.tags.map((t) => clean(t, 40)).filter(Boolean).slice(0, 10)
    : undefined;
  const website = brand?.website !== undefined ? clean(brand.website, 300) : undefined;
  const rate = brand?.rate !== undefined ? clean(brand.rate, 200) : undefined;
  const notes = brand?.notes !== undefined ? clean(brand.notes, 5000) : undefined;
  const historyNote = clean(brand?.historyNote, 500);

  const now = new Date().toISOString();
  const all = await readAll();
  const id = clean(brand?.id, 60);
  let result: Brand;

  if (id) {
    const idx = all.findIndex((b) => b.id === id);
    if (idx === -1) return { ok: false, error: 'That brand no longer exists.' };
    const existing = all[idx];
    const history = Array.isArray(existing.history) ? existing.history.slice() : [];
    if (historyNote) {
      history.unshift({
        at: now,
        type: status && status !== existing.status ? 'status_change' : 'note',
        text: historyNote,
      });
    }
    result = {
      ...existing,
      name,
      website: website ?? existing.website ?? '',
      contactEmail: contactEmail || existing.contactEmail || '',
      tags: tags ?? existing.tags ?? [],
      status: status ?? existing.status ?? 'not_contacted',
      rate: rate ?? existing.rate ?? '',
      notes: notes ?? existing.notes ?? '',
      history,
      updatedAt: now,
    };
    all[idx] = result;
  } else {
    result = {
      id: `${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 8)}`,
      name,
      website: website ?? '',
      contactEmail,
      tags: tags ?? [],
      status: status ?? 'not_contacted',
      rate: rate ?? '',
      notes: notes ?? '',
      history: [{ at: now, type: 'created', text: historyNote || 'Added to the tracker.' }],
      createdAt: now,
      updatedAt: now,
    };
    all.push(result);
  }

  await wmill.setState({ brands: all }, BRANDS_STORE);
  all.sort((a, b) => b.updatedAt.localeCompare(a.updatedAt));
  return { ok: true, brand: result, brands: all };
}
