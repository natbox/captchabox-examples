'use server';

import { verifyCaptchaBox } from '@/lib/captchabox';

export type State = { ok: boolean; message: string } | null;

export async function sendMessage(_prev: State, formData: FormData): Promise<State> {
  if (!(await verifyCaptchaBox(formData.get('captchabox-response')))) {
    return { ok: false, message: 'The captcha check failed. Please try again.' };
  }
  // The visitor passed: send the email, save the message, etc.
  return { ok: true, message: 'Thanks, your message was sent.' };
}
