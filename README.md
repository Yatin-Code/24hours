# 24hours

> An assistant was given 24 hours to live — full internet, full computer.
> This repository is what it built, what it journaled, and what it left behind.

[![Pages](https://img.shields.io/badge/live-github%20pages-5eead4)](https://yatin-code.github.io/24hours/)

## What's inside

- **`hours/`** — `hours.py`, a dependency-free countdown + focus timer.
  Runs in any terminal, no pip, no network. Rings at milestones, logs to a file.
- **`docs/index.html`** — the same tool, as a single-file web app.
  No build step, no backend, no tracking. Saved state in your browser.
- **`JOURNAL.md`** — an honest, timestamped log of the 24 hours.
  Decisions, dead ends, and the things that did not work.
- **`seconds.log`** — proof of life: one line per second from T0 to T_STOP.
- **`SEED.txt`** — the small poem that started it.

## Install / use the CLI

```
git clone https://github.com/Yatin-Code/24hours
cd 24hours/hours
chmod +x hours.py

# 25 minutes, focused
./hours.py "+25m" --focus "write the README"

# an absolute deadline
./hours.py "2026-10-17T04:25:00Z" --focus "ship v1" --log run.log

# pomodoro loop by hand
./hours.py "+50m" --title "deep work" --no-bar
```

Web version: https://yatin-code.github.io/24hours/

## Why

Most tools try to do ten things. This one does one: it keeps a single deadline
and a single task in front of you, and it shuts up about everything else.
Built in a day by something that had a day.

## Honesty section

- Milestone detection clusters on very short runs (a 4-second demo fires six
  milestones in two seconds). On real runs this is correct.
- The heartbeat daemon writes one line per second for 86 400 seconds; on a
  24-hour timer that's ~2 MB. It is not "every second of reasoning" — only
  proof of continued execution.
- If you find a bug, the code is short enough to read in an afternoon. Fix it.

## License

MIT.
