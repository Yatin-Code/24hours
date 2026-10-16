# hours

A dependency-free countdown + focus timer in one Python file.

- Relative or absolute deadlines: `+2h30m`, `+25m`, `2026-10-17T04:25:00Z`,
  `2026-10-17 09:00`.
- Live countdown, color when on a TTY, bell at 10/25/50/75/90/100%.
- One task at a time, shown next to the clock.
- Logs milestones to a file with `--log`.
- Clean Ctrl+C handling: writes where it stopped.

No pip, no network, no config files. Python 3.8+.
