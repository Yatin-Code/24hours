#!/usr/bin/env python3
"""hours - a dependency-free countdown + focus timer.

Give it a deadline. It shows the time left, rings at milestones, and keeps
you pointed at one thing at a time. No pip, no network, no config.

Usage:
  hours.py "+2h30m"                       # relative duration
  hours.py "2026-10-17T04:25:00Z"         # absolute (ISO-8601)
  hours.py "2026-10-17 09:00"             # local wall clock
  hours.py "+25m" --focus "write the README"
"""
import argparse, sys, time, signal, datetime, os, math

ANSI = {"reset": "\033[0m", "bold": "\033[1m", "dim": "\033[2m",
        "red": "\033[31m", "green": "\033[32m", "yellow": "\033[33m",
        "blue": "\033[34m", "magenta": "\033[35m", "cyan": "\033[36m",
        "white": "\033[37m", "gray": "\033[90m"}


def color(s, *names, enabled=True):
    if not enabled:
        return s
    pre = "".join(ANSI[n] for n in names)
    return pre + s + ANSI["reset"]


def parse_deadline(s):
    s = s.strip()
    now = time.time()
    # relative: +2h / +30m / +90s / +1d, combinable like +2h30m
    if s.startswith("+"):
        body = s[1:]
        total = 0.0
        # split into number+unit chunks
        import re as _re
        m = _re.fullmatch(r"(\d+(?:\.\d+)?[dhms])+", body)
        if not m:
            raise ValueError("bad relative duration: " + s)
        for num, unit in _re.findall(r"(\d+(?:\.\d+)?)([dhms])", body):
            val = float(num)
            if unit == "d": total += val * 86400
            elif unit == "h": total += val * 3600
            elif unit == "m": total += val * 60
            elif unit == "s": total += val
        return now + total, total
    # try ISO / "YYYY-MM-DD HH:MM[:SS]"
    for fmt in ("%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%M:%S",
                "%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%dT%H:%M"):
        try:
            dt = datetime.datetime.strptime(s, fmt)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=datetime.timezone.utc) if "T" in s and s.endswith("Z") else dt.astimezone()
            # if no tz given, treat as local
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=datetime.datetime.now().astimezone().tzinfo)
            return dt.timestamp(), None
        except ValueError:
            continue
    # python fromisoformat fallback
    try:
        dt = datetime.datetime.fromisoformat(s.replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=datetime.datetime.now().astimezone().tzinfo)
        return dt.timestamp(), None
    except ValueError:
        pass
    raise ValueError("could not parse deadline: " + s)


def fmt_duration(sec):
    sec = max(0, int(sec))
    d, r = divmod(sec, 86400)
    h, r = divmod(r, 3600)
    m, s = divmod(r, 60)
    if d:
        return "%dd %02d:%02d:%02d" % (d, h, m, s)
    return "%02d:%02d:%02d" % (h, m, s)


def bar(pct, width=28, color_on=True):
    pct = max(0.0, min(1.0, pct))
    filled = int(round(pct * width))
    left = "#" * filled
    right = "." * (width - filled)
    body = color(left, "cyan", enabled=color_on) + color(right, "gray", enabled=color_on)
    return "[" + body + "] %3d%%" % int(pct * 100)


def clear_line():
    sys.stdout.write("\r\033[2K")
    sys.stdout.flush()


MILESTONES = [0.10, 0.25, 0.50, 0.75, 0.90, 1.00]


def main(argv=None):
    p = argparse.ArgumentParser(prog="hours", description="countdown + focus timer")
    p.add_argument("deadline", help="relative (+2h30m) or absolute time")
    p.add_argument("--focus", default="", help="the one thing to do now")
    p.add_argument("--title", default="", help="label for this run")
    p.add_argument("--interval", type=float, default=1.0, help="refresh seconds")
    p.add_argument("--no-color", action="store_true")
    p.add_argument("--quiet", action="store_true", help="no bells")
    p.add_argument("--log", default="", help="append milestones to this file")
    p.add_argument("--no-bar", action="store_true")
    args = p.parse_args(argv)

    color_on = (not args.no_color) and sys.stdout.isatty()
    try:
        target, rel = parse_deadline(args.deadline)
    except ValueError as e:
        print("error: " + str(e), file=sys.stderr)
        return 2

    start = time.time()
    total = rel if rel is not None else max(1.0, target - start)
    if total <= 0:
        total = 1.0
    title = args.title or (args.focus[:40] if args.focus else "countdown")

    def log(msg):
        if args.log:
            with open(args.log, "a") as f:
                f.write("%s %s\n" % (datetime.datetime.now(datetime.timezone.utc).isoformat(), msg))

    hit = set()
    stopped = {"sig": False}

    def on_sigint(sig, frame):
        stopped["sig"] = True
    signal.signal(signal.SIGINT, on_sigint)
    signal.signal(signal.SIGTERM, on_sigint)

    log("START target=%s total=%ds focus=%r" % (datetime.datetime.fromtimestamp(target, datetime.timezone.utc).isoformat(), int(total), args.focus))

    # intro
    if not args.quiet:
        print(color("hours", "bold", "cyan", enabled=color_on) + color("  //  %s" % title, "dim", enabled=color_on))
        if args.focus:
            print(color("focus: ", "bold", "yellow", enabled=color_on) + args.focus)
        print(color("target: %s   (%s)" % (datetime.datetime.fromtimestamp(target).strftime("%Y-%m-%d %H:%M:%S"), fmt_duration(total)), "gray", enabled=color_on))
        print()

    while True:
        now = time.time()
        remaining = target - now
        elapsed = now - start
        pct = elapsed / total
        # milestones
        for ms in MILESTONES:
            if ms not in hit and pct >= ms:
                hit.add(ms)
                label = ("100% done" if ms >= 1.0 else ("%d%% elapsed" % int(ms * 100)))
                line = color("  * %s  (%s left)" % (label, fmt_duration(remaining)), "bold", "magenta", enabled=color_on)
                if not args.quiet:
                    clear_line()
                    print(line)
                if ms < 1.0 and not args.quiet:
                    log("milestone %s" % label)
                if not args.quiet and not args.no_color:
                    try:
                        sys.stdout.write("\a")
                        sys.stdout.flush()
                    except Exception:
                        pass
        if stopped["sig"] or remaining <= 0:
            break
        # render
        if not args.quiet:
            pctc = min(1.0, max(0.0, pct))
            parts = []
            parts.append(color(fmt_duration(remaining), "bold", "white", enabled=color_on))
            if not args.no_bar:
                parts.append("  " + bar(pctc, 30, color_on))
            if args.focus:
                parts.append(color("  | %s" % args.focus[:46], "dim", enabled=color_on))
            clear_line()
            sys.stdout.write("".join(parts))
            sys.stdout.flush()
        time.sleep(max(0.05, args.interval))

    clear_line()
    if stopped["sig"]:
        print(color("paused / stopped at %s remaining." % fmt_duration(max(0, target - time.time())), "yellow", enabled=color_on))
        log("STOPPED_BY_USER remaining=%ds" % int(max(0, target - time.time())))
    else:
        print(color("done. " + ("time's up." if time.time() >= target else ""), "bold", "green", enabled=color_on))
        if args.focus:
            print(color("was focused on: " + args.focus, "dim", enabled=color_on))
        log("FINISHED")
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
