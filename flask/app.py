"""CaptchaBox example: Flask.
Run: pip install flask && CAPTCHABOX_SITE_KEY=... CAPTCHABOX_SECRET=... flask --app app run
Test keys that always pass, on any domain: cb_test_pass / cbs_test_pass
"""
import json
import os
import urllib.parse
import urllib.request
from functools import wraps

from flask import Flask, abort, render_template_string, request

SITE_KEY = os.environ.get("CAPTCHABOX_SITE_KEY", "cb_test_pass")
SECRET = os.environ.get("CAPTCHABOX_SECRET", "cbs_test_pass")

app = Flask(__name__)


def verify_captchabox(token):
    """Asks CaptchaBox whether the token from the form is valid. Each token works once, for 5 minutes."""
    if not token:
        return False
    data = urllib.parse.urlencode({"secret": SECRET, "response": token}).encode()
    try:
        with urllib.request.urlopen("https://captcha.natbox.io/v1/siteverify", data, timeout=10) as r:
            return json.load(r).get("success") is True
    except OSError:
        return False  # could not reach CaptchaBox


def captchabox_required(view):
    """Decorator for POST views that take a form."""
    @wraps(view)
    def wrapper(*args, **kwargs):
        if request.method == "POST" and not verify_captchabox(request.form.get("captchabox-response", "")):
            abort(400, "The captcha check failed. Please go back and try again.")
        return view(*args, **kwargs)
    return wrapper


PAGE = """<!doctype html>
<meta charset="utf-8">
<title>Contact</title>
<script src="https://captcha.natbox.io/v1/widget.js" async defer></script>
{% if sent %}<p id="result">Thanks, your message was sent.</p>{% endif %}
<form method="post">
  <input name="email" type="email" placeholder="Your email" required>
  <div class="captchabox" data-sitekey="{{ site_key }}"></div>
  <button>Send</button>
</form>"""


@app.route("/", methods=["GET", "POST"])
@captchabox_required
def contact():
    sent = request.method == "POST"  # the visitor passed: send the email, save the message, etc.
    return render_template_string(PAGE, site_key=SITE_KEY, sent=sent)
