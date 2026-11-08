"""CaptchaBox for Django: a form field. Copy this file into your app.

settings.py:  CAPTCHABOX_SITE_KEY = "..."   CAPTCHABOX_SECRET = "..."
forms.py:     from .captchabox import CaptchaBoxField
              class ContactForm(forms.Form):
                  email = forms.EmailField()
                  captcha = CaptchaBoxField()
Test keys that always pass, on any domain: cb_test_pass / cbs_test_pass
"""
import json
import urllib.parse
import urllib.request

from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.html import format_html

VERIFY_URL = "https://captcha.natbox.io/v1/siteverify"


def verify_captchabox(token, secret=None):
    """Asks CaptchaBox whether a token is valid. Each token works once, for 5 minutes."""
    if not token:
        return False
    data = urllib.parse.urlencode({"secret": secret or settings.CAPTCHABOX_SECRET, "response": token}).encode()
    try:
        with urllib.request.urlopen(VERIFY_URL, data, timeout=10) as r:
            return json.load(r).get("success") is True
    except OSError:
        return False


class CaptchaBoxWidget(forms.Widget):
    """Shows the widget. The widget itself adds a hidden captchabox-response field to the form."""

    def __init__(self, attrs=None, theme="auto", size="normal"):
        super().__init__(attrs)
        self.theme, self.size = theme, size

    def render(self, name, value, attrs=None, renderer=None):
        return format_html(
            '<script src="https://captcha.natbox.io/v1/widget.js" async defer></script>'
            '<div class="captchabox" data-sitekey="{}" data-theme="{}" data-size="{}"></div>',
            settings.CAPTCHABOX_SITE_KEY, self.theme, self.size)

    def value_from_datadict(self, data, files, name):
        return data.get("captchabox-response", "")


class CaptchaBoxField(forms.Field):
    widget = CaptchaBoxWidget
    default_error_messages = {"captcha": "The captcha check failed. Please try again."}

    def __init__(self, **kwargs):
        kwargs.setdefault("label", "")
        super().__init__(**kwargs)

    def validate(self, value):
        if not verify_captchabox(value):
            raise ValidationError(self.error_messages["captcha"], code="captcha")
