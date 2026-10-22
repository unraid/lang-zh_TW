#!/usr/bin/env python3
"""Build a Unraid-importable zh_TW.zip from translation source files.

Run from repository root: python3 scripts/build_language_zip.py
The ZIP preserves plugin subfolder structure, without repository metadata.
"""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

if __package__:
    from .check_upstream_coverage import parse_text_entries
else:
    from check_upstream_coverage import parse_text_entries

# Helpers.php in Unraid WebGUI uses explode(' ', ' '.prefix) to select units.
EXPECTED_PREFIXES = {
    'prefix_SI': 'K M G T P E Z Y',
    'prefix_IEC': 'Ki Mi Gi Ti Pi Ei Zi Yi',
}


def validate_prefixes(data: str) -> None:
    rows = [line for line in data.splitlines() if line.startswith(tuple(key + '=' for key in EXPECTED_PREFIXES))]
    for key, expected in EXPECTED_PREFIXES.items():
        matches = [row.split('=', 1)[1] for row in rows if row.startswith(key + '=')]
        if matches != [expected]:
            raise RuntimeError(f'Unexpected {key} in packaged language: {matches!r}; expected {expected!r}')
        prefix_parts = matches[0].split(' ')
        assert len(prefix_parts) == 8 and all(prefix_parts)


ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "dist" / "zh_TW.zip"

# Unraid loads translations by URI segment. The embedded UD page on /Main
# never loads unassigneddevices.txt; its lib.php does not call parse_plugin().
# Supplement only missing entries so Main's context-specific wording wins.
RUNTIME_SUPPLEMENTS = {
    "main.txt": ("Unassigned Devices/unassigneddevices.txt",),
}


def supplement_page(base: str, extra: str) -> str:
    keys, blocks = parse_text_entries(base)
    extra_keys, extra_blocks = parse_text_entries(extra)
    additions = [f"{key}={value}" for key, value in extra_keys.items() if key not in keys]
    additions.extend(f"{tag}\n{body.rstrip()}\n:end"
                     for tag, body in extra_blocks.items() if tag not in blocks)
    if not additions:
        return base
    return (base.rstrip() + "\n\n; Runtime supplement for embedded plugin pages\n"
            + "\n".join(additions) + "\n")


def package_text(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    for relative in RUNTIME_SUPPLEMENTS.get(path.relative_to(ROOT).as_posix(), ()):
        text = supplement_page(text, (ROOT / relative).read_text(encoding="utf-8"))
    return text


def included(path: Path) -> bool:
    relative = path.relative_to(ROOT)
    if path.suffix != ".txt" or path.name == "LICENSE.txt":
        return False
    if any(part.startswith(".") for part in relative.parts):
        return False
    if "dist" in relative.parts:
        return False
    return True


def main() -> None:
    files = sorted(path for path in ROOT.rglob("*.txt") if included(path))
    if not files:
        raise RuntimeError("No translation files found")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    # FileUpload.php flattens ZIP paths and lowercases the basename.
    names = [path.name.lower() for path in files]
    if len(names) != len(set(names)):
        raise RuntimeError("Translation basenames collide after Unraid's flattened import")
    with ZipFile(OUT, "w", compression=ZIP_DEFLATED) as z:
        for path in files:
            z.writestr(path.relative_to(ROOT).as_posix(), package_text(path).encode("utf-8"))
    # Verify the actual installable ZIP, not only the working-tree file.
    with ZipFile(OUT) as z:
        for name in z.namelist():
            raw = z.read(name)
            raw.decode('utf-8')
            if raw.startswith(b'\xef\xbb\xbf') or b'\r' in raw:
                raise RuntimeError(f'Packaged {name} must use UTF-8 without BOM and LF line endings')
        validate_prefixes(z.read('translations.txt').decode('utf-8'))
    print(f"Verified SI/IEC units in packaged {OUT.relative_to(ROOT)}")
    print(f"Created {OUT.relative_to(ROOT)} with {len(files)} translation files")


if __name__ == "__main__":
    main()
