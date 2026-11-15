---
title: "Send Email Code in PHP: Build a Reliable Mailer in 6 Steps"
slug: "send-email-code-in-php"
date: "2026-08-25T07:18:55"
updated: "2026-08-25T07:20:34"
author: "santajigade"
categories: ["development", "php"]
primaryCategory: "development"
description: "Learn how to write send email code in PHP using PHPMailer and SMTP, with attachments, error handling, and safe testing."
focusKeyword: "send email code in php"
image: "/wp-content/uploads/2026/08/send-email-code-in-php.webp"
imageAlt: "send email code in php"
words: 1410
views: 289
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

.bx-stats { display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; margin: 22px 0 30px; }
.bx-stat-card { background: #f4faef; border: 1px solid #dff0d3; border-radius: 10px; padding: 20px 14px; text-align: center; }
.bx-stat-num { font-family: var(--bx-disp); font-weight: 800; font-size: 30px; color: var(--bx-green-deep); display: block; line-height: 1.1; }
.bx-stat-label { font-size: 14px; color: var(--bx-charcoal-soft); margin-top: 6px; display: block; }
@media (max-width: 640px) { .bx-stats { grid-template-columns: 1fr; } }

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
table.bx-table thead tr { background: var(--bx-charcoal); }
table.bx-table thead th { color: #fff; font-family: var(--bx-disp); font-weight: 700; text-align: left; padding: 13px 14px; font-size: 17px; }
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
    <span class="bx-pill">Email</span>
    <span class="bx-pill">SMTP</span>
  </div>

  <p class="bx-lede">A contact form that quietly fails to deliver its emails is worse than no form at all, because nobody finds out until a customer complains somewhere else. Send email code in PHP done properly means SMTP, authentication, and a way to know when a message actually failed.</p>

  <div class="bx-section-head">
    <span class="bx-num">01</span>
    <h2 class="bx-h2" id="why-send-email-code-in-php-needs-more-than-the-mail-function">Why Send Email Code in PHP Needs More Than the mail Function</h2>
    <div class="bx-rule"></div>
  </div>

  <p>PHP ships with a built in <a href="https://www.php.net/manual/en/function.mail.php" target="_blank" rel="noopener"><code>mail()</code></a> function, and it looks like the obvious starting point for sending a message from a form.</p>

  <p>In practice it depends on the server having a working local mail transfer agent configured, which many shared hosts either skip or configure poorly.</p>

  <p>Messages sent through a poorly configured <code>mail()</code> call also tend to land in spam, since they usually skip proper authentication headers entirely.</p>

  <p>An SMTP library talking directly to a real mail provider avoids both problems, which is why most working PHP applications reach for one instead.</p>

  <div class="bx-ad">
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-3931314195561246" crossorigin="anonymous"></script>
    <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-3931314195561246" data-ad-slot="4249015278" data-ad-format="auto" data-full-width-responsive="true"></ins>
    <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
  </div>

  <div class="bx-section-head">
    <span class="bx-num">02</span>
    <h2 class="bx-h2" id="choosing-how-to-send-mail-from-php">Choosing How to Send Mail From PHP</h2>
    <div class="bx-rule"></div>
  </div>

  <p>Three realistic options cover almost every PHP project, and picking between them mostly comes down to how much control the app needs over delivery.</p>

  <div class="bx-table-wrap">
    <table class="bx-table">
      <thead><tr><th>Approach</th><th>Reliability</th><th>Best For</th></tr></thead>
      <tbody>
        <tr><td>Built in mail() function</td><td>Depends entirely on server configuration</td><td>Quick local testing only</td></tr>
        <tr><td>PHPMailer over SMTP</td><td>Reliable, authenticated delivery</td><td>Most production applications</td></tr>
        <tr><td>Transactional email API (SendGrid, Mailgun)</td><td>Very reliable, includes analytics</td><td>High volume or marketing style sending</td></tr>
      </tbody>
    </table>
  </div>

  <p>This guide builds around <a href="https://github.com/PHPMailer/PHPMailer" target="_blank" rel="noopener">PHPMailer</a>, the most widely used SMTP library in the PHP ecosystem, since it fits both a small contact form and a larger notification system. Both <a href="https://docs.sendgrid.com/for-developers/sending-email/api-getting-started" target="_blank" rel="noopener">SendGrid</a> and <a href="https://documentation.mailgun.com/en/latest/quickstart-sending.html" target="_blank" rel="noopener">Mailgun</a> also publish their own PHP quickstarts, worth comparing once send volume grows past what shared SMTP handles well.</p>

  <div class="bx-section-head">
    <span class="bx-num">03</span>
    <h2 class="bx-h2" id="installing-phpmailer-with-composer">Installing PHPMailer With Composer</h2>
    <div class="bx-rule"></div>
  </div>

  <p>Composer is the standard way to pull PHPMailer into a project, and it also handles autoloading so nothing needs a manual include path.</p>

  <div class="bx-code-wrap">
    <div class="bx-code-title">terminal</div>
    <pre><code><span class="tok-cm"># install PHPMailer through Composer</span>
composer <span class="tok-fn">require</span> phpmailer/phpmailer</code></pre>
  </div>

  <p>If the project has no <code>composer.json</code> yet, running <code>composer init</code> first creates one, and PHPMailer becomes the first real dependency listed inside it.</p>

  <div class="bx-section-head">
    <span class="bx-num">04</span>
    <h2 class="bx-h2" id="writing-a-basic-send-email-function">Writing a Basic Send Email Function</h2>
    <div class="bx-rule"></div>
  </div>

  <p>A single reusable function keeps SMTP configuration in one place instead of scattered across every form handler that needs to send a message.</p>

  <div class="bx-code-wrap">
    <div class="bx-code-title">mailer.php</div>
    <pre><code><span class="tok-kw">require</span> <span class="tok-str">'vendor/autoload.php'</span>;

<span class="tok-kw">use</span> PHPMailer\PHPMailer\PHPMailer;
<span class="tok-kw">use</span> PHPMailer\PHPMailer\Exception;

<span class="tok-kw">function</span> <span class="tok-fn">send_notification_email</span>(<span class="tok-val">$to</span>, <span class="tok-val">$subject</span>, <span class="tok-val">$body</span>) {
    <span class="tok-val">$mail</span> = <span class="tok-kw">new</span> PHPMailer(<span class="tok-val">true</span>);

    <span class="tok-kw">try</span> {
        <span class="tok-val">$mail</span>->isSMTP();
        <span class="tok-val">$mail</span>->Host = <span class="tok-str">'smtp.gmail.com'</span>;
        <span class="tok-val">$mail</span>->SMTPAuth = <span class="tok-val">true</span>;
        <span class="tok-val">$mail</span>->Username = getenv(<span class="tok-str">'SMTP_USER'</span>);
        <span class="tok-val">$mail</span>->Password = getenv(<span class="tok-str">'SMTP_PASS'</span>);
        <span class="tok-val">$mail</span>->SMTPSecure = <span class="tok-str">'tls'</span>;
        <span class="tok-val">$mail</span>->Port = <span class="tok-val">587</span>;

        <span class="tok-val">$mail</span>->setFrom(<span class="tok-str">'noreply@brandella.in'</span>, <span class="tok-str">'Brandella Journal'</span>);
        <span class="tok-val">$mail</span>->addAddress(<span class="tok-val">$to</span>);
        <span class="tok-val">$mail</span>->Subject = <span class="tok-val">$subject</span>;
        <span class="tok-val">$mail</span>->Body = <span class="tok-val">$body</span>;

        <span class="tok-val">$mail</span>->send();
        <span class="tok-kw">return</span> <span class="tok-val">true</span>;
    } <span class="tok-kw">catch</span> (Exception <span class="tok-val">$e</span>) {
        <span class="tok-fn">error_log</span>(<span class="tok-str">"Mail failed: "</span> . <span class="tok-val">$mail</span>->ErrorInfo);
        <span class="tok-kw">return</span> <span class="tok-val">false</span>;
    }
}</code></pre>
  </div>

  <p>Reading credentials with <code>getenv()</code> instead of hardcoding them keeps a real password out of version control entirely. Gmail also requires an <a href="https://support.google.com/accounts/answer/185833" target="_blank" rel="noopener">app password</a> rather than the normal account password once two factor authentication is turned on.</p>

  <div class="bx-section-head">
    <span class="bx-num">05</span>
    <h2 class="bx-h2" id="sending-html-emails-with-dynamic-content">Sending HTML Emails With Dynamic Content</h2>
    <div class="bx-rule"></div>
  </div>

  <p>Plain text is fine for a simple alert, but most real notifications benefit from formatting, a logo, and a clear call to action.</p>

  <div class="bx-code-wrap">
    <div class="bx-code-title">html_mailer.php</div>
    <pre><code><span class="tok-val">$mail</span>->isHTML(<span class="tok-val">true</span>);
<span class="tok-val">$mail</span>->Subject = <span class="tok-str">'Your order has shipped'</span>;
<span class="tok-val">$mail</span>->Body = <span class="tok-fn">sprintf</span>(
    <span class="tok-str">'&lt;h2&gt;Thanks, %s&lt;/h2&gt;&lt;p&gt;Order #%s is on its way.&lt;/p&gt;'</span>,
    <span class="tok-fn">htmlspecialchars</span>(<span class="tok-val">$customer_name</span>),
    <span class="tok-fn">htmlspecialchars</span>(<span class="tok-val">$order_id</span>)
);
<span class="tok-val">$mail</span>->AltBody = <span class="tok-fn">sprintf</span>(<span class="tok-str">'Thanks, %s. Order #%s is on its way.'</span>, <span class="tok-val">$customer_name</span>, <span class="tok-val">$order_id</span>);</code></pre>
  </div>

  <p><code>htmlspecialchars()</code> around any value that came from a user matters here, since an unescaped name field is a real injection risk inside an HTML email body.</p>

  <p>Setting <code>AltBody</code> gives email clients that block HTML a readable plain text fallback instead of a blank or broken message.</p>

  <div class="bx-section-head">
    <span class="bx-num">06</span>
    <h2 class="bx-h2" id="adding-attachments">Adding Attachments</h2>
    <div class="bx-rule"></div>
  </div>

  <p>An invoice, a receipt, or a generated report often needs to travel with the email rather than living behind a separate download link.</p>

  <div class="bx-code-wrap">
    <div class="bx-code-title">attachment.php</div>
    <pre><code><span class="tok-val">$mail</span>->addAttachment(<span class="tok-str">'/tmp/invoice_1042.pdf'</span>, <span class="tok-str">'Invoice.pdf'</span>);</code></pre>
  </div>

  <p>PHPMailer reads the file straight from disk, so anything generated moments earlier by an invoice script can be attached without an extra upload step.</p>

  <div class="bx-section-head">
    <span class="bx-num">07</span>
    <h2 class="bx-h2" id="handling-errors-and-delivery-failures">Handling Errors and Delivery Failures</h2>
    <div class="bx-rule"></div>
  </div>

  <p>A send that fails silently is the exact problem this whole approach is meant to fix, so failures need to surface somewhere a developer will actually see them.</p>

  <div class="bx-code-wrap">
    <div class="bx-code-title">error_handling.php</div>
    <pre><code><span class="tok-val">$mail</span>->SMTPDebug = <span class="tok-val">0</span>;

<span class="tok-kw">if</span> (!send_notification_email(<span class="tok-val">$to</span>, <span class="tok-val">$subject</span>, <span class="tok-val">$body</span>)) {
    <span class="tok-fn">error_log</span>(<span class="tok-fn">sprintf</span>(<span class="tok-str">'Notification to %s failed at %s'</span>, <span class="tok-val">$to</span>, <span class="tok-fn">date</span>(<span class="tok-str">'c'</span>)));
}</code></pre>
  </div>

  <p>Logging the recipient and timestamp on failure turns a silent problem into something a support ticket or a monitoring alert can actually catch. This is the part of send email code in PHP that most tutorials skip, and it is usually the part that saves a debugging session later.</p>

  <div class="bx-section-head">
    <span class="bx-num">08</span>
    <h2 class="bx-h2" id="testing-emails-safely-before-going-live">Testing Emails Safely Before Going Live</h2>
    <div class="bx-rule"></div>
  </div>

  <p>Sending real test emails to a real inbox during development is how a test message ends up in front of an actual customer by accident.</p>

  <p>A tool like <a href="https://mailtrap.io/" target="_blank" rel="noopener">Mailtrap</a> catches outgoing SMTP traffic in a safe sandbox inbox, so every send during development can be inspected without ever leaving the test environment.</p>

  <ul class="bx-checklist">
    <li><b>Swap SMTP credentials by environment:</b> point at Mailtrap locally and the real provider in production through environment variables, never a hardcoded host.</li>
    <li><b>Check the AltBody every time:</b> a broken plain text fallback is easy to miss since most developers only ever look at the HTML version.</li>
    <li><b>Rate limit outgoing mail:</b> a loop that sends hundreds of emails without pacing can trip a provider's spam protection mid batch.</li>
    <li><b>Verify <a href="https://www.rfc-editor.org/rfc/rfc7208" target="_blank" rel="noopener">SPF</a> and <a href="https://www.cloudflare.com/learning/dns/dns-records/dns-dkim-record/" target="_blank" rel="noopener">DKIM</a> on the sending domain:</b> authentication records matter as much as the code, since even perfect code cannot fix a missing DNS record.</li>
    <li><b>Never log a full email body with personal data:</b> log the recipient and status, not the message contents, to avoid storing sensitive information in a log file.</li>
  </ul>

  <div class="bx-ad">
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-3931314195561246" crossorigin="anonymous"></script>
    <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-3931314195561246" data-ad-slot="4249015278" data-ad-format="auto" data-full-width-responsive="true"></ins>
    <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
  </div>

  <div class="bx-section-head">
    <span class="bx-num">09</span>
    <h2 class="bx-h2" id="watch-sending-email-with-phpmailer">Watch: Sending Email With PHPMailer</h2>
    <div class="bx-rule"></div>
  </div>

  <p>Codecourse walks through a working PHPMailer setup end to end, which pairs well with the environment variable pattern used throughout this guide.</p>

  <div style="position:relative; padding-bottom:56.25%; height:0; overflow:hidden; border-radius:12px; margin:18px 0 8px;">
    <iframe src="https://www.youtube.com/embed/mQ3TXOxj7cs" title="Send Email With PHPMailer: Basic email" style="position:absolute; top:0; left:0; width:100%; height:100%; border:0;" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen loading="lazy"></iframe>
  </div>
  <p style="font-size:14px; color:var(--bx-charcoal-soft); margin-top:6px;">Video credit: Codecourse.</p>

  <p>Seeing the SMTP handshake fail and succeed on screen makes the try and catch block in the code above much easier to reason about.</p>

  <svg width="100%" height="220" viewBox="0 0 800 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Diagram of send email code in PHP moving from a form submission through PHPMailer and SMTP authentication to inbox delivery" style="margin:26px 0;">
    <rect width="800" height="220" fill="#f4faef" rx="12"/>
    <g font-family="Open Sans, sans-serif" font-size="14" fill="#2b2b2b">
      <rect x="20" y="85" width="130" height="60" rx="8" fill="#ffffff" stroke="#5DB92E" stroke-width="2"/>
      <text x="85" y="112" text-anchor="middle" font-weight="700">Form</text>
      <text x="85" y="130" text-anchor="middle" font-weight="700">Submission</text>

      <line x1="150" y1="115" x2="200" y2="115" stroke="#4a9e24" stroke-width="2" marker-end="url(#arrow)"/>

      <rect x="200" y="85" width="140" height="60" rx="8" fill="#ffffff" stroke="#5DB92E" stroke-width="2"/>
      <text x="270" y="120" text-anchor="middle" font-weight="700">PHPMailer</text>

      <line x1="340" y1="115" x2="390" y2="115" stroke="#4a9e24" stroke-width="2" marker-end="url(#arrow)"/>

      <rect x="390" y="85" width="150" height="60" rx="8" fill="#ffffff" stroke="#5DB92E" stroke-width="2"/>
      <text x="465" y="120" text-anchor="middle" font-weight="700">SMTP Auth</text>

      <line x1="540" y1="115" x2="590" y2="115" stroke="#4a9e24" stroke-width="2" marker-end="url(#arrow)"/>

      <rect x="590" y="85" width="170" height="60" rx="8" fill="#2b2b2b" stroke="#5DB92E" stroke-width="2"/>
      <text x="675" y="120" text-anchor="middle" font-weight="700" fill="#5DB92E">Inbox Delivery</text>
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
      <button type="button" class="bx-faq-q">Why not just use the built in PHP mail function?</button>
      <div class="bx-faq-a"><p>It depends on local server configuration that is often missing or incomplete, and messages sent through it commonly land in spam because they lack proper authentication.</p></div>
    </div>
    <div class="bx-faq-item">
      <button type="button" class="bx-faq-q">What is the simplest way to write send email code in PHP that actually works?</button>
      <div class="bx-faq-a"><p>PHPMailer configured for SMTP with a real provider like Gmail, SendGrid, or Mailgun is the most reliable starting point, since it handles authentication and delivery details the built in function does not.</p></div>
    </div>
    <div class="bx-faq-item">
      <button type="button" class="bx-faq-q">Can PHPMailer send emails to multiple recipients at once?</button>
      <div class="bx-faq-a"><p>Yes. Calling addAddress multiple times adds more recipients, and addBCC or addCC work the same way for blind copies and carbon copies.</p></div>
    </div>
    <div class="bx-faq-item">
      <button type="button" class="bx-faq-q">How do I stop my emails from landing in spam?</button>
      <div class="bx-faq-a"><p>Authenticate through a real SMTP provider, set up SPF and DKIM records for the sending domain, and avoid spam trigger words in the subject line.</p></div>
    </div>
    <div class="bx-faq-item">
      <button type="button" class="bx-faq-q">Is it safe to store SMTP passwords directly in the PHP file?</button>
      <div class="bx-faq-a"><p>No. Environment variables or a properly excluded configuration file keep credentials out of version control, which matters even for a small internal project.</p></div>
    </div>
  </div>

  <div class="bx-learn">
    <h2 id="what-we-learn-today">What We Learn Today</h2>
    <div class="bx-learn-grid">
      <div class="bx-learn-card"><span class="bx-learn-num">1</span><div><h4>mail() is not reliable enough</h4><p>Server configuration and missing authentication headers make it a poor production choice.</p></div></div>
      <div class="bx-learn-card"><span class="bx-learn-num">2</span><div><h4>SMTP beats local mail transfer</h4><p>Authenticating with a real provider gets messages delivered instead of flagged.</p></div></div>
      <div class="bx-learn-card"><span class="bx-learn-num">3</span><div><h4>HTML needs a plain text fallback</h4><p>AltBody keeps the message readable for clients that block HTML.</p></div></div>
      <div class="bx-learn-card"><span class="bx-learn-num">4</span><div><h4>Errors must be visible</h4><p>A silent failure defeats the entire purpose of sending a notification.</p></div></div>
      <div class="bx-learn-card"><span class="bx-learn-num">5</span><div><h4>Testing needs a sandbox</h4><p>A tool like Mailtrap keeps test sends away from real inboxes.</p></div></div>
      <div class="bx-learn-card"><span class="bx-learn-num">6</span><div><h4>DNS matters as much as code</h4><p>SPF and DKIM records affect delivery just as much as the script itself.</p></div></div>
    </div>
  </div>

  <div class="bx-ad">
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-3931314195561246" crossorigin="anonymous"></script>
    <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-3931314195561246" data-ad-slot="4249015278" data-ad-format="auto" data-full-width-responsive="true"></ins>
    <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
  </div>

  <div class="bx-cta">
    <h3>Ready to Send Reliable Email From PHP?</h3>
    <p>Pair send email code in PHP with a wider toolkit to keep every notification landing where it should.</p>
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
