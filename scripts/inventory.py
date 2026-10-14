#!/usr/bin/env python3
"""Regenerate docs/inventory.md from package/Lutetia.epc.

Usage: python scripts/inventory.py [--epc package/Lutetia.epc] [--out docs/inventory.md]

Standard library only. The output is deterministic (no date, no host), so CI can
regenerate it and fail on any difference.

Two independent readings of each object are compared: the part name
(`<Type>_<uuid>.xml`) and the root element of the XML. A disagreement is listed
at the end of the report and makes the script exit with status 1.
"""
import argparse
import collections
import re
import sys
import zipfile

NAMESPACES = {
    "http://www.energistics.org/energyml/data/resqmlv2": "RESQML",
    "http://www.energistics.org/energyml/data/commonv2": "EML (common)",
    "http://www.energistics.org/energyml/data/witsmlv2": "WITSML",
    "http://www.energistics.org/energyml/data/prodmlv2": "PRODML",
}
PART = re.compile(r"^([A-Za-z0-9]+)_([0-9a-fA-F-]{36})\.xml$")
ROOT = re.compile(rb"<(?:([A-Za-z0-9_]+):)?([A-Za-z0-9_]+)(\s[^>]*)?>", re.S)


def read_root(data):
    """Return (type, namespace uri, schemaVersion) of the root element; the type is xsi:type when present."""
    text = data
    if text.startswith(b"\xef\xbb\xbf"):
        text = text[3:]
    pos = 0
    while True:
        m = ROOT.search(text, pos)
        if m is None:
            return None
        if m.group(2) in (b"xml",) or text[m.start() + 1 : m.start() + 2] in (b"?", b"!"):
            pos = m.end()
            continue
        break
    attrs = (m.group(3) or b"").decode("utf-8", "replace")
    prefix = m.group(1).decode() if m.group(1) else None
    pat = r'xmlns%s="([^"]+)"' % ((":" + re.escape(prefix)) if prefix else "")
    ns = re.search(pat, attrs)
    ver = re.search(r'schemaVersion="([^"]*)"', attrs)
    xsi = re.search(r'xsi:type="(?:[A-Za-z0-9_]+:)?([A-Za-z0-9_]+)"', attrs)
    # An element declared as an abstract/base type carries its real class in xsi:type.
    local = xsi.group(1) if xsi else m.group(2).decode()
    return local, ns.group(1) if ns else "", ver.group(1) if ver else ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--epc", default="package/Lutetia.epc")
    ap.add_argument("--out", default="docs/inventory.md")
    args = ap.parse_args()

    counts = collections.Counter()
    mismatches = []
    other_parts = 0
    rels = 0
    with zipfile.ZipFile(args.epc) as z:
        for name in sorted(z.namelist()):
            if name.startswith("_rels/") or name.endswith(".rels"):
                rels += 1
                continue
            m = PART.match(name)
            if not m:
                other_parts += 1
                continue
            root = read_root(z.read(name)[:4096])
            if root is None:
                mismatches.append((name, "no root element"))
                continue
            local, ns, ver = root
            if local != m.group(1):
                mismatches.append((name, "root element is %s" % local))
            counts[(NAMESPACES.get(ns, ns or "?"), ver or "?", local)] += 1

    total = sum(counts.values())
    by_std = collections.Counter()
    for (std, ver, _), n in counts.items():
        by_std[(std, ver)] += n

    out = []
    out.append("# Inventory\n")
    out.append(
        "> **Generated** by `scripts/inventory.py` from `%s`. Do not edit by hand: "
        "CI regenerates this file and fails if it differs.\n" % args.epc.replace("\\", "/")
    )
    out.append(
        "Objects are counted from the part names (`<Type>_<uuid>.xml`) and checked "
        "against the root element of each part; the schema version is the "
        "`schemaVersion` attribute of that element.\n"
    )
    out.append("- Data objects: **%d**" % total)
    out.append("- Distinct object types: **%d**" % len(counts))
    out.append("- Relationship parts (`.rels`): %d" % rels)
    out.append("- Other parts (attachments, properties, content types): %d\n" % other_parts)
    out.append("## By standard and schema version\n")
    out.append("| Standard | Schema version | Objects |")
    out.append("|---|---|---:|")
    for (std, ver), n in sorted(by_std.items()):
        out.append("| %s | %s | %d |" % (std, ver, n))
    out.append("\n## By type\n")
    out.append("| Standard | Schema version | Type | Objects |")
    out.append("|---|---|---|---:|")
    for (std, ver, local), n in sorted(counts.items()):
        out.append("| %s | %s | `%s` | %d |" % (std, ver, local, n))
    out.append("\n## Consistency\n")
    if mismatches:
        out.append("Part name and root element disagree for:\n")
        for name, why in mismatches:
            out.append("- `%s`: %s" % (name, why))
    else:
        out.append("Part names and root elements agree for every object.")
    text = "\n".join(out) + "\n"
    with open(args.out, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    return 1 if mismatches else 0


if __name__ == "__main__":
    sys.exit(main())
