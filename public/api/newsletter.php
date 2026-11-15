<?php
// Newsletter signup for Brandella Journal.
// Emails are saved to a CSV file (opens in Excel) outside public_html:
// domains/brandella.in/newsletter-data/subscribers.csv
header('Content-Type: application/json');
header('Cache-Control: no-store');
$origin = $_SERVER['HTTP_ORIGIN'] ?? '';
if ($_SERVER['REQUEST_METHOD'] !== 'POST' || ($origin !== '' && $origin !== 'https://brandella.in')) {
  http_response_code(405); echo '{"ok":false,"msg":"Not allowed"}'; exit;
}
$raw = file_get_contents('php://input', false, null, 0, 2048);
$in = json_decode($raw, true) ?: [];
// Honeypot: real people never fill this hidden field
if (!empty($in['website'])) { echo '{"ok":true}'; exit; }
$email = strtolower(trim((string)($in['email'] ?? '')));
$page = substr(preg_replace('#[^a-z0-9/_\-]#i', '', (string)($in['page'] ?? '')), 0, 120);
if (strlen($email) > 254 || !filter_var($email, FILTER_VALIDATE_EMAIL)) {
  http_response_code(400); echo '{"ok":false,"msg":"Please enter a valid email address."}'; exit;
}
$dir = dirname(__DIR__, 2) . '/newsletter-data';
if (!is_dir($dir)) { mkdir($dir, 0700, true); }
// Simple rate limit: max 5 signups per IP per hour
$ipKey = $dir . '/rate-' . sha1(($_SERVER['REMOTE_ADDR'] ?? '') . gmdate('YmdH'));
$hits = (int)@file_get_contents($ipKey);
if ($hits >= 5) { http_response_code(429); echo '{"ok":false,"msg":"Too many attempts, please try later."}'; exit; }
file_put_contents($ipKey, (string)($hits + 1), LOCK_EX);
foreach (glob($dir . '/rate-*') as $f) { if (filemtime($f) < time() - 7200) { @unlink($f); } }
$file = $dir . '/subscribers.csv';
$fh = fopen($file, 'c+');
if (!$fh || !flock($fh, LOCK_EX)) { http_response_code(500); echo '{"ok":false,"msg":"Please try again."}'; exit; }
$exists = false; $rows = 0;
while (($row = fgetcsv($fh)) !== false) {
  $rows++;
  if (isset($row[0]) && strtolower($row[0]) === $email) { $exists = true; break; }
}
if (!$exists) {
  if ($rows > 200000) { flock($fh, LOCK_UN); fclose($fh); http_response_code(507); echo '{"ok":false,"msg":"Please try again later."}'; exit; }
  fseek($fh, 0, SEEK_END);
  if ($rows === 0) { fputcsv($fh, ['email', 'subscribed_at_ist', 'page']); }
  $safe = function ($v) { return preg_match('/^[=+\-@]/', $v) ? "'" . $v : $v; }; // stop Excel formula injection
  $dt = new DateTime('now', new DateTimeZone('Asia/Kolkata'));
  fputcsv($fh, [$safe($email), $dt->format('Y-m-d H:i'), $safe($page)]);
}
fflush($fh); flock($fh, LOCK_UN); fclose($fh);
echo $exists ? '{"ok":true,"msg":"You are already subscribed. Thank you!"}' : '{"ok":true,"msg":"Thanks for subscribing!"}';
