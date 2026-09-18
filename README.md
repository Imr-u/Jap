# JLPT Reader

Light, static Japanese reading practice site graded by JLPT level. Built with Astro, deploys straight to Vercel with zero config (static output).

## Run locally

```bash
npm install
npm run dev
```

## Deploy to Vercel

Push this to a GitHub repo and import it in Vercel — it auto-detects Astro. No env vars or backend needed for v1.

## Adding a story

Drop a new JSON file in `src/data/<level>/stage-<n>/<id>.json` (e.g. `src/data/n5/stage-1/story-03.json`). Pages are generated automatically at build time — no code changes needed.

Each story looks like this:

```json
{
  "id": "story-03",
  "title": "...",
  "level": "n5",
  "stage": 1,
  "tokens": [
    { "surface": "私", "furigana": "わたし", "romaji": "watashi", "dictForm": "私", "pos": "pronoun", "gloss": "I / me" }
  ],
  "translation": "Full English translation of the story."
}
```

- `surface`: the text as it appears in the story
- `furigana`: reading shown above kanji (leave `""` for punctuation/kana-only words with no reading needed)
- `pos: "punct"` tokens are rendered as plain punctuation, not clickable words
- `gloss`, `dictForm`, `pos`, `romaji` all feed the click-popover

**The sample stories' tokens were hand-written for demonstration.** For real content at scale, run each story through a tokenizer (Kuromoji or Sudachi) plus a JMdict lookup to auto-generate the `tokens` array instead of typing it by hand — see the earlier discussion on the content pipeline.

## What's in v1

- Level → stage → story browsing (N5 stage 1 has 2 sample stories; other levels/stages show "coming soon" / "no stories yet" automatically once you drop JSON files in)
- Furigana toggle (on by default)
- Click any word for reading (romaji), part of speech, and gloss
- Full story translation, hidden behind a reveal button

## Not in v1 (by design, see project discussion)

Audio/TTS, vocab review/SRS, user accounts, progress tracking. Worth adding once the content pipeline and reading UX are proven out.
