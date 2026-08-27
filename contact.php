<?php
// TAPIS DIGITECH — production contact handler for Hostinger.
// Primary transport: Hostinger SMTP when TAPIS_SMTP_PASSWORD is available.
// Safe fallback: Hostinger/PHP mail() so the form remains operational if SMTP env vars are not configured.

header('Content-Type: text/html; charset=UTF-8');

function redirect_back($query = '') {
    header('Location: /contact.html' . ($query ? '?' . $query : ''), true, 303);
    exit;
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    redirect_back();
}

function clean($value) {
    return trim(preg_replace('/\s+/', ' ', strip_tags((string)$value)));
}

function esc($value) {
    return htmlspecialchars((string)$value, ENT_QUOTES, 'UTF-8');
}

function smtp_read($socket, $expected) {
    $data = '';
    while (($line = fgets($socket, 515)) !== false) {
        $data .= $line;
        if (isset($line[3]) && $line[3] === ' ') break;
    }
    $code = (int)substr($data, -strlen($data) + 0, 3);
    $last = preg_match('/^(\d{3}) /m', trim($data), $m) ? (int)$m[1] : 0;
    if ($last !== $expected) {
        throw new RuntimeException('SMTP response ' . $last . ' expected ' . $expected);
    }
    return $data;
}

function smtp_cmd($socket, $command, $expected) {
    fwrite($socket, $command . "\r\n");
    return smtp_read($socket, $expected);
}

function smtp_send($to, $subject, $html, $replyTo, $fromName) {
    $password = getenv('TAPIS_SMTP_PASSWORD');
    if (!$password) return false;

    $host = 'ssl://smtp.hostinger.com';
    $port = 465;
    $username = 'hello@tapisdigitech.com';
    $socket = @fsockopen($host, $port, $errno, $errstr, 15);
    if (!$socket) {
        error_log('TAPIS SMTP connect failed: ' . $errno . ' ' . $errstr);
        return false;
    }

    stream_set_timeout($socket, 15);
    try {
        smtp_read($socket, 220);
        smtp_cmd($socket, 'EHLO tapisdigitech.com', 250);
        smtp_cmd($socket, 'AUTH LOGIN', 334);
        smtp_cmd($socket, base64_encode($username), 334);
        smtp_cmd($socket, base64_encode($password), 235);
        smtp_cmd($socket, 'MAIL FROM:<' . $username . '>', 250);
        smtp_cmd($socket, 'RCPT TO:<' . $to . '>', 250);
        smtp_cmd($socket, 'DATA', 354);

        $headers = [];
        $headers[] = 'From: ' . $fromName . ' <' . $username . '>';
        $headers[] = 'To: <' . $to . '>';
        if ($replyTo) $headers[] = 'Reply-To: ' . $replyTo;
        $headers[] = 'MIME-Version: 1.0';
        $headers[] = 'Content-Type: text/html; charset=UTF-8';
        $headers[] = 'X-Mailer: TAPIS DIGITECH Website';

        $payload = implode("\r\n", $headers) . "\r\n\r\n" . $html;
        $payload = preg_replace('/(?m)^\./', '..', $payload);
        fwrite($socket, $payload . "\r\n.\r\n");
        smtp_read($socket, 250);
        smtp_cmd($socket, 'QUIT', 221);
        fclose($socket);
        return true;
    } catch (Throwable $e) {
        error_log('TAPIS SMTP send failed: ' . $e->getMessage());
        @fwrite($socket, "QUIT\r\n");
        @fclose($socket);
        return false;
    }
}

function native_mail_send($to, $subject, $html, $replyTo, $fromName) {
    $headers = [
        'From: ' . $fromName . ' <hello@tapisdigitech.com>',
        'Reply-To: ' . $replyTo,
        'MIME-Version: 1.0',
        'Content-Type: text/html; charset=UTF-8',
        'X-Mailer: TAPIS DIGITECH Website'
    ];
    return @mail($to, $subject, $html, implode("\r\n", $headers), '-fhello@tapisdigitech.com');
}

// Honeypot: quietly stop bots without sending mail.
if (!empty($_POST['company_url'] ?? '')) {
    redirect_back('sent=1');
}

$name = clean($_POST['name'] ?? '');
$email = trim((string)($_POST['email'] ?? ''));
$phone = clean($_POST['phone'] ?? '');
$service = clean($_POST['service'] ?? '');
$message = trim(strip_tags((string)($_POST['message'] ?? '')));

if ($name === '' || $message === '' || !filter_var($email, FILTER_VALIDATE_EMAIL)) {
    redirect_back('error=validation');
}

if (preg_match('/[\r\n]/', $email) || strlen($message) > 10000 || strlen($name) > 150 || strlen($phone) > 80 || strlen($service) > 120) {
    redirect_back('error=invalid');
}

$to = 'hello@tapisdigitech.com';
$subject = 'New TAPIS DIGITECH Enquiry — ' . ($service ?: 'General Enquiry');
$safeName = esc($name);
$safeEmail = esc($email);
$safePhone = esc($phone ?: 'Not provided');
$safeService = esc($service ?: 'Not specified');
$safeMessage = nl2br(esc($message));
$safeIp = esc($_SERVER['REMOTE_ADDR'] ?? 'Unknown');
$safeTime = esc(date('d M Y, h:i A'));

$internalHtml = '<!doctype html><html><body style="margin:0;background:#f4f5f7;font-family:Arial,Helvetica,sans-serif;color:#18202a;">'
 . '<div style="max-width:680px;margin:32px auto;background:#fff;border:1px solid #e4e7eb;border-radius:14px;overflow:hidden;">'
 . '<div style="background:#0b1220;padding:28px 32px;color:#fff;"><div style="font-size:12px;letter-spacing:2px;text-transform:uppercase;color:#cbd5e1;">TAPIS DIGITECH</div><h1 style="margin:8px 0 0;font-size:25px;">New Website Enquiry</h1><p style="margin:8px 0 0;color:#cbd5e1;font-size:14px;">A new business lead has been submitted through tapisdigitech.com.</p></div>'
 . '<div style="padding:30px 32px;"><h2 style="font-size:16px;margin:0 0 14px;">Client Details</h2>'
 . '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="border-collapse:collapse;border:1px solid #e5e7eb;"><tr><td style="padding:12px 14px;border-bottom:1px solid #e5e7eb;font-weight:700;width:34%;">Name</td><td style="padding:12px 14px;border-bottom:1px solid #e5e7eb;">'.$safeName.'</td></tr>'
 . '<tr><td style="padding:12px 14px;border-bottom:1px solid #e5e7eb;font-weight:700;">Email</td><td style="padding:12px 14px;border-bottom:1px solid #e5e7eb;"><a href="mailto:'.$safeEmail.'" style="color:#2563eb;">'.$safeEmail.'</a></td></tr>'
 . '<tr><td style="padding:12px 14px;border-bottom:1px solid #e5e7eb;font-weight:700;">Phone</td><td style="padding:12px 14px;border-bottom:1px solid #e5e7eb;">'.$safePhone.'</td></tr>'
 . '<tr><td style="padding:12px 14px;font-weight:700;">Service</td><td style="padding:12px 14px;">'.$safeService.'</td></tr></table>'
 . '<h2 style="font-size:16px;margin:28px 0 14px;">Project Details</h2><div style="background:#f8fafc;border:1px solid #e5e7eb;border-radius:10px;padding:18px;font-size:15px;line-height:1.65;">'.$safeMessage.'</div>'
 . '<div style="margin-top:26px;padding:18px;background:#f8fafc;border-radius:10px;font-size:12px;color:#667085;line-height:1.6;"><strong style="color:#344054;">Lead information</strong><br>Submitted: '.$safeTime.'<br>Source: tapisdigitech.com contact form<br>IP: '.$safeIp.'</div>'
 . '<div style="margin-top:26px;text-align:center;"><a href="mailto:'.$safeEmail.'" style="display:inline-block;background:#0b1220;color:#fff;text-decoration:none;padding:12px 20px;border-radius:8px;font-weight:700;margin-right:8px;">Reply to Client</a><a href="https://wa.me/917428996299" style="display:inline-block;background:#f3f4f6;color:#111827;text-decoration:none;padding:12px 20px;border-radius:8px;font-weight:700;">WhatsApp +91 74289 96299</a></div>'
 . '</div><div style="padding:18px 32px;border-top:1px solid #e5e7eb;color:#98a2b3;font-size:12px;text-align:center;">TAPIS DIGITECH · AI · Automation · Software</div></div></body></html>';

$clientSubject = 'We\'ve received your enquiry — TAPIS DIGITECH';
$clientHtml = '<!doctype html><html><body style="margin:0;background:#f4f5f7;font-family:Arial,Helvetica,sans-serif;color:#18202a;">'
 . '<div style="max-width:680px;margin:32px auto;background:#fff;border:1px solid #e4e7eb;border-radius:14px;overflow:hidden;">'
 . '<div style="background:#0b1220;padding:30px 32px;color:#fff;text-align:center;"><div style="font-size:12px;letter-spacing:2px;text-transform:uppercase;color:#cbd5e1;">TAPIS DIGITECH</div><h1 style="margin:10px 0 0;font-size:25px;">Enquiry Received</h1><p style="margin:8px 0 0;color:#cbd5e1;font-size:14px;">AI · Automation · Software</p></div>'
 . '<div style="padding:32px;"><p style="font-size:16px;line-height:1.65;margin-top:0;">Hello '.$safeName.',</p><p style="font-size:15px;line-height:1.7;">Thank you for reaching out to <strong>TAPIS DIGITECH</strong>. We have successfully received your enquiry. Our team will review your requirements and get back to you within one business day.</p>'
 . '<div style="margin:24px 0;padding:20px;background:#f8fafc;border:1px solid #e5e7eb;border-radius:10px;"><div style="font-size:12px;text-transform:uppercase;letter-spacing:1.2px;color:#667085;font-weight:700;margin-bottom:8px;">Your enquiry</div><div style="font-size:15px;line-height:1.65;">'.$safeMessage.'</div></div>'
 . '<div style="text-align:center;margin:28px 0;"><a href="https://wa.me/917428996299" style="display:inline-block;background:#0b1220;color:#fff;text-decoration:none;padding:13px 22px;border-radius:8px;font-weight:700;">WhatsApp +91 74289 96299</a></div>'
 . '<p style="font-size:14px;line-height:1.7;color:#667085;">If your requirement is urgent, you can contact us directly on WhatsApp. We look forward to understanding your project and helping you move it forward.</p><p style="margin-bottom:0;font-size:14px;line-height:1.7;">Regards,<br><strong>TAPIS DIGITECH Team</strong><br><a href="https://www.tapisdigitech.com" style="color:#2563eb;">www.tapisdigitech.com</a></p></div>'
 . '<div style="padding:18px 32px;border-top:1px solid #e5e7eb;color:#98a2b3;font-size:12px;text-align:center;">TAPIS DIGITECH · AI · Automation · Software</div></div></body></html>';

// Send the internal lead first. If SMTP credentials are configured, SMTP is preferred.
$sent = smtp_send($to, $subject, $internalHtml, $email, 'TAPIS DIGITECH Website');
if (!$sent) {
    $sent = native_mail_send($to, $subject, $internalHtml, $email, 'TAPIS DIGITECH Website');
}

// Acknowledge the client only after the internal lead has been accepted for delivery.
if ($sent) {
    $clientSent = smtp_send($email, $clientSubject, $clientHtml, $to, 'TAPIS DIGITECH');
    if (!$clientSent) {
        $clientSent = native_mail_send($email, $clientSubject, $clientHtml, $to, 'TAPIS DIGITECH');
    }
    if (!$clientSent) {
        error_log('TAPIS contact acknowledgement failed for ' . $email);
    }
    redirect_back('sent=1');
}

error_log('TAPIS contact delivery failed for ' . $email);
redirect_back('error=mail');
