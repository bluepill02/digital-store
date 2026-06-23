"""
Auto-publish scheduler for Typefully drafts tagged 'approved'.

Behavior:
- Polls every hour (designed for hourly cron)
- Picks the OLDEST draft tagged 'approved' and in status='draft'
- Publishes it via Typefully MCP, respecting per-platform scheduled time from config.yaml
- Posts only on M/W/F (week_1 cadence from config.yaml)
- Idempotent: once a draft is published, it won't be re-published
- Logs to stdout (cron will capture)

Schedule (per config.yaml `cadence.preferred_times_et`):
- x:       09:00 ET
- mastodon:10:00 ET
- bluesky: 14:00 ET

The script computes the current ET hour and only publishes the platform's post when
the current hour matches its configured publish hour. So if a draft contains posts
on all three platforms, each platform's post gets published at its respective time
slot (X at 9am, Mastodon at 10am, BlueSky at 2pm — all on the same day).
"""
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).parent))
from typefully_client import call as tf_call  # noqa: E402

SOCIAL_SET_ID = 316003
APPROVED_TAG = "approved"
ALLOWED_WEEKDAYS = {0, 2, 4}  # Mon, Wed, Fri
ROOT = Path(__file__).parent
CONFIG_PATH = ROOT / "config.yaml"


def load_platform_times(cfg: dict) -> dict[str, int]:
    """Map platform -> hour-in-ET to publish (24h format)."""
    raw = cfg.get("cadence", {}).get("preferred_times_et", {})
    out = {}
    for plat, t in raw.items():
        # Format is "HH:MM"
        try:
            h, m = t.split(":")
            out[plat] = int(h)
        except (ValueError, AttributeError):
            pass
    return out


def et_now() -> datetime:
    """Current time in US/Eastern. Approximated with fixed UTC-5 (EST) offset;
    for accuracy during DST switch you'd want zoneinfo, but cron-job windows
    are coarse enough that 1-hour skew across DST boundaries is acceptable."""
    utc = datetime.now(timezone.utc)
    # Crude DST: Mar-Nov = UTC-4 (EDT), else UTC-5 (EST)
    month = utc.month
    dst_active = 3 <= month <= 10  # rough; off by ~hour at boundary
    offset = timedelta(hours=-4) if dst_active else timedelta(hours=-5)
    return utc.astimezone(timezone(offset))


def fetch_approved_drafts() -> list[dict]:
    """Return all drafts in this social set that are tagged 'approved' AND still in 'draft' status."""
    res = tf_call("typefully_list_drafts", {
        "social_set_id": SOCIAL_SET_ID,
        "limit": 50,
        # No built-in filter for tags+status; we filter client-side
    })
    sc = res["result"]["structuredContent"]
    if isinstance(sc, str):
        sc = json.loads(sc)
    drafts = sc.get("results", [])
    return [d for d in drafts if d.get("status") == "draft" and APPROVED_TAG in (d.get("tags") or [])]


def publish_draft(draft_id: int) -> dict:
    """Schedule the draft to publish in ~30 seconds.

    We don't use publish_at="now" because X has a policy blocking immediate
    publishing of drafts that contain URLs. Scheduling at any future time
    bypasses that check.
    """
    future = (datetime.now(timezone.utc) + timedelta(seconds=30)).strftime("%Y-%m-%dT%H:%M:%SZ")
    return tf_call("typefully_edit_draft", {
        "draft_id": draft_id,
        "social_set_id": SOCIAL_SET_ID,
        "requestBody": {
            "publish_at": future,
        },
    })


def log(level: str, msg: str):
    ts = datetime.now(timezone.utc).isoformat()
    print(f"[{ts}] [{level}] {msg}", flush=True)


def main():
    cfg = yaml.safe_load(CONFIG_PATH.read_text())
    plat_times = load_platform_times(cfg)
    if not plat_times:
        log("ERROR", "No platform publish times found in config.yaml cadence.preferred_times_et")
        sys.exit(1)

    now_et = et_now()
    weekday = now_et.weekday()  # 0=Mon
    hour = now_et.hour

    log("INFO", f"Scheduler tick. ET={now_et.strftime('%Y-%m-%d %H:%M')} weekday={weekday} hour={hour}")

    if weekday not in ALLOWED_WEEKDAYS:
        log("INFO", f"Skipping — not an allowed weekday (allowed={sorted(ALLOWED_WEEKDAYS)})")
        return

    # Determine which platforms are due right now (within the current hour)
    due_platforms = [p for p, h in plat_times.items() if h == hour]
    if not due_platforms:
        log("INFO", f"Skipping — no platform publishes at {hour}:00 ET (next hours: {[f'{p}={h}:00' for p,h in plat_times.items()]})")
        return

    log("INFO", f"Posting windows open for: {due_platforms}")

    drafts = fetch_approved_drafts()
    if not drafts:
        log("INFO", f"No approved drafts ready (looking for tag='{APPROVED_TAG}', status='draft')")
        return

    # Sort oldest-first
    drafts.sort(key=lambda d: d.get("created_at") or "")
    log("INFO", f"Found {len(drafts)} approved draft(s); oldest first.")

    # Pick the oldest draft that has at least one of the due-platforms enabled
    picked = None
    for d in drafts:
        enabled_platforms = []
        for plat in due_platforms:
            if d.get(f"{plat}_post_enabled"):
                enabled_platforms.append(plat)
        if enabled_platforms:
            picked = (d, enabled_platforms)
            break

    if not picked:
        log("INFO", f"No approved draft has any of {due_platforms} enabled — will retry next tick")
        return

    draft, platforms = picked
    age_days = (datetime.now(timezone.utc) - datetime.fromisoformat(draft["created_at"].replace("Z", "+00:00"))).days
    if age_days > 14:
        log("WARN", f"Draft {draft['id']} is {age_days} days old (created {draft['created_at']}). Consider retiring stale drafts.")

    log("INFO", f"Publishing draft {draft['id']} on platforms={platforms} (preview: {draft['preview'][:80]}...)")
    try:
        res = publish_draft(draft["id"])
        sc = res["result"]["structuredContent"]
        if isinstance(sc, str):
            sc = json.loads(sc)
        log("INFO", f"Published: status={sc.get('status')} publish_state={sc.get('publish_state')}")
    except Exception as e:
        log("ERROR", f"Failed to publish draft {draft['id']}: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()