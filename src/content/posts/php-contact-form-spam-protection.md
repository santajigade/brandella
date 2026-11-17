---
title: "PHP Contact Form With Spam Protection: Build It in 4 Layers"
slug: "php-contact-form-spam-protection"
date: "2026-08-25T12:20:30"
updated: "2026-08-25T12:20:55"
author: "santajigade"
categories: ["development", "php"]
primaryCategory: "development"
description: "Build a php contact form with spam protection using a honeypot, rate limiting, CSRF tokens, and reCAPTCHA v3, then send it with PHPMailer."
focusKeyword: "PHP Contact Form"
takeaways:
  - "An unprotected PHP contact form can start receiving dozens of bot submissions a day soon after going live."
  - "A honeypot field hidden with CSS, not type hidden, catches simple bots because real visitors never see or fill it in."
  - "Limiting each IP address to five submissions per hour stops scripted flooding, and a temporary file per IP needs no database."
  - "Server side validation and a CSRF token are essential, since bots skip the browser and forged requests can come from other sites."
  - "Google reCAPTCHA v3 runs invisibly and returns a score from 0 to 1, with 0.5 as a reasonable starting threshold."
image: "/wp-content/uploads/2026/08/PHP-Contact-Form.webp"
imageAlt: "PHP Contact Form"
words: 1657
views: 56
format: "html"
---
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<style>
@import url('https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600;700;800&display=swap');

#bx-article, #bx-article * { box-sizing: border-box; }
#bx-article {
  --bx-disp: 'Open Sans', sans-serif;
  --bx-body: 'Open Sans', sans-serif;
  --bx-green: #5DB92E;
  --bx-green-deep: #4a9e24;
  --bx-charcoal: #2b2b2b;
  --bx-charcoal-soft: #4a4a4a;
  --bx-dark: #20272C;
  font-family: var(--bx-body);
  font-weight: 400;
  font-size: 17px;
  line-height: 1.75;
  color: var(--bx-charcoal);
  max-width: 860px;
  margin: 0 auto;
  padding: 10px 18px 40px;
}
#bx-article a { color: var(--bx-green-deep); text-decoration: none; font-weight: 600; }
#bx-article a:hover { color: var(--bx-charcoal); }
#bx-article p { font-size: 17px; margin: 0 0 16px; }
#bx-article img, #bx-article svg { max-width: 100%; height: auto; }

.bx-pills { display: flex; flex-wrap: wrap; gap: 8px; margin: 18px 0 20px; }
.bx-pill {
  font-family: var(--bx-disp); font-size: 13px; font-weight: 700;
  color: var(--bx-green-deep); background: #eef8e6; border: 1px solid var(--bx-green);
  padding: 5px 14px; border-radius: 30px; letter-spacing: .3px;
}

.bx-lede {
  font-style: italic; font-size: 17px; color: var(--bx-charcoal-soft);
  border-left: 4px solid var(--bx-green); padding: 6px 20px; margin: 0 0 28px;
}

.bx-section-head { margin: 46px 0 18px; }
.bx-num {
  font-family: var(--bx-disp); font-weight: 800; font-size: 15px; color: var(--bx-green-deep);
  letter-spacing: 2px; display: block; margin-bottom: 4px;
}
#bx-article h2.bx-h2 {
  font-family: var(--bx-disp); font-weight: 700; font-size: 25px; color: var(--bx-charcoal);
  margin: 0 0 10px; line-height: 1.35;
}
.bx-rule { width: 64px; height: 4px; background: var(--bx-green); border-radius: 2px; }

h3.bx-h3 { font-family: var(--bx-disp); font-weight: 700; font-size: 20px; color: var(--bx-charcoal); margin: 26px 0 12px; }

.bx-code-wrap { margin: 18px 0 26px; border-radius: 10px; overflow: hidden; background: #1e1e2e; box-shadow: 0 2px 10px rgba(0,0,0,.15); }
.bx-code-title {
  background: #171724; color: #a9adc1; font-family: 'Courier New', monospace; font-size: 13px;
  padding: 10px 16px; border-bottom: 1px solid #2f2f45; letter-spacing: .3px;
}
.bx-code-wrap pre { margin: 0; padding: 18px 20px; overflow-x: auto; }
.bx-code-wrap code { font-family: 'Courier New', Consolas, monospace; font-size: 16px; line-height: 1.65; color: #e4e4f0; white-space: pre; }
.tok-kw { color: #c792ea; }
.tok-fn { color: #82aaff; }
.tok-str { color: #f5d76e; }
.tok-val { color: #f78c50; }
.tok-cm  { color: #7c7f93; font-style: italic; }
.tok-sel { color: #9ece6a; }
.tok-prop{ color: #7fdbca; }

.bx-table-wrap { overflow-x: auto; margin: 20px 0 30px; border-radius: 10px; }
table.bx-table { width: 100%; border-collapse: collapse; font-size: 17px; min-width: 620px; }
table.bx-table thead tr { background: var(--bx-charcoal) !important; }
table.bx-table thead th { color: #fff !important; font-family: var(--bx-disp); font-weight: 700; text-align: left; padding: 13px 14px; font-size: 17px; }
table.bx-table tbody td { padding: 12px 14px; font-size: 17px; border-bottom: 1px solid #e7f2dd; }
table.bx-table tbody tr:nth-child(odd) { background: #f4faef; }
table.bx-table tbody tr:nth-child(even) { background: #ffffff; }

.bx-checklist { list-style: none; margin: 18px 0 28px; padding: 0; display: grid; gap: 12px; }
.bx-checklist li {
  background: #fff; border: 1px solid #e9e9e9; border-left: 4px solid var(--bx-green);
  border-radius: 8px; padding: 14px 16px 14px 44px; position: relative; font-size: 17px;
}
.bx-checklist li::before {
  content: "✓"; position: absolute; left: 14px; top: 13px; color: var(--bx-green-deep); font-weight: 800; font-size: 17px;
}
.bx-checklist b { color: var(--bx-charcoal); }

.bx-faq { margin: 20px 0 30px; }
.bx-faq-item { border-bottom: 1px solid #e3e3e3; }
.bx-faq-q {
  width: 100%; text-align: left; background: none; border: none; cursor: pointer;
  font-family: var(--bx-disp); font-weight: 700; font-size: 17px; color: var(--bx-charcoal);
  padding: 18px 34px 18px 4px; position: relative;
}
.bx-faq-q::after {
  content: "+"; position: absolute; right: 4px; top: 50%; transform: translateY(-50%);
  color: var(--bx-green-deep); font-size: 22px; font-weight: 400; transition: transform .25s ease;
}
.bx-faq-item.open .bx-faq-q::after { transform: translateY(-50%) rotate(45deg); }
.bx-faq-a { max-height: 0; overflow: hidden; transition: max-height .3s ease; }
.bx-faq-a p { padding: 0 4px 18px; margin: 0; font-size: 17px; color: var(--bx-charcoal-soft); }

.bx-related { background: #eef8e6; border-radius: 12px; padding: 26px 26px 10px; margin: 34px 0; }
.bx-related h3 { font-family: var(--bx-disp); font-size: 19px; color: var(--bx-charcoal); margin: 0 0 16px; }
.bx-related ul { list-style: none; margin: 0; padding: 0; display: grid; grid-template-columns: 1fr 1fr; gap: 10px 20px; }
.bx-related li { font-size: 17px; padding-bottom: 16px; border-bottom: 1px dashed #cfe8bd; }
@media (max-width: 640px) { .bx-related ul { grid-template-columns: 1fr; } }

.bx-learn { margin: 40px 0 10px; }
.bx-learn h2 { font-family: var(--bx-disp); font-size: 24px; color: var(--bx-charcoal); margin-bottom: 20px; }
.bx-learn-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
.bx-learn-card {
  border: 1px solid #e3efdc; border-radius: 12px; padding: 20px; background: #fff;
  display: flex; gap: 14px; align-items: flex-start;
}
.bx-learn-num {
  flex-shrink: 0; width: 34px; height: 34px; border-radius: 50%; background: var(--bx-charcoal);
  color: var(--bx-green); font-family: var(--bx-disp); font-weight: 800; font-size: 15px;
  display: flex; align-items: center; justify-content: center;
}
.bx-learn-card h4 { margin: 0 0 6px; font-family: var(--bx-disp); font-size: 16px; color: var(--bx-charcoal); }
.bx-learn-card p { margin: 0; font-size: 17px; color: var(--bx-charcoal-soft); }
@media (max-width: 640px) { .bx-learn-grid { grid-template-columns: 1fr; } }

.bx-cta {
  background: linear-gradient(120deg, var(--bx-green) 0%, var(--bx-green-deep) 100%);
  border-radius: 14px; padding: 38px 32px; text-align: center; margin: 40px 0 20px; color: #fff;
}
.bx-cta h3 { font-family: var(--bx-disp); font-size: 24px; margin: 0 0 10px; color: #fff; }
.bx-cta p { color: #eafbe0; margin: 0 0 22px; font-size: 17px; }
.bx-cta-btns { display: flex; flex-wrap: wrap; gap: 12px; justify-content: center; }
.bx-cta-btns a {
  background: #fff; color: var(--bx-green-deep) !important; font-family: var(--bx-disp); font-weight: 700;
  padding: 12px 26px; border-radius: 30px; font-size: 15px;
}
.bx-cta-btns a.bx-cta-outline { background: transparent; color: #fff !important; border: 2px solid #fff; }

.bx-ad { text-align: center; margin: 34px 0; padding: 18px 0; border-top: 1px dashed #cfcfcf; border-bottom: 1px dashed #cfcfcf; }
</style>

<div id="bx-article">

  <div class="bx-pills">
    <span class="bx-pill">Development</span>
    <span class="bx-pill">PHP</span>
    <span class="bx-pill">Contact Forms</span>
    <span class="bx-pill">Spam Protection</span>
  </div>

  <p class="bx-lede">A contact form with no defenses fills an inbox with junk within days of going live, long before a real customer ever finds it. A php contact form with spam protection stays useful because the bot traffic never reaches the inbox at all.</p>

  <div class="bx-section-head">
    <span class="bx-num">01</span>
    <h2 class="bx-h2" id="why-a-php-contact-form-with-spam-protection-beats-a-bare-html-form">Why a PHP Contact Form With Spam Protection Beats a Bare HTML Form</h2>
    <div class="bx-rule"></div>
  </div>

  <p>A plain HTML form with a PHP handler behind it works the moment it ships. It also has no idea whether the request came from a person or a script.</p>

  <p>Automated bots crawl the web looking for exactly this pattern, an open form action pointing at a PHP file with no checks in front of it. <a href="https://www.cloudflare.com/learning/bots/what-is-a-bot/" target="_blank" rel="noopener">Cloudflare's overview of bot traffic</a> gives a good sense of just how much of the web this kind of scanning actually covers.</p>

  <p>Within a short time, a completely unprotected form starts receiving dozens of submissions a day that are not from real visitors at all.</p>

  <p>Each layer added below blocks a different kind of automated traffic, and together they cover almost everything a small site actually sees.</p>

  <div class="bx-ad">
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-3931314195561246" crossorigin="anonymous"></script>
    <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-3931314195561246" data-ad-slot="4249015278" data-ad-format="auto" data-full-width-responsive="true"></ins>
    <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
  </div>

  <div class="bx-section-head">
    <span class="bx-num">02</span>
    <h2 class="bx-h2" id="setting-up-the-html-form-and-php-handler">Setting Up the HTML Form and PHP Handler</h2>
    <div class="bx-rule"></div>
  </div>

  <p>The form itself stays simple. Every protection layer in this guide lives in the PHP file that processes the submission, not in extra form fields the visitor has to fill out.</p>

  <div class="bx-code-wrap">
    <div class="bx-code-title">contact.html</div>
    <pre><code>&lt;form action=<span class="tok-str">"submit.php"</span> method=<span class="tok-str">"POST"</span>&gt;
  &lt;input type=<span class="tok-str">"text"</span> name=<span class="tok-str">"name"</span> required&gt;
  &lt;input type=<span class="tok-str">"email"</span> name=<span class="tok-str">"email"</span> required&gt;
  &lt;textarea name=<span class="tok-str">"message"</span> required&gt;&lt;/textarea&gt;
  &lt;input type=<span class="tok-str">"text"</span> name=<span class="tok-str">"website"</span> class=<span class="tok-str">"bx-hidden-field"</span> autocomplete=<span class="tok-str">"off"</span> tabindex=<span class="tok-str">"-1"</span>&gt;
  &lt;button type=<span class="tok-str">"submit"</span>&gt;Send&lt;/button&gt;
&lt;/form&gt;</code></pre>
  </div>

  <p>That extra <code>website</code> field is not a mistake. It is the honeypot the next section relies on, and it needs to already exist in the markup.</p>

  <div class="bx-section-head">
    <span class="bx-num">03</span>
    <h2 class="bx-h2" id="adding-a-honeypot-field-to-catch-bots">Adding a Honeypot Field to Catch Bots</h2>
    <div class="bx-rule"></div>
  </div>

  <p>A honeypot is a form field real visitors never see or fill in, but that most automated bots fill in anyway since they do not render the page.</p>

  <div class="bx-code-wrap">
    <div class="bx-code-title">submit.php</div>
    <pre><code><span class="tok-kw">if</span> (!<span class="tok-fn">empty</span>(<span class="tok-val">$_POST</span>[<span class="tok-str">'website'</span>])) {
    <span class="tok-cm">// a filled honeypot means a bot, so exit quietly with no error</span>
    <span class="tok-fn">http_response_code</span>(<span class="tok-val">200</span>);
    <span class="tok-kw">exit</span>;
}</code></pre>
  </div>

  <p>Hiding the field with CSS instead of <code>type="hidden"</code> matters, since some bots specifically skip inputs with a hidden type but still fill in a text field they can see in the raw markup. Setting <a href="https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/tabindex" target="_blank" rel="noopener"><code>tabindex</code></a> to a negative value also keeps the field out of the normal keyboard navigation order for real visitors.</p>

  <div class="bx-code-wrap">
    <div class="bx-code-title">style.css</div>
    <pre><code><span class="tok-sel">.bx-hidden-field</span> {
  <span class="tok-prop">position</span>: <span class="tok-val">absolute</span>;
  <span class="tok-prop">left</span>: <span class="tok-val">-9999px</span>;
}</code></pre>
  </div>

  <div class="bx-section-head">
    <span class="bx-num">04</span>
    <h2 class="bx-h2" id="rate-limiting-submissions-by-ip">Rate Limiting Submissions by IP</h2>
    <div class="bx-rule"></div>
  </div>

  <p>A honeypot stops simple bots, but a more determined script can still hammer the form with dozens of submissions a minute from the same address.</p>

  <div class="bx-code-wrap">
    <div class="bx-code-title">rate_limit.php</div>
    <pre><code><span class="tok-kw">function</span> <span class="tok-fn">is_rate_limited</span>(<span class="tok-val">$ip</span>, <span class="tok-val">$max_per_hour</span> = <span class="tok-val">5</span>) {
    <span class="tok-val">$file</span> = sys_get_temp_dir() . <span class="tok-str">'/rate_'</span> . md5(<span class="tok-val">$ip</span>) . <span class="tok-str">'.json'</span>;
    <span class="tok-val">$now</span> = time();
    <span class="tok-val">$hits</span> = file_exists(<span class="tok-val">$file</span>) ? json_decode(file_get_contents(<span class="tok-val">$file</span>), <span class="tok-val">true</span>) : [];
    <span class="tok-val">$hits</span> = array_filter(<span class="tok-val">$hits</span>, <span class="tok-kw">fn</span>(<span class="tok-val">$t</span>) => <span class="tok-val">$now</span> - <span class="tok-val">$t</span> &lt; <span class="tok-val">3600</span>);

    <span class="tok-kw">if</span> (count(<span class="tok-val">$hits</span>) >= <span class="tok-val">$max_per_hour</span>) {
        <span class="tok-kw">return</span> <span class="tok-val">true</span>;
    }

    <span class="tok-val">$hits</span>[] = <span class="tok-val">$now</span>;
    file_put_contents(<span class="tok-val">$file</span>, json_encode(<span class="tok-val">$hits</span>));
    <span class="tok-kw">return</span> <span class="tok-val">false</span>;
}</code></pre>
  </div>

  <p>A five submission per hour limit is generous for a real visitor filling out a contact form once, but tight enough to stop a script from flooding the inbox. PHPMailer itself, available through <a href="https://packagist.org/packages/phpmailer/phpmailer" target="_blank" rel="noopener">Packagist</a> and installed with <a href="https://getcomposer.org/" target="_blank" rel="noopener">Composer</a>, still handles the actual sending once a message clears every check in this guide.</p>

  <div class="bx-section-head">
    <span class="bx-num">05</span>
    <h2 class="bx-h2" id="validating-and-sanitizing-input-server-side">Validating and Sanitizing Input Server Side</h2>
    <div class="bx-rule"></div>
  </div>

  <p>Client side validation is easy to bypass, since a bot skips the browser entirely and sends a POST request directly to the PHP file.</p>

  <div class="bx-code-wrap">
    <div class="bx-code-title">validate.php</div>
    <pre><code><span class="tok-val">$name</span> = <span class="tok-fn">trim</span>(<span class="tok-fn">filter_input</span>(<span class="tok-val">INPUT_POST</span>, <span class="tok-str">'name'</span>, <span class="tok-val">FILTER_SANITIZE_SPECIAL_CHARS</span>));
<span class="tok-val">$email</span> = <span class="tok-fn">filter_input</span>(<span class="tok-val">INPUT_POST</span>, <span class="tok-str">'email'</span>, <span class="tok-val">FILTER_VALIDATE_EMAIL</span>);
<span class="tok-val">$message</span> = <span class="tok-fn">trim</span>(<span class="tok-fn">filter_input</span>(<span class="tok-val">INPUT_POST</span>, <span class="tok-str">'message'</span>, <span class="tok-val">FILTER_SANITIZE_SPECIAL_CHARS</span>));

<span class="tok-kw">if</span> (!<span class="tok-val">$name</span> || !<span class="tok-val">$email</span> || !<span class="tok-val">$message</span>) {
    <span class="tok-kw">exit</span>(<span class="tok-str">'Please fill in every field with a valid value.'</span>);
}</code></pre>
  </div>

  <p><a href="https://www.php.net/manual/en/filter.filters.validate.php" target="_blank" rel="noopener"><code>FILTER_VALIDATE_EMAIL</code></a> catches most malformed addresses on its own, and rejecting the submission outright when it fails keeps obviously fake entries out of the message.</p>

  <div class="bx-table-wrap">
    <table class="bx-table">
      <thead><tr><th>Layer</th><th>Stops</th><th>Visitor Friction</th></tr></thead>
      <tbody>
        <tr><td>Honeypot field</td><td>Simple form scraping bots</td><td>None, invisible to real visitors</td></tr>
        <tr><td>Rate limiting by IP</td><td>Scripted flooding attacks</td><td>None for normal one time submissions</td></tr>
        <tr><td>Server side validation</td><td>Malformed or fake data</td><td>None, just standard field rules</td></tr>
        <tr><td>reCAPTCHA v3</td><td>Sophisticated bots and scrapers</td><td>Very low, runs silently in the background</td></tr>
      </tbody>
    </table>
  </div>

  <div class="bx-section-head">
    <span class="bx-num">06</span>
    <h2 class="bx-h2" id="protecting-the-form-with-a-csrf-token">Protecting the Form With a CSRF Token</h2>
    <div class="bx-rule"></div>
  </div>

  <p>A cross site request forgery token confirms the submission actually came from the form on your own site, not from a request forged on another page. <a href="https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html" target="_blank" rel="noopener">OWASP's CSRF prevention guide</a> covers the reasoning behind this in more depth than a single contact form needs, but it is worth reading once.</p>

  <div class="bx-code-wrap">
    <div class="bx-code-title">csrf.php</div>
    <pre><code>session_start();
<span class="tok-kw">if</span> (empty(<span class="tok-val">$_SESSION</span>[<span class="tok-str">'csrf_token'</span>])) {
    <span class="tok-val">$_SESSION</span>[<span class="tok-str">'csrf_token'</span>] = bin2hex(random_bytes(<span class="tok-val">32</span>));
}
<span class="tok-cm">// echo this into a hidden input named csrf_token when rendering the form</span>

<span class="tok-kw">if</span> (<span class="tok-val">$_POST</span>[<span class="tok-str">'csrf_token'</span> ?? <span class="tok-str">''</span>] !== <span class="tok-val">$_SESSION</span>[<span class="tok-str">'csrf_token'</span>]) {
    <span class="tok-fn">http_response_code</span>(<span class="tok-val">403</span>);
    <span class="tok-kw">exit</span>(<span class="tok-str">'Invalid request.'</span>);
}</code></pre>
  </div>

  <p><a href="https://www.php.net/manual/en/function.random-bytes.php" target="_blank" rel="noopener"><code>random_bytes()</code></a> generates a cryptographically strong token, which is a meaningfully different guarantee than a predictable value like a timestamp would give.</p>

  <div class="bx-section-head">
    <span class="bx-num">07</span>
    <h2 class="bx-h2" id="adding-google-recaptcha-v3-for-a-final-layer">Adding Google reCAPTCHA v3 for a Final Layer</h2>
    <div class="bx-rule"></div>
  </div>

  <p>The layers above stop most automated traffic. <a href="https://developers.google.com/recaptcha/docs/v3" target="_blank" rel="noopener">reCAPTCHA v3</a> catches the more sophisticated bots that get past everything else, and it runs invisibly in the background. Registering a site key takes a few minutes through the <a href="https://www.google.com/recaptcha/admin" target="_blank" rel="noopener">reCAPTCHA admin console</a>.</p>

  <div class="bx-code-wrap">
    <div class="bx-code-title">verify_recaptcha.php</div>
    <pre><code><span class="tok-kw">function</span> <span class="tok-fn">verify_recaptcha</span>(<span class="tok-val">$token</span>, <span class="tok-val">$secret</span>) {
    <span class="tok-val">$response</span> = file_get_contents(
        <span class="tok-str">'https://www.google.com/recaptcha/api/siteverify?secret='</span> . <span class="tok-val">$secret</span> . <span class="tok-str">'&response='</span> . <span class="tok-val">$token</span>
    );
    <span class="tok-val">$result</span> = json_decode(<span class="tok-val">$response</span>, <span class="tok-val">true</span>);
    <span class="tok-kw">return</span> (<span class="tok-val">$result</span>[<span class="tok-str">'success'</span>] ?? <span class="tok-val">false</span>) && (<span class="tok-val">$result</span>[<span class="tok-str">'score'</span>] ?? <span class="tok-val">0</span>) >= <span class="tok-val">0.5</span>;
}</code></pre>
  </div>

  <p>The score returned ranges from 0 to 1, and a threshold around 0.5 is a reasonable starting point that most sites can tune later based on real traffic.</p>

  <div class="bx-section-head">
    <span class="bx-num">08</span>
    <h2 class="bx-h2" id="sending-the-verified-message-with-phpmailer">Sending the Verified Message With PHPMailer</h2>
    <div class="bx-rule"></div>
  </div>

  <p>Once a submission has passed every check above, sending it uses the same PHPMailer pattern this series has covered for writing send email code in PHP, an SMTP call wrapped in a try and catch block.</p>

  <div class="bx-code-wrap">
    <div class="bx-code-title">send_message.php</div>
    <pre><code><span class="tok-kw">if</span> (!is_rate_limited(<span class="tok-val">$_SERVER</span>[<span class="tok-str">'REMOTE_ADDR'</span>]) &amp;&amp; verify_recaptcha(<span class="tok-val">$_POST</span>[<span class="tok-str">'g_recaptcha_response'</span>], <span class="tok-val">$secret</span>)) {
    send_notification_email(<span class="tok-str">'contact@brandella.in'</span>, <span class="tok-str">'New contact form message'</span>, <span class="tok-val">$message</span>);
}</code></pre>
  </div>

  <p>Every layer runs before this final step, so by the time <code>send_notification_email()</code> executes, the message has already survived four separate checks. This is the complete shape of a php contact form with spam protection, four layers working together instead of one control doing all the work.</p>

  <ul class="bx-checklist">
    <li><b>Never trust the honeypot alone:</b> a determined bot can eventually learn to skip a hidden field, so layer it with rate limiting and validation.</li>
    <li><b>Store the reCAPTCHA secret as an environment variable:</b> it belongs alongside SMTP credentials, never committed to the repository.</li>
    <li><b>Log rejected submissions briefly:</b> a short log of blocked attempts helps confirm the protections are actually catching something.</li>
    <li><b>Keep error messages generic:</b> telling a bot exactly which check failed only helps it adjust and try again.</li>
    <li><b>Review the reCAPTCHA score threshold periodically:</b> real visitor behavior varies by site, so 0.5 is a starting point, not a fixed rule.</li>
  </ul>

  <div class="bx-ad">
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-3931314195561246" crossorigin="anonymous"></script>
    <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-3931314195561246" data-ad-slot="4249015278" data-ad-format="auto" data-full-width-responsive="true"></ins>
    <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
  </div>

  <div class="bx-section-head">
    <span class="bx-num">09</span>
    <h2 class="bx-h2" id="watch-building-a-php-contact-form">Watch: Building a PHP Contact Form</h2>
    <div class="bx-rule"></div>
  </div>

  <p>Traversy Media's PHP series walks through a working contact form handler, which pairs well with the honeypot and validation layers added in this guide.</p>

  <div style="position:relative; padding-bottom:56.25%; height:0; overflow:hidden; border-radius:12px; margin:18px 0 8px;">
    <iframe src="https://www.youtube.com/embed/tJ5eUgOxITE" title="PHP Front To Back, PHP Contact Form" style="position:absolute; top:0; left:0; width:100%; height:100%; border:0;" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen loading="lazy"></iframe>
  </div>
  <p style="font-size:14px; color:var(--bx-charcoal-soft); margin-top:6px;">Video credit: Traversy Media.</p>

  <p>The base handler shown in the video is a solid starting point once the honeypot, rate limiting, and reCAPTCHA layers from this guide sit in front of it.</p>

  <svg width="100%" height="220" viewBox="0 0 800 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Diagram of a php contact form with spam protection moving a submission through honeypot, rate limit, validation, and reCAPTCHA checks before delivery" style="margin:26px 0;">
    <rect width="800" height="220" fill="#f4faef" rx="12"/>
    <g font-family="Open Sans, sans-serif" font-size="13" fill="#2b2b2b">
      <rect x="15" y="85" width="115" height="55" rx="8" fill="#ffffff" stroke="#5DB92E" stroke-width="2"/>
      <text x="72" y="117" text-anchor="middle" font-weight="700">Form Submit</text>

      <line x1="130" y1="112" x2="170" y2="112" stroke="#4a9e24" stroke-width="2" marker-end="url(#arrow)"/>

      <rect x="170" y="85" width="115" height="55" rx="8" fill="#ffffff" stroke="#5DB92E" stroke-width="2"/>
      <text x="227" y="117" text-anchor="middle" font-weight="700">Honeypot</text>

      <line x1="285" y1="112" x2="325" y2="112" stroke="#4a9e24" stroke-width="2" marker-end="url(#arrow)"/>

      <rect x="325" y="85" width="115" height="55" rx="8" fill="#ffffff" stroke="#5DB92E" stroke-width="2"/>
      <text x="382" y="117" text-anchor="middle" font-weight="700">Rate Limit</text>

      <line x1="440" y1="112" x2="480" y2="112" stroke="#4a9e24" stroke-width="2" marker-end="url(#arrow)"/>

      <rect x="480" y="85" width="115" height="55" rx="8" fill="#ffffff" stroke="#5DB92E" stroke-width="2"/>
      <text x="537" y="117" text-anchor="middle" font-weight="700">reCAPTCHA v3</text>

      <line x1="595" y1="112" x2="635" y2="112" stroke="#4a9e24" stroke-width="2" marker-end="url(#arrow)"/>

      <rect x="635" y="85" width="150" height="55" rx="8" fill="#2b2b2b" stroke="#5DB92E" stroke-width="2"/>
      <text x="710" y="117" text-anchor="middle" font-weight="700" fill="#5DB92E">Inbox Delivery</text>
    </g>
    <defs>
      <marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto" markerUnits="strokeWidth">
        <path d="M0,0 L0,6 L9,3 z" fill="#4a9e24"/>
      </marker>
    </defs>
  </svg>

    <div class="bx-faq">
    <h3 class="bx-h3">Frequently Asked Questions</h3>

    <div class="bx-faq-item">
      <button type="button" class="bx-faq-q">Is a honeypot field enough spam protection on its own?</button>
      <div class="bx-faq-a"><p>It stops simple bots but not every one. Pairing it with rate limiting and reCAPTCHA covers the more determined scripts a honeypot alone will miss.</p></div>
    </div>
    <div class="bx-faq-item">
      <button type="button" class="bx-faq-q">Does a php contact form with spam protection need a database?</button>
      <div class="bx-faq-a"><p>No. The rate limiting example in this guide uses a temporary file per IP address, which is enough for a small to medium site without any database setup.</p></div>
    </div>
    <div class="bx-faq-item">
      <button type="button" class="bx-faq-q">Will reCAPTCHA v3 show a visible checkbox to visitors?</button>
      <div class="bx-faq-a"><p>No. Version 3 runs entirely in the background and returns a score, unlike the older checkbox based version 2 that visitors had to click.</p></div>
    </div>
    <div class="bx-faq-item">
      <button type="button" class="bx-faq-q">What happens if a real visitor gets rate limited by mistake?</button>
      <div class="bx-faq-a"><p>A five submission per hour limit rarely affects a genuine visitor, since nobody normally submits the same contact form that many times in one session.</p></div>
    </div>
    <div class="bx-faq-item">
      <button type="button" class="bx-faq-q">Is a CSRF token really necessary for a simple contact form?</button>
      <div class="bx-faq-a"><p>Yes. Without it, another site could submit forged requests to your form handler using a visitor's own browser session without their knowledge.</p></div>
    </div>
  </div>

  <div class="bx-learn">
    <h2 id="what-we-learn-today">What We Learn Today</h2>
    <div class="bx-learn-grid">
      <div class="bx-learn-card"><span class="bx-learn-num">1</span><div><h4>Layers beat a single defense</h4><p>No single check stops every kind of automated traffic on its own.</p></div></div>
      <div class="bx-learn-card"><span class="bx-learn-num">2</span><div><h4>A honeypot is invisible by design</h4><p>Real visitors never notice it, but simple bots fill it in anyway.</p></div></div>
      <div class="bx-learn-card"><span class="bx-learn-num">3</span><div><h4>Rate limiting needs no database</h4><p>A temporary file per IP address is enough for most small sites.</p></div></div>
      <div class="bx-learn-card"><span class="bx-learn-num">4</span><div><h4>Server side validation is not optional</h4><p>Client side checks alone are trivial for a bot to bypass entirely.</p></div></div>
      <div class="bx-learn-card"><span class="bx-learn-num">5</span><div><h4>CSRF tokens confirm the source</h4><p>They prove a submission came from your own form, not a forged request.</p></div></div>
      <div class="bx-learn-card"><span class="bx-learn-num">6</span><div><h4>reCAPTCHA v3 adds a final filter</h4><p>It catches the sophisticated bots everything else lets through.</p></div></div>
    </div>
  </div>

  <div class="bx-ad">
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-3931314195561246" crossorigin="anonymous"></script>
    <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-3931314195561246" data-ad-slot="4249015278" data-ad-format="auto" data-full-width-responsive="true"></ins>
    <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
  </div>

  <div class="bx-cta">
    <h3>Ready to Stop Spam on Your Contact Form?</h3>
    <p>Pair a php contact form with spam protection alongside a wider toolkit to keep every inbound message legitimate.</p>
    <div class="bx-cta-btns">
      <a href="/10-best-free-seo-tools-every-marketer-should-use/" target="_blank" rel="noopener">Explore Free SEO Tools</a>
      <a href="/best-keyword-research-tools-compared/" target="_blank" rel="noopener" class="bx-cta-outline">Compare Keyword Tools</a>
    </div>
  </div>

</div>

<script>
(function() {
  var items = document.querySelectorAll('.bx-faq-item');
  items.forEach(function(item) {
    var q = item.querySelector('.bx-faq-q');
    var a = item.querySelector('.bx-faq-a');
    q.addEventListener('click', function() {
      var isOpen = item.classList.contains('open');
      items.forEach(function(other) {
        other.classList.remove('open');
        other.querySelector('.bx-faq-a').style.maxHeight = null;
      });
      if (!isOpen) {
        item.classList.add('open');
        a.style.maxHeight = a.scrollHeight + 'px';
      }
    });
  });
})();
</script>
