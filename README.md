# bluepill02 · Digital Store

Source repo for digital products sold under the **bluepill02** brand.

**Author / legal seller:** B.P. Miller
**Channel:** Gumroad storefront
**Focus:** AI prompt packs and workflow kits for content creators

## Product principles

- **Specific, not generic.** Every prompt has a job. No "10 ChatGPT prompts that will blow your mind."
- **Tested in the wild.** Each pack ships with example output, not just the input.
- **Copy-paste ready.** Zero setup. Open the file, paste, ship.
- **Honest scope.** We state what each pack does, and what it doesn't.

## Repo layout

- `products/` - one folder per product, with the source bundle that gets zipped and uploaded
- `marketing/` - landing page copy, social posts, email sequences
- `roadmap.md` - product pipeline (current top 5, ranked by demand signal)

## Sales model

- Storefront handles payments, tax, fulfillment (Gumroad).
- Payouts go to the seller's bank.
- Products are sold as single-purchase digital downloads. No subscriptions in v1.

## How to use this repo

Each product folder contains:
- `product.md` - the deliverable spec (what the buyer gets)
- `bundle/` - the actual files (prompts, docs, examples) - zipped into `bundle.zip` for upload
- `marketing.md` - landing page copy, social posts, email follow-ups

The agent commits new products here, then publishes to Gumroad via API.
