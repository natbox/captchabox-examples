// Server-side check. Import only from server code (Server Actions, Route Handlers).
// Each token works once, for 5 minutes.
export async function verifyCaptchaBox(token: unknown): Promise<boolean> {
  if (typeof token !== 'string' || token === '') return false;
  try {
    const res = await fetch('https://captcha.natbox.io/v1/siteverify', {
      method: 'POST',
      body: new URLSearchParams({ secret: process.env.CAPTCHABOX_SECRET ?? '', response: token }),
      cache: 'no-store',
      signal: AbortSignal.timeout(10_000),
    });
    const data = await res.json();
    return data.success === true;
  } catch {
    return false;
  }
}
