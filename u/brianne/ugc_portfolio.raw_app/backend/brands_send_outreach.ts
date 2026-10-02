import * as wmill from 'windmill-client';
import nodemailer from 'nodemailer';

const PASSWORD_VARIABLE = 'u/brianne/brand_crm_password';
const BRANDS_STORE = 'u/brianne/brand_crm_brands';
// Reuses the SMTP resource already set up for brixx-first-birthday and the
// contact form.
const SMTP_RESOURCE = 'u/brianne/rsvp_smtp';
// Your own email (same one contact-form notifications go to) — set as the
// reply-to, so a brand's reply lands in your inbox, not the SMTP account's.
const REPLY_TO_VARIABLE = 'u/brianne/contact_notify_email';

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

const clean = (s: unknown, max: number) => String(s ?? '').trim().slice(0, max);
const isEmail = (s: string) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(s);

async function checkPassword(password: string): Promise<string | null> {
  const expected = String((await wmill.getVariable(PASSWORD_VARIABLE)) ?? '').trim();
  if (!expected) return "The dashboard password hasn't been set up yet — add a Windmill variable at u/brianne/brand_crm_password.";
  if (String(password ?? '').trim() !== expected) return 'Incorrect password.';
  return null;
}

function describeError(err: unknown) {
  const e = err as any;
  const parts = [e?.message ?? String(err)];
  if (e?.code) parts.push(`code ${e.code}`);
  if (e?.responseCode) parts.push(`SMTP ${e.responseCode}`);
  if (e?.response && e.response !== e.message) parts.push(String(e.response));
  if (e?.command) parts.push(`during ${e.command}`);
  return parts.join(' | ').slice(0, 600);
}

function hint(detail: string) {
  const d = detail.toLowerCase();
  if (d.includes('rsvp_smtp') && (d.includes('not found') || d.includes('404') || d.includes('does not exist')))
    return 'SMTP resource not found: create it at exactly u/brianne/rsvp_smtp.';
  if (d.includes('535') || d.includes('badcredentials') || d.includes('username and password not accepted') || d.includes('eauth'))
    return 'Gmail rejected the login: use a 16-character app password (not your normal password) and your full Gmail address as user.';
  if (d.includes('etimedout') || d.includes('econnrefused') || d.includes('enotfound') || d.includes('esocket'))
    return 'Could not reach the mail server: check host smtp.gmail.com and port 465.';
  if (d.includes('no recipients') || d.includes('eenvelope'))
    return "No valid recipient — check this brand's contact email.";
  return '';
}

const esc = (s: unknown) =>
  String(s ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]!);

function toHtml(message: string) {
  return `<div style="font-family:'Helvetica Neue',Arial,sans-serif;font-size:15px;line-height:1.6;color:#17140F;white-space:pre-wrap;">${esc(message)}</div>`;
}

export async function main(
  password: string,
  id: string,
  subject: string,
  message: string,
): Promise<{ ok: true; brand: Brand } | { ok: false; error: string; detail?: string }> {
  const authError = await checkPassword(password);
  if (authError) return { ok: false, error: authError };

  const subj = clean(subject, 200);
  const msg = clean(message, 8000);
  if (!subj) return { ok: false, error: 'Please add a subject line.' };
  if (!msg) return { ok: false, error: 'Please write a message.' };

  const stored = await wmill.getState(BRANDS_STORE);
  const list: Brand[] = Array.isArray(stored?.brands) ? stored.brands : [];
  const idx = list.findIndex((b) => b?.id === id);
  if (idx === -1) return { ok: false, error: 'That brand no longer exists.' };
  const brand = list[idx];

  if (!isEmail(brand.contactEmail)) return { ok: false, error: "This brand doesn't have a valid contact email yet." };

  let current = 'Load SMTP resource';
  try {
    const smtp: any = await wmill.getResource(SMTP_RESOURCE);
    const missing = ['host', 'port', 'user', 'password'].filter((f) => !smtp?.[f]);
    if (missing.length) throw new Error(`SMTP resource is missing: ${missing.join(', ')}`);

    current = 'Load reply-to variable';
    const replyTo = String((await wmill.getVariable(REPLY_TO_VARIABLE)) ?? '').trim();

    current = 'Connect and log in to mail server';
    const port = Number(smtp.port ?? 465);
    const transporter = nodemailer.createTransport({
      host: smtp.host,
      port,
      secure: port === 465,
      auth: { user: smtp.user, pass: String(smtp.password).replace(/\s+/g, '') },
      connectionTimeout: 15000,
      greetingTimeout: 15000,
    });
    await transporter.verify();

    current = 'Send email';
    const info = await transporter.sendMail({
      from: `"Brianne — UGC Partnerships" <${smtp.user}>`,
      to: brand.contactEmail,
      ...(replyTo.includes('@') ? { replyTo } : {}),
      subject: subj,
      text: msg,
      html: toHtml(msg),
    });
    const rejected = (info.rejected ?? []).map(String);
    if (rejected.length) throw new Error(`Mail server rejected: ${rejected.join(', ')} (${info.response ?? ''})`);
  } catch (err) {
    const d = describeError(err);
    const h = hint(`${current} ${d}`);
    console.log(`✘ ${current} — ${d}`);
    return { ok: false, error: 'Could not send that email. Please try again.', detail: h || d };
  }

  const now = new Date().toISOString();
  const history = Array.isArray(brand.history) ? brand.history.slice() : [];
  history.unshift({ at: now, type: 'outreach_sent', text: subj });
  const updated: Brand = {
    ...brand,
    status: brand.status === 'not_contacted' ? 'contacted' : brand.status,
    history,
    updatedAt: now,
  };
  list[idx] = updated;
  await wmill.setState({ brands: list }, BRANDS_STORE);

  return { ok: true, brand: updated };
}
