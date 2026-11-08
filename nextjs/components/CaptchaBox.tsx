'use client';

import { useEffect, useRef } from 'react';

declare global {
  interface Window {
    captchabox?: {
      render: (el: HTMLElement, opts: Record<string, unknown>) => number;
      reset: (el?: HTMLElement) => void;
    };
  }
}

const SRC = 'https://captcha.natbox.io/v1/widget.js';

// Loads the widget once and renders it into this element. It adds a hidden
// "captchabox-response" field to the surrounding <form>.
// Change `resetKey` (e.g. after each submit) to get a fresh token.
export default function CaptchaBox({ siteKey, theme = 'auto', resetKey }: { siteKey: string; theme?: 'auto' | 'light' | 'dark'; resetKey?: unknown }) {
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    const render = () => window.captchabox?.render(el, { sitekey: siteKey, theme });
    if (window.captchabox) return void render();
    let s = document.querySelector<HTMLScriptElement>(`script[src="${SRC}"]`);
    if (!s) {
      s = document.createElement('script');
      s.src = SRC;
      s.async = true;
      document.head.appendChild(s);
    }
    s.addEventListener('load', render, { once: true });
  }, [siteKey, theme]);

  useEffect(() => {
    if (resetKey !== undefined && ref.current && window.captchabox) window.captchabox.reset(ref.current);
  }, [resetKey]);

  return <div ref={ref} />;
}
