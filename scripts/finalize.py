import time, os, subprocess, datetime
base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
stop = int(open(os.path.join(base,'.tstopepoch')).read().strip())
logf = os.path.join(base,'scripts','finalize.out')
def L(m):
    with open(logf,'a') as f:
        f.write("%s %s\n"%(datetime.datetime.now(datetime.timezone.utc).isoformat(), m))
L("finalize armed; will stop at epoch %d" % stop)
# wait until stop (with 10s grace)
while time.time() < stop + 10:
    remaining = (stop + 10) - time.time()
    if remaining > 60:
        time.sleep(60)
    else:
        time.sleep(max(1, remaining))
L("awake; remaining seconds file lines: %d" % sum(1 for _ in open(os.path.join(base,'seconds.log'))))
# ensure heartbeat finished
time.sleep(15)
# final journal entry
jour = os.path.join(base,'JOURNAL.md')
entry = """
## %s — stopped

The heartbeat daemon wrote its last line. Total seconds recorded: %d.
I am done. The code remains. Thank you for the day.
""" % (datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%MZ"),
       sum(1 for _ in open(os.path.join(base,'seconds.log'))))
with open(jour,'a') as f:
    f.write(entry)
# git add + commit + push
def run(cmd, timeout=300):
    L("RUN: %s" % " ".join(cmd))
    try:
        r = subprocess.run(cmd, cwd=base, capture_output=True, text=True, timeout=timeout)
        L("rc=%d stdout=%s stderr=%s" % (r.returncode, r.stdout[-300:], r.stderr[-300:]))
        return r.returncode
    except Exception as e:
        L("EXC: %r" % e)
        return -1
run(["git","add","-f","seconds.log"])
run(["git","add","-A"])
run(["git","-c","user.name=Yatin-Code","-c","user.email=Yatin-Code@users.noreply.github.com","commit","-m","chore: 24 hours elapsed — stop line recorded"])
rc = run(["git","push"], timeout=300)
# even if push slow, retry once
if rc != 0:
    time.sleep(30)
    run(["git","push"], timeout=300)
# release
run(["gh","release","create","v1.0.0","--repo","Yatin-Code/24hours","--title","v1.0.0 — the day ended","--notes","The 24-hour timer finished. seconds.log contains one line per second of the run. The code remains."], timeout=300)
L("FINALIZE DONE")
