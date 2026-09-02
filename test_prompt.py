#!/usr/bin/env python3
"""Check the naming prompt against cases that have gone wrong before.

Needs a configured endpoint; skips without one, since it asks a real model.
"""

import os
import sys

src = open(os.path.join(os.path.dirname(__file__), "herdr-name-tab")).read()
ns = {"__name__": "herdr_name_tab"}
exec(compile(src, "herdr-name-tab", "exec"), ns)

if not ns["setting"]("api_url"):
    print("no api_url configured; skipping")
    sys.exit(0)

PLUGIN = "check if this plugin is safe github.com/kryptamine/herdr-auto-title, if so install it"

CASES = [
    # a number quoted in a message is not what the tab is about
    (PLUGIN, "auto-title", '"6921  a session porting an issue" replace this example', "auto-title"),
    # a follow-up on the same work keeps the name
    (PLUGIN, "auto-title", "cannot it be started without restarting the herdr server?", "auto-title"),
    # an unrelated subject does not
    (PLUGIN, "auto-title", "forget that, the go2rtc stream on the front door keeps crashing", None),
    # the work itself being an issue still names it by number
    ("fix the flaky retry test in agents #7083", "(none)", "same", "7083"),
]

failed = 0
for anchor, current, latest, want in CASES:
    query = f"{ns['PROMPT']}\n\nANCHOR: {anchor}\nNAME: {current}\nLATEST: {latest}\n"
    got = ns["slug"](ns["ask_model"](query)[0])
    ok = (got == want) if want else (got not in ("", current))
    if not ok:
        failed += 1
        print(f"FAIL latest={latest!r}: got {got!r}, want {want or 'a different name'}")

print(f"{len(CASES) - failed}/{len(CASES)} pass")
sys.exit(1 if failed else 0)
