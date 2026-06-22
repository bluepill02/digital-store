# Storefront Design System

Two sub-brands under one Gumroad account (B.P. Miller / bpmiller02). Each product page signals its sub-brand via visual identity. Shared infrastructure (navbar, footer, modal, accessibility, theme toggle, buy mechanics) lives in `_partials/`.

## Sub-brand 1: bluepill02

**For:** Operator/technical products (B2B workflows, freelancer tools, productivity systems)

**Visual:**
- Background: deep navy `#0f172a` (light: `#f8fafc`)
- Surface: ink scale (slate-900 family)
- Accent: amber `#fbbf24` for primary CTAs
- Text: high-contrast white-on-navy, slate-on-white
- Type: Inter (sans-serif), monospace for code/section labels
- Mood: precise, technical, considered

**Voice:** Direct. Numbers before adjectives. Mechanism before outcome.

**Tagline slot:** "Prompt packs for content operators"

## Sub-brand 2: BP Creative

**For:** Lifestyle/creative products (coloring books, fiction, mindful downloads)

**Visual:**
- Background: warm cream `#faf6f1` (dark: `#1c1917`)
- Surface: paper tones `#f5ebd9`, deep teal `#0f4c4a` for contrast blocks
- Accent: terracotta `#c4623a` for primary CTAs
- Secondary: dusty rose `#d9a0a0`, sage `#8a9a7a`
- Type: Fraunces (display, serif) for headings, Inter (body, sans-serif)
- Mood: warm, inviting, editorial

**Voice:** Softer. Inviting. Sensory. "Step into" rather than "execute."

**Tagline slot:** "Printables and stories worth slowing down for"

## Shared system

Both sub-brands share:
- Tailwind CDN (with sub-brand-specific config block)
- Same navbar structure (sub-brand mark, nav, theme toggle, buy CTA)
- Same footer (B.P. Miller + sub-brand, contact, terms link)
- Same accessibility (skip link, focus-visible, aria labels, reduced motion, sr-only description)
- Same modal pattern for previews
- Same theme persistence (localStorage)
- Same responsive breakpoints (mobile-first, sm/md/lg)
- Same buy mechanics (`data-gumroad-action="buy"` + Gumroad postMessage handler)

## Per-product template

Every product page has:
1. Hero (image + headline + buy CTA + sub-brand badge)
2. "What's inside" section (3-6 deliverables with visual icons)
3. Preview/sample (real content from the product)
4. Who it's for / not for
5. Final buy section (large, with guarantee/license summary)
6. Footer (B.P. Miller + sub-brand)
7. Preview modal (deeper sample if room)

## CSS variable system

Each page sets `:root` CSS variables for its sub-brand palette. Components use `var(--bg)`, `var(--accent)`, etc. This lets the same markup render differently per sub-brand.

```
--bg-primary: ...
--bg-surface: ...
--text-primary: ...
--accent: ...
--accent-hover: ...
```

## Future: cross-sell

When a buyer purchases any product, the receipt email could include 1-2 related products from the same sub-brand. Out of scope for this session but worth designing for.
