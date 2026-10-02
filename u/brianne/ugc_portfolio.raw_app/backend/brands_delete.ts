import * as wmill from 'windmill-client';

const PASSWORD_VARIABLE = 'u/brianne/brand_crm_password';
const BRANDS_STORE = 'u/brianne/brand_crm_brands';

async function checkPassword(password: string): Promise<string | null> {
  const expected = String((await wmill.getVariable(PASSWORD_VARIABLE)) ?? '').trim();
  if (!expected) return "The dashboard password hasn't been set up yet — add a Windmill variable at u/brianne/brand_crm_password.";
  if (String(password ?? '').trim() !== expected) return 'Incorrect password.';
  return null;
}

export async function main(
  password: string,
  id: string,
): Promise<{ ok: true; brands: any[] } | { ok: false; error: string }> {
  const authError = await checkPassword(password);
  if (authError) return { ok: false, error: authError };

  const stored = await wmill.getState(BRANDS_STORE);
  const list: any[] = Array.isArray(stored?.brands) ? stored.brands : [];
  const next = list.filter((b) => b?.id !== id);
  await wmill.setState({ brands: next }, BRANDS_STORE);
  next.sort((a: any, b: any) => String(b.updatedAt).localeCompare(String(a.updatedAt)));
  return { ok: true, brands: next };
}
