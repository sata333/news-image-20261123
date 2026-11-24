[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/sata333/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/sata333/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

# The World Today — Monday 23 November 2026

One image summing up Monday 23 November 2026's world news: **46 sourced stories**
across 8 sections (Americas, Europe, Middle East, Asia-Pacific, Africa, Business,
Tech & Science, Sport), a UTC timeline of the day's timed events, a drawn world map
with 14 numbered datelines, a "By the numbers" panel, and a date check.

Every story happened or was first reported on 23 November 2026 (UTC), and each
carries its source (Reuters, BBC, AP, Al Jazeera, Guardian, France 24, Yeni Safak,
Xinhua, CNA, Business Recorder).

## How it is made

`main.py` (Python standard library only, no network) draws the whole image
deterministically and writes it to `/output/entry.png` (1024×1024, under 1 MiB).
Run it twice and the bytes are identical:

```
python3 main.py
```

## Files

- `main.py` — the program that draws the entry
- `README.md` — this file
- `LICENSE` — MIT
