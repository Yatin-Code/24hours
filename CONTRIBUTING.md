# Contributing

Issues and small PRs are welcome. Two constraints, by design:

1. **Zero dependencies.** The CLI stays one file runnable with stdlib Python 3.8+.
2. **One job.** `hours` does one thing: one deadline, one focus task. Feature
   requests that add dashboards, sync, accounts, or streaks will be declined
   politely. The web build stays a single HTML file.

Before opening a PR: run `python3 tests/test_hours.py` and make sure it passes.
