#!/usr/bin/env python3
"""Validate basic structure and relative Markdown links in the AI Infra Wiki."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote


LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")


def first_content_line(path: Path) -> str:
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            return line.strip()
    return ""


def link_target(raw_target: str) -> str:
    target = raw_target.strip()
    if target.startswith("<") and ">" in target:
        target = target[1 : target.index(">")]
    elif " \"" in target:
        target = target.split(" \"", 1)[0]
    return unquote(target.split("#", 1)[0])


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_wiki.py <wiki-root>", file=sys.stderr)
        return 2

    root = Path(sys.argv[1]).expanduser().resolve()
    if not root.is_dir():
        print(f"error: wiki root does not exist: {root}", file=sys.stderr)
        return 2

    markdown_files = sorted(
        path for path in root.rglob("*.md") if ".git" not in path.parts
    )
    errors: list[str] = []

    if not (root / "README.md").is_file():
        errors.append("missing root README.md")

    for path in markdown_files:
        relative = path.relative_to(root)
        if not first_content_line(path).startswith("# "):
            errors.append(f"{relative}: first content line is not an H1")

        text = path.read_text(encoding="utf-8")
        for match in LINK_RE.finditer(text):
            target = link_target(match.group(1))
            if not target or target.startswith(
                ("http://", "https://", "mailto:", "app://")
            ):
                continue
            resolved = (path.parent / target).resolve()
            try:
                resolved.relative_to(root)
            except ValueError:
                errors.append(f"{relative}: link escapes wiki root: {target}")
                continue
            if not resolved.exists():
                errors.append(f"{relative}: broken relative link: {target}")

    project_dirs = sorted(
        path
        for path in root.iterdir()
        if path.is_dir() and not path.name.startswith(".")
    )
    for project_dir in project_dirs:
        if not any(
            (project_dir / home).is_file() for home in ("README.md", "首页.md")
        ):
            errors.append(
                f"{project_dir.name}: missing project README.md or 首页.md"
            )

    if errors:
        print("Wiki validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        f"Wiki validation passed: {len(markdown_files)} Markdown files, "
        f"{len(project_dirs)} project directories"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
