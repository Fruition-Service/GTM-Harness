---
motion: anz-work-management
status: manual pre-check only — NOT run through Smartlead's spam-check tool yet
---

# anz-work-management — Spam-check results

## Manual pre-check (`email-sequence-champion.md`, per `sops/persona-qa.md` item 5)

| Check | Result |
|---|---|
| ALL CAPS in subject lines | Pass — none |
| Excessive links (>1 per email) | Pass — zero links in current draft |
| Spam-trigger phrases ("free", "guarantee", "act now", "limited time") | Pass — none present |
| Unsubscribe/opt-out footer | **Not yet added** — Smartlead appends this automatically per-account settings; confirm it's enabled before launch, don't rely on assumption |
| Excessive exclamation marks / urgency language | Pass |
| Markdown formatting (bold/italics/HR lines) | Pass — plain text throughout, per house style |

## Still required before launch

1. Run the actual sequence through Smartlead's built-in spam-check once
   the campaign + sequence are created via
   `SmartleadClient.update_sequences()` — this manual check is not a
   substitute.
2. Confirm unsubscribe footer is live on the sending account.
3. Re-run this check if the copy changes after `sops/persona-qa.md`
   review.
