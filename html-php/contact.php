<?php
// CaptchaBox example: a plain PHP contact form (one file).
// Run: CAPTCHABOX_SITE_KEY=... CAPTCHABOX_SECRET=... php -S 0.0.0.0:8000 contact.php
// Test keys that always pass, on any domain: cb_test_pass / cbs_test_pass

$siteKey = getenv('CAPTCHABOX_SITE_KEY') ?: 'cb_test_pass';
$secret  = getenv('CAPTCHABOX_SECRET') ?: 'cbs_test_pass';

/** Asks CaptchaBox whether the token from the form is valid. Each token works once, for 5 minutes. */
function captchabox_verify(string $secret, string $token): bool
{
    if ($token === '') {
        return false;
    }
    $ch = curl_init('https://captcha.natbox.io/v1/siteverify');
    curl_setopt_array($ch, [
        CURLOPT_POST => true,
        CURLOPT_POSTFIELDS => http_build_query(['secret' => $secret, 'response' => $token]),
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_TIMEOUT => 10,
    ]);
    $body = curl_exec($ch);
    curl_close($ch);
    $r = json_decode((string) $body, true);
    return !empty($r['success']);
}

$message = '';
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if (!captchabox_verify($secret, $_POST['captchabox-response'] ?? '')) {
        http_response_code(400);
        $message = 'The captcha check failed. Please try again.';
    } else {
        // The visitor passed: send the email, save the message, etc.
        $message = 'Thanks, your message was sent.';
    }
}
?>
<!doctype html>
<meta charset="utf-8">
<title>Contact</title>
<script src="https://captcha.natbox.io/v1/widget.js" async defer></script>

<?php if ($message): ?><p id="result"><?= htmlspecialchars($message) ?></p><?php endif ?>
<form method="post">
  <input name="email" type="email" placeholder="Your email" required>
  <textarea name="message" placeholder="Message" required></textarea>
  <div class="captchabox" data-sitekey="<?= htmlspecialchars($siteKey) ?>"></div>
  <button>Send</button>
</form>
