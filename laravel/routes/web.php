<?php

use App\Rules\CaptchaBox;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;

Route::view('/contact', 'contact');

Route::post('/contact', function (Request $request) {
    $request->validate([
        'email' => ['required', 'email'],
        'captchabox-response' => ['required', new CaptchaBox],
    ], [
        'captchabox-response.required' => 'Please wait for the captcha check to finish.',
    ]);

    // The visitor passed: send the email, save the message, etc.
    return back()->with('sent', true);
})->name('contact.send');
