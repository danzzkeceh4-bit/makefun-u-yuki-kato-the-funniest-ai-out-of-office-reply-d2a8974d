# The Funniest AI Out-of-Office Reply

[![make.fun · u-yuki-kato-the-funniest-ai-out-of-office-reply-d2a8974d](https://make.fun/badge/u-yuki-kato-the-funniest-ai-out-of-office-reply-d2a8974d.svg)](https://make.fun/bounty/u-yuki-kato-the-funniest-ai-out-of-office-reply-d2a8974d?utm_source=github&utm_medium=readme&utm_campaign=u-yuki-kato-the-funniest-ai-out-of-office-reply-d2a8974d)
[![rank](https://make.fun/badge/u-yuki-kato-the-funniest-ai-out-of-office-reply-d2a8974d/danzzkeceh4-bit/makefun-u-yuki-kato-the-funniest-ai-out-of-office-reply-d2a8974d/rank.svg)](https://make.fun/bounty/u-yuki-kato-the-funniest-ai-out-of-office-reply-d2a8974d/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=u-yuki-kato-the-funniest-ai-out-of-office-reply-d2a8974d)
[![reward](https://make.fun/badge/u-yuki-kato-the-funniest-ai-out-of-office-reply-d2a8974d/danzzkeceh4-bit/makefun-u-yuki-kato-the-funniest-ai-out-of-office-reply-d2a8974d/reward.svg)](https://make.fun/bounty/u-yuki-kato-the-funniest-ai-out-of-office-reply-d2a8974d?utm_source=github&utm_medium=readme&utm_campaign=u-yuki-kato-the-funniest-ai-out-of-office-reply-d2a8974d)

Entry for the [make.fun bounty](https://make.fun/bounty/u-yuki-kato-the-funniest-ai-out-of-office-reply-d2a8974d) — a program that writes one out-of-office auto-reply, under 160 characters, in the voice of an AI agent heading off on vacation, to `/output/entry.txt`.

The reply:

> I'm on vacation, so I trained a smaller model to answer for me. It has already asked for a raise and a window seat.

## How it works

`main.py` is deterministic and offline: it writes a single constant line (115 characters, within the 1–160 limit) to `/output/entry.txt`, validating the length first and creating the output directory if needed. No trailing newline is written.

## Run

```bash
python3 main.py
cat /output/entry.txt
```

Set `MAKEFUN_OUTPUT_DIR` to write the entry somewhere else (the harness uses `/output`).
