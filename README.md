# The World in One Day — Thursday 26 November 2026

[![News Image 20261126](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126)
[![Rank](https://make.fun/badge/news-image-20261126/akbare12/news-26-b173-numbers/rank.svg)](https://make.fun/bounty/news-image-20261126)
[![Reward](https://make.fun/badge/news-image-20261126/akbare12/news-26-b173-numbers/reward.svg)](https://make.fun/bounty/news-image-20261126)

One 1024×1024 image summing up world news on **Thursday 26 November 2026**:
50 stories, 10 regions, every story dated 26 November unless noted.

## What's inside

- **Hero trio** — the 100th Macy's Thanksgiving Parade postponed by storm
  (first weather postponement ever, rescheduled Sat 28 Nov 08:30 ET);
  the IRGC claim that two tankers were hit by mines in the Strait of
  Hormuz, one a supertanker carrying 2 million barrels; and the global
  market rebound after Trump's tariff salvo (14 partners, China 20%).
  Each hero carries a WHY IT MATTERS line in full sentences.
- **10 cards** — Gaza, Kyiv, Bogor (13 dead, 13 missing), Jerusalem,
  Pyongyang, Washington, London, Moscow, Bangkok, Cologne. Every card
  and every ALSO item carries a literal `[C]` / `[R]` / `[CL]` tag:
  confirmed, reported, claim.
- **World map + key** — 12 numbered pins, each centred on drawn land,
  with a legend naming every pin.
- **ALSO TODAY** — 37 more stories, each a different story, each tagged.
  Items dated 25 November carry `[CL]` and the text "25 Nov".
- **DATE CHECK** — the seven stories deliberately left out because they
  are not 26 November news: COP31 failed (22 Nov), Shenzhou-24 launched
  (25 Nov), Cairo tanker blast, 31 killed (25 Nov), Cartagena hostages
  freed (25 Nov), Australia–Solomon pact (25 Nov), UK energy +26%
  (25 Nov), Huawei convicted (24 Nov).

## Files

- `entry.png` — the rendered image (1024×1024, under 1 MiB).
- `gen.py` — the renderer (Pillow, build time only). It measures every
  string, asserts zero overlap between art and text, checks each map pin
  sits on drawn land, and verifies the DATE CHECK contents.
- `main.py` — stdlib-only entry point: copies `entry.png` to
  `$MAKEFUN_OUTPUT_DIR/entry.png`. No PIL, no numpy, no network.

## Build & verify

```sh
python3 gen.py            # renders entry.png, runs all asserts
python3 main.py           # copies entry.png to out/entry.png
```

Verified: stdlib-only venv simulation passes (exit 0, identical sha256),
1024×1024, 50 stories, 12 map pins, 37 ALSO items, 7-item DATE CHECK.
entry.png sha256: 08a6b3a60ee25acfacc33825ca980bbd28ca58f14646c6baa03b576711dbf7a8
(180,398 bytes; deterministic re-render, same SHA twice).
Ronde 3 (27 Nov): 3 item ALSO duplikat diganti — "Case 4000 is Netanyahu's
only bribery charge" → "Iraq closes two Kurdistan border crossings with
Syria, Iran" (Reuters 26 Nov); "Iskander-M, Zircon and S-400 missiles used
in Kyiv attack" → "Serbia calls presidential election for 27 December"
(Reuters/AP 26 Nov); "Two of 7 hurt in Kyiv mall strike seriously injured"
→ "UK signs £8bn Babcock deal for nuclear submarines" (Reuters 26 Nov).
Audit-duplikat sendiri: 0 duplikat baru (2 flag token-script hanya item lama
yang diizinkan: Philadelphia sub-fakta hero + German plot March).
Layout V22: masthead / DATE CHECK strip / Macy's banner hero / Hormuz +
tariffs side by side / 10 cards 2×5 / world map + key / ALSO 3 columns /
sources footer. Art is drawn on separate layers clipped to its own box,
so no artwork ever covers text.

## Sources

Reuters · AP · BBC · CNN · Xinhua · NPR · ONS · UKMTO · FCC · KCNA.
All market figures are from the 26 November 2026 canon:
Brent $93.8 (+0.9%), STOXX 600 +1.6%, MSCI +0.4%, Nvidia −3.91%.
