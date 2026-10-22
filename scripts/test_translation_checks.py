"""Regression checks for omissions that previously passed localization validation."""
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

import check_upstream_coverage as coverage
import validate_translations as validation
import build_language_zip as build
from zipfile import ZipFile


class TranslationChecks(unittest.TestCase):
    def check_fixture(self, source: str, translated: str) -> int:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            upstream = root / "en"
            local = root / "tw"
            for folder, content in ((upstream, source), (local, translated)):
                (folder / "Plugin").mkdir(parents=True)
                (folder / "Plugin" / "labels.txt").write_text(content, encoding="utf-8")
            with patch.object(coverage, "ROOT", local), patch("sys.argv", ["check", str(upstream)]):
                with redirect_stdout(StringIO()):
                    return coverage.main()

    def test_present_keys_do_not_hide_empty_translations(self):
        self.assertEqual(self.check_fixture("Start=\n", "Start=\n"), 1)

    def test_present_tags_do_not_hide_empty_help(self):
        source = ":example_help:\nA complete explanation.\n:end\n"
        self.assertEqual(self.check_fixture(source, ":example_help:\n\n:end\n"), 1)

    def test_exact_keys_preserve_case_and_trailing_spaces(self):
        self.assertEqual(self.check_fixture("Start =\n", "Start=啟動\n"), 1)
        self.assertEqual(self.check_fixture("Start=\n", "start=啟動\n"), 1)

    def test_plugin_values_and_help_are_read_separately(self):
        source = "Start=\n:example_help:\nUse mode=a.\n:end\n"
        translated = "Start=啟動\n:example_help:\n使用 mode=a。\n:end\n"
        self.assertEqual(self.check_fixture(source, translated), 0)

    def test_empty_reference_directory_is_not_a_success(self):
        with TemporaryDirectory() as directory, patch("sys.argv", ["check", directory]):
            with redirect_stdout(StringIO()):
                self.assertEqual(coverage.main(), 2)

    def test_help_preserves_executable_php_variables(self):
        source = ":vpn_help:\nPort <?=$netport['wg0']?>\n:end\n"
        translated = ":vpn_help:\n連接埠 <?=$netport['wg0']?>\n:end\n"
        self.assertEqual(self.check_fixture(source, translated), 0)
        # Losing the variable leaves a valid PHP array that renders as 'Array'.
        self.assertEqual(self.check_fixture(source, translated.replace("$netport", "")), 1)
        self.assertEqual(self.check_fixture(source, translated.replace("$netport", "$netpool")), 1)
        self.assertEqual(self.check_fixture(source, translated.replace("<?=$netport['wg0']?>", "")), 1)

    def test_translation_cannot_introduce_php_into_plain_help(self):
        source = ":vpn_help:\nUse your configured port.\n:end\n"
        translated = ":vpn_help:\n使用連接埠 <?=['wgX']?>\n:end\n"
        self.assertEqual(self.check_fixture(source, translated), 1)

    def test_usb_help_survives_real_package_and_both_loader_paths(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            for relative in ("translations.txt", "USB Manager/usb_manager.txt",
                             "USB Manager/usbmanagersettings.txt"):
                target = root / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text((build.ROOT / relative).read_text(encoding="utf-8"),
                                  encoding="utf-8")
            out = root / "dist" / "zh_TW.zip"
            with patch.object(build, "ROOT", root), patch.object(build, "OUT", out):
                with redirect_stdout(StringIO()):
                    build.main()
            with ZipFile(out) as archive:
                installed = {Path(name).name.lower(): archive.read(name).decode("utf-8")
                             for name in archive.namelist()}
            # USBDevices.page and its AJAX renderer call parse_plugin('usb_manager').
            _, device_help = coverage.parse_text_entries(installed["usb_manager.txt"])
            self.assertIn(":usbip_devices_switches_plug:", device_help)
            # USBManagerSettings does not call parse_plugin; URI loading is required.
            _, settings_help = coverage.parse_text_entries(installed["usbmanagersettings.txt"])
            self.assertIn(":usbmgr_HostCheck_freq_help:", settings_help)
            self.assertNotIn(":ud_settings_symlinks_plug:", device_help)

    def test_english_sentence_with_unicode_dash_is_detected(self):
        value = "New features, security patches, or bug fixes – keep your server up to date."
        issues = validation.check_localization_text("example.txt", 1, value)
        self.assertTrue(any("untranslated English" in issue for issue in issues))

    def test_unfilled_or_duplicate_plugin_help_is_rejected(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "plugin.txt").write_text(
                ":example_plug:\n>\n:end\n:example_plug:\n說明\n:end\n", encoding="utf-8")
            with patch.object(validation, "ROOT", root):
                issues, _, _ = validation.check_file("plugin.txt")
            self.assertTrue(any("duplicate" in issue for issue in issues))

    def test_empty_plugin_help_is_rejected(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "plugin.txt").write_text(":example_plug:\n>\n:end\n", encoding="utf-8")
            with patch.object(validation, "ROOT", root):
                issues, _, _ = validation.check_file("plugin.txt")
            self.assertTrue(any("empty translation block" in issue for issue in issues))

    def test_plugin_paths_use_portable_separators(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "Plugin").mkdir()
            (root / "Plugin" / "labels.txt").touch()
            self.assertEqual(set(coverage.translation_files(root)), {"Plugin/labels.txt"})

    def test_date_maps_match_unraid_parse_str_behavior(self):
        from urllib.parse import parse_qsl
        for name in ("Days_array", "Months_array"):
            value = " ".join(f"{key}:譯文" for key in validation.KEYWORD_MAP_KEYS[name])
            self.assertTrue(validation.valid_keyword_map(name, value))
            self.assertFalse(validation.valid_keyword_map(name, value.replace(" ", "")))
            decoded = dict(parse_qsl(value.replace(" ", "&").replace(":", "=")))
            self.assertEqual(set(decoded), set(validation.KEYWORD_MAP_KEYS[name]))

    def test_package_supports_main_embedded_ud_after_flattened_import(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "Unassigned Devices").mkdir()
            (root / "main.txt").write_text("Device=主頁裝置\n", encoding="utf-8")
            (root / "Unassigned Devices" / "unassigneddevices.txt").write_text(
                "Device=裝置\nMount=掛載\n:ud_plug:\n> 完整說明\n:end\n", encoding="utf-8")
            (root / "translations.txt").write_text(
                "prefix_SI=K M G T P E Z Y\nprefix_IEC=Ki Mi Gi Ti Pi Ei Zi Yi\n", encoding="utf-8")
            out = root / "dist" / "zh_TW.zip"
            with patch.object(build, "ROOT", root), patch.object(build, "OUT", out):
                with redirect_stdout(StringIO()):
                    build.main()
            with ZipFile(out) as archive:
                # Reproduce FileUpload.php basename/lowercase import.
                installed = {Path(name).name.lower(): archive.read(name).decode("utf-8")
                             for name in archive.namelist()}
            values, blocks = coverage.parse_text_entries(installed["main.txt"])
            self.assertEqual(values["Device"], "主頁裝置")
            self.assertEqual(values["Mount"], "掛載")
            self.assertIn("完整說明", blocks[":ud_plug:"])
            self.assertIn("Device=裝置", installed["unassigneddevices.txt"])

    def test_package_rejects_flattened_filename_collisions(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "Plugin").mkdir()
            (root / "labels.txt").write_text("A=甲\n", encoding="utf-8")
            (root / "Plugin" / "labels.txt").write_text("B=乙\n", encoding="utf-8")
            with patch.object(build, "ROOT", root), patch.object(build, "OUT", root / "dist" / "test.zip"):
                with self.assertRaisesRegex(RuntimeError, "basenames collide"):
                    build.main()


if __name__ == "__main__":
    unittest.main()
