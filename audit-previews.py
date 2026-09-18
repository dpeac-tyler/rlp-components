#!/usr/bin/env python3
"""
Audit component.html against css/styles.css.

Why this exists
---------------
The catalog's left/middle columns are a LIVE PREVIEW. If a class used in a
preview is not defined in css/styles.css, the preview silently renders wrong
while the HTML column still shows correct markup. A developer comparing the
two is then actively misled - which is worse than having no preview at all.

This actually happened: `.display-inline` was undefined, so a label's
"Required" span dropped onto its own line instead of sitting to the right of
the label text, in every entry that used the production label structure.

Run:  python3 audit-previews.py
Exit: 0 if clean, 1 if anything needs attention.
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).parent
HTML = HERE / "component.html"
CSS = HERE / "css" / "styles.css"

# Classes that are intentionally unstyled.
#   demo-*                 - JS hooks for the catalog's own interactive demos
#   ql-snow / quill-*      - Quill theme markers; the look is hand-rolled here
#   rich-text-input        - structural wrapper only
#   svg-inline--fa / fa-*  - Font Awesome, documented in code blocks but not
#                            bundled into prototypes
ALLOW_EXACT = {
    "ql-snow",
    "rich-text-input",
    "quill-editor-container",
    "is-hidden-input",
}
ALLOW_PREFIX = ("demo-", "svg-inline--fa", "fa-")


def defined_classes(css: str) -> set:
    found = set(re.findall(r"\.([A-Za-z0-9_-]+(?:\\:[A-Za-z0-9_-]+)?)", css))
    return {c.replace("\\:", ":") for c in found}


def allowed(cls: str) -> bool:
    return cls in ALLOW_EXACT or cls.startswith(ALLOW_PREFIX)


def used_classes(html: str, field: str) -> dict:
    blocks = re.findall(rf"^  {field}: `(.*?)`,$", html, re.S | re.M)
    counts = {}
    for block in blocks:
        for attr in re.findall(r'class="([^"]+)"', block):
            for cls in attr.split():
                counts[cls] = counts.get(cls, 0) + 1
    return counts


def main() -> int:
    html = HTML.read_text()
    css = CSS.read_text()
    have = defined_classes(css)
    problems = 0

    # 1. Undefined classes. Only `preview` is fatal - that is what renders.
    for field, fatal in (("preview", True), ("code", False)):
        used = used_classes(html, field)
        missing = {c: n for c, n in used.items() if c not in have and not allowed(c)}
        label = "PREVIEW" if fatal else "code (informational)"
        if missing:
            if fatal:
                problems += len(missing)
            print(f"\n{label}: {len(missing)} undefined class(es) of {len(used)} used")
            for cls, n in sorted(missing.items(), key=lambda kv: -kv[1]):
                print(f"   {cls}  (x{n})")
            if fatal:
                print("   ^ these make the rendered preview disagree with the markup")
        else:
            print(f"{label}: all {len(used)} classes defined")

    # 2. Structural sanity of the COMPONENTS array.
    region = html[html.index("const COMPONENTS = ["):html.index("\n];")]
    names = re.findall(r'^  name: "(.*)",$', region, re.M)
    fidelities = re.findall(r'^  fidelity: "(\w+)",$', region, re.M)

    if len(names) != len(fidelities):
        print(f"\nSTRUCTURE: {len(names)} entries but {len(fidelities)} fidelity tags")
        problems += 1

    bad_fid = [f for f in fidelities if f not in ("verified", "unverified", "proposed")]
    if bad_fid:
        print(f"\nSTRUCTURE: invalid fidelity value(s): {set(bad_fid)}")
        problems += 1

    if names != sorted(names, key=lambda s: s.lower()):
        print("\nORDER: entries are not alphabetical")
        for a, b in zip(names, sorted(names, key=lambda s: s.lower())):
            if a != b:
                print(f"   expected {b!r} but found {a!r}")
                break
        problems += 1

    # 3. A literal </script> inside a template literal ends the page's script
    #    tag and blanks the whole library. The file's convention is `</` + `script>`.
    if html.count("</script>") > 1:
        print("\nFATAL: more than one literal </script> - use `</` + `script>` inside "
              "template literals, or the entire catalog goes blank")
        problems += 1

    counts = {f: fidelities.count(f) for f in set(fidelities)}
    print(f"\n{len(names)} entries: " +
          ", ".join(f"{n} {f}" for f, n in sorted(counts.items())))

    if problems:
        print(f"\n{problems} problem(s) need attention.")
        return 1
    print("\nClean.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
