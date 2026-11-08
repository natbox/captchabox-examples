// CaptchaBox example: Express (Node.js 18+, uses the built-in fetch).
// Run: npm install express && CAPTCHABOX_SITE_KEY=... CAPTCHABOX_SECRET=... node server.js
// Test keys that always pass, on any domain: cb_test_pass / cbs_test_pass
const express = require('express');

const SITE_KEY = process.env.CAPTCHABOX_SITE_KEY || 'cb_test_pass';
const SECRET = process.env.CAPTCHABOX_SECRET || 'cbs_test_pass';

// Asks CaptchaBox whether the token from the form is valid. Each token works once, for 5 minutes.
async function verifyCaptchaBox(token) {
  if (!token) return false;
  try {
    const res = await fetch('https://captcha.natbox.io/v1/siteverify', {
      method: 'POST',
      body: new URLSearchParams({ secret: SECRET, response: token }),
      signal: AbortSignal.timeout(10000),
    });
    const data = await res.json();
    return data.success === true;
  } catch {
    return false; // could not reach CaptchaBox: refuse (or allow, if you prefer to fail open)
  }
}

// Middleware: put it in front of any POST route that takes a form.
async function requireCaptchaBox(req, res, next) {
  if (await verifyCaptchaBox(req.body['captchabox-response'])) return next();
  res.status(400).send('The captcha check failed. Please go back and try again.');
}

const app = express();
app.use(express.urlencoded({ extended: false }));

app.get('/', (req, res) => {
  res.send(`<!doctype html>
<meta charset="utf-8">
<title>Contact</title>
<script src="https://captcha.natbox.io/v1/widget.js" async defer></script>
<form method="post" action="/contact">
  <input name="email" type="email" placeholder="Your email" required>
  <div class="captchabox" data-sitekey="${SITE_KEY}"></div>
  <button>Send</button>
</form>`);
});

app.post('/contact', requireCaptchaBox, (req, res) => {
  // The visitor passed: send the email, save the message, etc.
  res.send('<p id="result">Thanks, your message was sent.</p>');
});

app.listen(process.env.PORT || 3000, () => console.log('listening on', process.env.PORT || 3000));
