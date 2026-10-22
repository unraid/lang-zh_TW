# Unraid 繁體中文（台灣）在地化指南

本語言包以 **台灣常用語彙、技術語意正確、跨頁面一致** 為原則。英文翻譯鍵名是 Unraid 的查找識別字，**不得修改等號左邊**。

## 核心術語

| English | 建議譯法 | 注意事項 |
| --- | --- | --- |
| Disk / Hard drive | 磁碟／硬碟 | 不用「磁盤、硬盤」 |
| Device | 裝置 | 依上下文可用「儲存裝置」 |
| Array | 陣列 | 指 Unraid 主陣列 |
| Pool | 儲存池 | **不可**一律譯成「快取池」；只有 Cache Pool 才稱快取池 |
| Parity disk / Drive | **校驗磁碟** | 專用來存放 Parity 資料的陣列磁碟 |
| Parity | 同位元校驗 | 泛指保護機制或校驗資料，視語境也可用「校驗」 |
| Parity Check | **同位元校驗檢查** | 重新計算並比對校驗資料，不等於同步重建 |
| Parity Sync | **校驗同步** | 重新計算並寫入校驗磁碟 |
| Parity-Swap | 校驗磁碟交換（Parity-Swap） | 特殊的校驗磁碟升級／故障資料磁碟替換流程 |
| Dual Parity | 雙校驗磁碟 | 指派兩顆校驗磁碟 |
| Data-Rebuild | 資料重建 | 與格式化或清除磁碟不同 |
| Disk-Clear | 磁碟清除 | 相關警告必須精確 |
| Cache | 快取 | 不等同一般儲存池 |
| Share / User Share | 共享資料夾 | 短標籤可使用「共享」 |
| Primary / Secondary storage | 主要／次要儲存位置 | Share 儲存政策 |
| Mover | Mover | 保留功能名稱，說明檔案移動方向 |
| Plugin | 外掛程式 | 不用「插件」 |
| Custom / Refresh | 自訂／重新整理 | 不用「自定義、刷新」 |
| Character / Byte | 字元／位元組 | 不用「字符、字節」 |
| Read-only | 唯讀 | 不用「只讀」 |
| Bus / Sound card | 匯流排／音效卡 | 不用「總線、聲卡」 |
| Certificate / Authentication | 憑證／身分驗證 | 注意憑證到期前與到期後的差異 |
| File / Folder | 檔案／資料夾 | 不用「文件、文件夾」 |
| Network / Port | 網路／連接埠 | 不用「網絡、端口」 |
| Default / Settings | 預設／設定 | 不用「默認、設置」 |
| Memory / Cache | 記憶體／快取 | 記憶體和快取不可混譯 |
| Flash boot device | USB 開機裝置 | 指 Unraid 開機媒體 |
| VM / Container | 虛擬機器／容器 | 保留 Docker、QEMU、KVM 專有名詞 |
| Snapshot / Scrub | 快照／資料校驗（Scrub） | Scrub 驗證 ZFS／Btrfs 資料與檢查碼，不是主陣列的 Parity Check |
| Log / Syslog | 日誌／系統日誌 | 必要時保留命令名稱 |
| Sign in / Sign out | 登入／登出 | 不用「登錄、註銷」 |
| Apply / Save | 套用／儲存 | 操作行為不同，不應混譯 |


## Parity（校驗）命名原則

- 在 **Main** 或 **Dashboard** 看到實體裝置時，使用「**校驗磁碟**」，避免稱作「同位元檢查磁碟」。
- 描述 **Parity Check** 的檢查操作，使用「**同位元校驗檢查**」，不是「資料重建」。
- 描述 **Parity Sync** 的重算與寫入操作，使用「**校驗同步**」。
- 在技術說明首次提到 Parity 時可寫「**同位元校驗（Parity）**」，其後採用短稱「校驗資料」或「校驗保護」。
- Parity 保護與檔案系統 **Scrub（資料校驗）** 是不同機制；兩者都不等同備份。

## 翻譯格式與保留項目

- 僅修改 `KEY=translation` 等號右邊，保留英文鍵名大小寫及空白。
- 保留 `%s`、`%d`、`%1$s`、`%2$s` 等佔位符，以及 HTML 屬性和網址。
- Docker、ZFS、Btrfs、NFSv4、Tailscale、TCP、IPv6、PCIe、VFIO、`raidz` 等為技術識別字。
- `/boot/config`、`syslog`、`vfio-pci`、`docker.img` 等路徑與命令不要翻譯。
- `:something_help:`／`:something_plug:` 必須與 `:end` 成對保留。
- SI／IEC 容量前綴必須以**空白分隔**：`prefix_SI=K M G T P E Z Y`、`prefix_IEC=Ki Mi Gi Ti Pi Ei Zi Yi`。
- 所有鍵都必須明確填入譯文；技術常數與產品名稱可明確填入原文，不再保留空白值。

## 高風險操作的翻譯規則

- **Format / Erase / Wipe：** 必須明確區分「格式化」、「清除」、「覆寫」，並清楚保留資料遺失警告。
- **Btrfs Scrub（資料校驗）：** 驗證資料及中繼資料檢查碼；只有具備正確備援副本才可能自動修復，**不是**清除或格式化。
- **Btrfs Check：** `--readonly` 是非修改式檢查；`--repair` 具有風險，應遵守 [Btrfs 官方警告](https://btrfs.readthedocs.io/en/latest/btrfs-check.html)，不可翻成一般的「按下即可修復」。
- **ZFS Scrub：** 與主陣列 Parity Check 不同，不可一律翻譯成「同位元校驗檢查」。
- **SSL/TLS、DNS：** 保留安全風險與憑證錯誤提示，不建議直接忽略憑證警告或全面停用 DNS 重新繫結保護。
- **路徑格式：** Linux 檔案路徑使用正斜線（`/`），不是反斜線（`\`）。複製程式碼、路徑與命令時須保留原樣。
- **appdata / system / domains：** 容器與虛擬機器的服務資料位置不可與一般共享資料搬移政策混為一談，Mover 也不能當作備份。

## 提交前檢查

1. 依功能判斷語意，不要只進行簡繁轉換或全域字串取代。
2. 保留 Markdown、HTML、變數及格式佔位符。
3. 執行 `python3 scripts/validate_translations.py`。
4. 在 Unraid WebGUI 實際測試 Main、Dashboard、Shares、Settings、Docker、VMs、Tools 的標籤、容量單位、警告及排版。
5. 格式化、磁碟清除、權限與金鑰更換等高風險文字應優先人工審閱，再合併 Pull Request。
