import * as wmill from 'windmill-client';
import nodemailer from 'nodemailer';

// Everything lives in your Windmill workspace (not in this repo):
//   - SMTP resource (type "smtp"): host, port, user, password
//     (reusing the same one set up for brixx-first-birthday: u/brianne/rsvp_smtp)
//   - Variable: the address that should receive contact-form messages.
//     This is a NEW, separate variable from the RSVP notify-email — create it
//     at exactly u/brianne/contact_notify_email with value parkbrianne@gmail.com.
const SMTP_RESOURCE = 'u/brianne/rsvp_smtp';
const NOTIFY_EMAIL_VARIABLE = 'u/brianne/contact_notify_email';

type Result = { ok: true } | { ok: false; error: string; detail?: string };

const clean = (s: unknown, max: number) => String(s ?? '').trim().slice(0, max);
const isEmail = (s: string) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(s);

function describeError(err: unknown) {
  const e = err as any;
  const parts = [e?.message ?? String(err)];
  if (e?.code) parts.push(`code ${e.code}`);
  if (e?.responseCode) parts.push(`SMTP ${e.responseCode}`);
  if (e?.response && e.response !== e.message) parts.push(String(e.response));
  if (e?.command) parts.push(`during ${e.command}`);
  return parts.join(' | ').slice(0, 600);
}

// Explain the errors people actually hit, in plain words.
function hint(detail: string) {
  const d = detail.toLowerCase();
  if (d.includes('rsvp_smtp') && (d.includes('not found') || d.includes('404') || d.includes('does not exist')))
    return 'SMTP resource not found: create it at exactly u/brianne/rsvp_smtp.';
  if (d.includes('contact_notify_email') && (d.includes('not found') || d.includes('404') || d.includes('does not exist')))
    return 'Notify-email variable not found: create it at exactly u/brianne/contact_notify_email.';
  if (d.includes('535') || d.includes('badcredentials') || d.includes('username and password not accepted') || d.includes('eauth'))
    return 'Gmail rejected the login: use a 16-character app password (not your normal password) and your full Gmail address as user.';
  if (d.includes('etimedout') || d.includes('econnrefused') || d.includes('enotfound') || d.includes('esocket'))
    return 'Could not reach the mail server: check host smtp.gmail.com and port 465.';
  if (d.includes('no recipients') || d.includes('eenvelope'))
    return 'No valid "to" address: check the value of u/brianne/contact_notify_email.';
  return '';
}

const esc = (s: unknown) =>
  String(s ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]!);

function toHtml(name: string, email: string, message: string) {
  const C = { green: '#A4502B', dark: '#17140F', cream: '#F4F1E7', paper: '#ECE7D8', line: 'rgba(23,20,15,0.14)', muted: '#524C3E' };
  const FONT = `font-family:'Helvetica Neue',Arial,sans-serif;`;
  return `<!doctype html><html><body style="margin:0;padding:0;background:${C.paper};">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:${C.paper};"><tr><td align="center" style="padding:24px 12px;">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="max-width:600px;background:#ffffff;border-radius:12px;overflow:hidden;border:1px solid ${C.line};">
  <tr><td style="background:${C.dark};padding:22px 24px;${FONT}">
    <div style="font-size:12px;letter-spacing:2px;text-transform:uppercase;color:${C.cream};opacity:.85;">Portfolio site · New contact message</div>
    <div style="margin-top:6px;font-size:18px;color:${C.cream};line-height:1.4;">${esc(name)} sent a brief</div>
  </td></tr>
  <tr><td style="padding:22px 24px;${FONT}font-size:14px;color:${C.dark};line-height:1.6;">
    <div style="margin-bottom:10px;"><b>From:</b> ${esc(name)} &lt;${esc(email)}&gt;</div>
    <div style="white-space:pre-wrap;padding:14px 16px;background:${C.paper};border:1px solid ${C.line};border-radius:8px;">${esc(message)}</div>
  </td></tr>
  <tr><td style="padding:0 24px 22px;${FONT}font-size:12px;color:${C.muted};">Reply directly to this email to get back to them.</td></tr>
</table>
</td></tr></table></body></html>`;
}

function toText(name: string, email: string, message: string) {
  return [`New contact message from ${name} <${email}>`, '', message].join('\n');
}

// ── Entry point ──────────────────────────────────────────────────────────
export async function main(
  name: string,
  email: string,
  message: string,
  website: string = '', // honeypot: people never see this field, bots fill it
): Promise<Result> {
  if (clean(website, 200)) return { ok: true };

  const n = clean(name, 100);
  const e = clean(email, 200);
  const m = clean(message, 4000);
  if (!n) return { ok: false, error: 'Please add your name.' };
  if (!isEmail(e)) return { ok: false, error: 'Please add a valid email so I can reply.' };
  if (!m) return { ok: false, error: 'Please add a short brief.' };

  let current = 'Load SMTP resource';
  try {
    const smtp: any = await wmill.getResource(SMTP_RESOURCE);
    const missing = ['host', 'port', 'user', 'password'].filter((f) => !smtp?.[f]);
    if (missing.length) throw new Error(`SMTP resource is missing: ${missing.join(', ')}`);

    current = 'Load notify-email variable';
    const to = String((await wmill.getVariable(NOTIFY_EMAIL_VARIABLE)) ?? '').trim();
    if (!to.includes('@')) throw new Error(`Variable value doesn't look like an email address: "${to}"`);

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
      from: `"Portfolio site" <${smtp.user}>`,
      to,
      replyTo: `"${n}" <${e}>`,
      subject: `New contact message from ${n}`,
      text: toText(n, e, m),
      html: toHtml(n, e, m),
    });
    const rejected = (info.rejected ?? []).map(String);
    if (rejected.length) throw new Error(`Mail server rejected: ${rejected.join(', ')} (${info.response ?? ''})`);

    return { ok: true };
  } catch (err) {
    const d = describeError(err);
    const h = hint(`${current} ${d}`);
    console.log(`✘ ${current} — ${d}`);
    return { ok: false, error: 'Something went wrong sending that. Please try again.', detail: h || d };
  }
}
