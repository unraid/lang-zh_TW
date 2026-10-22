# 2026-10-22 官方英文語系比對紀錄

此頁記錄初次來源比對；後續實機發現、修正與目前驗證結果請參閱 [實機介面稽核](RUNTIME-AUDIT.zh-TW.md)。

## 來源與索引

- 英文來源：[unraid/lang-en_US](https://github.com/unraid/lang-en_US)，比對提交 [`98e4e91e870663720f749c27035d69c31a680ce9`](https://github.com/unraid/lang-en_US/commit/98e4e91e870663720f749c27035d69c31a680ce9)；本次直接取得官方儲存庫的預設分支。
- 本機專案先執行 codebase-memory 的 `full` 索引。程式結構涵蓋驗證、覆蓋比對、封裝腳本及 CI。
- 索引工具不會將 `.txt` 語言檔解析為程式符號；因此另直接逐檔讀取全部 51 個語言檔，比對精確鍵名、區塊、空白值及格式。`.git` 不在內容稽核範圍。
- `LICENSE.txt` 是授權條款，不屬於語言查找檔，維持原文。

## 發現與修正

原本已具備全部上游鍵與區塊，缺失主要存在於譯文及說明內容：

- 填入原先 40 個留白值。介面文字如接收、傳送改用中文；Docker、Tailscale、RAID、通訊協定與單位等技術名稱明確保留原文。
- 修正 427 個不重複鍵的譯文，調整 188 個說明區塊；包含用語修訂與內容補回，並非全部都是原先未翻譯。
- 補回校驗調校的分段範例、手動與自動檢查差異、停止陣列後的續行條件、溫度差值計算、日誌等級及局部檢查限制。
- 補回預清除的各種操作、NFS 公用與專用預設規則、CPU 調節器選項與命令、髒頁回寫參數的預設值及 UPS 條件。
- 補回 Docker 容器命名限制、儲存庫格式、通知摘要、Time Machine 的 macOS Ventura 13.6 條件，以及 SSL/TLS 模式、憑證更新時程與金鑰檔案限制。
- 移除一個錯置的重複 `:smb_security_help:` 區塊。原區塊內容是 Mover 說明；正確的 SMB 區塊保留，Mover 的服務停用條件回歸快取政策說明。
- 修正 `Capabilities` 誤譯為容量、憑證續期時間誤譯為到期後、Scrub 誤譯為清理、VNC 顯示驅動誤譯為影片驅動等語意問題。
- 統一外掛程式、執行、自訂、重新整理、位址、字元、位元組、唯讀、作業系統、匯流排等台灣用語。
- 新增 `.gitattributes`，固定語言檔使用 LF；修正 Windows 路徑分隔符號造成驗證規則未套用至外掛檔的問題。
- 補強空白值、空白與重複說明區塊、Unicode 標點英文句子的檢查；封裝後再次檢查 ZIP 內每個檔案的 UTF-8、BOM 與換行格式。

## 檢查結果

- 上游：51/51 個語言檔、5,170/5,170 個精確鍵、633/633 個不重複說明區塊。
- 本機：5,326 筆單行翻譯（含重複項目及額外相容鍵），0 個留白值。
- 結構、佔位符、台灣用語、UTF-8/LF、SI/IEC 前綴檢查通過。
- 9 項驗證器回歸測試通過；CI 已納入執行。
- 已產生 `dist/zh_TW.zip`，內含 51 個語言檔與原本的外掛目錄結構。

| 語言檔 | 上游精確鍵覆蓋 | 上游說明區塊覆蓋 | 空白值 |
| --- | ---: | ---: | ---: |
| `CA Auto Update/autoupdateapps.txt` | 19/19 | 0/0 | 0 |
| `CA Config File Edit/configedit.txt` | 11/11 | 0/0 | 0 |
| `Cleanup Appdata/cleanupappdata.txt` | 18/18 | 0/0 | 0 |
| `Community Apps/apps.txt` | 380/380 | 0/0 | 0 |
| `Community Apps/ca_settings.txt` | 25/25 | 0/0 | 0 |
| `Community Apps/javascript.ca.txt` | 14/14 | 0/0 | 0 |
| `Disable Security Mitigations/disablesecurity.txt` | 11/11 | 0/0 | 0 |
| `Dynamix Active Streams/activestreams.txt` | 9/9 | 1/1 | 0 |
| `Dynamix Auto Fan/fansettings.txt` | 10/10 | 0/0 | 0 |
| `Dynamix Cache Dirs/foldercachingsettings.txt` | 25/25 | 19/19 | 0 |
| `Dynamix Date Time/datetime.txt` | 7/7 | 8/8 | 0 |
| `Dynamix Day Night/daynightsettings.txt` | 21/21 | 1/1 | 0 |
| `Dynamix File Integrity/fileintegrity.txt` | 50/50 | 13/13 | 0 |
| `Dynamix File Integrity/integrity.txt` | 5/5 | 0/0 | 0 |
| `Dynamix Local Master/smb.txt` | 6/6 | 4/4 | 0 |
| `Dynamix S3 Sleep/sleepsettings.txt` | 37/37 | 18/18 | 0 |
| `Dynamix SSD Trim/scheduler.txt` | 20/20 | 4/4 | 0 |
| `Dynamix System Info/systemprofiler.txt` | 5/5 | 0/0 | 0 |
| `Dynamix System Stats/stats.txt` | 33/33 | 0/0 | 0 |
| `Dynamix System Stats/statsettings.txt` | 39/39 | 9/9 | 0 |
| `Dynamix System Temp/tempsettings.txt` | 14/14 | 5/5 | 0 |
| `Enhanced Log/enhancedsyslog.txt` | 4/4 | 0/0 | 0 |
| `Enhanced Log/enhancedsyslogsettings.txt` | 33/33 | 29/29 | 0 |
| `File Activity/fileactivity.txt` | 10/10 | 5/5 | 0 |
| `Gui Search/javascript.guiSearch.txt` | 1/1 | 0/0 | 0 |
| `Hotplug USB/libvirthotplugusb.txt` | 16/16 | 1/1 | 0 |
| `Open Files/openfiles.txt` | 15/15 | 1/1 | 0 |
| `Parity Check Tuning/paritychecktuning.txt` | 175/175 | 25/25 | 0 |
| `Recycle Bin/recyclebin.txt` | 40/40 | 15/15 | 0 |
| `Tips and Tweaks/tipsandtweaks.txt` | 79/79 | 24/24 | 0 |
| `Unassigned Devices Preclear/javascript.preclear.txt` | 22/22 | 0/0 | 0 |
| `Unassigned Devices Preclear/preclear.txt` | 52/52 | 1/1 | 0 |
| `Unassigned Devices/editdevicesettings.txt` | 48/48 | 9/9 | 0 |
| `Unassigned Devices/fsck.txt` | 10/10 | 0/0 | 0 |
| `Unassigned Devices/scriptlog.txt` | 1/1 | 0/0 | 0 |
| `Unassigned Devices/unassigneddevices.txt` | 171/171 | 2/2 | 0 |
| `Unassigned Devices/unassigneddevicessettings.txt` | 55/55 | 21/21 | 0 |
| `dashboard.txt` | 200/200 | 0/0 | 0 |
| `docker.txt` | 159/159 | 0/0 | 0 |
| `helptext.txt` | 0/0 | 398/398 | 0 |
| `javascript.txt` | 69/69 | 0/0 | 0 |
| `main.txt` | 416/416 | 0/0 | 0 |
| `outgoingproxy.txt` | 9/9 | 4/4 | 0 |
| `plugins.txt` | 43/43 | 0/0 | 0 |
| `scripts.txt` | 5/5 | 0/0 | 0 |
| `settings.txt` | 991/991 | 0/0 | 0 |
| `shares.txt` | 93/93 | 0/0 | 0 |
| `tools.txt` | 196/196 | 16/16 | 0 |
| `translations.txt` | 1169/1169 | 0/0 | 0 |
| `users.txt` | 27/27 | 0/0 | 0 |
| `vms.txt` | 302/302 | 0/0 | 0 |

## 重現檢查

```sh
python -m unittest discover -s scripts -p 'test_*.py'
python scripts/validate_translations.py
python scripts/check_upstream_coverage.py /path/to/lang-en_US
python scripts/build_language_zip.py
```

## 驗收界線

此紀錄證明與上述英文提交的語言來源對齊，並記錄翻譯內容修訂；不代表已在 Unraid 伺服器逐頁實測。專案未提供可執行的 Unraid WebGUI，因此仍須匯入語言包確認畫面、排版與執行階段替換結果。未經語言機制處理的硬編碼字串，以及英文語言庫尚未收錄的新功能，仍須由上游介面或外掛提供翻譯掛鉤。
