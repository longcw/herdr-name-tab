#!/usr/bin/env python3
"""Check that an ssh command names its host and never its user."""

import os
import sys

# a name other than __main__ is what keeps the script from running itself
src = open(os.path.join(os.path.dirname(__file__), "herdr-name-tab")).read()
ns = {"__name__": "herdr_name_tab"}
exec(compile(src, "herdr-name-tab", "exec"), ns)

CASES = [
    # the user is the same on every machine, so it never names one
    ("ssh longc@192.168.100.121", "ssh-121"),
    ("ssh root@prod-01", "prod-01"),
    ("ssh dev@production.example.com", "production"),
    # options that take a value hide the host one token further along
    ("ssh -p 2222 deploy@prod-01", "prod-01"),
    ("ssh -p2222 prod-01", "prod-01"),
    ("ssh -i ~/.ssh/id_ed25519 prod-01", "prod-01"),
    ("ssh -J bastion prod-01", "prod-01"),
    ("ssh -o StrictHostKeyChecking=no prod-01", "prod-01"),
    ("ssh -L 8080:localhost:80 prod-01", "prod-01"),
    ("ssh -4 -q -t prod-01", "prod-01"),
    # a command after the host is not the host
    ("ssh root@prod-01 tail -f /var/log/syslog", "prod-01"),
    ("ssh ssh://deploy@prod-01:2222", "prod-01"),
    ("ssh root@[2001:db8::1]:22", "ssh-1"),
    ("ssh 10.0.0.5", "ssh-5"),
    ("mosh backup-2", "backup-2"),
    ("sshpass -p secret ssh longc@10.1.2.99", "ssh-99"),
    ("ssh prod-01", "prod-01"),
]

failed = 0
for command, want in CASES:
    got = ns["slug"](ns["ssh_label"](command))
    if got != want:
        failed += 1
        print(f"FAIL {command!r}: got {got!r}, want {want!r}")

print(f"{len(CASES) - failed}/{len(CASES)} pass")
sys.exit(1 if failed else 0)
