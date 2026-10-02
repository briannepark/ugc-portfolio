import * as wmill from 'windmill-client';

// Private brand-outreach dashboard (site/brands.html — not linked from the
// public nav, reached directly at ?page=brands). Gated by a password stored
// as a Windmill variable, checked on every call (not just client-side), so
// the data stays private even though this app's backend is reachable by
// anyone who knows the script name.
const PASSWORD_VARIABLE = 'u/brianne/brand_crm_password';
const BRANDS_STORE = 'u/brianne/brand_crm_brands';

export type Brand = {
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

export async function checkPassword(password: string): Promise<string | null> {
  const expected = String((await wmill.getVariable(PASSWORD_VARIABLE)) ?? '').trim();
  if (!expected) return "The dashboard password hasn't been set up yet — add a Windmill variable at u/brianne/brand_crm_password.";
  if (String(password ?? '').trim() !== expected) return 'Incorrect password.';
  return null;
}

export async function readAll(): Promise<Brand[]> {
  const stored = await wmill.getState(BRANDS_STORE);
  const list: any[] = Array.isArray(stored?.brands) ? stored.brands : [];
  return list.map((b) => ({
    id: String(b?.id ?? ''),
    name: String(b?.name ?? ''),
    website: String(b?.website ?? ''),
    contactEmail: String(b?.contactEmail ?? ''),
    tags: Array.isArray(b?.tags) ? b.tags.map(String) : [],
    status: String(b?.status ?? 'not_contacted'),
    rate: String(b?.rate ?? ''),
    notes: String(b?.notes ?? ''),
    history: Array.isArray(b?.history) ? b.history : [],
    createdAt: String(b?.createdAt ?? b?.updatedAt ?? new Date().toISOString()),
    updatedAt: String(b?.updatedAt ?? b?.createdAt ?? new Date().toISOString()),
  }));
}

export async function main(password: string): Promise<{ ok: true; brands: Brand[] } | { ok: false; error: string }> {
  const authError = await checkPassword(password);
  if (authError) return { ok: false, error: authError };

  const brands = await readAll();
  brands.sort((a, b) => b.updatedAt.localeCompare(a.updatedAt));
  return { ok: true, brands };
}
