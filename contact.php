<?php
// TAPIS DIGITECH — Hostinger contact form handler
// Sends website enquiries to hello@tapisdigitech.com and a premium acknowledgement to the client.

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

// Premium internal notification for TAPIS DIGITECH.
$htmlBody = '<!doctype html><html><body style="margin:0;background:#f4f5f7;font-family:Arial,Helvetica,sans-serif;color:#18202a;">'
    . '<div style="max-width:680px;margin:32px auto;background:#ffffff;border:1px solid #e4e7eb;border-radius:14px;overflow:hidden;">'
    . '<div style="background:#111827;padding:28px 32px;color:#ffffff;">'
    . '<div style="font-size:12px;letter-spacing:2px;text-transform:uppercase;opacity:.75;">TAPIS DIGITECH</div>'
    . '<h1 style="margin:8px 0 0;font-size:25px;line-height:1.25;">New Website Enquiry</h1>'
    . '<p style="margin:8px 0 0;color:#d1d5db;font-size:14px;">A new business lead has been submitted through tapisdigitech.com.</p>'
    . '</div><div style="padding:30px 32px;">'
    . '<h2 style="font-size:16px;margin:0 0 14px;">Client Details</h2>'
    . '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="border-collapse:collapse;border:1px solid #e5e7eb;">'
    . '<tr><td style="padding:12px 14px;border-bottom:1px solid #e5e7eb;font-weight:700;width:34%;">Name</td><td style="padding:12px 14px;border-bottom:1px solid #e5e7eb;">'.$safeName.'</td></tr>'
    . '<tr><td style="padding:12px 14px;border-bottom:1px solid #e5e7eb;font-weight:700;">Email</td><td style="padding:12px 14px;border-bottom:1px solid #e5e7eb;"><a href="mailto:'.$safeEmail.'" style="color:#2563eb;">'.$safeEmail.'</a></td></tr>'
    . '<tr><td style="padding:12px 14px;border-bottom:1px solid #e5e7eb;font-weight:700;">Phone</td><td style="padding:12px 14px;border-bottom:1px solid #e5e7eb;">'.$safePhone.'</td></tr>'
    . '<tr><td style="padding:12px 14px;font-weight:700;">Service</td><td style="padding:12px 14px;">'.$safeService.'</td></tr></table>'
    . '<h2 style="font-size:16px;margin:28px 0 14px;">Project Details</h2>'
    . '<div style="background:#f8fafc;border:1px solid #e5e7eb;border-radius:10px;padding:18px;font-size:15px;line-height:1.65;">'.$safeMessage.'</div>'
    . '<div style="margin-top:26px;padding:18px;background:#f8fafc;border-radius:10px;font-size:12px;color:#667085;line-height:1.6;"><strong style="color:#344054;">Lead information</strong><br>Submitted: '.$safeTime.'<br>Source: tapisdigitech.com contact form<br>IP: '.$safeIp.'</div>'
    . '<div style="margin-top:26px;text-align:center;"><a href="mailto:'.$safeEmail.'" style="display:inline-block;background:#111827;color:#ffffff;text-decoration:none;padding:12px 20px;border-radius:8px;font-weight:700;margin-right:8px;">Reply to Client</a><a href="https://wa.me/917428996299" style="display:inline-block;background:#f3f4f6;color:#111827;text-decoration:none;padding:12px 20px;border-radius:8px;font-weight:700;">WhatsApp: +91 74289 96299</a></div>'
    . '</div><div style="padding:18px 32px;border-top:1px solid #e5e7eb;color:#98a2b3;font-size:12px;text-align:center;">TAPIS DIGITECH · AI · Automation · Software</div></div></body></html>';

$headers = [
    'From: TAPIS DIGITECH Website <hello@tapisdigitech.com>',
    'Reply-To: ' . $email,
    'MIME-Version: 1.0',
    'Content-Type: text/html; charset=UTF-8'
];

$sent = mail($to, $subject, $htmlBody, implode("\r\n", $headers));

// Premium acknowledgement sent directly by the website, so every valid enquiry gets one.
$clientSubject = 'We\'ve received your enquiry — TAPIS DIGITECH';
$clientHtml = '<!doctype html><html><body style="margin:0;background:#f4f5f7;font-family:Arial,Helvetica,sans-serif;color:#18202a;">'
    . '<div style="max-width:680px;margin:32px auto;background:#ffffff;border:1px solid #e4e7eb;border-radius:14px;overflow:hidden;">'
    . '<div style="background:#111827;padding:30px 32px;color:#ffffff;text-align:center;"><div style="font-size:12px;letter-spacing:2px;text-transform:uppercase;color:#cbd5e1;">TAPIS DIGITECH</div><h1 style="margin:10px 0 0;font-size:25px;">Enquiry Received</h1><p style="margin:8px 0 0;color:#d1d5db;font-size:14px;">AI · Automation · Software</p></div>'
    . '<div style="padding:32px;"><p style="font-size:16px;line-height:1.65;margin-top:0;">Hello '.$safeName.',</p>'
    . '<p style="font-size:15px;line-height:1.7;">Thank you for reaching out to <strong>TAPIS DIGITECH</strong>. We have successfully received your enquiry and our team will review your requirements and get back to you within one business day.</p>'
    . '<div style="margin:24px 0;padding:20px;background:#f8fafc;border:1px solid #e5e7eb;border-radius:10px;"><div style="font-size:12px;text-transform:uppercase;letter-spacing:1.2px;color:#667085;font-weight:700;margin-bottom:8px;">Your enquiry</div><div style="font-size:15px;line-height:1.65;">'.$safeMessage.'</div></div>'
    . '<div style="text-align:center;margin:28px 0;"><a href="https://wa.me/917428996299" style="display:inline-block;background:#111827;color:#ffffff;text-decoration:none;padding:13px 22px;border-radius:8px;font-weight:700;">WhatsApp +91 74289 96299</a></div>'
    . '<p style="font-size:14px;line-height:1.7;color:#667085;">If your requirement is urgent, you can contact us directly on WhatsApp. We look forward to understanding your project and helping you move it forward.</p>'
    . '<p style="margin-bottom:0;font-size:14px;line-height:1.7;">Regards,<br><strong>TAPIS DIGITECH Team</strong><br><a href="https://www.tapisdigitech.com" style="color:#2563eb;">www.tapisdigitech.com</a></p></div>'
    . '<div style="padding:18px 32px;border-top:1px solid #e5e7eb;color:#98a2b3;font-size:12px;text-align:center;">TAPIS DIGITECH · AI · Automation · Software</div></div></body></html>';

$clientHeaders = [
    'From: TAPIS DIGITECH <hello@tapisdigitech.com>',
    'Reply-To: hello@tapisdigitech.com',
    'MIME-Version: 1.0',
    'Content-Type: text/html; charset=UTF-8'
];

$clientSent = mail($email, $clientSubject, $clientHtml, implode("\r\n", $clientHeaders));

if ($sent) {
    header('Location: /contact.html?sent=1', true, 303);
} else {
    header('Location: /contact.html?error=mail', true, 303);
}
exit;
