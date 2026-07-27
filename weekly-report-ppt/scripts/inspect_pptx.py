#!/usr/bin/env python3
"""Inspect a PPTX template using only the Python standard library."""

from __future__ import annotations

import argparse
import re
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


NS = {
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
}


def slide_number(name: str) -> int:
    match = re.search(r"slide(\d+)\.xml$", name)
    return int(match.group(1)) if match else 10**9


def emu_to_inches(value: str | None) -> str:
    if not value:
        return "?"
    return f"{int(value) / 914400:.2f}"


def shape_summary(shape: ET.Element) -> str:
    meta = shape.find(".//p:cNvPr", NS)
    name = meta.get("name", "?") if meta is not None else "?"
    texts = [node.text or "" for node in shape.findall(".//a:t", NS)]
    text = " | ".join(part.strip() for part in texts if part.strip())

    xfrm = shape.find(".//a:xfrm", NS)
    position = "x=? y=? w=? h=?"
    if xfrm is not None:
        off = xfrm.find("a:off", NS)
        ext = xfrm.find("a:ext", NS)
        if off is not None and ext is not None:
            position = (
                f"x={emu_to_inches(off.get('x'))} "
                f"y={emu_to_inches(off.get('y'))} "
                f"w={emu_to_inches(ext.get('cx'))} "
                f"h={emu_to_inches(ext.get('cy'))}"
            )

    sizes = {
        f"{int(node.get('sz')) / 100:g}pt"
        for node in shape.findall(".//*[@sz]")
        if node.get("sz", "").isdigit()
    }
    colors = {
        node.get("val")
        for node in shape.findall(".//a:srgbClr", NS)
        if node.get("val")
    }
    details = [position]
    if sizes:
        details.append("fonts=" + ",".join(sorted(sizes)))
    if colors:
        details.append("colors=" + ",".join(sorted(colors)))
    if text:
        details.append(f"text={text!r}")
    return f"{name}: " + "; ".join(details)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pptx", type=Path)
    args = parser.parse_args()
    path = args.pptx.resolve()

    if path.suffix.lower() != ".pptx":
        parser.error("template must be a .pptx file")
    if not path.is_file():
        parser.error(f"file not found: {path}")

    try:
        with zipfile.ZipFile(path) as archive:
            bad = archive.testzip()
            if bad:
                raise ValueError(f"corrupt archive entry: {bad}")
            names = archive.namelist()
            presentation = ET.fromstring(archive.read("ppt/presentation.xml"))
            size = presentation.find("p:sldSz", NS)
            if size is not None:
                print(
                    "slide_size_inches:",
                    emu_to_inches(size.get("cx")),
                    "x",
                    emu_to_inches(size.get("cy")),
                )
            slides = sorted(
                (
                    name
                    for name in names
                    if re.fullmatch(r"ppt/slides/slide\d+\.xml", name)
                ),
                key=slide_number,
            )
            media = [name for name in names if name.startswith("ppt/media/")]
            print(f"slides: {len(slides)}")
            print(f"media_files: {len(media)}")

            for index, name in enumerate(slides, 1):
                root = ET.fromstring(archive.read(name))
                print(f"\n--- slide {index}: {name}")
                shapes = root.findall(".//p:sp", NS)
                pictures = root.findall(".//p:pic", NS)
                groups = root.findall(".//p:grpSp", NS)
                print(
                    f"shapes={len(shapes)} pictures={len(pictures)} groups={len(groups)}"
                )
                for shape in shapes:
                    print(" ", shape_summary(shape))
    except (KeyError, ValueError, zipfile.BadZipFile, ET.ParseError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
