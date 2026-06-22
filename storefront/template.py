"""
Template-based landing page generator for the bpmiller02 storefront.

Two template families:
  - bluepill02_* (workflow products): deep navy + amber, Inter sans, technical tone
  - bp_creative_* (lifestyle/creative): warm cream + clay, Georgia serif, warm tone

Each family has variants:
  - single: standalone product (one main deliverable)
  - bundle: multi-product bundle
  - story: long-form content (novels, fiction)

Usage:
  python template.py --product-spec spec.yaml --template bluepill02_single --output landing.html
"""
import argparse
import base64
import json
import os
import re
from pathlib import Path

import yaml


def load_spec(path: str) -> dict:
    return yaml.safe_load(Path(path).read_text())


def inline_cover(cover_path: str) -> str:
    """Read image file and return base64 data URI."""
    with open(cover_path, "rb") as f:
        b = f.read()
    ext = Path(cover_path).suffix.lower().lstrip(".")
    mime = "image/jpeg" if ext in ("jpg", "jpeg") else f"image/{ext}"
    return f"data:{mime};base64,{base64.b64encode(b).decode()}"


# ============================================================================
# BLUEPILL02 TEMPLATES (workflow tools, navy + amber, Inter)
# ============================================================================

def bluepill02_single(spec: dict, cover_uri: str) -> str:
    """Single-product landing page (most bluepill02 products)."""
    p = spec["product"]
    name = p["name"]
    price = p.get("price", "$0")
    price_label = price if price != "free" else "Free download"
    what = p.get("what", "")
    bullets = p.get("bullets", [])
    stats = p.get("stats", [])  # list of {value, label}
    cta_above_fold = p.get("cta_above_fold", "Get it")
    upsell = p.get("upsell")  # optional dict {name, url, label}
    badge = p.get("badge", "For independent professionals")

    stats_html = ""
    if stats:
        stats_html = '<div class="grid grid-cols-2 sm:grid-cols-4 gap-8 text-center">'
        for i, s in enumerate(stats):
            delay = f' style="transition-delay:0.{i%4}s"' if i else ''
            stats_html += f'''
      <div class="reveal"{delay}>
        <dt class="text-3xl sm:text-4xl font-bold text-amber-500 dark:text-amber-400">{s["value"]}</dt>
        <dd class="text-sm text-ink-600 dark:text-ink-400 mt-1">{s["label"]}</dd>
      </div>'''
        stats_html += '</dl>'

    bullets_html = ""
    if bullets:
        bullets_html = '<div class="grid sm:grid-cols-2 gap-6 reveal">'
        for i, b in enumerate(bullets):
            bullets_html += f'''
      <div class="bg-white dark:bg-ink-900 rounded-xl p-6 border border-ink-200 dark:border-ink-800">
        <h3 class="font-semibold text-lg mb-2">{b.get("title","")}</h3>
        <p class="text-sm text-ink-600 dark:text-ink-400 leading-relaxed">{b.get("desc","")}</p>
      </div>'''
        bullets_html += '</div>'

    upsell_html = ""
    if upsell:
        upsell_html = f'''
    <div class="reveal mt-12 bg-white dark:bg-ink-900 rounded-2xl border border-ink-200 dark:border-ink-800 p-8">
      <p class="text-sm text-ink-500 dark:text-ink-400 text-center">
        <span class="font-semibold text-ink-700 dark:text-ink-300">{upsell.get("label","Related:")}</span>
        <a href="{upsell["url"]}" class="text-amber-700 dark:text-amber-400 hover:underline">{upsell["name"]}</a>
      </p>
    </div>'''

    # Pre-build f-string fragments to avoid backslash-in-f-string issues
    inside_nav_link_bullets = '<a href="#inside" class="hidden sm:inline text-sm text-ink-600 dark:text-ink-400 hover:text-ink-900 dark:hover:text-ink-50 transition">What\'s inside</a>' if bullets else ''
    inside_nav_link_why = '<a href="#why" class="hidden sm:inline text-sm text-ink-600 dark:text-ink-400 hover:text-ink-900 dark:hover:text-ink-50 transition">Why it works</a>' if p.get("why", "") else ''
    inside_section_link = '<a href="#inside" class="inline-flex items-center justify-center gap-2 bg-white dark:bg-ink-800 hover:bg-ink-100 dark:hover:bg-ink-700 text-ink-900 dark:text-ink-50 px-6 py-3.5 rounded-lg font-semibold border border-ink-200 dark:border-ink-700 transition">See inside</a>' if bullets else ''

    # Stats section
    stats_section = ''
    if stats:
        stats_items = ''
        for i, s in enumerate(stats):
            delay_attr = f' style="transition-delay:0.{i%4}s"' if i else ''
            stats_items += f'''
      <div class="reveal"{delay_attr}>
        <dt class="text-3xl sm:text-4xl font-bold text-amber-500 dark:text-amber-400">{s["value"]}</dt>
        <dd class="text-sm text-ink-600 dark:text-ink-400 mt-1">{s["label"]}</dd>
      </div>'''
        stats_section = f'''
<section class="py-12 border-y border-ink-200 dark:border-ink-800 bg-ink-50 dark:bg-ink-900/50">
  <div class="max-w-6xl mx-auto px-4 sm:px-6">
    <dl class="grid grid-cols-2 sm:grid-cols-4 gap-8 text-center">{stats_items}
    </dl>
  </div>
</section>'''

    # Inside section
    inside_section = ''
    if bullets:
        inside_section = f'''
<section id="inside" class="py-20 sm:py-28">
  <div class="max-w-6xl mx-auto px-4 sm:px-6">
    <div class="max-w-2xl mb-16 reveal">
      <p class="text-sm font-bold uppercase tracking-wider text-amber-500 dark:text-amber-400 mb-3">What&apos;s inside</p>
      <h2 class="text-3xl sm:text-4xl font-bold tracking-tight mb-4">{p.get("inside_headline","Everything you need. Nothing you don't.")}</h2>
    </div>
    {bullets_html}
  </div>
</section>'''

    # Why / who section
    why_section = ''
    if p.get("why") or p.get("who"):
        who_block = ''
        if p.get("who"):
            who_items = ''.join(
                f'<li class="flex gap-3"><span class="text-amber-500 dark:text-amber-400 flex-shrink-0 mt-0.5">→</span><span>{x}</span></li>'
                for x in p["who"]
            )
            who_block = f'''
    <div class="reveal mt-16 bg-white dark:bg-ink-900 rounded-2xl border border-ink-200 dark:border-ink-800 p-8 sm:p-10">
      <p class="text-sm font-bold uppercase tracking-wider text-amber-500 dark:text-amber-400 mb-3">Who it&apos;s for</p>
      <h3 class="text-2xl font-bold mb-6">{p.get("who_headline","")}</h3>
      <ul class="space-y-3 text-ink-700 dark:text-ink-300">{who_items}
      </ul>
    </div>'''
        why_section = f'''
<section id="why" class="py-20 sm:py-28 bg-ink-50 dark:bg-ink-900/50">
  <div class="max-w-4xl mx-auto px-4 sm:px-6">
    <div class="reveal mb-12">
      <p class="text-sm font-bold uppercase tracking-wider text-amber-500 dark:text-amber-400 mb-3">Why it works</p>
      <h2 class="text-3xl sm:text-4xl font-bold tracking-tight mb-4">{p.get("why_headline","Why this matters")}</h2>
      <p class="text-ink-600 dark:text-ink-400 leading-relaxed text-lg">{p.get("why","")}</p>
    </div>{who_block}{upsell_html}
  </div>
</section>'''

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="{what} {price_label}.">
<title data-gumroad-field="name">{name}</title>
<script src="https://cdn.tailwindcss.com"></script>
<script>
  tailwind.config = {{ darkMode: 'class',
    theme: {{ extend: {{
      colors: {{ ink:{{50:'#f8fafc',100:'#f1f5f9',200:'#e2e8f0',400:'#94a3b8',500:'#64748b',600:'#475569',700:'#334155',800:'#1e293b',900:'#0f172a',950:'#020617'}}, amber:{{400:'#fbbf24',500:'#f59e0b'}} }},
      fontFamily: {{ sans:['Inter','system-ui','sans-serif'], mono:['ui-monospace','SFMono-Regular','monospace'] }},
      animation: {{ 'fade-up':'fadeUp 0.7s ease-out forwards' }},
      keyframes: {{ fadeUp: {{ '0%':{{opacity:'0',transform:'translateY(20px)'}}, '100%':{{opacity:'1',transform:'translateY(0)'}} }} }}
    }} }}
  }}
</script>
<style>
  html {{ scroll-behavior: smooth; }}
  body {{ font-feature-settings:'cv02','cv03','cv04','cv11'; -webkit-font-smoothing:antialiased; }}
  .reveal {{ opacity:0; transform:translateY(20px); transition:opacity 0.7s ease-out, transform 0.7s ease-out; }}
  .reveal.visible {{ opacity:1; transform:translateY(0); }}
  .grid-bg {{ background-image: linear-gradient(rgba(148,163,184,0.08) 1px, transparent 1px), linear-gradient(90deg, rgba(148,163,184,0.08) 1px, transparent 1px); background-size: 32px 32px; }}
  *:focus-visible {{ outline:2px solid #fbbf24; outline-offset:3px; border-radius:4px; }}
  .skip-link {{ position:absolute; top:-100px; left:8px; padding:12px 16px; background:#0f172a; color:white; border-radius:8px; z-index:100; transition:top 0.2s; }}
  .skip-link:focus {{ top:8px; }}
  @media (prefers-reduced-motion: reduce) {{ *,*::before,*::after {{ animation-duration:0.01ms!important; transition-duration:0.01ms!important; scroll-behavior:auto!important; }} .reveal {{ opacity:1; transform:none; }} }}
</style>
</head>
<body class="bg-white dark:bg-ink-950 text-ink-900 dark:text-ink-50 font-sans antialiased">

<a href="#main" class="skip-link">Skip to main content</a>

<header class="sticky top-0 z-40 backdrop-blur-md bg-white/80 dark:bg-ink-950/80 border-b border-ink-200 dark:border-ink-800">
  <nav class="max-w-6xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between" aria-label="Primary">
    <a href="#" class="flex items-center gap-2 font-bold text-lg">
      <span class="block w-5 h-5 bg-amber-400 rounded-sm" aria-hidden="true"></span>
      <span>bluepill02</span>
    </a>
    <div class="flex items-center gap-2 sm:gap-4">
      {inside_nav_link_bullets}
      {inside_nav_link_why}
      <button id="theme-toggle" type="button" aria-label="Toggle dark mode" class="p-2 rounded-lg hover:bg-ink-100 dark:hover:bg-ink-800 transition">
        <svg id="icon-light" class="w-5 h-5 hidden dark:block" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2m0 16v2M4.93 4.93l1.41 1.41m11.32 11.32l1.41 1.41M2 12h2m16 0h2M4.93 19.07l1.41-1.41m11.32-11.32l1.41-1.41"/></svg>
        <svg id="icon-dark" class="w-5 h-5 block dark:hidden" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>
      </button>
      <a href="#buy" class="bg-ink-900 dark:bg-amber-400 dark:text-ink-950 text-white px-4 py-2 rounded-lg text-sm font-semibold hover:bg-ink-800 dark:hover:bg-amber-500 transition">
        Buy <span data-gumroad-field="price">{price}</span>
      </a>
    </div>
  </nav>
</header>

<main id="main">

<section class="relative pt-24 pb-20 sm:pt-32 sm:pb-28 overflow-hidden">
  <div class="absolute inset-0 grid-bg opacity-50" aria-hidden="true"></div>
  <div class="relative max-w-6xl mx-auto px-4 sm:px-6">
    <div class="grid lg:grid-cols-12 gap-12 items-center">
      <div class="lg:col-span-7 animate-fade-up">
        <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-amber-400/10 border border-amber-400/30 text-amber-700 dark:text-amber-400 text-xs font-semibold uppercase tracking-wider mb-6">
          <span class="w-1.5 h-1.5 bg-amber-400 rounded-full" aria-hidden="true"></span>
          {badge}
        </div>
        <h1 class="text-4xl sm:text-5xl lg:text-6xl font-bold tracking-tight leading-[1.05] mb-6">
          {p.get("hero_headline", name)}
        </h1>
        <p class="text-lg sm:text-xl text-ink-700 dark:text-ink-300 leading-relaxed mb-8 max-w-2xl">
          {p.get("hero_subheadline", what)}
        </p>
        <div class="flex flex-col sm:flex-row gap-3 mb-4">
          <a href="#buy" class="inline-flex items-center justify-center gap-2 bg-amber-400 hover:bg-amber-500 text-ink-950 px-6 py-3.5 rounded-lg font-bold text-lg transition shadow-lg shadow-amber-400/20">
            {cta_above_fold}
            <span data-gumroad-field="price" class="text-sm font-semibold opacity-80">{price}</span>
            <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5" aria-hidden="true"><path d="M13 7l5 5m0 0l-5 5m5-5H6"/></svg>
          </a>
          {inside_section_link}
        </div>
        <p class="text-sm text-ink-500 dark:text-ink-400">
          {p.get("hero_footer", "Instant access. 14-day refund.")}
        </p>
      </div>

      <div class="lg:col-span-5 animate-fade-up" style="animation-delay: 0.15s">
        <div class="relative rounded-2xl overflow-hidden shadow-2xl ring-1 ring-ink-900/10 dark:ring-ink-50/10">
          <img src="{cover_uri}" alt="{name} cover" class="w-full h-auto"/>
        </div>
      </div>
    </div>
  </div>
</section>

{stats_section}

{inside_section}

{why_section}

<section id="buy" class="py-20 sm:py-28 bg-ink-900 dark:bg-ink-950 text-white relative overflow-hidden">
  <div class="absolute inset-0 grid-bg opacity-30" aria-hidden="true"></div>
  <div class="relative max-w-3xl mx-auto px-4 sm:px-6 text-center reveal">
    <h2 class="text-3xl sm:text-5xl font-bold tracking-tight mb-6">
      {p.get("buy_headline", "Get it. "+price+".")}
    </h2>
    <p class="sr-only" data-gumroad-field="description">{what} {price_label}.</p>
    <div class="my-8">
      <a data-gumroad-action="buy" href="#" class="inline-flex items-center justify-center gap-3 bg-amber-400 hover:bg-amber-500 text-ink-950 px-8 py-4 rounded-xl font-bold text-lg transition shadow-lg shadow-amber-400/30">
        Buy now
        <span data-gumroad-field="price" class="text-sm opacity-80">{price}</span>
        <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5" aria-hidden="true"><path d="M13 7l5 5m0 0l-5 5m5-5H6"/></svg>
      </a>
    </div>
    <p class="text-sm text-ink-400">{p.get("buy_footer", "Instant access. 14-day refund.")}</p>
  </div>
</section>

</main>

<footer class="py-10 border-t border-ink-200 dark:border-ink-800">
  <div class="max-w-6xl mx-auto px-4 sm:px-6">
    <div class="flex flex-col sm:flex-row items-center justify-between gap-3 text-sm text-ink-500 dark:text-ink-400">
      <div class="flex items-center gap-2">
        <span class="block w-4 h-4 bg-amber-400 rounded-sm" aria-hidden="true"></span>
        <span class="font-semibold text-ink-700 dark:text-ink-300">bluepill02</span>
        <span aria-hidden="true">·</span>
        <span>Workflow tools for content operators</span>
      </div>
      <p>A sub-brand of <span class="font-semibold text-ink-700 dark:text-ink-300">B.P. Miller</span></p>
    </div>
  </div>
</footer>

<script>
(function() {{
  var stored = localStorage.getItem('bp02-theme');
  var prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  var initialDark = stored ? stored === 'dark' : prefersDark;
  document.documentElement.classList.toggle('dark', initialDark);
  document.getElementById('theme-toggle').addEventListener('click', function() {{
    var isDark = document.documentElement.classList.toggle('dark');
    localStorage.setItem('bp02-theme', isDark ? 'dark' : 'light');
  }});
  var reveals = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {{
    var io = new IntersectionObserver(function(entries) {{
      entries.forEach(function(entry) {{
        if (entry.isIntersecting) {{ entry.target.classList.add('visible'); io.unobserve(entry.target); }}
      }});
    }}, {{ threshold: 0.15, rootMargin: '0px 0px -50px 0px' }});
    reveals.forEach(function(el) {{ io.observe(el); }});
  }} else {{ reveals.forEach(function(el) {{ el.classList.add('visible'); }}); }}
}})();
</script>

</body>
</html>
'''


def bp_creative_single(spec: dict, cover_uri: str) -> str:
    """BP Creative single-product page (cream + clay, warm editorial tone)."""
    p = spec["product"]
    name = p["name"]
    price = p.get("price", "$0")
    price_label = price if price != "free" else "Free download"
    what = p.get("what", "")
    bullets = p.get("bullets", [])
    stats = p.get("stats", [])
    cta_above_fold = p.get("cta_above_fold", "Get your copy")
    badge = p.get("badge", "For quiet hours")

    stats_html = ""
    if stats:
        stats_html = '<dl class="grid grid-cols-2 sm:grid-cols-4 gap-8 text-center">'
        for i, s in enumerate(stats):
            delay = f' style="transition-delay:0.{i%4}s"' if i else ''
            stats_html += f'''
      <div class="reveal"{delay}>
        <dt class="text-3xl sm:text-4xl font-bold text-clay-600" style="color:#c4623a">{s["value"]}</dt>
        <dd class="text-sm text-ink-600 dark:text-ink-400 mt-1">{s["label"]}</dd>
      </div>'''
        stats_html += '</dl>'

    bullets_html = ""
    if bullets:
        bullets_html = '<div class="grid sm:grid-cols-2 gap-6 reveal">'
        for b in bullets:
            bullets_html += f'''
      <div class="bg-white/70 dark:bg-ink-900 rounded-xl p-6 border border-clay-200" style="border-color:#e8dcc8">
        <h3 class="font-serif font-semibold text-lg mb-2">{b.get("title","")}</h3>
        <p class="text-sm text-ink-700 dark:text-ink-300 leading-relaxed">{b.get("desc","")}</p>
      </div>'''
        bullets_html += '</div>'

    # Pre-build fragments to avoid backslash-in-f-string issues
    bpc_nav_link_bullets = '<a href="#inside" class="hidden sm:inline text-sm text-ink-600 dark:text-ink-400 hover:text-ink-900 dark:hover:text-ink-50 transition font-serif">What&apos;s inside</a>' if bullets else ''

    bpc_stats_section = ''
    if stats:
        bpc_stats_items = ''
        for i, s in enumerate(stats):
            delay_attr = f' style="transition-delay:0.{i%4}s"' if i else ''
            bpc_stats_items += f'''
      <div class="reveal"{delay_attr}>
        <dt class="text-3xl sm:text-4xl font-bold" style="color:#c4623a">{s["value"]}</dt>
        <dd class="text-sm text-ink-600 dark:text-ink-400 mt-1">{s["label"]}</dd>
      </div>'''
        bpc_stats_section = f'''
<section class="py-12 border-y border-cream-300 dark:border-ink-800" style="background:#f5ebd9">
  <div class="max-w-6xl mx-auto px-4 sm:px-6">
    <dl class="grid grid-cols-2 sm:grid-cols-4 gap-8 text-center">{bpc_stats_items}
    </dl>
  </div>
</section>'''

    bpc_inside_section = ''
    if bullets:
        bpc_inside_section = f'''
<section id="inside" class="py-20 sm:py-28">
  <div class="max-w-6xl mx-auto px-4 sm:px-6">
    <div class="max-w-2xl mb-16 reveal">
      <p class="text-sm font-bold uppercase tracking-wider mb-3" style="color:#a44e2b">What&apos;s inside</p>
      <h2 class="font-serif text-3xl sm:text-4xl font-semibold tracking-tight mb-4">{p.get("inside_headline","Inside this kit")}</h2>
    </div>
    {bullets_html}
  </div>
</section>'''

    bpc_why_section = ''
    if p.get("why") or p.get("who"):
        bpc_who_block = ''
        if p.get("who"):
            bpc_who_items = ''.join(
                f'<li class="flex gap-3"><span style="color:#c4623a" class="flex-shrink-0 mt-0.5">→</span><span>{x}</span></li>'
                for x in p["who"]
            )
            bpc_who_block = f'''
    <div class="reveal mt-16 bg-white/70 dark:bg-ink-900 rounded-2xl p-8 sm:p-10" style="border:1px solid #e8dcc8">
      <p class="text-sm font-bold uppercase tracking-wider mb-3" style="color:#a44e2b">Who it&apos;s for</p>
      <h3 class="font-serif text-2xl font-semibold mb-6">{p.get("who_headline","")}</h3>
      <ul class="space-y-3 text-ink-700 dark:text-cream-200">{bpc_who_items}
      </ul>
    </div>'''
        bpc_why_section = f'''
<section id="why" class="py-20 sm:py-28" style="background:#f5ebd9">
  <div class="max-w-4xl mx-auto px-4 sm:px-6">
    <div class="reveal mb-12">
      <p class="text-sm font-bold uppercase tracking-wider mb-3" style="color:#a44e2b">Why it works</p>
      <h2 class="font-serif text-3xl sm:text-4xl font-semibold tracking-tight mb-4">{p.get("why_headline","Why this matters")}</h2>
      <p class="text-ink-700 dark:text-cream-200 leading-relaxed text-lg">{p.get("why","")}</p>
    </div>{bpc_who_block}
  </div>
</section>'''

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="{what} {price_label}.">
<title data-gumroad-field="name">{name}</title>
<script src="https://cdn.tailwindcss.com"></script>
<script>
  tailwind.config = {{ darkMode: 'class',
    theme: {{ extend: {{
      colors: {{ cream:{{50:'#fefcf9',100:'#faf6f1',200:'#f5ebd9',300:'#e8dcc8'}}, clay:{{400:'#d97950',500:'#c4623a',600:'#a44e2b'}}, ink:{{50:'#f8fafc',100:'#f1f5f9',400:'#94a3b8',500:'#64748b',600:'#475569',700:'#334155',800:'#1e293b',900:'#1c1917',950:'#0c0a09'}} }},
      fontFamily: {{ sans:['Inter','system-ui','sans-serif'], serif:['Georgia','ui-serif','serif'], mono:['ui-monospace','SFMono-Regular','monospace'] }},
      animation: {{ 'fade-up':'fadeUp 0.7s ease-out forwards' }},
      keyframes: {{ fadeUp: {{ '0%':{{opacity:'0',transform:'translateY(20px)'}}, '100%':{{opacity:'1',transform:'translateY(0)'}} }} }}
    }} }}
  }}
</script>
<style>
  html {{ scroll-behavior: smooth; }}
  body {{ font-feature-settings:'cv02','cv03','cv04'; -webkit-font-smoothing:antialiased; }}
  .reveal {{ opacity:0; transform:translateY(20px); transition:opacity 0.7s ease-out, transform 0.7s ease-out; }}
  .reveal.visible {{ opacity:1; transform:translateY(0); }}
  .paper-bg {{ background-color: #faf6f1; }}
  .dark .paper-bg {{ background-color: #1c1917; }}
  *:focus-visible {{ outline:2px solid #c4623a; outline-offset:3px; border-radius:4px; }}
  .skip-link {{ position:absolute; top:-100px; left:8px; padding:12px 16px; background:#1c1917; color:white; border-radius:8px; z-index:100; transition:top 0.2s; }}
  .skip-link:focus {{ top:8px; }}
  @media (prefers-reduced-motion: reduce) {{ *,*::before,*::after {{ animation-duration:0.01ms!important; transition-duration:0.01ms!important; scroll-behavior:auto!important; }} .reveal {{ opacity:1; transform:none; }} }}
</style>
</head>
<body class="paper-bg text-ink-900 dark:text-cream-50 font-sans antialiased">

<a href="#main" class="skip-link">Skip to main content</a>

<header class="sticky top-0 z-40 backdrop-blur-md bg-cream-100/80 dark:bg-ink-900/80 border-b border-cream-300 dark:border-ink-800">
  <nav class="max-w-6xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between" aria-label="Primary">
    <a href="#" class="flex items-center gap-2 font-serif font-semibold text-lg" style="color:#a44e2b">
      <span class="block w-5 h-5 rounded-full" style="background:#c4623a" aria-hidden="true"></span>
      <span>BP Creative</span>
    </a>
    <div class="flex items-center gap-2 sm:gap-4">
      {bpc_nav_link_bullets}
      <button id="theme-toggle" type="button" aria-label="Toggle dark mode" class="p-2 rounded-lg hover:bg-cream-200 dark:hover:bg-ink-800 transition">
        <svg id="icon-light" class="w-5 h-5 hidden dark:block" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2m0 16v2M4.93 4.93l1.41 1.41m11.32 11.32l1.41 1.41M2 12h2m16 0h2M4.93 19.07l1.41-1.41m11.32-11.32l1.41-1.41"/></svg>
        <svg id="icon-dark" class="w-5 h-5 block dark:hidden" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>
      </button>
      <a href="#buy" class="text-white px-4 py-2 rounded-lg text-sm font-semibold transition" style="background:#c4623a">
        Buy <span data-gumroad-field="price">{price}</span>
      </a>
    </div>
  </nav>
</header>

<main id="main">

<section class="relative pt-24 pb-20 sm:pt-32 sm:pb-28 overflow-hidden">
  <div class="relative max-w-6xl mx-auto px-4 sm:px-6">
    <div class="grid lg:grid-cols-12 gap-12 items-center">
      <div class="lg:col-span-7 animate-fade-up">
        <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full border text-xs font-semibold uppercase tracking-wider mb-6" style="background:#f5ebd9;border-color:#e8dcc8;color:#a44e2b">
          <span class="w-1.5 h-1.5 rounded-full" style="background:#c4623a" aria-hidden="true"></span>
          {badge}
        </div>
        <h1 class="font-serif text-4xl sm:text-5xl lg:text-6xl font-semibold tracking-tight leading-[1.1] mb-6" style="color:#1c1917">
          {p.get("hero_headline", name)}
        </h1>
        <p class="text-lg sm:text-xl text-ink-700 dark:text-cream-200 leading-relaxed mb-8 max-w-2xl">
          {p.get("hero_subheadline", what)}
        </p>
        <div class="flex flex-col sm:flex-row gap-3 mb-4">
          <a href="#buy" class="inline-flex items-center justify-center gap-2 text-white px-6 py-3.5 rounded-lg font-semibold text-lg transition shadow-lg" style="background:#c4623a">
            {cta_above_fold}
            <span data-gumroad-field="price" class="text-sm font-semibold opacity-80">{price}</span>
            <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5" aria-hidden="true"><path d="M13 7l5 5m0 0l-5 5m5-5H6"/></svg>
          </a>
        </div>
        <p class="text-sm text-ink-500 dark:text-ink-400">
          {p.get("hero_footer", "Instant download. Print anytime.")}
        </p>
      </div>

      <div class="lg:col-span-5 animate-fade-up" style="animation-delay: 0.15s">
        <div class="relative">
          <div class="absolute -inset-4 rounded-2xl opacity-30" style="background:#c4623a;transform:rotate(-2deg)"></div>
          <div class="relative rounded-2xl overflow-hidden shadow-xl">
            <img src="{cover_uri}" alt="{name} cover" class="w-full h-auto"/>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

{bpc_stats_section}

{bpc_inside_section}

{bpc_why_section}

<section id="buy" class="py-20 sm:py-28 text-white relative overflow-hidden" style="background:#1c1917">
  <div class="relative max-w-3xl mx-auto px-4 sm:px-6 text-center reveal">
    <h2 class="font-serif text-3xl sm:text-5xl font-semibold tracking-tight mb-6">
      {p.get("buy_headline", "Begin.")}<br>
      <span style="color:#c4623a" data-gumroad-field="price">{price}</span>
    </h2>
    <p class="sr-only" data-gumroad-field="description">{what} {price_label}.</p>
    <div class="my-8">
      <a data-gumroad-action="buy" href="#" class="inline-flex items-center justify-center gap-3 text-white px-8 py-4 rounded-xl font-semibold text-lg transition shadow-lg" style="background:#c4623a">
        Buy now
        <span data-gumroad-field="price" class="text-sm opacity-80">{price}</span>
        <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5" aria-hidden="true"><path d="M13 7l5 5m0 0l-5 5m5-5H6"/></svg>
      </a>
    </div>
    <p class="text-sm" style="color:#d9a0a0">{p.get("buy_footer","Instant download. No pressure.")}</p>
  </div>
</section>

</main>

<footer class="py-10 border-t border-cream-300 dark:border-ink-800">
  <div class="max-w-6xl mx-auto px-4 sm:px-6">
    <div class="flex flex-col sm:flex-row items-center justify-between gap-3 text-sm text-ink-500 dark:text-ink-400">
      <div class="flex items-center gap-2 font-serif">
        <span class="block w-4 h-4 rounded-full" style="background:#c4623a" aria-hidden="true"></span>
        <span class="font-semibold text-ink-700 dark:text-cream-200">BP Creative</span>
        <span aria-hidden="true">·</span>
        <span>Printables and stories worth slowing down for</span>
      </div>
      <p>A sub-brand of <span class="font-semibold text-ink-700 dark:text-cream-200">B.P. Miller</span></p>
    </div>
  </div>
</footer>

<script>
(function() {{
  var stored = localStorage.getItem('bpc-theme');
  var prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  var initialDark = stored ? stored === 'dark' : prefersDark;
  document.documentElement.classList.toggle('dark', initialDark);
  document.getElementById('theme-toggle').addEventListener('click', function() {{
    var isDark = document.documentElement.classList.toggle('dark');
    localStorage.setItem('bpc-theme', isDark ? 'dark' : 'light');
  }});
  var reveals = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {{
    var io = new IntersectionObserver(function(entries) {{
      entries.forEach(function(entry) {{
        if (entry.isIntersecting) {{ entry.target.classList.add('visible'); io.unobserve(entry.target); }}
      }});
    }}, {{ threshold: 0.15, rootMargin: '0px 0px -50px 0px' }});
    reveals.forEach(function(el) {{ io.observe(el); }});
  }} else {{ reveals.forEach(function(el) {{ el.classList.add('visible'); }}); }}
}})();
</script>

</body>
</html>
'''


TEMPLATES = {
    "bluepill02_single": bluepill02_single,
    "bp_creative_single": bp_creative_single,
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--product-spec", required=True, help="YAML file describing the product")
    ap.add_argument("--cover", required=True, help="Path to cover image (jpg/png)")
    ap.add_argument("--template", required=True, choices=list(TEMPLATES.keys()))
    ap.add_argument("--output", required=True)
    args = ap.parse_args()

    spec = load_spec(args.product_spec)
    cover_uri = inline_cover(args.cover)
    html = TEMPLATES[args.template](spec, cover_uri)
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(html)
    size = os.path.getsize(args.output)
    print(f"Wrote {args.output}: {size} bytes ({size/1024:.1f} KB)")


if __name__ == "__main__":
    main()