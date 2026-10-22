# Unraid 繁體中文語言包深度稽核

最新完整比對與內容補譯結果請參閱 [2026-10-22 官方語系比對紀錄](UPSTREAM-COVERAGE.zh-TW.md)。以下為先前稽核紀錄。

## 稽核基準與範圍

- 基準：`unraid/lang-en_US` 的完整語言檔目錄（目前涵蓋 52 個 `.txt`，包含 `LICENSE.txt`；其中 51 個是語言查找檔）。
- 工具：`scripts/check_upstream_coverage.py` 比對英文來源與繁體中文的完整檔案路徑、大小寫敏感的鍵名，以及 `_help`、`_plug` 多行區塊；CI 使用固定版本來源。
- 內容：以繁體中文檔案為對象，另行查找與英文原文相同的譯文、過長的純英文文字、未翻譯的按鈕與提示，以及不合台灣慣用的字詞。
- 檢查範圍包含 `translations.txt`、`main.txt`、`settings.txt`、`dashboard.txt`、`docker.txt`、`vms.txt`、`shares.txt`、`tools.txt`、`Community Apps`、`Unassigned Devices`、`Parity Check Tuning`、`Tips and Tweaks`、`Dynamix` 與其他外掛翻譯；檢視 `helptext.txt` 等長篇說明的英文殘留。

## 本次修正類別

| 類別 | 代表英文原文 | 改進方向 |
|---|---|---|
| 危險提示與降級 | `Downgrades are only recommended...` | 完整台灣繁體中文，保留原本風險 |
| WAN IPv4 警告 | `Remark Unraids WAN IPv4 %1s...` | 翻譯整句並保留兩個替換參數 |
| 確認對話框 | `Are you sure you want to install...` | 補齊安裝 Docker 與外掛的完整中文 |
| 儀表板統計 | `Share count %s with...` | 翻譯共享數量及 SMB/NFS 欄位 |
| Docker／外掛安全 | Community Applications 權限說明 | 說明外掛具有系統層級權限 |
| 台灣用語 | 運行、打印字符、字段、插件 | 改用執行、可列印字元、欄位、外掛程式 |

## 必須留意的限制

- **字串覆蓋率不等於畫面覆蓋率：**第 3 方外掛新增或硬編碼的英文，可能未列在官方 `en_US` 檔案中。須以已安裝的 Unraid 7.3.3 與外掛版本實測。
- **技術名稱不應強制翻譯：**Docker、ZFS、Btrfs、SMB、NFS、S.M.A.R.T.、IP 等識別名稱可以維持英文。
- **不應修改原始英文鍵名：**翻譯檔的等號左側需與執行階段查找字串完全吻合；此處連大小寫、空格、拼字與標點都可能重要。
- **SI／IEC 單位格式已經修復並驗證：**持續保留 `prefix_SI=K M G T P E Z Y` 及 `prefix_IEC=Ki Mi Gi Ti Pi Ei Zi Yi`，不可改回無空白格式。

## 後續人工驗收

使用 GitHub Actions 中的實際 `zh_TW.zip`，逐頁確認 Main、Dashboard、Shares、Settings、Docker、VMs、Tools、Community Applications、Unassigned Devices 的按鈕、提示、表格欄位與說明。將仍顯示的英文文字及頁面／外掛版本記錄後，再依來源鍵名或未提供語言掛鉤的程式碼分別處理。
