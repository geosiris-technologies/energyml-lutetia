"""The findings of `energyml check --errors-only`, one per line, sorted: what
`docs/errors.expected.txt` holds and what the `check` workflow compares.

    energyml check --errors-only --max 1000 package-with-errors/Lutetia.epc | python scripts/findings.py

A line is the object's uuid and what is wrong with it: `kind <name>` for a
property on an abstract property kind, `<rule> <severity>` for a business rule.
The uuids are derived from the content of the recipe, so they only move when the
recipe does. The last line is the totals line of the report.
"""

import re
import sys

UUID = r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"
KIND = re.compile(rf"^\s+({UUID}) its property kind `([^`]+)` \(\S+\) is abstract")
RULE = re.compile(rf"^\s+({UUID}) ((?:trg|house)/\S+) \[(error|warning)\]")
TOTALS = re.compile(r"^\d+ error\(s\), \d+ warning\(s\)$")


def main() -> int:
    found, totals = set(), None
    for line in sys.stdin.read().splitlines():
        if m := KIND.match(line):
            found.add(f"{m.group(1)} kind {m.group(2)}")
        elif m := RULE.match(line):
            found.add(f"{m.group(1)} {m.group(2)} {m.group(3)}")
        elif TOTALS.match(line.strip()):
            totals = line.strip()
    for f in sorted(found):
        print(f)
    if totals is None:
        print("no totals line: is this the output of `energyml check`?", file=sys.stderr)
        return 1
    print(totals)
    return 0


if __name__ == "__main__":
    sys.exit(main())
