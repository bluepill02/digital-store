# bpmiller02 / digital-store — autonomous operation status

_Last updated: 2026-06-23 ~10:55 UTC_

## Storefront
- 10 active products, all on custom landing pages
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
- Approved queue: 16 drafts (covers ~5 weeks of M/W/F posting)
- Drafting queue: 25 drafts (waiting for future approval)
- Stale queue: 0

## Quota
- 5 posts published in June (1 X + 2 Mastodon + 2 BlueSky)
- 16 approved pending
- Estimated 21 total by mid-July if no new approvals

## Sales
- $0 lifetime
- 0 units
- 0 refunds

## Strategy shift (this session)
- Earlier wave was bluepill02-heavy (workflow tools)
- New wave (10 BP Creative drafts generated, 6 approved) emphasizes
  mindful coloring + fiction products ($2.99-$6.99 lower-friction offers)
- Approved queue now has roughly 1/3 BP Creative, 2/3 bluepill02

## Critical bugs fixed this session
1. **X publish-URL-block**: Typefully 403 FORBIDDEN when `publish_at: "now"` and draft contains URL. Fixed by scheduling publish 30s ahead.
2. **Gateway not running**: Cron jobs were registered but never executed. Fixed by `hermes gateway install`.

## Outstanding user actions (CLI can't do these)
1. **Update Gumroad profile bio** — see GUMROAD_BIO_UPDATE.txt for exact text to paste
2. **Disconnect LinkedIn from Typefully** (UI-only)

## Next automatic event
Wed 2026-06-24 9:00 ET = 13:00 UTC — scheduler fires next X draft