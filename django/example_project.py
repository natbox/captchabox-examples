"""A one-file Django site that uses captchabox.py, to try it out.
Run: pip install django && python example_project.py runserver 0.0.0.0:8000
"""
import os
import sys

from django.conf import settings

settings.configure(
    DEBUG=True,
    SECRET_KEY="change-me",
    ROOT_URLCONF=__name__,
    ALLOWED_HOSTS=["*"],
    MIDDLEWARE=["django.middleware.csrf.CsrfViewMiddleware"],
    TEMPLATES=[{"BACKEND": "django.template.backends.django.DjangoTemplates"}],
    CAPTCHABOX_SITE_KEY=os.environ.get("CAPTCHABOX_SITE_KEY", "cb_test_pass"),
    CAPTCHABOX_SECRET=os.environ.get("CAPTCHABOX_SECRET", "cbs_test_pass"),
)

from django import forms  # noqa: E402
from django.http import HttpResponse  # noqa: E402
from django.middleware.csrf import get_token  # noqa: E402
from django.urls import path  # noqa: E402
from django.utils.html import format_html  # noqa: E402

from captchabox import CaptchaBoxField  # noqa: E402


class ContactForm(forms.Form):
    email = forms.EmailField()
    captcha = CaptchaBoxField()


def contact(request):
    form = ContactForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        # The visitor passed: send the email, save the message, etc.
        return HttpResponse('<p id="result">Thanks, your message was sent.</p>')
    return HttpResponse(format_html(
        '<!doctype html><meta charset="utf-8"><title>Contact</title>'
        '<form method="post"><input type="hidden" name="csrfmiddlewaretoken" value="{}">{}<button>Send</button></form>',
        get_token(request), form.as_p()))


urlpatterns = [path("", contact)]

if __name__ == "__main__":
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
