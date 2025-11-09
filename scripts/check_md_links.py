"""Check markdown files for broken local links and wiki-style links.

Usage: python scripts/check_md_links.py

- Scans all .md files under the repository root.
- Detects [text](url) links and [[wiki_links]]
- For relative links (not starting with http:// or https:// or mailto:), checks that the target file exists.
- For wiki links like [[foo_bar]], attempts to map to either a matching file name under the repo (with .md) or to a file in a common folders list.

Exit code: 0 if no broken links found, 2 if broken links were detected.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MD_GLOB = "**/*.md"

# Patterns
MD_LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
WIKI_LINK_RE = re.compile(r"\[\[([^\]]+)\]\]")

IGNORED_SCHEMES = ("http://", "https://", "mailto:")

# Common folders to try when resolving wiki links
WIKI_FOLDERS = [Path("patterns"), Path("problems"), Path("")]


def resolve_relative(base: Path, target: str) -> Path:
    """Resolve a relative link target against the base file's directory.
    Handles fragments like file.md#heading by stripping the fragment.
    """
    target_no_frag = target.split('#', 1)[0]
    return (base.parent / target_no_frag).resolve()


def find_wiki_target(name: str) -> Path:
    """Try to find a file for a wiki link name.

    Try exact name + .md, name with numeric prefixes, and common folders.
    """
    candidates = []
    # exact
    candidates.append(Path(name + ".md"))
    # underscores to spaces variation
    candidates.append(Path(name.replace(' ', '_') + ".md"))
    # try numeric prefix patterns (e.g., 011_container_with_most_water)
    candidates.append(Path(name))

    for folder in WIKI_FOLDERS:
        for c in list(candidates):
            candidates.append(folder / c)

    for c in candidates:
        p = (ROOT / c).resolve()
        if p.exists():
            return p
    return None


def is_ignored_target(target: str) -> bool:
    return any(target.startswith(s) for s in IGNORED_SCHEMES)


def main() -> int:
    md_files = list(ROOT.glob(MD_GLOB))
    broken = []

    for md in md_files:
        text = md.read_text(encoding='utf-8')
        for m in MD_LINK_RE.finditer(text):
            link_text, link_target = m.group(1), m.group(2)
            if is_ignored_target(link_target):
                continue
            # absolute anchor or intra-file anchor
            if link_target.startswith('#'):
                # optional: could check heading exists — skip for now
                continue
            try:
                resolved = resolve_relative(md, link_target)
            except Exception:
                resolved = None
            if resolved is None or not resolved.exists():
                broken.append((md, link_target))
        for m in WIKI_LINK_RE.finditer(text):
            name = m.group(1)
            target = find_wiki_target(name)
            if not target:
                broken.append((md, f"[[{name}]]"))

    if broken:
        print("Broken links found:\n")
        for md, target in broken:
            print(f"{md.relative_to(ROOT)} -> {target}")
        return 2

    print("No broken local markdown links found.")
    return 0


if __name__ == '__main__':
    sys.exit(main())
