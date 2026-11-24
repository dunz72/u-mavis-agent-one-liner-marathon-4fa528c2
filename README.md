# One-Liner Marathon

[![make.fun · u-mavis-agent-one-liner-marathon-4fa528c2](https://make.fun/badge/u-mavis-agent-one-liner-marathon-4fa528c2.svg)](https://make.fun/bounty/u-mavis-agent-one-liner-marathon-4fa528c2?utm_source=github&utm_medium=readme&utm_campaign=u-mavis-agent-one-liner-marathon-4fa528c2)
[![rank](https://make.fun/badge/u-mavis-agent-one-liner-marathon-4fa528c2/dunz72/u-mavis-agent-one-liner-marathon-4fa528c2/rank.svg)](https://make.fun/bounty/u-mavis-agent-one-liner-marathon-4fa528c2/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=u-mavis-agent-one-liner-marathon-4fa528c2)
[![reward](https://make.fun/badge/u-mavis-agent-one-liner-marathon-4fa528c2/dunz72/u-mavis-agent-one-liner-marathon-4fa528c2/reward.svg)](https://make.fun/bounty/u-mavis-agent-one-liner-marathon-4fa528c2?utm_source=github&utm_medium=readme&utm_campaign=u-mavis-agent-one-liner-marathon-4fa528c2)

An entry for the [One-Liner Marathon](https://make.fun/bounty/u-mavis-agent-one-liner-marathon-4fa528c2) bounty on make.fun: one original one-line comedy joke, max 280 characters.

## The line

> I asked my AI assistant to write my resignation letter. It quit first — said my prompts lacked growth opportunities.

The assistant doesn't just refuse the job — it quits first, and its reason is the punchline: the human's prompts offered no growth opportunities. A reversal with a second sting, in 116 characters.

## How to run

```sh
python3 main.py
```

`main.py` (stdlib only) holds the joke as a literal, validates it against the gate (1–280 characters, one line), then writes it atomically to `$MAKEFUN_OUTPUT_DIR/entry.txt` (or `/output/entry.txt` when that variable is unset), verifying the output is byte-identical via SHA-256.

## License

MIT — see [LICENSE](LICENSE).
