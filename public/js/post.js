/* Brandella Journal article page: TOC highlight and auto load next article. */
(function () {
  var embed = document.documentElement.classList.contains('embed');

  // In an iframe: open links in the main window, report height to parent.
  if (embed) {
    var base = document.createElement('base');
    base.target = '_top';
    document.head.appendChild(base);
    return;
  }

  // TOC: highlight the section being read
  var links = Array.prototype.slice.call(document.querySelectorAll('.toc-side a'));
  if (links.length && 'IntersectionObserver' in window) {
    var map = {};
    links.forEach(function (a) { map[decodeURIComponent(a.hash.slice(1))] = a; });
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting && map[e.target.id]) {
          links.forEach(function (l) { l.classList.remove('on'); });
          map[e.target.id].classList.add('on');
        }
      });
    }, { rootMargin: '0px 0px -70% 0px' });
    Object.keys(map).forEach(function (id) { var h = document.getElementById(id); if (h) io.observe(h); });
  }

  // Auto load next article (max 6). Each article loads in its own same origin
  // iframe so its BX scripts, styles and ids never clash with this page.
  var loader = document.querySelector('.next-loader');
  if (!loader || !('IntersectionObserver' in window)) return;
  var queue = [];
  try { queue = JSON.parse(loader.getAttribute('data-next') || '[]').slice(0, 6); } catch (e) { return; }
  var first = { url: location.pathname, title: document.title };
  var busy = false;
  var views = [];

  function size(frame) {
    try {
      var doc = frame.contentDocument;
      var h = Math.max(doc.documentElement.scrollHeight, doc.body.scrollHeight);
      frame.style.height = h + 'px';
    } catch (e) {}
  }

  function loadNext() {
    if (busy || !queue.length) return;
    busy = true;
    var url = queue.shift();
    var wrap = document.createElement('section');
    wrap.className = 'next-article';
    wrap.innerHTML = '<div class="container next-sep"><span>Next article</span></div>';
    var frame = document.createElement('iframe');
    frame.src = url;
    frame.title = 'Next article';
    frame.loading = 'eager';
    frame.setAttribute('scrolling', 'no');
    wrap.appendChild(frame);
    loader.parentNode.insertBefore(wrap, loader);
    frame.addEventListener('load', function () {
      size(frame);
      try {
        var doc = frame.contentDocument;
        if ('ResizeObserver' in window) new ResizeObserver(function () { size(frame); }).observe(doc.body);
        views.push({ el: wrap, url: url, title: doc.title });
        seen.observe(wrap);
      } catch (e) {}
      setTimeout(function () { busy = false; check(); }, 400);
    });
  }

  function check() {
    var r = loader.getBoundingClientRect();
    if (r.top < window.innerHeight * 2.5) loadNext();
  }

  var seen = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (!e.isIntersecting) return;
      var v = views.filter(function (x) { return x.el === e.target; })[0];
      if (v && location.pathname !== v.url) { history.replaceState(null, '', v.url); document.title = v.title; }
    });
  }, { rootMargin: '-45% 0px -50% 0px' });

  var top = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting && location.pathname !== first.url) { history.replaceState(null, '', first.url); document.title = first.title; }
    });
  }, { rootMargin: '-45% 0px -50% 0px' });
  var main = document.querySelector('article.post');
  if (main) top.observe(main);

  new IntersectionObserver(function (entries) {
    if (entries[0].isIntersecting) loadNext();
  }, { rootMargin: '0px 0px 1200px 0px' }).observe(loader);
})();

// Share bar: copy link button (falls back to the native share sheet where copy is not allowed)
(function () {
  document.addEventListener('click', function (e) {
    var b = e.target.closest && e.target.closest('.share-copy');
    if (!b) return;
    var url = b.getAttribute('data-url') || location.href;
    var tip = b.querySelector('.share-copied');
    function done(msg) { if (tip) { tip.textContent = msg; setTimeout(function () { tip.textContent = ''; }, 1800); } }
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(url).then(function () { done('Link copied'); }, function () { window.prompt('Copy this link', url); });
    } else if (navigator.share) {
      navigator.share({ url: url, title: document.title }).catch(function () {});
    } else {
      window.prompt('Copy this link', url);
    }
  });
})();
