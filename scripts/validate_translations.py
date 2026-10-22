#!/usr/bin/env python3
"""Validate the structure of the Unraid Traditional Chinese language pack.

Run from the repository root: python3 scripts/validate_translations.py
Only the right-hand side of KEY=translation may be localized.
"""
from collections import Counter
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent

# Discover every plugin translation automatically; exclude the license (not a lookup file).
TRANSLATION_FILES = sorted(
    path.relative_to(ROOT).as_posix()
    for path in ROOT.rglob("*.txt")
    if path.name != "LICENSE.txt" and ".git" not in path.parts
)

# Every label must have an explicit value, including unchanged technical names.
ALLOWED_EMPTY: dict[str, set[str]] = {}

# Some runtime UI components supply substitutions only in the translated
# template (the English lookup key does not contain those placeholders).
ALLOWED_DYNAMIC_FORMAT = {
    ("translations.txt", "You will no longer have access to this server using this url"),
}

# Ordinal printf formats (%1$s) are equivalent to ordinary %s for
# signature checking. Preserve both the count and the conversion types.
PRINTF = re.compile(r"%(?:[1-9]\d*\$)?[-+ #0]*\d*(?:\.\d+)?([sdfu])")
BLOCK_BEGIN = re.compile(r":[A-Za-z0-9_-]+_(?:help|plug):")


# Flag Simplified-only characters and known misleading translation phrases.
SIMPLIFIED_ONLY = re.compile(
    r"[这们吗为会过还从发经网软盘页图标简设选显断编务数归户开关识销结进读键诊络"
    r"贴购题动权试级导写应员没间顶声创观黄议资录壳处协议长隐细预内许继于扩稳谢]"
)
BAD_TERMS = re.compile(
    r"同位元檢查磁碟|同位元檢查檢查|奇偶校驗|CPU\s*討論串|虛擬機器器"
    r"|插件|運行|自定義|刷新|設備|圖標|復制|粘貼|窗口|文本|字符|字節"
    r"|操作系統|總線|光盤|聲卡|兼容|進程|線程|傳感器|模塊|軟件|硬件"
    r"|加載|搜索|鏈接|協議|只讀|高級|網關|客戶端|身份|反饋|模板|數據|訪問"
)
HAN = re.compile(r"[\u3400-\u9fff]")
ASCII_PROSE = re.compile(r"^[A-Za-z0-9 _.,!?;:()'/\-+&*\u2010-\u201f]+$")
ALLOW_ENGLISH_VALUES = {"Numbers_array", "prefix_SI", "prefix_IEC",
                        "Active Directory", "httpIPport or httphostport"}

KEYWORD_MAP_KEYS = {
    "Days_array": (
        "Sunday Monday Tuesday Wednesday Thursday Friday Saturday "
        "Sun Mon Tue Wed Thu Fri Sat"
    ).split(),
    "Months_array": (
        "January February March April May June July August September October November December "
        "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec"
    ).split(),
}


def valid_keyword_map(name: str, value: str) -> bool:
    # Translations.php converts spaces to '&' and ':' to '=' before parse_str.
    parts = [part.split(":") for part in value.split(" ")]
    return (all(len(part) == 2 and part[1] for part in parts)
            and [part[0] for part in parts] == KEYWORD_MAP_KEYS[name])

def check_localization_text(relative: str, lineno: int, value: str,
                            is_block: bool = False, key: str = "") -> list[str]:
    issues: list[str] = []
    if "\ufffd" in value:
        issues.append(f"{relative}:{lineno}: invalid replacement character in translation")
    if SIMPLIFIED_ONLY.search(value):
        issues.append(f"{relative}:{lineno}: likely Simplified Chinese in translation")
    if BAD_TERMS.search(value):
        issues.append(f"{relative}:{lineno}: deprecated or inaccurate terminology")
    if key in ALLOW_ENGLISH_VALUES:
        return issues

    candidate = value.strip()
    code_tick = chr(96)
    if is_block and (
        not candidate or candidate.startswith((";", "#", code_tick, "'tailscale"))
        or code_tick in candidate or candidate.startswith(("<?", "config/"))
        or re.match(r"^[+*]\s*\d", candidate) or ".pem" in candidate
    ):
        return issues

    if (len(candidate) >= 40 and not HAN.search(candidate)
            and ASCII_PROSE.fullmatch(candidate)):
        issues.append(f"{relative}:{lineno}: likely untranslated English sentence")
    return issues


# Guard the most visible Parity terms from accidental global replacements.
PARITY_EXPECTATIONS = {
    "translations.txt": {
        "Parity": "同位元校驗",
        "Parity-Check": "同位元校驗檢查",
        "Parity-Sync": "同位元校驗同步",
    },
    "dashboard.txt": {
        "Parity disk not present": "未偵測到校驗磁碟",
    },
    "settings.txt": {
        "Parity Check": "同位元校驗檢查",
    },
}


# Fail on regressions in particularly misleading or unsafe UI labels.
CRITICAL_UI_TRANSLATIONS = {
    "translations.txt": {
        "No errors reported": "沒有回報任何錯誤",
        "Downgrades are only recommended if youre unable to solve a critical issue": "只有在重大問題無法解決時，才建議降級至舊版。",
        "If you fill this field out then your email will not be sent": "如果填寫此欄位，系統將不會寄出電子郵件。",
        "Device": "裝置",
        "FAVORITES": "我的最愛",
        "UNASSIGNED DISKS": "未指派磁碟",
        "REMOTE SHARES": "遠端共享",
        "HISTORICAL UNASSIGNED DEVICES": "歷史未指派裝置",
        "SLEEP": "睡眠",
        "Output voltage": "輸出電壓",
        "Data Partition": "資料分割區",
    },
    "main.txt": {
        "Array Devices": "陣列裝置",
        "Unassigned Devices": "未指派裝置",
    },
    "dashboard.txt": {
        "Share count %s with %s public SMB and %s public NFS": "共有 %s 個共享資料夾，其中 %s 個公開使用 SMB、%s 個公開使用 NFS。",
    },
    "Community Apps/apps.txt": {
        "Are you sure you want to install %s docker and %s plugin applications": "確定要安裝 %s 個 Docker 應用程式及 %s 個外掛程式嗎？",
    },
    "settings.txt": {
        "Output voltage": "輸出電壓",
        "Display world-wide-name in device ID":
            "在裝置識別碼中顯示全球唯一名稱（WWN）",
    },
}

# Safety-related help sections must retain their core warning or direction.
REQUIRED_HELP_MARKERS = {
    "info_file_system_help": ("格式化", "清除", "備份"),
    "info_btrfs_check_help": ("--readonly", "--repair", "危險"),
    "info_btrfs_scrub_help": ("資料校驗", "備援", "備份"),
    "docker_appdata_location_help": ("正斜線", "/config"),
    "mgmt_certificate_expiration_help": ("DNS", "保護"),
}

def formats(text: str) -> Counter[str]:
    return Counter(m.group(1) for m in PRINTF.finditer(text))

def check_file(relative: str) -> tuple[list[str], int, int]:
    errors: list[str] = []
    path = ROOT / relative
    try:
        raw = path.read_bytes()
        body = raw.decode("utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        return [f"{relative}: could not read valid UTF-8 ({exc})"], 0, 0

    if raw.startswith(b"\xef\xbb\xbf"):
        errors.append(f"{relative}: UTF-8 BOM is not supported")
    if b"\r" in raw:
        errors.append(f"{relative}: expected Unix LF line endings")

    active_block = None
    block_text: dict[str, list[str]] = {}
    keys = 0
    empty = 0
    labels: dict[str, str] = {}

    for lineno, line in enumerate(body.splitlines(), 1):
        if BLOCK_BEGIN.fullmatch(line):
            if active_block:
                errors.append(f"{relative}:{lineno}: nested translation block")
            if line.strip(":") in block_text:
                errors.append(f"{relative}:{lineno}: duplicate translation block {line}")
            active_block = line
            block_text[line.strip(":")] = []
            continue
        if line == ":end":
            if not active_block:
                errors.append(f"{relative}:{lineno}: unexpected :end")
            active_block = None
            continue
        if active_block:
            block_text[active_block.strip(":")].append(line)
            if not line.startswith((";", "#")):
                errors.extend(check_localization_text(relative, lineno, line, is_block=True))
            continue
        if not line.strip() or line.startswith((";", "#")):
            continue
        if "=" not in line:
            errors.append(f"{relative}:{lineno}: expected KEY=translation")
            continue

        key, translated = line.split("=", 1)
        if not key:
            errors.append(f"{relative}:{lineno}: empty lookup key")
            continue
        keys += 1
        if key in labels and labels[key] != translated:
            errors.append(f"{relative}:{lineno}: conflicting translation for {key!r}")
        labels[key] = translated

        if not translated.strip():
            empty += 1
            if key not in ALLOWED_EMPTY.get(relative, set()):
                errors.append(f"{relative}:{lineno}: untranslated UI label: {key!r}")
            continue

        errors.extend(check_localization_text(relative, lineno, translated, key=key))

        if formats(key) != formats(translated):
            if (relative, key) not in ALLOWED_DYNAMIC_FORMAT:
                errors.append(
                    f"{relative}:{lineno}: placeholder mismatch "
                    f"{dict(formats(key))!r} -> {dict(formats(translated))!r}"
                )

    if active_block:
        errors.append(f"{relative}: unterminated translation block {active_block}")
    for name, lines in block_text.items():
        if not any(line.strip(" >\t") for line in lines):
            errors.append(f"{relative}: empty translation block {name}")

    if relative == "translations.txt":
        for name in KEYWORD_MAP_KEYS:
            if not valid_keyword_map(name, labels.get(name, "")):
                errors.append(f"{relative}: {name} must contain space-separated key:value pairs")
        for key, expected in {
            "prefix_SI": "K M G T P E Z Y",
            "prefix_IEC": "Ki Mi Gi Ti Pi Ei Zi Yi",
        }.items():
            if labels.get(key) != expected:
                errors.append(f"{relative}: unexpected {key} unit prefixes")

    for key, expected in PARITY_EXPECTATIONS.get(relative, {}).items():
        if labels.get(key) != expected:
            errors.append(f"{relative}: expected {key!r} to be {expected!r}")

    for key, expected in CRITICAL_UI_TRANSLATIONS.get(relative, {}).items():
        if labels.get(key) != expected:
            errors.append(f"{relative}: critical label {key!r} must remain {expected!r}")

    if relative == "helptext.txt":
        for name, required_terms in REQUIRED_HELP_MARKERS.items():
            body = "\n".join(block_text.get(name, []))
            if not body:
                errors.append(f"{relative}: missing required help block {name!r}")
                continue
            for term in required_terms:
                if term not in body:
                    errors.append(
                        f"{relative}: required text {term!r} missing in {name!r}"
                    )

    return errors, keys, empty

def main() -> int:
    failures = []
    total_keys = total_empty = 0
    for relative in TRANSLATION_FILES:
        errors, keys, empty = check_file(relative)
        failures.extend(errors)
        total_keys += keys
        total_empty += empty
        print(f"{relative}: {keys} labels, {empty} empty values")
    if failures:
        print("\nTranslation validation failed:", file=sys.stderr)
        for error in failures:
            print(f"  - {error}", file=sys.stderr)
        return 1
    print(f"\nPASS: {len(TRANSLATION_FILES)} files, "
          f"{total_keys} labels, {total_empty} empty values.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
