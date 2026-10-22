#!/usr/bin/env python3
"""Compare every translation lookup key and help section against upstream en_US.

Usage: python3 scripts/check_upstream_coverage.py /path/to/lang-en_US
The upstream git reference is pinned in .github/workflows/validate-translations.yml.
"""
from pathlib import Path
from collections import Counter
import re
import sys

ROOT = Path(__file__).resolve().parent.parent


def embedded_php(text: str) -> Counter[str]:
    """PHP in help is executed by translate(); preserve the exact source code."""
    return Counter(re.findall(r"<\?.*?\?>", text, flags=re.S))


def translation_files(root: Path) -> dict[str, Path]:
    return {
        p.relative_to(root).as_posix(): p
        for p in root.rglob("*.txt")
        if p.name != "LICENSE.txt" and ".git" not in p.parts
    }


def parse_entries(path: Path) -> tuple[dict[str, str], dict[str, str]]:
    return parse_text_entries(path.read_text(encoding="utf-8"))


def parse_text_entries(text: str) -> tuple[dict[str, str], dict[str, str]]:
    keys: dict[str, str] = {}
    blocks: dict[str, str] = {}
    active: str | None = None
    for line in text.splitlines():
        if line.startswith(":") and line.endswith(":") and line != ":end":
            # Unraid translation help sections, not arbitrary colon content.
            if line.endswith(("_help:", "_plug:")):
                active = line
                blocks[line] = ""
                continue
        if line == ":end":
            active = None
            continue
        if active:
            blocks[active] += line + "\n"
            continue
        if not line.strip() or line.startswith((";", "#")):
            continue
        if "=" in line:
            key, value = line.split("=", 1)
            if key:
                keys[key] = value
    return keys, blocks


def parse(path: Path) -> tuple[set[str], set[str]]:
    keys, blocks = parse_entries(path)
    return set(keys), set(blocks)


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: check_upstream_coverage.py UPSTREAM_LANG_EN_US_DIR")
        return 2
    upstream = Path(sys.argv[1]).resolve()
    if not upstream.is_dir():
        print(f"Upstream source directory unavailable: {upstream}")
        return 2

    en_files = translation_files(upstream)
    if not en_files:
        print(f"No upstream translation files found: {upstream}")
        return 2
    tw_files = translation_files(ROOT)
    missing_files = sorted(en_files.keys() - tw_files.keys())
    errors: list[str] = [f"Missing translation file: {x}" for x in missing_files]
    total_keys = matched_keys = 0
    total_blocks = matched_blocks = 0
    for rel, en_path in sorted(en_files.items()):
        source_keys, source_blocks = parse(en_path)
        total_keys += len(source_keys)
        total_blocks += len(source_blocks)
        if rel not in tw_files:
            continue
        tw_keys, tw_blocks = parse(tw_files[rel])
        values, bodies = parse_entries(tw_files[rel])
        source_values, source_bodies = parse_entries(en_path)
        for local, source, kind in ((values, source_values, "key"),
                                    (bodies, source_bodies, "help block")):
            errors.extend(f"{rel}: embedded PHP changed in {kind} {name!r}"
                          for name in local.keys() & source.keys()
                          if embedded_php(local[name]) != embedded_php(source[name]))
        errors.extend(f"{rel}: empty translation for {key!r}"
                      for key in source_keys & tw_keys if not values[key].strip())
        errors.extend(f"{rel}: empty help block {tag}"
                      for tag in source_blocks & tw_blocks if not bodies[tag].strip())
        matched_keys += len(source_keys & tw_keys)
        matched_blocks += len(source_blocks & tw_blocks)
        missing_keys = sorted(source_keys - tw_keys)
        missing_blocks = sorted(source_blocks - tw_blocks)
        errors.extend(f"{rel}: missing exact English key {key!r}" for key in missing_keys)
        errors.extend(f"{rel}: missing help block {tag}" for tag in missing_blocks)
        print(f"{rel}: {len(source_keys & tw_keys)}/{len(source_keys)} keys, "
              f"{len(source_blocks & tw_blocks)}/{len(source_blocks)} help sections")

    print(f"\nTOTAL: {len(en_files) - len(missing_files)}/{len(en_files)} files, "
          f"{matched_keys}/{total_keys} exact keys, "
          f"{matched_blocks}/{total_blocks} help sections")
    if errors:
        print("\nCoverage check failed:")
        for error in errors:
            print("  -", error)
        return 1
    print("PASS: all upstream translation files, keys and help sections are present.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
