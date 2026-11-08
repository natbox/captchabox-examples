'use client';

import { useActionState } from 'react';
import CaptchaBox from '@/components/CaptchaBox';
import { sendMessage } from './actions';

export default function ContactForm() {
  const [state, action, pending] = useActionState(sendMessage, null);
  return (
    <form action={action}>
      {state && <p id="result">{state.message}</p>}
      <input name="email" type="email" placeholder="Your email" required />
      {/* a token works once, so get a new one after every send */}
      <CaptchaBox siteKey={process.env.NEXT_PUBLIC_CAPTCHABOX_SITE_KEY!} resetKey={state} />
      <button disabled={pending}>Send</button>
    </form>
  );
}
