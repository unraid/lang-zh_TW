# 更新語言包後的設定頁逐頁稽核

## 範圍

使用者確認已匯入上一版語言包後，於 Unraid 7.3.3 重新檢查「設定」的 **41 個入口**，並補查網路的其他介面／進階／規則／路由、Docker 與虛擬機器進階檢視、電源按鈕、Unraid API、Tailscale、Appdata 備份進階與還原，以及自動更新的 Docker 分頁。

逐頁展開全域「說明」，閱讀當前組態下可見的欄位與說明；有進階檢視或其他分頁者，另行查看。並以公開原始碼核對翻譯掛鉤、查找鍵正規化、動態 PHP 片段及語言檔載入方式。

本次未套用設定、停止服務、啟用 USB/IP、建立金鑰、傳送測試通知、執行備份／還原、重新掃描硬體，或啟動資料搬移。需變更服務或組態才能出現的條件式欄位，未冒稱完成實機驗收。檢查結束後回到設定總覽。

## 逐頁結果

「已校對」表示實機文字已檢查，相關修正寫入本機語言檔；**不表示本次修正已再次匯入伺服器**。硬編碼及獨立前端內容的中文對照見 [設定頁補充說明](SETTINGS-HELP.zh-TW.md)。

| 設定入口 | 路徑 | 檢查與處理 |
| --- | --- | --- |
| 開機參數 | `/Settings/BootParameters` | 補譯 IOMMU、VFIO、影格緩衝區、ACPI、PCIe、USB 省電及 NVMe 警告；介紹與部分選單內容需上游提供掛鉤。 |
| CPU 綁定 | `/Settings/CPUset` | 重寫虛擬機器／容器的停止、變更及重新啟動流程，保留隔離核心限制與等待更新警告。 |
| 日期和時間 | `/Settings/DateTime` | 校對 NTP 與時區說明，補日期格式字串；地區／鍵盤等系統清單仍可能保留原文。 |
| 磁碟設定 | `/Settings/DiskSettings` | 校對休眠、喚醒群組、逾時、NCQ、核心 I/O 排程器、條帶池與 SMART；補 ZFS ARC 選項。 |
| Docker | `/Settings/DockerSettings` | 檢查基本及進階說明；修正版本、appdata、日誌輪替及自訂網路說明。命令輸出保留原文。 |
| 識別資訊 | `/Settings/Identification` | 修正主機名稱允許字元、15 字元限制及 Windows／macOS 瀏覽說明。 |
| 管理介面存取 | `/Settings/ManagementAccess` | 檢查 SSL/TLS、SSH、TELNET、UPnP、憑證及網址說明；API 子分頁仍有獨立前端英文／簡體。 |
| 網路設定 | `/Settings/NetworkSettings` | 檢查三個實體介面、進階資訊、介面規則及路由表；重寫綁定模式、IPv4／IPv6、DNS、MTU 及 VLAN 說明。 |
| 電源選項 | `/Settings/PowerMode` | 檢查電源模式及電源按鈕分頁，補譯實體按鈕、關機及不執行動作選項。 |
| 全域共享設定 | `/Settings/ShareSettings` | 校對磁碟／使用者共享、包含排除、專用共享、硬式連結及直接 I/O；保留資料遺失警告。 |
| UPS 設定 | `/Settings/UPSsettings` | 校對 apcupsd、纜線與通訊方式、裝置格式及三個關機門檻；修正錯置句子與 `private` 技術值。 |
| USB 設定 | `/Settings/USBManagerSettings` | 檢查目前可見設定；依原始碼補譯 USB/IP 模組與遠端探索說明，未為檢查而啟用 USB/IP。 |
| 虛擬機器管理員 | `/Settings/VMSettings` | 檢查基本／進階；修正停用啟動選項的反向語意、VirtIO、儲存、關機及 libvirt 日誌文字。 |
| NFS | `/Settings/NFS` | 完整重寫 fuse_remember，包括 330 秒、0、-1 與每筆約 108 位元組的記憶體影響。 |
| SMB | `/Settings/SMB` | 校對工作群組、隱藏檔、macOS、NetBIOS、WSD 與額外設定。未切換至 Active Directory 模式。 |
| FTP 伺服器 | `/Settings/FTP` | 校對啟停、使用者清單、root 限制及讀寫刪除權限警告。 |
| 網路統計 | `/Settings/NetworkStats` | 介面清單與 vnStat 狀態仍有英文，提供中文對照。 |
| 對外代理伺服器管理 | `/Settings/OutgoingProxy` | 三組代理皆檢查，補上遺漏的密碼詳細說明區塊。 |
| 系統日誌伺服器 | `/Settings/SyslogSettings` | 修正 USB「寫入磨損」誤譯為「插拔」，校對本機／遠端接收與保存。 |
| Tailscale | `/Settings/Tailscale` | 查看主頁、設定、狀態、Lock 與資訊；簡體來自獨立前端詞庫，附功能對照。 |
| VPN 管理器 | `/Settings/VPNmanager` | 找到動態說明顯示 Array 的原因，還原遺失的 PHP 變數；未顯示或複製私密金鑰。 |
| 確認 | `/Settings/Confirmations` | 檢查重新啟動、關機、停止陣列與睡眠確認選項。 |
| 主控台設定 | `/Settings/Console` | 檢查鍵盤、螢幕逾時與 Bash 歷史說明，保留寫入及清除記錄警告。 |
| 顯示設定 | `/Settings/DisplaySettings` | 校對字型、WWN、版面、色彩及單位說明；改用分頁模式等台灣用詞。 |
| 通知設定 | `/Settings/Notifications` | 檢查一般、SMTP 及所有可見代理；校對分類及通知方式。代理 XML 的欄位／說明未呼叫翻譯函式，另附完整中文對照。 |
| 排程器 | `/Settings/Scheduler` | 移除同位元校驗修正說明中的通知摘要文字，修正「最後一天」及 Mover 頻率說明，檢查 TRIM。 |
| 備份／還原 Appdata | `/Settings/AB.Main` | 展開備份進階，查看還原限制；頁面多為硬編碼，附來源分類、停止容器、排除、指令碼及覆寫警告的中文說明。 |
| 應用程式自動更新 | `/Settings/AutoUpdateApps` | 檢查外掛／Docker 分頁；補第三方容器與致謝用語。星期選項已正常分列。 |
| 清理 Appdata | `/Settings/CleanUpAppdata` | 確認先前完整清除警告已顯示，補「未找到孤立資料夾」提示。未執行清理。 |
| Fix Common Problems | `/Settings/FixProblems` | 檢查掃描排程、通知、略過測試及權限排除項目，提供硬編碼內容的中文對照。 |
| 睡眠設定 | `/Settings/SleepSettings` | 逐項查看磁碟、網路、主機、登入、WOL、喚醒及除錯說明；部分星期清單為外掛原文。 |
| 統計設定 | `/Settings/StatSettings` | 檢查取樣、刻度、欄數、網路單位及時間視窗，現有完整說明可讀。 |
| 系統溫度 | `/Settings/TempSettings` | 檢查驅動程式及感測器說明，未按下偵測、載入或卸除。硬體感測器名稱保留原文。 |
| TurboWrite | `/Settings/Turbo` | 英文為外掛介面內容，附自動切換門檻、輪詢與強制排程的中文說明。 |
| USB 裝置 | `/Settings/USBDevices` | 新增 USB Manager 語言檔，補開關、裝置與完整說明；部分動態表格仍硬編碼。 |
| 未指派裝置 | `/Settings/UnassignedDevicesSettings` | 檢查共用、SMB、NFS、密碼、UUID、ZFS 與遠端測試說明；補 ZFS 磁碟區說明與拆分後的不可逆警告鍵。 |
| 使用者指令碼 | `/Settings/Userscripts` | 檢查排程選項與支援文字；附固定介面中文對照，未修改使用者指令碼。 |
| 社群應用程式 | `/Settings/ca_settings` | 補應用更新、精選停用、Cloudflare CDN 的精確查找鍵，校對已棄用／不相容說明。 |
| Compose | `/Settings/compose.manager.settings` | 標籤可翻譯，但詳細說明為硬編碼；附目錄不自動搬移及重新建立容器等中文警告。 |
| NVIDIA 驅動程式 | `/Settings/nvidia-driver` | 檢查更新通知及各驅動分支說明，附中文對照。NVIDIA-SMI 錯誤屬執行狀態，未變更驅動。 |
| unBALANCE | `/Settings/unbalance` | 檢查服務開關、連接埠與獨立網頁介面入口；未執行搬移。 |

## 重要修正

- 共修改 **45 個既有單行譯文**，新增 **82 個查找鍵**；修改 **153 個既有說明區塊**，新增 **11 個區塊**。此數字相對於上一筆提交 `0db3b92`，按各語言檔內的唯一鍵／區塊計算。
- 新增 `USB Manager/usb_manager.txt`，對應 `parse_plugin('usb_manager')`，以及裝置頁的 AJAX 載入。
- 新增 `USB Manager/usbmanagersettings.txt`，對應設定頁 URI；不將同名的 UD 相容路徑說明混入裝置頁字典。USB 外掛重複使用同一說明標記的欄位，採用對兩處均適用的說明。
- 依官方英文片段還原 `$nginx`、`$netpool`、`$netpool6` 及 `$netport`。移除其他通道說明中原文不存在的 PHP；不以硬寫固定連接埠掩蓋 Array 問題。
- 英文覆蓋檢查現在會比對每個鍵／說明區塊內嵌 PHP 的完整片段，拒絕遺失變數、替換變數或額外加入執行片段。

## 來源與載入限制

| 來源 | 核對版本與用途 |
| --- | --- |
| 官方英文語系 | `98e4e91e870663720f749c27035d69c31a680ce9`：完整鍵、說明區塊及 PHP 片段比對。 |
| [WebGUI](https://github.com/unraid/webgui/tree/26eb1b5c1d547ddbf44a38e63956ba24f659098b) | 核對 BootParameters、NotificationAgents、VMSettings、OutgoingProxy 與 Translations 的實際掛鉤。 |
| [Unassigned Devices](https://github.com/unraid/unassigned.devices/tree/7bdcd03cccb67320598e95a1cab38821182f633b/source/unassigned.devices/usr/local/emhttp/plugins/unassigned.devices) | 核對 ZFS 磁碟區區塊、遠端測試精確鍵，以及不可逆警告被拆成兩個查找字串的情況。 |
| [USB Manager](https://github.com/SimonFair/USB_Manager/tree/2874838c0697bc4ef3447c3a908a0368ec8bb47a/source) | 核對 URI／外掛字典載入及硬編碼表格。 |
| [Compose Manager](https://github.com/dcflachs/compose_plugin/blob/074a9af3a29d14b346e5dae8a700a0649cda601c/source/compose.manager/compose.manager.settings.page) | 確認詳細說明直接輸出，不支援語言包替換。 |
| [Appdata Backup](https://github.com/Commifreak/unraid-appdata.backup/blob/cf336627b85060d296e8dac8df738c7b798cbd2c/src/pages/content/settings.php) | 核對備份設定的硬編碼內容。 |

公開程式版本用於核對，不能據此推定伺服器所有外掛程式檔與上游完全一致。其餘外掛的硬編碼判斷以目前畫面與已存在查找鍵仍未生效的情形為依據，未將未核對的外掛程式宣稱為已完成原始碼修復。

## 驗證與待複驗

- 官方參照仍完整覆蓋：51/51 檔案、5,170/5,170 精確鍵、633/633 說明區塊，另含 USB Manager 的兩個擴充語言檔。
- 本機語言檔共 **53 個、5,677 筆單行翻譯，零空白值**。
- **15 項回歸測試通過**，新增 PHP 片段保留與 USB 兩種載入方式的實際封裝測試。
- 新版 `dist/zh_TW.zip` 包含 53 個語言檔；通過編碼、LF、SI／IEC、檔名衝突與封裝檢查。
- 本輪修正尚未重新匯入伺服器。下一次應優先複驗：開機參數詳細警告、VPN 連接埠／網段、停用 VM 啟動選項、UPS 裝置格式、代理密碼說明、校驗修正說明、UD ZFS 警告及 USB 開關／說明。
- 獨立前端的 `zh_CN` 選擇限制、通知代理 XML 及外掛硬編碼仍需相關上游支援。新增對照文件不等於已修復遠端畫面。
