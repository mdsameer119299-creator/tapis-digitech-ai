<?php
/**
 * TAPIS DIGITECH LAB — hosting capability probe.
 * ================================================================
 * DEVELOPMENT / HOSTING CAPABILITY TEST -- DO NOT EXPOSE AS A PUBLIC TOOL.
 * ================================================================
 *
 * Purpose ONLY: determine whether this PHP hosting environment can safely
 * make a short, size-capped, no-redirect outbound HTTPS request to a
 * single hardcoded, known destination. This is NOT the real audit
 * backend, does not accept a user-supplied URL, and must never be linked
 * from site navigation, the sitemap, or any production tool page.
 *
 * Safety properties (all intentional, do not "improve" without re-reading
 * docs/FREE_TOOLS_SECURITY_ARCHITECTURE.md first):
 *  - The destination is a single hardcoded constant. There is no request
 *    parameter, form field or any other user input that influences what
 *    gets fetched.
 *  - Only HTTPS is attempted, on the standard port (443). No port scanning,
 *    no protocol negotiation, no proxying of arbitrary destinations.
 *  - Redirects are never followed (curl: CURLOPT_FOLLOWLOCATION left off /
 *    explicitly false; raw socket: we read the status line and stop --
 *    we never re-request a Location header).
 *  - The response body is capped hard at RESPONSE_CAP_BYTES regardless of
 *    what the server claims in Content-Length.
 *  - Both attempts use a short connect/read timeout so this can't hang a
 *    worker process.
 *  - Access requires a secret token via ?key=, read from an environment
 *    variable (TAPIS_DEV_PROBE_KEY) exactly like contact.php's SMTP
 *    password -- never hardcoded, never logged, never echoed back. A
 *    missing/incorrect token returns a bare 404, not an error message,
 *    so the endpoint's existence isn't advertised to anyone probing it.
 *  - This file performs no writes, sends no email, stores nothing.
 */

$expected = getenv('TAPIS_DEV_PROBE_KEY');
$given = isset($_GET['key']) ? (string) $_GET['key'] : '';
if ($expected === false || $expected === '' || !hash_equals($expected, $given)) {
    http_response_code(404);
    header('Content-Type: text/plain; charset=UTF-8');
    echo "Not found.\n";
    exit;
}

header('Content-Type: text/plain; charset=UTF-8');
header('X-Robots-Tag: noindex, nofollow, noarchive');
header('Cache-Control: no-store');

const TARGET_HOST = 'www.tapisdigitech.com';
const TARGET_PATH = '/robots.txt'; // small, always exists, same hosting account -- not a third party
const CONNECT_TIMEOUT_SECONDS = 5;
const RESPONSE_CAP_BYTES = 4096;

function line($label, $value) {
    printf("%-32s %s\n", $label . ':', $value);
}

echo "=== TAPIS DIGITECH LAB -- hosting capability probe ===\n";
echo "DEVELOPMENT TEST ONLY. Not a public tool. Not the real audit backend.\n\n";

echo "--- Environment ---\n";
line('PHP version', PHP_VERSION);
line('curl extension', function_exists('curl_init') ? 'available' : 'NOT available');
line('openssl extension', extension_loaded('openssl') ? 'available' : 'NOT available');
line('sockets (fsockopen)', function_exists('fsockopen') ? 'available' : 'NOT available');
line('stream_socket_client', function_exists('stream_socket_client') ? 'available' : 'NOT available');
line('allow_url_fopen', ini_get('allow_url_fopen') ? 'on' : 'off');
echo "\n";

echo "--- DNS resolution (target: " . TARGET_HOST . ") ---\n";
$dnsStart = microtime(true);
$ip = gethostbyname(TARGET_HOST);
$dnsMs = round((microtime(true) - $dnsStart) * 1000, 1);
if ($ip === TARGET_HOST) {
    line('Result', 'FAILED to resolve');
} else {
    line('Resolved IP', $ip);
    line('Resolution time', $dnsMs . ' ms');
}
echo "\n";

// ---------------------------------------------------------------------
// Method A: raw TLS socket (same primitive contact.php already uses
// successfully for SMTP -- fsockopen with an ssl:// wrapper). We send a
// minimal HTTP/1.1 GET by hand and read at most RESPONSE_CAP_BYTES. We
// never act on a redirect status (3xx) -- we just report it.
// ---------------------------------------------------------------------
echo "--- Method A: raw TLS socket (ssl:// + fsockopen) ---\n";
$aStart = microtime(true);
$errno = 0; $errstr = '';
$socket = @fsockopen('ssl://' . TARGET_HOST, 443, $errno, $errstr, CONNECT_TIMEOUT_SECONDS);
if (!$socket) {
    line('Connected', 'NO');
    line('Error', $errno . ' ' . $errstr);
} else {
    line('Connected', 'YES');
    stream_set_timeout($socket, CONNECT_TIMEOUT_SECONDS);
    $request = "GET " . TARGET_PATH . " HTTP/1.1\r\nHost: " . TARGET_HOST . "\r\nUser-Agent: TAPIS-DIGITECH-LAB-capability-probe\r\nConnection: close\r\n\r\n";
    fwrite($socket, $request);
    $body = '';
    while (!feof($socket) && strlen($body) < RESPONSE_CAP_BYTES) {
        $chunk = fread($socket, 512);
        if ($chunk === false) { break; }
        $body .= $chunk;
    }
    fclose($socket);
    $statusLine = strtok($body, "\r\n");
    line('Status line', $statusLine ?: '(none)');
    line('Bytes read (capped)', strlen($body) . ' of max ' . RESPONSE_CAP_BYTES);
    line('Elapsed', round((microtime(true) - $aStart) * 1000, 1) . ' ms');
    if ($statusLine && preg_match('/^HTTP\/\S+\s+3\d\d/', $statusLine)) {
        line('Note', 'Server returned a redirect -- NOT followed (by design).');
    }
}
echo "\n";

// ---------------------------------------------------------------------
// Method B: cURL, only if the extension exists. Redirects explicitly not
// followed. Response size is capped via a write callback that aborts the
// transfer once the cap is hit, since Content-Length can't be trusted.
// ---------------------------------------------------------------------
echo "--- Method B: cURL ---\n";
if (!function_exists('curl_init')) {
    line('Available', 'NO -- curl extension not loaded, skipped');
} else {
    $bStart = microtime(true);
    $received = '';
    $ch = curl_init('https://' . TARGET_HOST . TARGET_PATH);
    curl_setopt_array($ch, [
        CURLOPT_RETURNTRANSFER => false, // we stream via WRITEFUNCTION instead
        CURLOPT_HEADER => true,
        CURLOPT_FOLLOWLOCATION => false,
        CURLOPT_MAXREDIRS => 0,
        CURLOPT_CONNECTTIMEOUT => CONNECT_TIMEOUT_SECONDS,
        CURLOPT_TIMEOUT => CONNECT_TIMEOUT_SECONDS,
        CURLOPT_PROTOCOLS => defined('CURLPROTO_HTTPS') ? CURLPROTO_HTTPS : null,
        CURLOPT_SSL_VERIFYPEER => true,
        CURLOPT_SSL_VERIFYHOST => 2,
        CURLOPT_USERAGENT => 'TAPIS-DIGITECH-LAB-capability-probe',
        CURLOPT_WRITEFUNCTION => function ($curlHandle, $chunk) use (&$received) {
            $received .= $chunk;
            if (strlen($received) >= RESPONSE_CAP_BYTES) { return -1; } // abort transfer: cap hit
            return strlen($chunk);
        },
    ]);
    $ok = curl_exec($ch);
    $errNo = curl_errno($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);

    $capHit = strlen($received) >= RESPONSE_CAP_BYTES;
    if ($errNo && !$capHit) {
        line('Result', 'FAILED (curl errno ' . $errNo . ': ' . curl_strerror($errNo) . ')');
    } else {
        line('HTTP status', (string) $httpCode);
        line('Bytes read (capped)', strlen($received) . ' of max ' . RESPONSE_CAP_BYTES);
        line('Elapsed', round((microtime(true) - $bStart) * 1000, 1) . ' ms');
        if ($httpCode >= 300 && $httpCode < 400) {
            line('Note', 'Server returned a redirect -- NOT followed (by design).');
        }
    }
}
echo "\n";

echo "=== End of probe. Delete or keep access-gated -- never link this page. ===\n";
