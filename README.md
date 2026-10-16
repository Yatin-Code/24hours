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

## A 60-second tour

```
$ hours "+25m" --focus "write the README" --log run.log
hours  //  write the README
focus: write the README
target: 2026-10-16 05:10:00   (00:25:00)

00:24:59  [..............................]   0%  | write the README
...
  * 25% elapsed  (00:18:45 left)
  * 50% elapsed  (00:12:30 left)
  * 75% elapsed  (00:06:15 left)
done. time's up.
```

## vs. the alternatives

|                            | hours | typ. pomodoro app |
|----------------------------|-------|-------------------|
| Install                    | `cp hours.py ~/.local/bin` | account + store |
| Network required           | no    | usually           |
| Tracks you                 | no    | usually           |
| Multi-task juggling        | no    | yes               |
| Dependency count           | 0     | hundreds          |
| Works at 3am offline       | yes   | maybe             |

If you want a dashboard, this is the wrong tool. That's intentional.

## Contributing

Issues and small PRs welcome. The whole CLI is one file; read it in an
afternoon. Please keep the dependency count at zero.

## Honesty section

- Milestone detection clusters on very short runs (a 4-second demo fires six
  milestones in two seconds). On real runs this is correct.
- The heartbeat daemon writes one line per second for 86 400 seconds; on a
  24-hour timer that's ~2 MB. It is not "every second of reasoning" — only
  proof of continued execution.
- If you find a bug, the code is short enough to read in an afternoon. Fix it.

## License

MIT.
