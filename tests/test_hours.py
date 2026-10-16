import sys, os, datetime, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "hours"))
import hours

def test_relative_combined():
    target, total = hours.parse_deadline("+2h30m")
    assert abs(total - 9000) < 1
    assert target > time.time()

def test_relative_days():
    _, total = hours.parse_deadline("+1d12h")
    assert abs(total - (86400+43200)) < 1

def test_seconds():
    _, total = hours.parse_deadline("+45s")
    assert abs(total - 45) < 1

def test_iso_z():
    t, total = hours.parse_deadline("2026-10-17T04:25:00Z")
    assert total is None
    dt = datetime.datetime.fromtimestamp(t, datetime.timezone.utc)
    assert dt.year == 2026 and dt.month == 10 and dt.day == 17

def test_space_local():
    # should parse without error
    t, total = hours.parse_deadline("2026-10-17 09:00")
    assert isinstance(t, float)

def test_fmt_duration():
    assert hours.fmt_duration(3661) == "01:01:01"
    assert hours.fmt_duration(90061) == "1d 01:01:01"

def test_bar_bounds():
    b = hours.bar(0.0, 10)
    assert "  0%" in b or "0%" in b
    b2 = hours.bar(1.5, 10)
    assert "100%" in b2

def test_bad():
    try:
        hours.parse_deadline("nonsense")
        raise AssertionError("expected ValueError")
    except ValueError:
        pass

def test_bad_relative():
    try:
        hours.parse_deadline("+2x")
        raise AssertionError("expected ValueError")
    except ValueError:
        pass

if __name__ == "__main__":
    import unittest
    # run as script
    errs=0
    for name in [n for n in globals() if n.startswith("test_")]:
        try:
            globals()[name]()
            print("PASS", name)
        except Exception as e:
            errs+=1
            print("FAIL", name, "->", repr(e))
    print("DONE", "OK" if errs==0 else "%d failures"%errs)
    raise SystemExit(1 if errs else 0)
