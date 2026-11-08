<?php

namespace App\Rules;

use Closure;
use Illuminate\Contracts\Validation\ValidationRule;
use Illuminate\Support\Facades\Http;

/**
 * CaptchaBox validation rule (Laravel 10+).
 * Usage: $request->validate(['captchabox-response' => ['required', new CaptchaBox]]);
 */
class CaptchaBox implements ValidationRule
{
    public function validate(string $attribute, mixed $value, Closure $fail): void
    {
        if (! is_string($value) || $value === '' || ! $this->passes($value)) {
            $fail('The captcha check failed. Please try again.');
        }
    }

    /** Asks CaptchaBox whether the token is valid. Each token works once, for 5 minutes. */
    private function passes(string $token): bool
    {
        try {
            return Http::asForm()->timeout(10)->post('https://captcha.natbox.io/v1/siteverify', [
                'secret' => config('services.captchabox.secret'),
                'response' => $token,
            ])->json('success') === true;
        } catch (\Throwable $e) {
            report($e);
            return false;
        }
    }
}
