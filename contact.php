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

function email_escape($value) {
    return htmlspecialchars((string)$value, ENT_QUOTES, 'UTF-8');
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
$subject = 'New TAPIS DIGITECH Enquiry — ' . ($service ?: 'General Enquiry');

$safeName = email_escape($name);
$safeEmail = email_escape($email);
$safePhone = email_escape($phone ?: 'Not provided');
$safeService = email_escape($service ?: 'Not specified');
$safeMessage = nl2br(email_escape($message));
$safeIp = email_escape($_SERVER['REMOTE_ADDR'] ?? 'Unknown');
$safeTime = email_escape(date('d M Y, h:i A'));

$htmlBody = '<!doctype html><html><body style="margin:0;background:#f4f5f7;font-family:Arial,Helvetica,sans-serif;color:#18202a;">'
    . '<div style="max-width:680px;margin:32px auto;background:#ffffff;border:1px solid #e4e7eb;border-radius:14px;overflow:hidden;">'
    . '<div style="background:#111827;padding:28px 32px;color:#ffffff;">'
    . '<div style="font-size:12px;letter-spacing:2px;text-transform:uppercase;opacity:.75;">TAPIS DIGITECH</div>'
    . '<h1 style="margin:8px 0 0;font-size:25px;line-height:1.25;">New Website Enquiry</h1>'
    . '<p style="margin:8px 0 0;color:#d1d5db;font-size:14px;">A new business lead has been submitted through tapisdigitech.com.</p>'
    . '</div>'
    . '<div style="padding:30px 32px;">'
    . '<h2 style="font-size:16px;margin:0 0 14px;">Client Details</h2>'
    . '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="border-collapse:collapse;border:1px solid #e5e7eb;border-radius:10px;overflow:hidden;">'
    . '<tr><td style="padding:12px 14px;border-bottom:1px solid #e5e7eb;font-weight:700;width:34%;">Name</td><td style="padding:12px 14px;border-bottom:1px solid #e5e7eb;">'.$safeName.'</td></tr>'
    . '<tr><td style="padding:12px 14px;border-bottom:1px solid #e5e7eb;font-weight:700;">Email</td><td style="padding:12px 14px;border-bottom:1px solid #e5e7eb;"><a href="mailto:'.$safeEmail.'" style="color:#2563eb;">'.$safeEmail.'</a></td></tr>'
    . '<tr><td style="padding:12px 14px;border-bottom:1px solid #e5e7eb;font-weight:700;">Phone</td><td style="padding:12px 14px;border-bottom:1px solid #e5e7eb;">'.$safePhone.'</td></tr>'
    . '<tr><td style="padding:12px 14px;font-weight:700;">Service</td><td style="padding:12px 14px;">'.$safeService.'</td></tr>'
    . '</table>'
    . '<h2 style="font-size:16px;margin:28px 0 14px;">Project Details</h2>'
    . '<div style="background:#f8fafc;border:1px solid #e5e7eb;border-radius:10px;padding:18px;font-size:15px;line-height:1.65;">'.$safeMessage.'</div>'
    . '<div style="margin-top:26px;padding:18px;background:#f8fafc;border-radius:10px;font-size:12px;color:#667085;line-height:1.6;">'
    . '<strong style="color:#344054;">Lead information</strong><br>Submitted: '.$safeTime.'<br>Source: tapisdigitech.com contact form<br>IP: '.$safeIp
    . '</div>'
    . '<div style="margin-top:26px;text-align:center;">'
    . '<a href="mailto:'.$safeEmail.'" style="display:inline-block;background:#111827;color:#ffffff;text-decoration:none;padding:12px 20px;border-radius:8px;font-weight:700;margin-right:8px;">Reply to Client</a>'
    . '<a href="https://wa.me/917428996299" style="display:inline-block;background:#f3f4f6;color:#111827;text-decoration:none;padding:12px 20px;border-radius:8px;font-weight:700;">WhatsApp: +91 74289 96299</a>'
    . '</div>'
    . '</div>'
    . '<div style="padding:18px 32px;border-top:1px solid #e5e7eb;color:#98a2b3;font-size:12px;text-align:center;">TAPIS DIGITECH · AI · Automation · Software</div>'
    . '</div></body></html>';

$headers = [
    'From: TAPIS DIGITECH Website <hello@tapisdigitech.com>',
    'Reply-To: ' . $email,
    'MIME-Version: 1.0',
    'Content-Type: text/html; charset=UTF-8'
];

$sent = mail($to, $subject, $htmlBody, implode("\r\n", $headers));

if ($sent) {
    header('Location: /contact.html?sent=1', true, 303);
} else {
    header('Location: /contact.html?error=mail', true, 303);
}
exit;
