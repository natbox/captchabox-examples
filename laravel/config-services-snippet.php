<?php
// Add to the array in config/services.php, then set CAPTCHABOX_SITE_KEY and CAPTCHABOX_SECRET in .env
// Test keys that always pass, on any domain: cb_test_pass / cbs_test_pass

    'captchabox' => [
        'site_key' => env('CAPTCHABOX_SITE_KEY'),
        'secret' => env('CAPTCHABOX_SECRET'),
    ],
