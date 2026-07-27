#!/usr/bin/env python3
"""Validate a generated weekly-report PPTX and its required text."""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


TEXT_TAG = "{http://schemas.openxmlformats.org/drawingml/2006/main}t"


def inspect_archive(path: Path) -> tuple[list[str], str, dict[str, str]]:
    with zipfile.ZipFile(path) as archive:
        bad = archive.testzip()
        if bad:
            raise ValueError(f"corrupt archive entry: {bad}")
        names = archive.namelist()
        required = {
            "[Content_Types].xml",
            "ppt/presentation.xml",
            "ppt/_rels/presentation.xml.rels",
        }
        missing = sorted(required.difference(names))
        if missing:
            raise ValueError("missing required entries: " + ", ".join(missing))

        xml_names = [name for name in names if name.endswith(".xml")]
        for name in xml_names:
            ET.fromstring(archive.read(name))

        slides = sorted(
            name
            for name in names
            if re.fullmatch(r"ppt/slides/slide\d+\.xml", name)
        )
        text_parts: list[str] = []
        for name in slides:
            root = ET.fromstring(archive.read(name))
            text_parts.extend(node.text or "" for node in root.iter(TEXT_TAG))

        media_hashes = {
            name: hashlib.sha256(archive.read(name)).hexdigest()
            for name in names
            if name.startswith("ppt/media/") and not name.endswith("/")
        }
    return slides, "\n".join(text_parts), media_hashes


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pptx", type=Path)
    parser.add_argument("--template", type=Path)
    parser.add_argument("--expected", action="append", default=[])
    args = parser.parse_args()

    output = args.pptx.resolve()
    if output.suffix.lower() != ".pptx" or not output.is_file():
        parser.error(f"output PPTX not found: {output}")
    if args.template and output == args.template.resolve():
        parser.error("output must not overwrite the template")

    try:
        slides, text, media = inspect_archive(output)
        if not slides:
            raise ValueError("presentation contains no slides")

        failures = [
            phrase for phrase in args.expected if phrase not in text
        ]
        placeholders = [
            marker for marker in ("TODO", "[TODO", "待补充") if marker in text
        ]
        if failures:
            raise ValueError("missing expected text: " + ", ".join(failures))
        if placeholders:
            raise ValueError(
                "unresolved placeholder text: " + ", ".join(placeholders)
            )

        print(f"archive: valid ({output})")
        print(f"slides: {len(slides)}")
        print(f"characters: {len(text.replace(chr(10), ''))}")
        print(f"expected_phrases: {len(args.expected)} present")

        if args.template:
            template = args.template.resolve()
            if not template.is_file():
                raise ValueError(f"template not found: {template}")
            _, _, template_media = inspect_archive(template)
            common = set(media).intersection(template_media)
            unchanged = sum(media[name] == template_media[name] for name in common)
            print(
                "template_media:",
                f"output={len(media)} template={len(template_media)} "
                f"same_name_and_hash={unchanged}",
            )
    except (ValueError, zipfile.BadZipFile, ET.ParseError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
