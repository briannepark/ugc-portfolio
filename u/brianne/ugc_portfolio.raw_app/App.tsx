import React, { useEffect, useRef, useState } from 'react';
import { HOME_HTML, GALLERY_HTML, CONTACT_HTML, BRANDS_HTML } from './pages.generated';
import { backend } from './wmill';

type Page = 'home' | 'gallery' | 'contact' | 'brands';

const PAGES: Record<Page, string> = {
  home: HOME_HTML,
  gallery: GALLERY_HTML,
  contact: CONTACT_HTML,
  brands: BRANDS_HTML,
};

function getInitialState(): { page: Page; hash: string } {
  if (typeof window === 'undefined') return { page: 'home', hash: '' };
  const params = new URLSearchParams(window.location.search);
  const p = params.get('page');
  // "brands" is the private brand-outreach dashboard — reached directly via
  // ?page=brands, never linked from the public nav.
  const page: Page = p === 'gallery' ? 'gallery' : p === 'contact' ? 'contact' : p === 'brands' ? 'brands' : 'home';
  return { page, hash: window.location.hash || '' };
}

export default function App() {
  const [page, setPage] = useState<Page>(() => getInitialState().page);
  const pendingHash = useRef<string>(getInitialState().hash);
  const iframeRef = useRef<HTMLIFrameElement | null>(null);

  // Keep the URL shareable/bookmarkable as the visitor navigates inside the app.
  // Windmill's public (guest) runtime executes this bundle from a `blob:` document,
  // where history.replaceState can't rewrite the address to a different origin/URL
  // shape — that throws a SecurityError there, even though it works fine in the
  // authenticated editor preview (served normally, not from a blob). Harmless to
  // skip: page switching itself is handled by React state + postMessage below,
  // this effect is purely a "nice to have" for bookmarking/sharing a direct link.
  useEffect(() => {
    try {
      const url = new URL(window.location.href);
      url.searchParams.set('page', page);
      window.history.replaceState(null, '', url.toString());
    } catch {
      // Not bookmarkable in this runtime context — navigation still works.
    }
  }, [page]);

  // Listen for navigation requests posted by the embedded page (see the bridge
  // script appended to /site/index.html, /site/gallery.html and /site/contact.html),
  // and for contact-form submissions from /site/contact.html.
  useEffect(() => {
    function onMessage(e: MessageEvent) {
      const data = e.data;
      if (!data || typeof data !== 'object') return;
      if (data.type === 'ugc-nav') {
        const nextPage: Page =
          data.page === 'gallery' ? 'gallery' : data.page === 'contact' ? 'contact' : data.page === 'brands' ? 'brands' : 'home';
        pendingHash.current = data.hash || '';
        if (nextPage === page) {
          // Same page, just scroll (e.g. in-page nav links).
          iframeRef.current?.contentWindow?.postMessage(
            { type: 'ugc-scroll', hash: pendingHash.current },
            '*'
          );
        } else {
          setPage(nextPage);
        }
      } else if (data.type === 'ugc-contact-submit') {
        (async () => {
          try {
            const res: any = await backend.submit_contact({
              name: data.name,
              email: data.email,
              message: data.message,
              website: data.website || '',
              attachments: Array.isArray(data.attachments) ? data.attachments : [],
            });
            iframeRef.current?.contentWindow?.postMessage(
              res?.ok
                ? { type: 'ugc-contact-result', ok: true }
                : { type: 'ugc-contact-result', ok: false, error: res?.error, detail: res?.detail },
              '*'
            );
          } catch (err: any) {
            iframeRef.current?.contentWindow?.postMessage(
              { type: 'ugc-contact-result', ok: false, error: 'Something went wrong sending that. Please try again.', detail: err?.message },
              '*'
            );
          }
        })();
      } else if (data.type === 'ugc-brands-call') {
        // Generic action dispatcher for the private /brands dashboard — see
        // site/brands.html. Each call carries a requestId so the dashboard can
        // correlate multiple concurrent async actions (unlike the single-in-flight
        // contact form above).
        (async () => {
          const requestId = data.requestId;
          try {
            let res: any;
            const payload = data.payload || {};
            switch (data.action) {
              case 'list':
                res = await backend.brands_list({ password: payload.password });
                break;
              case 'save':
                res = await backend.brands_save({ password: payload.password, brand: payload.brand });
                break;
              case 'delete':
                res = await backend.brands_delete({ password: payload.password, id: payload.id });
                break;
              case 'send_outreach':
                res = await backend.brands_send_outreach({
                  password: payload.password,
                  id: payload.id,
                  subject: payload.subject,
                  message: payload.message,
                });
                break;
              case 'enrich':
                res = await backend.brands_enrich({
                  password: payload.password,
                  name: payload.name,
                  website: payload.website,
                });
                break;
              default:
                res = { ok: false, error: 'Unknown action.' };
            }
            iframeRef.current?.contentWindow?.postMessage(
              { type: 'ugc-brands-result', requestId, ...res },
              '*'
            );
          } catch (err: any) {
            iframeRef.current?.contentWindow?.postMessage(
              {
                type: 'ugc-brands-result',
                requestId,
                ok: false,
                error: 'Something went wrong. Please try again.',
                detail: err?.message,
              },
              '*'
            );
          }
        })();
      }
    }
    window.addEventListener('message', onMessage);
    return () => window.removeEventListener('message', onMessage);
  }, [page]);

  // After the iframe (re)loads a new page, tell it to scroll to any pending hash.
  function handleIframeLoad() {
    if (pendingHash.current) {
      iframeRef.current?.contentWindow?.postMessage(
        { type: 'ugc-scroll', hash: pendingHash.current },
        '*'
      );
      pendingHash.current = '';
    }
  }

  return (
    <div style={{ width: '100%', height: '100vh', margin: 0, padding: 0 }}>
      <iframe
        key={page}
        ref={iframeRef}
        title="Brianne — portfolio"
        srcDoc={PAGES[page]}
        onLoad={handleIframeLoad}
        sandbox="allow-scripts allow-same-origin allow-popups allow-forms allow-top-navigation-by-user-activation"
        style={{ width: '100%', height: '100%', border: 'none', display: 'block' }}
      />
    </div>
  );
}
