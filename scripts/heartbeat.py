import time, datetime, os
base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
t0 = int(open(os.path.join(base,'.t0epoch')).read().strip())
stop = t0 + 86400
path = os.path.join(base,'seconds.log')
f = open(path,'a',buffering=1)
line_no = 0
# resume if log exists (count lines)
try:
    with open(path) as rf:
        line_no = sum(1 for _ in rf)
except FileNotFoundError:
    pass
# advance cursor
now = int(time.time())
# if starting fresh, start at 0; else continue
started = line_no
# write header if empty
if started == 0:
    f.write("# one line per second from T0 (unix epoch) ; started %s\n" % datetime.datetime.fromtimestamp(t0, datetime.timezone.utc).isoformat())
    started = 1
while True:
    now = int(time.time())
    if now >= stop:
        f.write("STOP|epoch=%d|utc=%s\n" % (now, datetime.datetime.fromtimestamp(now, datetime.timezone.utc).isoformat()))
        f.flush()
        f.close()
        break
    idx = now - t0  # 0-based second
    # only write if not already written for this second (avoid dups on restart)
    # We'll write monotonically; simple approach: write current second line
    f.write("%d|%s|%d\n" % (idx, datetime.datetime.fromtimestamp(now, datetime.timezone.utc).isoformat(), stop-now))
    f.flush()
    # sleep to next second boundary
    time.sleep(max(0.0, (now+1) - time.time()))
