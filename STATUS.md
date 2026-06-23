# bpmiller02 / digital-store — autonomous operation status

_Last updated: 2026-06-23 ~10:30 UTC_

## Storefront
- 10 active products, all on custom landing pages
- 6/10 with custom permalinks (aokhqy→bluepill02, evkov→freelancer-starterfreelancer-starter, retdie→algo_dust)
- All buy flows verified
- Profile bio: still OLD (user action required — see GUMROAD_BIO_UPDATE.txt on Desktop)

## Live posts (verified via platform APIs)
- X:        https://x.com/bpmiller02/status/2069363082623877350
- Mastodon: https://mastodon.social/@bpmiller02/116798898927832418
- Mastodon: https://mastodon.social/@bpmiller02/116798898903904034
- BlueSky:  https://bsky.app/profile/b-pmiller.bsky.social/post/3mox67vn7oi2t
- BlueSky:  https://bsky.app/profile/b-pmiller.bsky.social/post/3mox67vnahn2r

## Pipeline
- Hermes Gateway running (PID 22880, auto-starts on Windows login)
- Cron job 9417f3831a03 firing hourly (verified)
- Approved queue: 7 drafts (will auto-publish Wed+Fri this week + next week)
- Drafting queue: 18 drafts (waiting for future approval)
- Stale queue: 0

## Quota
- 5 posts published in June (1 X + 2 Mastodon + 2 BlueSky)
- 7 approved pending (will publish M/W/F over next ~2.3 weeks)
- Estimated quota: 15/month → 10 remaining after pending publishes

## Sales
- $0 lifetime
- 0 units
- 0 refunds

## Critical bugs fixed this session
1. **X publish-URL-block**: Typefully 403 FORBIDDEN when `publish_at: "now"` and draft contains URL. Fixed by scheduling publish 30s ahead. Saved to memory.
2. **Gateway not running**: Cron jobs were registered but never executed. Fixed by `hermes gateway install`.

## Outstanding user actions (CLI can't do these)
1. **Update Gumroad profile bio** — see GUMROAD_BIO_UPDATE.txt for exact text to paste
2. **Disconnect LinkedIn from Typefully** (UI-only, brand-consistent attribution)

## Next automatic event
Wed 2026-06-24 9:00 ET = 13:00 UTC — scheduler fires next X draft