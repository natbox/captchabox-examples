<!doctype html>
<meta charset="utf-8">
<title>Contact</title>
<script src="https://captcha.natbox.io/v1/widget.js" async defer></script>

@if (session('sent'))
    <p id="result">Thanks, your message was sent.</p>
@endif
@error('captchabox-response')
    <p id="error">{{ $message }}</p>
@enderror

<form method="post" action="{{ route('contact.send') }}">
    @csrf
    <input name="email" type="email" value="{{ old('email') }}" placeholder="Your email" required>
    <div class="captchabox" data-sitekey="{{ config('services.captchabox.site_key') }}"></div>
    <button>Send</button>
</form>
