<?php
// TAPIS DIGITECH — production contact/newsletter handler for Hostinger.
// Sends website enquiries (with a premium acknowledgement to the client)
// and newsletter sign-ups to hello@tapisdigitech.com.
//
// Delivery: SMTP-only, deliberately. PHP's mail() function was previously
// used as a silent fallback whenever SMTP failed, but mail() can return
// true without the message ever actually being delivered (no error, no
// exception -- it just vanishes), which meant a visitor could see "message
// received" while nobody actually got an email. Success is now reported
// to the visitor if and only if the SMTP conversation with Hostinger's
// mail server completed successfully end to end. If SMTP fails for any
// reason, the real reason is logged server-side (never the password) and
// the visitor is told honestly that sending failed. The SMTP password is
// never stored in this repository -- it's read from the server-side
// TAPIS_SMTP_PASSWORD environment variable, or an untracked smtp-secret.php
// file (see .gitignore / .htaccess), configured directly on the host.

header('Content-Type: text/html; charset=UTF-8');

// Writes one line to a private, .htaccess-protected diagnostic log so the
// EXACT SMTP failure stage can be seen on the live server without ever
// exposing anything to visitors or to git. Never pass a password, a
// base64-encoded credential, or the raw AUTH LOGIN exchange into $detail --
// only stage names and SMTP response codes.
function smtp_debug_log($stage, $detail = '') {
    $line = '[' . date('Y-m-d H:i:s') . '] ' . $stage;
    if ($detail !== '') {
        $line .= ' - ' . $detail;
    }
    @file_put_contents(__DIR__ . '/contact-mail-debug.log', $line . PHP_EOL, FILE_APPEND | LOCK_EX);
}

// Maps an internal SMTP step name to the specific, human-readable failure
// label used in contact-mail-debug.log.
function smtp_stage_label($stage) {
    $labels = [
        'SMTP greeting'       => 'SMTP GREETING FAILED',
        'EHLO'                => 'EHLO FAILED',
        'AUTH LOGIN'          => 'AUTH LOGIN FAILED',
        'SMTP username'       => 'USERNAME AUTH FAILED',
        'SMTP authentication' => 'PASSWORD AUTH FAILED',
        'MAIL FROM'           => 'MAIL FROM FAILED',
        'RCPT TO'             => 'RCPT TO FAILED',
        'DATA'                => 'DATA FAILED',
        'message body'        => 'DATA FAILED',
    ];
    return $labels[$stage] ?? (strtoupper($stage) . ' FAILED');
}

$TAPIS_SMTP_PASSWORD = getenv('TAPIS_SMTP_PASSWORD') ?: '';
if ($TAPIS_SMTP_PASSWORD === '') {
    if (is_file(__DIR__ . '/smtp-secret.php')) {
        require_once __DIR__ . '/smtp-secret.php'; // defines $TAPIS_SMTP_PASSWORD on the server only
    } else {
        smtp_debug_log('SECRET FILE MISSING', 'expected at ' . __DIR__ . '/smtp-secret.php');
    }
}
if ($TAPIS_SMTP_PASSWORD === '') {
    smtp_debug_log('SMTP PASSWORD MISSING', 'not set via TAPIS_SMTP_PASSWORD env var or smtp-secret.php');
}

// $stage names the SMTP step being read, purely for clear, specific server
// logs (e.g. "SMTP authentication failed (got 535, expected 235)") -- never
// includes the password or the base64-encoded credentials themselves.
function smtp_read($socket, $expected, $stage) {
    $data = '';
    while (($line = fgets($socket, 515)) !== false) {
        $data .= $line;
        if (isset($line[3]) && $line[3] === ' ') break;
    }
    $last = preg_match('/^(\d{3}) /m', trim($data), $m) ? (int)$m[1] : 0;
    if ($last !== $expected) {
        throw new RuntimeException($stage . ' failed (got ' . $last . ', expected ' . $expected . ')');
    }
    return $data;
}

function smtp_cmd($socket, $command, $expected, $stage) {
    fwrite($socket, $command . "\r\n");
    return smtp_read($socket, $expected, $stage);
}

// Sends one HTML email over a direct SMTP connection to Hostinger's mail
// server. Returns true ONLY if the message was actually accepted by the
// server (response 250 immediately after DATA) -- this is the sole source
// of truth for "was this email actually sent," used directly as the
// success value reported to the visitor. Never throws; every failure is
// caught, logged server-side with a specific stage name to
// contact-mail-debug.log (never the password or any credential), and
// reported back as false.
function smtp_send($to, $subject, $html, $replyTo, $fromName) {
    global $TAPIS_SMTP_PASSWORD;
    if (!$TAPIS_SMTP_PASSWORD) {
        error_log('TAPIS SMTP not configured: TAPIS_SMTP_PASSWORD is not set (checked env var and smtp-secret.php)');
        return false;
    }

    $host = 'ssl://smtp.hostinger.com';
    $port = 465;
    $username = 'hello@tapisdigitech.com';
    $socket = @fsockopen($host, $port, $errno, $errstr, 15);
    if (!$socket) {
        error_log('TAPIS SMTP connection failed: ' . $errno . ' ' . $errstr);
        smtp_debug_log('SMTP CONNECTION FAILED', $errno . ' ' . $errstr);
        return false;
    }

    stream_set_timeout($socket, 15);
    try {
        smtp_read($socket, 220, 'SMTP greeting');
        smtp_cmd($socket, 'EHLO tapisdigitech.com', 250, 'EHLO');
        smtp_cmd($socket, 'AUTH LOGIN', 334, 'AUTH LOGIN');
        smtp_cmd($socket, base64_encode($username), 334, 'SMTP username');
        smtp_cmd($socket, base64_encode($TAPIS_SMTP_PASSWORD), 235, 'SMTP authentication');
        smtp_cmd($socket, 'MAIL FROM:<' . $username . '>', 250, 'MAIL FROM');
        smtp_cmd($socket, 'RCPT TO:<' . $to . '>', 250, 'RCPT TO');
        smtp_cmd($socket, 'DATA', 354, 'DATA');

        $headers = [
            'From: ' . $fromName . ' <' . $username . '>',
            'To: <' . $to . '>',
            'MIME-Version: 1.0',
            'Content-Type: text/html; charset=UTF-8',
            'X-Mailer: TAPIS DIGITECH Website'
        ];
        if ($replyTo) $headers[] = 'Reply-To: ' . $replyTo;

        $payload = implode("\r\n", $headers) . "\r\n\r\n" . $html;
        $payload = preg_replace('/(?m)^\./', '..', $payload);
        fwrite($socket, $payload . "\r\n.\r\n");
        smtp_read($socket, 250, 'message body');

        // The message has now been genuinely accepted by the server -- this
        // is the real, meaningful point of success. QUIT is just a polite
        // goodbye; some mail servers close the connection immediately after
        // accepting the message, or respond to QUIT in a way that doesn't
        // match the exact expected code. That must never turn an already-
        // accepted email into a reported failure, so a QUIT problem is only
        // logged as a warning, not treated as a send failure.
        try {
            smtp_cmd($socket, 'QUIT', 221, 'QUIT');
        } catch (Throwable $e) {
            smtp_debug_log('QUIT WARNING', $e->getMessage());
        }
        @fclose($socket);
        return true;
    } catch (Throwable $e) {
        if (preg_match('/^(.*?) failed \(got (\d+), expected (\d+)\)$/', $e->getMessage(), $m)) {
            smtp_debug_log(smtp_stage_label($m[1]), 'got ' . $m[2] . ', expected ' . $m[3]);
        } else {
            smtp_debug_log('SMTP SEND FAILED', $e->getMessage());
        }
        error_log('TAPIS SMTP send failed: ' . $e->getMessage());
        @fwrite($socket, "QUIT\r\n");
        @fclose($socket);
        return false;
    }
}

function clean($value) {
    return trim(preg_replace('/\s+/', ' ', strip_tags((string)$value)));
}

// Resolve a safe, same-site path to redirect back to (used by the
// newsletter form, which can be submitted from any of the 36 pages).
// Falls back to "/" if the referer is missing, malformed, or off-site --
// never redirects to an attacker-supplied external URL.
function safe_return_path() {
    $referer = $_SERVER['HTTP_REFERER'] ?? '';
    if ($referer === '') return '/';
    $parts = parse_url($referer);
    if (!$parts || empty($parts['host'])) return '/';
    $allowedHosts = ['tapisdigitech.com', 'www.tapisdigitech.com', $_SERVER['HTTP_HOST'] ?? ''];
    if (!in_array($parts['host'], $allowedHosts, true)) return '/';
    $path = $parts['path'] ?? '/';
    // Only allow a plain relative path within this site, no scheme/host smuggling.
    if ($path === '' || $path[0] !== '/') return '/';
    return $path;
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    header('Location: /contact.html', true, 303);
    exit;
}

$formType = ($_POST['form_type'] ?? 'contact') === 'newsletter' ? 'newsletter' : 'contact';

// The site's own fetch()-based form submission (assets/js/main.js) sends this
// header so it can get a real JSON success/failure response and update the
// page without a reload. A classic no-JS form POST never sends it, so it
// gets the original 303-redirect-with-query-param behaviour instead. Either
// way the outcome reported is the real, server-confirmed one -- this never
// changes what actually happened, only how it's communicated back.
$wantsJson = isset($_SERVER['HTTP_X_TDX_AJAX']) && $_SERVER['HTTP_X_TDX_AJAX'] === '1';

// Reports the real, already-determined outcome of this submission -- never
// called with a success this script hasn't actually verified.
function respond($wantsJson, $redirectPath, $success, $message) {
    if ($wantsJson) {
        header('Content-Type: application/json; charset=UTF-8');
        echo json_encode(['success' => $success, 'message' => $message]);
        exit;
    }
    header('Location: ' . $redirectPath, true, 303);
    exit;
}

function email_escape($value) {
    return htmlspecialchars((string)$value, ENT_QUOTES, 'UTF-8');
}

// Honeypot: silently tell the bot it "succeeded" (this field is hidden from
// real visitors by CSS, so only an automated submission ever fills it) and
// send no email at all.
if (!empty($_POST['company_url'] ?? '')) {
    if ($formType === 'newsletter') {
        respond($wantsJson, safe_return_path() . '?subscribed=1', true, 'Thanks — you’re subscribed.');
    }
    respond($wantsJson, '/contact.html?sent=1', true, 'Thank you! Your message has been received. We’ll reply within one business day.');
}

if ($formType === 'newsletter') {
    $email = trim((string)($_POST['email'] ?? ''));
    $returnPath = safe_return_path();

    if ($email === '' || !filter_var($email, FILTER_VALIDATE_EMAIL) || preg_match('/[\r\n]/', $email)) {
        respond($wantsJson, $returnPath . '?sub_error=validation', false, 'Please enter a valid email address.');
    }

    $subject = 'TAPIS DIGITECH — new newsletter subscriber';
    $safeNewsEmail = htmlspecialchars($email, ENT_QUOTES, 'UTF-8');
    $safeNewsSource = htmlspecialchars($returnPath, ENT_QUOTES, 'UTF-8');
    $safeNewsIp = htmlspecialchars($_SERVER['REMOTE_ADDR'] ?? 'unknown', ENT_QUOTES, 'UTF-8');
    $newsHtml = '<!doctype html><html><body style="margin:0;background:#f4f5f7;font-family:Arial,Helvetica,sans-serif;color:#18202a;">'
        . '<div style="max-width:560px;margin:32px auto;background:#ffffff;border:1px solid #e4e7eb;border-radius:14px;padding:28px 32px;">'
        . '<div style="font-size:12px;letter-spacing:2px;text-transform:uppercase;color:#667085;">TAPIS DIGITECH</div>'
        . '<h1 style="margin:8px 0 18px;font-size:20px;">New newsletter subscriber</h1>'
        . '<p style="font-size:14px;line-height:1.7;margin:0 0 6px;"><strong>Email:</strong> ' . $safeNewsEmail . '</p>'
        . '<p style="font-size:14px;line-height:1.7;margin:0 0 6px;"><strong>Source page:</strong> ' . $safeNewsSource . '</p>'
        . '<p style="font-size:14px;line-height:1.7;margin:0;color:#667085;"><strong>IP:</strong> ' . $safeNewsIp . '</p>'
        . '</div></body></html>';
    $sent = smtp_send('hello@tapisdigitech.com', $subject, $newsHtml, $email, 'TAPIS DIGITECH Website');
    if ($sent) {
        respond($wantsJson, $returnPath . '?subscribed=1', true, 'Thanks — you’re subscribed.');
    }
    respond($wantsJson, $returnPath . '?sub_error=mail', false, 'We could not subscribe you right now. Please try again or email hello@tapisdigitech.com.');
}

// -- default: main contact form ------------------------------------------
$name = clean($_POST['name'] ?? '');
$email = trim((string)($_POST['email'] ?? ''));
$phone = clean($_POST['phone'] ?? '');
$service = clean($_POST['service'] ?? '');
$message = trim(strip_tags((string)($_POST['message'] ?? '')));

if ($name === '' || $message === '' || !filter_var($email, FILTER_VALIDATE_EMAIL)) {
    respond($wantsJson, '/contact.html?error=validation', false, 'Please fill in your name, a valid email, and your message.');
}

if (preg_match('/[\r\n]/', $email) || strlen($message) > 10000 || strlen($name) > 150) {
    respond($wantsJson, '/contact.html?error=invalid', false, 'Please check your details and try again.');
}

$to = 'hello@tapisdigitech.com';
$subject = 'New TAPIS DIGITECH Enquiry — ' . ($service ?: 'General Enquiry');
$sourcePage = safe_return_path();

$safeName = email_escape($name);
$safeEmail = email_escape($email);
$safePhone = email_escape($phone ?: 'Not provided');
$safeService = email_escape($service ?: 'Not specified');
$safeMessage = nl2br(email_escape($message));
$safeFormType = email_escape($service ? 'Service Enquiry' : 'General Enquiry');
$safeSource = email_escape($sourcePage);
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
    . '<tr><td style="padding:12px 14px;border-bottom:1px solid #e5e7eb;font-weight:700;">Service</td><td style="padding:12px 14px;border-bottom:1px solid #e5e7eb;">'.$safeService.'</td></tr>'
    . '<tr><td style="padding:12px 14px;border-bottom:1px solid #e5e7eb;font-weight:700;">Form Type</td><td style="padding:12px 14px;border-bottom:1px solid #e5e7eb;">'.$safeFormType.'</td></tr>'
    . '<tr><td style="padding:12px 14px;font-weight:700;">Source Page</td><td style="padding:12px 14px;">'.$safeSource.'</td></tr></table>'
    . '<h2 style="font-size:16px;margin:28px 0 14px;">Project Details</h2>'
    . '<div style="background:#f8fafc;border:1px solid #e5e7eb;border-radius:10px;padding:18px;font-size:15px;line-height:1.65;">'.$safeMessage.'</div>'
    . '<div style="margin-top:26px;padding:18px;background:#f8fafc;border-radius:10px;font-size:12px;color:#667085;line-height:1.6;"><strong style="color:#344054;">Lead information</strong><br>Submitted: '.$safeTime.'<br>Source: tapisdigitech.com contact form<br>IP: '.$safeIp.'</div>'
    . '<div style="margin-top:26px;text-align:center;"><a href="mailto:'.$safeEmail.'" style="display:inline-block;background:#111827;color:#ffffff;text-decoration:none;padding:12px 20px;border-radius:8px;font-weight:700;margin-right:8px;">Reply to Client</a><a href="https://wa.me/917428996299" style="display:inline-block;background:#f3f4f6;color:#111827;text-decoration:none;padding:12px 20px;border-radius:8px;font-weight:700;">WhatsApp: +91 74289 96299</a></div>'
    . '</div><div style="padding:18px 32px;border-top:1px solid #e5e7eb;color:#98a2b3;font-size:12px;text-align:center;">TAPIS DIGITECH · AI · Automation · Software</div></div></body></html>';

$sent = smtp_send($to, $subject, $htmlBody, $email, 'TAPIS DIGITECH Website');

// Premium acknowledgement sent directly by the website, so every valid enquiry gets one.
$clientSubject = 'We\'ve received your enquiry — TAPIS DIGITECH';

// Service line is only shown to the client when they actually selected one --
// an internal "Not specified" placeholder has no place in a message sent
// back to them.
$serviceRowHtml = $service
    ? '<div style="font-size:12px;text-transform:uppercase;letter-spacing:1.2px;color:#667085;font-weight:700;margin-bottom:4px;">Service</div><div style="font-size:15px;line-height:1.5;margin-bottom:16px;">'.$safeService.'</div>'
    : '';

$clientHtml = '<!doctype html><html><body style="margin:0;background:#f4f5f7;font-family:Arial,Helvetica,sans-serif;color:#18202a;">'
    . '<div style="max-width:680px;margin:32px auto;background:#ffffff;border:1px solid #e4e7eb;border-radius:14px;overflow:hidden;">'
    . '<div style="background:#111827;padding:30px 32px;color:#ffffff;text-align:center;"><div style="font-size:12px;letter-spacing:2px;text-transform:uppercase;color:#cbd5e1;">TAPIS DIGITECH</div><h1 style="margin:10px 0 0;font-size:25px;">Enquiry Received</h1><p style="margin:8px 0 0;color:#d1d5db;font-size:14px;">AI · Automation · Software</p></div>'
    . '<div style="padding:32px;"><p style="font-size:16px;line-height:1.65;margin-top:0;">Hello '.$safeName.',</p>'
    . '<p style="font-size:15px;line-height:1.7;">Thank you for contacting <strong>TAPIS DIGITECH</strong>. We have successfully received your enquiry and our team will carefully review your requirements. A relevant member of our team will get back to you shortly.</p>'
    . '<div style="margin:24px 0;padding:20px;background:#f8fafc;border:1px solid #e5e7eb;border-radius:10px;"><div style="font-size:12px;text-transform:uppercase;letter-spacing:1.2px;color:#667085;font-weight:700;margin-bottom:12px;">Your enquiry</div>'
    . $serviceRowHtml
    . '<div style="font-size:12px;text-transform:uppercase;letter-spacing:1.2px;color:#667085;font-weight:700;margin-bottom:4px;">Message</div><div style="font-size:15px;line-height:1.65;">'.$safeMessage.'</div></div>'
    . '<div style="margin:24px 0;"><div style="font-size:12px;text-transform:uppercase;letter-spacing:1.2px;color:#667085;font-weight:700;margin-bottom:10px;">What happens next?</div>'
    . '<ol style="margin:0;padding-left:20px;font-size:14px;line-height:1.9;color:#344054;">'
    . '<li>Our team reviews your requirements.</li>'
    . '<li>We evaluate the most suitable approach for your business.</li>'
    . '<li>A relevant team member contacts you to discuss next steps.</li>'
    . '</ol></div>'
    . '<div style="text-align:center;margin:28px 0;"><a href="https://wa.me/917428996299" style="display:inline-block;background:#111827;color:#ffffff;text-decoration:none;padding:13px 22px;border-radius:8px;font-weight:700;">WhatsApp +91 74289 96299</a></div>'
    . '<p style="font-size:14px;line-height:1.7;color:#667085;">If your requirement is urgent, you can contact us directly on WhatsApp. We look forward to understanding your project and helping you move it forward.</p>'
    . '<p style="margin-bottom:0;font-size:14px;line-height:1.7;">Regards,<br><strong>TAPIS DIGITECH Team</strong><br><a href="https://www.tapisdigitech.com" style="color:#2563eb;">www.tapisdigitech.com</a></p></div>'
    . '<div style="padding:18px 32px;border-top:1px solid #e5e7eb;color:#98a2b3;font-size:12px;text-align:center;">TAPIS DIGITECH · Innovate. Automate. Elevate.<br>tapisdigitech.com</div></div></body></html>';

// The client acknowledgement is only attempted once the admin enquiry email
// has actually been accepted by SMTP -- if the enquiry itself couldn't be
// delivered, there is nothing to acknowledge, and we don't want a client
// email that implies the enquiry was received when it wasn't.
if ($sent) {
    $clientSent = smtp_send($email, $clientSubject, $clientHtml, $to, 'TAPIS DIGITECH');
    if (!$clientSent) {
        // The enquiry itself was still received (that's what $sent/success
        // below reflects) -- this is only server-side visibility so the team
        // can manually follow up if the automatic acknowledgement didn't go out.
        error_log('TAPIS contact acknowledgement failed for ' . $email);
    }
    respond($wantsJson, '/contact.html?sent=1', true, 'Thank you! Your enquiry has been received successfully. Our team will review your requirements and get back to you shortly.');
}
respond($wantsJson, '/contact.html?error=mail', false, "Sorry, we couldn't send your enquiry at the moment. Please try again or contact us directly.");
