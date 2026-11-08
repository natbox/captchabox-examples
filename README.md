# CaptchaBox examples

Ready-to-run examples for [CaptchaBox](https://captcha.natbox.io/), a free, private captcha: no image puzzles, no cookies, no tracking. The visitor's browser does about a second of proof-of-work in the background, and your server checks the result.

Free for 10,000 checks a month. Get keys at [my.natbox.io/captchabox](https://my.natbox.io/captchabox).

| Folder | Stack | Guide |
|---|---|---|
| [`html-php`](html-php) | Plain PHP, one file | [docs/php](https://captcha.natbox.io/docs/php) |
| [`laravel`](laravel) | Laravel 10+ validation rule | [docs/laravel](https://captcha.natbox.io/docs/laravel) |
| [`express`](express) | Node.js + Express middleware | [docs/nodejs](https://captcha.natbox.io/docs/nodejs) |
| [`nextjs`](nextjs) | Next.js App Router, Server Action | [docs/nextjs](https://captcha.natbox.io/docs/nextjs) |
| [`flask`](flask) | Flask decorator | [docs/flask](https://captcha.natbox.io/docs/flask) |
| [`django`](django) | Django form field | [docs/django](https://captcha.natbox.io/docs/django) |

WordPress? Use the plugin: [docs/wordpress](https://captcha.natbox.io/docs/wordpress).

## How it works

1. Add the widget to your form:

   ```html
   <script src="https://captcha.natbox.io/v1/widget.js" async defer></script>
   <div class="captchabox" data-sitekey="YOUR_SITE_KEY"></div>
   ```

   It puts a one-time token in a hidden field named `captchabox-response`.

2. On your server, check the token before you accept the form:

   ```
   POST https://captcha.natbox.io/v1/siteverify
   secret=YOUR_SECRET&response=TOKEN
   → {"success": true, "challenge_ts": "...", "hostname": "example.com", "error-codes": []}
   ```

Each token works once, for 5 minutes. The API answers like reCAPTCHA's and Turnstile's, so switching is quick: [docs/switch-from-recaptcha](https://captcha.natbox.io/docs/switch-from-recaptcha).

## Test keys

Every example runs out of the box with the test keys, which work on any domain (including localhost) and are not counted:

| Site key | Secret | Result |
|---|---|---|
| `cb_test_pass` | `cbs_test_pass` | always passes |
| `cb_test_fail` | `cbs_test_fail` | always fails |

Set `CAPTCHABOX_SITE_KEY` and `CAPTCHABOX_SECRET` to your own keys before going live.

## Links

- Full documentation: https://captcha.natbox.io/docs
- Service status: https://status.natbox.io
- Privacy: https://natbox.io/privacy#captchabox

License: MIT
