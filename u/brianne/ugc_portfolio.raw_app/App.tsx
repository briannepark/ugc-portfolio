import React, { useEffect, useRef, useState } from 'react';
import { HOME_HTML, GALLERY_HTML } from './pages.generated';

type Page = 'home' | 'gallery';

const PAGES: Record<Page, string> = {
  home: HOME_HTML,
  gallery: GALLERY_HTML,
};

function getInitialState(): { page: Page; hash: string } {
  if (typeof window === 'undefined') return { page: 'home', hash: '' };
  const params = new URLSearchParams(window.location.search);
  const page = params.get('page') === 'gallery' ? 'gallery' : 'home';
  return { page, hash: window.location.hash || '' };
}

export default function App() {
  const [page, setPage] = useState<Page>(() => getInitialState().page);
  const pendingHash = useRef<string>(getInitialState().hash);
  const iframeRef = useRef<HTMLIFrameElement | null>(null);

  // Keep the URL shareable/bookmarkable as the visitor navigates inside the app.
  useEffect(() => {
    const url = new URL(window.location.href);
    url.searchParams.set('page', page);
    window.history.replaceState(null, '', url.toString());
  }, [page]);

  // Listen for navigation requests posted by the embedded page (see the bridge
  // script appended to /site/index.html and /site/gallery.html).
  useEffect(() => {
    function onMessage(e: MessageEvent) {
      const data = e.data;
      if (!data || typeof data !== 'object') return;
      if (data.type === 'ugc-nav') {
        const nextPage: Page = data.page === 'gallery' ? 'gallery' : 'home';
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
