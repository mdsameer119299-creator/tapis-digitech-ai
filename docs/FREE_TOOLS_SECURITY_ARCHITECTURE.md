# TAPIS DIGITECH LAB — Required Security Architecture for the Real Audit Backend

Status: **documentation only — not implemented.** This describes what the
real Website SEO Audit backend (the piece that fetches and analyzes an
arbitrary visitor-supplied URL) must do before it exists. Nothing in this
document is wired up yet. `free-tools/assets/js/audit-engine.js`'s
`AuditFetcher.endpoint` stays `null` — and the frontend keeps showing its
honest "not connected yet" error — until a backend built to this spec is
in place and reviewed.

Building this is explicitly **not** part of the current phase. Per the
governing instructions: no arbitrary-URL fetching backend yet, no
assumption that Hostinger permits unrestricted outbound HTTP/HTTPS, and no
unsafe workaround. See `free-tools/_dev/hosting-capability-test.php` for
the narrow, hardcoded-destination capability probe that comes first.

## Why this is a different risk class than `contact.php`

`contact.php` already makes an outbound network connection (SMTP to
`ssl://smtp.hostinger.com:465`), but the destination is a single hardcoded
host on the same hosting account, with no user influence over where the
connection goes. A URL-fetching audit backend is fundamentally different:
the visitor supplies the destination. That's a textbook SSRF surface —
without controls, a visitor could point it at `http://localhost`,
`http://169.254.169.254` (cloud metadata endpoints), an internal-only
admin panel, or an arbitrary external target and use TAPIS DIGITECH's
server as a scanning/relay proxy.

## Required controls

**URL scheme validation.** Accept only `http://` and `https://`. Reject
`file://`, `ftp://`, `gopher://`, `data:`, and anything else outright, at
parse time, before any network activity.

**DNS resolution and private/loopback/link-local rejection.** Resolve the
hostname server-side (never trust a client-supplied IP), then reject the
request if the resolved address falls in any of: loopback (`127.0.0.0/8`,
`::1`), private ranges (`10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`),
link-local (`169.254.0.0/16`, including the `169.254.169.254` cloud
metadata address specifically), unique local IPv6 (`fc00::/7`), and any
other non-globally-routable range. This check must run against the
*resolved* address, not the hostname string, since hostnames can be
crafted to resolve to blocked ranges (DNS rebinding).

**Redirect handling.** Do not blindly follow redirects. If a redirect must
be supported at all, cap the redirect count low (e.g. 2), and **re-run the
full scheme + DNS + private-IP check on every redirect target** before
following it — a redirect is a second, independent request and must be
treated as one for validation purposes. The simplest safe default is not
to follow redirects at all and report "this URL redirects" as a finding.

**Timeouts.** Short connect and total-request timeouts (a few seconds
each), enforced regardless of what the target server does.

**Response size limit.** Cap the number of bytes read, enforced by the
client side of the connection (not by trusting a `Content-Length` header,
which the server can lie about), matching the technique already used in
`free-tools/_dev/hosting-capability-test.php`.

**Content-type restriction.** Only parse responses whose `Content-Type` is
HTML-like (`text/html`, `application/xhtml+xml`). Reject or ignore
everything else rather than attempting to parse it as a page.

**Rate limiting and abuse prevention.** Hostinger shared hosting has no
database or in-memory store assumed available by default, so this needs a
concrete, deployable mechanism — options to evaluate before building
(not decided here): a simple per-IP file-based token bucket (with the
caveats that file-locking on shared hosting can be unreliable under
concurrency, and this doesn't survive a deploy/redeploy cleanly), a
lightweight external rate-limiting service, or Hostinger-side mechanisms
if the plan offers them. Whichever is chosen must fail safe (i.e. if the
rate-limit store is unavailable, the safer failure mode is "temporarily
unavailable," not "unlimited").

**Request count / concurrency limits.** Independent of per-visitor rate
limiting, the backend should cap how many outbound audit fetches it will
run concurrently, so a burst of legitimate traffic can't exhaust the
hosting account's resources or outbound connection limits.

**Safe error handling.** Error messages shown to the visitor must never
include raw internal details — no stack traces, no internal IPs, no
resolved-address information, no filesystem paths. Log full detail
server-side only, the same pattern `contact.php` already uses for SMTP
failures (`error_log(...)`, never surfaced to the client).

**No proxying of arbitrary destinations.** Even with all of the above, the
backend must never become a general-purpose fetch proxy — it should do
exactly one thing (fetch a page, run the specific audit checks, discard
the raw response) and expose no way to retrieve arbitrary response content
verbatim through it.

## What the hosting capability test (Step 7) is and isn't

`free-tools/_dev/hosting-capability-test.php` answers a narrower, prior
question: can this hosting account make *any* outbound HTTPS request at
all, to a single hardcoded, known-safe destination (TAPIS DIGITECH's own
`robots.txt`)? It deliberately implements none of the controls above,
because it doesn't need to — there is no user-supplied destination for
them to protect against. A passing capability-test result is a
prerequisite for building the real backend, not a substitute for any item
on this list.

## Suggested build order, once this phase is approved to proceed

1. Confirm the capability-test result on live Hostinger (not just in a dev
   sandbox — see the probe's own report for why that distinction matters).
2. Implement scheme validation + DNS resolution + private/loopback/
   link-local rejection first, with tests, before writing any HTML-parsing
   logic.
3. Implement the size-capped, timeout-bound, no-redirect-by-default fetch.
4. Add content-type restriction and safe error handling.
5. Decide and implement a concrete rate-limiting mechanism appropriate to
   Hostinger shared hosting.
6. Only then wire real checks (title/meta/H1/etc.) on top, and set
   `AuditFetcher.endpoint` in `free-tools/assets/js/audit-engine.js` to
   point at it.
