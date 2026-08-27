<?php
// TAPIS DIGITECH — Hostinger contact form handler
// Sends website enquiries to hello@tapisdigitech.com.

header('Content-Type: text/html; charset=UTF-8');

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    header('Location: /contact.html', true, 303);
    exit;
}

function clean($value) {
    return trim(preg_replace('/\s+/', ' ', strip_tags((string)$value)));
}

// Honeypot: silently accept bot submissions without sending email.
if (!empty($_POST['company_url'] ?? '')) {
    header('Location: /contact.html?sent=1', true, 303);
    exit;
}

$name = clean($_POST['name'] ?? '');
$email = trim((string)($_POST['email'] ?? ''));
$phone = clean($_POST['phone'] ?? '');
$service = clean($_POST['service'] ?? '');
$message = trim(strip_tags((string)($_POST['message'] ?? '')));

if ($name === '' || $message === '' || !filter_var($email, FILTER_VALIDATE_EMAIL)) {
    header('Location: /contact.html?error=validation', true, 303);
    exit;
}

if (preg_match('/[\r\n]/', $email) || strlen($message) > 10000 || strlen($name) > 150) {
    header('Location: /contact.html?error=invalid', true, 303);
    exit;
}

$to = 'hello@tapisdigitech.com';
$subject = 'New TAPIS DIGITECH enquiry — ' . ($service ?: 'General enquiry');
$body = "New website enquiry\n\n" .
        "Name: {$name}\n" .
        "Email: {$email}\n" .
        "Phone: " . ($phone ?: 'Not provided') . "\n" .
        "Service: " . ($service ?: 'Not specified') . "\n\n" .
        "Project details:\n{$message}\n\n" .
        "Source: tapisdigitech.com contact form\n" .
        "IP: " . ($_SERVER['REMOTE_ADDR'] ?? 'unknown') . "\n";

$headers = [
    'From: TAPIS DIGITECH Website <hello@tapisdigitech.com>',
    'Reply-To: ' . $email,
    'MIME-Version: 1.0',
    'Content-Type: text/plain; charset=UTF-8'
];

$sent = mail($to, $subject, $body, implode("\r\n", $headers));

if ($sent) {
    header('Location: /contact.html?sent=1', true, 303);
} else {
    header('Location: /contact.html?error=mail', true, 303);
}
exit;
