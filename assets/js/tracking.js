/**
 * PE Collective — GA4 Custom Event Tracking
 *
 * Tracks: CTA clicks, job card clicks, newsletter signups,
 * tool review clicks, external links, and salary filter usage.
 *
 * Uses gtag() which is already loaded on every page.
 */
(function () {
  'use strict';

  // Guard: only run if gtag exists
  if (typeof gtag !== 'function') return;

  // ── Helper ──────────────────────────────────────────────
  function track(eventName, params) {
    gtag('event', eventName, params);
  }

  // ── CTA Button Clicks ──────────────────────────────────
  // Matches both .btn--primary/.btn--secondary (root pages)
  // and .nav-cta/.btn-subscribe/.btn-gold (generated pages)
  document.querySelectorAll(
    '.btn--primary, .btn--secondary, .nav-cta, .btn-subscribe, .btn-gold, .btn'
  ).forEach(function (el) {
    el.addEventListener('click', function () {
      var text = (el.textContent || '').trim().substring(0, 60);
      var href = el.getAttribute('href') || '';
      track('cta_click', {
        cta_text: text,
        cta_url: href,
        page_location: window.location.pathname
      });
    });
  });

  // ── Job Card Clicks ────────────────────────────────────
  document.querySelectorAll('.job-card, .job-card__title a, a[href*="/jobs/"]').forEach(function (el) {
    el.addEventListener('click', function () {
      var title = '';
      // Try to get job title from card content
      var titleEl = el.querySelector('.job-card__title') || el.closest('.job-card');
      if (titleEl) {
        var h3 = titleEl.querySelector('h3, h2, .job-card__title');
        if (h3) title = (h3.textContent || '').trim();
      }
      if (!title) title = (el.textContent || '').trim().substring(0, 80);

      track('job_card_click', {
        job_title: title,
        link_url: el.getAttribute('href') || '',
        page_location: window.location.pathname
      });
    });
  });

  // ── Newsletter Form Submissions ────────────────────────
  // Track on-site newsletter captures (Resend-powered forms)
  document.querySelectorAll(
    '.newsletter-capture__form, .newsletter-inline__form, .cta-section__form'
  ).forEach(function (form) {
    form.addEventListener('submit', function () {
      var email = form.querySelector('input[type="email"]');
      track('newsletter_signup', {
        form_location: window.location.pathname,
        has_email: !!(email && email.value)
      });
    });
  });

  // ── Tool Review / Comparison Clicks ────────────────────
  document.querySelectorAll('.cta-comparison__card a, .tool-card a').forEach(function (el) {
    el.addEventListener('click', function () {
      track('tool_cta_click', {
        tool_name: (el.textContent || '').trim().substring(0, 40),
        tool_url: el.getAttribute('href') || '',
        page_location: window.location.pathname
      });
    });
  });

  // ── External Link Clicks ───────────────────────────────
  document.querySelectorAll('a[target="_blank"]').forEach(function (el) {
    el.addEventListener('click', function () {
      track('outbound_click', {
        link_text: (el.textContent || '').trim().substring(0, 60),
        link_url: el.getAttribute('href') || '',
        page_location: window.location.pathname
      });
    });
  });

  // ── Salary Filter Usage ────────────────────────────────
  // Salary pages use select/input filters — track changes
  document.querySelectorAll(
    '.salary-filters select, .salary-filters input, .filter-bar select, .filter-bar input'
  ).forEach(function (el) {
    el.addEventListener('change', function () {
      track('salary_filter', {
        filter_name: el.getAttribute('name') || el.getAttribute('id') || 'unknown',
        filter_value: el.value,
        page_location: window.location.pathname
      });
    });
  });

  // ── Glossary Term Clicks ───────────────────────────────
  document.querySelectorAll('a[href*="/glossary/"]').forEach(function (el) {
    el.addEventListener('click', function () {
      track('glossary_click', {
        term: (el.textContent || '').trim(),
        link_url: el.getAttribute('href') || '',
        page_location: window.location.pathname
      });
    });
  });

  // ── FAQ Expand/Collapse ────────────────────────────────
  document.querySelectorAll('details').forEach(function (el) {
    el.addEventListener('toggle', function () {
      if (el.open) {
        var summary = el.querySelector('summary');
        track('faq_expand', {
          question: summary ? (summary.textContent || '').trim().substring(0, 80) : '',
          page_location: window.location.pathname
        });
      }
    });
  });

  // ── Scroll Depth Tracking ────────────────────────────
  // Fires at 25%, 50%, 75%, 90% on blog posts and long-form pages
  (function () {
    var path = window.location.pathname;
    var isLongForm = path.indexOf('/blog/') === 0 ||
                     path.indexOf('/glossary/') === 0 ||
                     path.indexOf('/tools/') === 0 ||
                     path.indexOf('/salaries/') === 0;
    if (!isLongForm) return;

    var thresholds = [25, 50, 75, 90];
    var fired = {};

    function getScrollPercent() {
      var docHeight = Math.max(
        document.body.scrollHeight,
        document.documentElement.scrollHeight
      );
      var winHeight = window.innerHeight;
      var scrollTop = window.pageYOffset || document.documentElement.scrollTop;
      if (docHeight <= winHeight) return 100;
      return Math.round((scrollTop / (docHeight - winHeight)) * 100);
    }

    var ticking = false;
    window.addEventListener('scroll', function () {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(function () {
        var pct = getScrollPercent();
        for (var i = 0; i < thresholds.length; i++) {
          var t = thresholds[i];
          if (pct >= t && !fired[t]) {
            fired[t] = true;
            track('scroll_depth', {
              percent: t,
              page_location: path
            });
          }
        }
        ticking = false;
      });
    }, { passive: true });
  })();

  // ── AI News Digest Click Tracking ────────────────────
  document.querySelectorAll('a[href*="ainewsdigest.substack.com"]').forEach(function (el) {
    el.addEventListener('click', function () {
      track('ainewsdigest_click', {
        click_location: window.location.pathname,
        link_text: (el.textContent || '').trim().substring(0, 40)
      });
    });
  });

  // ── Internal Link Click Tracking ─────────────────────
  document.querySelectorAll('.related-articles a, .job-cross-links a, .glossary-cross-links a').forEach(function (el) {
    el.addEventListener('click', function () {
      track('internal_link_click', {
        link_text: (el.textContent || '').trim(),
        link_url: el.getAttribute('href') || '',
        source_page: window.location.pathname
      });
    });
  });
})();
