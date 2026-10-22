# 設定頁補充說明（台灣繁體中文）

本文件對照 Unraid 7.3.3 實際設定頁，補譯目前未提供翻譯掛鉤的說明。**本文件不會自動改變管理介面的文字。**可由語言包載入的內容已修正於對應 `.txt`；本文件保留硬編碼內容的中文對照，供操作時閱讀及外掛作者後續採用。

檢查方式與逐頁結果見 [設定頁稽核](SETTINGS-AUDIT.zh-TW.md)。以下均為功能說明，並未代為變更設定、執行測試通知、備份、還原或重啟服務。

## 開機參數：未提供翻譯掛鉤的介紹

核心開機參數可控制硬體初始化、PCIe 直通、GPU 影格緩衝區、電源管理及開機選單。「選單檢視」提供開關與說明，引導您調整設定；「原始檢視」則可直接編輯開機載入程式設定。此功能會自動備份並驗證變更。

虛擬機器直通區的選項用來處理硬體限制：PCIe ACS Override 可拆分原本無法個別直通的裝置群組；允許 VFIO 不安全中斷，則讓不支援中斷重新對應的硬體也能嘗試直通。**這些選項會降低硬體隔離能力；使用不受信任的虛擬機器或敏感硬體時，必須謹慎評估。**

開機項目的 `Toggle = Apply parameters to entry` 表示「啟用開關，即將參數套用至該開機項目」。此查找字串包含等號，與語言檔的 `鍵=值` 格式衝突，需要上游調整鍵名。

## 通知代理

通知代理從 XML 讀取欄位與說明；受測版本直接輸出這些內容，沒有經過翻譯函式。一般通知、SMTP 及通知分類的翻譯仍由語言包提供。

### 共用欄位

| 原文 | 台灣繁體中文與用途 |
| --- | --- |
| Notification title | 通知標題：選擇標題要包含的欄位。 |
| Notification message | 通知內文：選擇訊息本文要包含的欄位。 |
| Event / Subject / Timestamp | 事件／主旨／時間戳記。 |
| Description / Importance / Content / Link | 說明／重要性／內容／連結。 |
| Access token / App token / User key / Api key | 存取權杖／應用程式權杖／使用者金鑰／API 金鑰；請使用對應服務提供的值。 |
| Full server base url | 完整伺服器基底網址，須包含通訊協定及連接埠，例如 `https://example.com:8888/`。 |
| Application name | 應用程式名稱，例如 Unraid Server。 |
| Webhook url | Webhook 網址，由對應服務的整合設定取得。 |

### 各服務的詳細說明

| 服務 | 功能說明 |
| --- | --- |
| Bark | 在 Bark 應用程式取得推播網址（Pushurl）。Group 為選填的訊息群組；Sound 為選填的提示音名稱，請從 Bark 複製。兩者都可填入 `none` 以停用。 |
| Boxcar | 依服務說明取得存取權杖，並選擇通知標題與內文的組成欄位。 |
| Discord | 在自己的 Discord 伺服器建立通知頻道，再依服務說明取得 Webhook 網址。同一 Webhook 可供多台 Unraid 使用。Server icon 可指定代表此伺服器的 HTTPS 圖示網址，填入 `none` 可停用。Discord tag id 須填入數字形式的個人 Discord ID；依原始說明，可將頻道通知設為「僅限 @提及」，讓警報優先等級的通知提及指定使用者。此欄位也可填入 `none` 停用。 |
| Gotify | 輸入含通訊協定及連接埠的伺服器基底網址，以及該應用程式的權杖，再選擇標題與內文欄位。 |
| Join | 從服務提供的連結取得 API 金鑰，再選擇標題與內文欄位。 |
| ntfy.sh | 輸入伺服器基底網址（例如 `https://ntfy.sh`）、權杖及主題（Topic）。 |
| Prowl | 依服務說明取得 API 金鑰；Application name 用來識別傳送通知的應用程式。 |
| PushBits | 輸入伺服器基底網址（例如 `https://example.com:8080/`）與應用程式權杖。 |
| Pushbullet | 取得存取權杖後，選擇通知標題與內文欄位。 |
| Pushover | 分別填入使用者金鑰及應用程式權杖，再選擇通知內文欄位。 |
| Pushplus | 填入推播權杖。Specific group code 為選填的群組代碼／API 文件中的 `topic`，可將訊息傳給多人；填 `none` 停用。Specific channel 指定管道，預設為 `wechat`。當管道為 `webhook` 或 `cp` 時，可指定 Webhook；填 `none` 停用。Callback url 是每次推播完成後，Pushplus 會以 POST 回報結果的網址；填 `none` 停用。 |
| ServerChan | 填入 SendKey。Specific channel 可指定一個或多個管道，例如 `9` 或 `9\|66`；Specific openid 可指定 OpenID／UID，例如 `openid1,openid2` 或 `UID1\|UID2`。不使用時可填 `none`。 |
| Slack | 依服務說明取得 Webhook，設定應用程式名稱，並選擇通知標題與內文欄位。 |
| Telegram | 使用 BotFather 建立機器人，將機器人權杖貼入 Bot access token。透過私訊或群組傳送訊息給機器人，再執行通知測試。若要重設接收通知的使用者／群組，原始說明要求移除 `/boot/config/plugins/dynamix/telegram/chatid` 後重新完成傳送訊息與測試兩步；本次檢查未執行刪除或測試。 |

## Appdata Backup：備份與還原

### 備份方式與來源判斷

此外掛可備份與還原容器的 appdata，並在備份過程處理容器停止／啟動，以及選用的更新作業。

它會直接讀取各 Docker 容器設定中的磁碟區對應，而非單純複製整個 appdata 資料夾。位於 **Appdata source(s)** 指定路徑內的對應，視為「內部磁碟區」，通常存放設定、日誌等應用程式資料；其他對應視為「外部磁碟區」，可能是媒體、下載或其他儲存資料。

預設備份內部磁碟區，略過外部磁碟區；可在個別容器設定調整。**新加入、尚未個別設定的容器會套用預設值。**

| 原文欄位 | 中文與詳細說明 |
| --- | --- |
| Backup type | 備份方式：先停止全部容器、備份後再啟動；或逐一停止、備份並啟動各容器。原本就未執行的容器，備份完成後仍保持停止。 |
| Delete backups if older than x days | 清理超過指定天數的備份。 |
| Keep at least this many backups | 至少保留指定份數的備份。設定清理天數時，也要一併確認這項保留條件。 |
| Appdata source(s) | Appdata 來源路徑，可指定多個。常見路徑為 `/mnt/user/appdata` 或 `/mnt/cache/appdata`；其他自訂路徑也必須列入。來源路徑內的磁碟區對應會被歸類為內部資料，不能只依欄位名稱猜測涵蓋範圍。 |
| Backup destination | 備份目的地。請確認可用空間及備份保存位置。 |
| Use Compression? | 是否壓縮：一般模式使用 gzip，多核心模式使用 zstdmt。多核心壓縮可能影響其他系統服務效能。 |
| How many cores should be used? | 選擇壓縮可使用的 CPU 核心數，或使用所有核心。 |
| Backup the flash drive? | 在備份中加入 USB 開機裝置的壓縮副本。 |
| Copy the flash backup to a custom destination | 另外將開機裝置備份複製到自訂目的地；此欄位為選填。 |
| Backup VM meta? | 備份虛擬機器中繼資料，保存 `/etc/libvirt/qemu`。此項不等同於備份虛擬磁碟。 |

### 進階設定

以下是所有容器的全域預設值，也可在個別容器調整。

| 原文 | 中文與影響 |
| --- | --- |
| Skip stopping of containers? | 略過停止容器：讓容器在備份時繼續執行。**可能造成備份內容不一致或損壞。** |
| Verify Backup? | 驗證備份：tar 本身會偵測備份時的錯誤，此選項再增加一層驗證。 |
| Ignore errors during backup? | 忽略備份錯誤：**可能留下損壞的備份，只有在了解影響時才應啟用。** |
| Enable --ignore-case for tar? | 讓 tar 比對排除規則時忽略大小寫。 |

### 通知與排程

Notification Settings 可選擇僅通知錯誤、通知警告與錯誤，或停用通知；Create success notification 可另行開啟成功通知；Send notification if containers were updated 可在容器更新後通知。

Scheduled Backup Frequency 可設為停用、每日、每週、每月或自訂；星期、日期、小時、分鐘及 Custom Cron Entry 共同決定執行時間。

### 個別容器

| 原文 | 中文與用途 |
| --- | --- |
| Skip? | 是否略過此容器的備份。 |
| Configured volumes — Click to exclude | 依容器設定列出磁碟區對應；點選項目可將其排除。請辨認內部與外部磁碟區。 |
| No volumes — container will NOT being backed up! | 沒有可備份的磁碟區，此容器將不會備份。 |
| Member of group | 所屬群組；可輸入名稱建立群組，其他行為請參閱外掛 Hints。 |
| Save external volumes? | 是否備份此外掛判定的外部磁碟區。 |
| Update container after backup? | 備份後是否更新容器；可沿用全域設定，或個別指定是／否。 |
| Excluded folders/files | 排除的檔案或資料夾，每行一個路徑或樣式。 |
| Start order | 容器啟動順序；停止時使用相反順序。 |

### 自訂指令碼與排除規則

指令碼必須放在 `/boot` 以外的位置，因為開機裝置的 FAT32 檔案系統不支援直接從該處執行指令碼。成功時應回傳結束碼 0；容器備份前的指令碼可回傳 2，要求略過該容器的備份。

| 階段 | 執行時機與傳入參數 |
| --- | --- |
| Pre-run | 所有工作開始前；`pre-run`、目的地路徑。 |
| Pre-backup | 開始備份前；`pre-backup`、目的地路徑。 |
| Pre-container-backup | 建立每個容器的 tar 封存檔之前；`pre-container`、容器名稱。回傳 2 可略過該容器備份。 |
| Post-container-backup | 建立每個容器的 tar 封存檔之後；`post-container`、容器名稱。 |
| Post-backup | 備份完成、容器重新啟動之前；`post-backup`、目的地路徑。 |
| Post-run | 所有工作完成後；`post-run`、目的地路徑、成功狀態（`true`／`false`）。 |

Include extra files/folders 可額外納入檔案及資料夾，這些項目會封裝至 `extra_files.tar.gz`。Global exclusion list 是全域排除清單，每行一項，可使用部分路徑與萬用字元，例如 `*.png`、`music/*.m4a` 或 `logs`；符合規則的檔案／資料夾不會備份。

### 還原限制

還原頁可還原容器資料、容器範本 XML、額外檔案及備份設定。**它不會自動建立 Docker 容器，也不會替您停止受影響的容器。還原前必須自行停止相關容器。**

Backup source 指向備份來源。預設會還原至備份時的原始位置；不存在的目的地會建立，**既有資料可能被覆寫**。若指定自訂目的地，封存檔會解壓縮至該處；此覆寫目的地的選項僅適用於封存檔。

## Compose Manager

| 原文功能 | 中文詳細說明 |
| --- | --- |
| Compose Project Directory | 選擇存放 Compose 專案／堆疊的資料夾。**變更路徑不會自動搬移既有專案資料夾。** |
| Compose Command Progress Display | 選擇命令輸出的顯示方式。「基本」顯示一般純文字；「終端機」使用 ttyd 視窗，支援彩色文字。 |
| Debug Logging | 啟用除錯日誌。 |
| Recreate During Autostart | 自動啟動堆疊時加入 `--force-recreate`，重新建立各容器。可改善容器原本連接的網路已不存在，導致無法自動啟動的問題。 |
| Show Compose in Header Menu | 將 Compose Manager 放到 Unraid 頁首的獨立分頁。 |

## USB Manager：仍硬編碼的裝置表格

裝置頁的切換開關與整段說明可經語言包翻譯。部分動態表格仍直接輸出英文，對照如下：

| 原文 | 中文 |
| --- | --- |
| Setting / Speed | 設定／速度 |
| Device Mapping / No Mappings | 裝置對應／尚無對應。 |
| Not Allowed | 不允許操作。 |
| INUSE UNRAID / UNRAID FLASH | Unraid 使用中／USB 開機裝置。 |
| Auto Connect Start/Resume VM at plugin | 外掛啟動時，自動連接並啟動或繼續虛擬機器。 |
| Auto Connect on VM Start | 虛擬機器啟動時自動連接。 |
| Connect as Serial | 以序列裝置連接。 |
| Disconnected | 未連接。 |

USB/IP 在受測環境中為停用，未為了查看條件式欄位而啟用。語言包依原始碼補譯遠端探索／檢查及模組載入說明，仍需在具備相應功能的環境驗證。

## 自動 TurboWrite

此外掛依目前停止旋轉的資料磁碟數量，切換一般寫入（讀取／修改／寫入）與 TurboWrite（重建寫入）。部分硬體配置使用重建寫入反而可能比較慢。

| 原文功能 | 中文詳細說明 |
| --- | --- |
| Current Status / Data Drives Spun Down | 目前狀態／上次輪詢時停止旋轉的資料磁碟數量。 |
| Script Not Running | 指令碼未執行。 |
| Enable Automatic Turbo Mode | 啟用或停用自動切換。 |
| Disks Allowed To Be Spun Down Before Invoking Turbo Mode | 停止旋轉的資料磁碟數量若超過此值，使用一般寫入；未超過時使用重建寫入。 |
| Polling Time In Seconds | 檢查磁碟旋轉狀態的間隔，單位為秒。 |
| Additional Debugging Logging | 記錄額外除錯資訊。 |

每個排程可選擇啟用狀態、強制啟用或停用 TurboWrite、Cron 執行時間與持續分鐘數。強制設定期間會暫停自動切換；到期後，若原本已啟用自動切換，便會恢復。No Schedules Defined 表示尚未建立排程。

## Fix Common Problems

列出的錯誤／警告來自上一次排程掃描；Rescan 是重新掃描，以更新目前結果。部分問題具有 Acknowledge（確認）按鈕，按下後會略過該項特定問題，直到下次重新開機。

| 原文功能 | 中文與用途 |
| --- | --- |
| Frequency to run background checks | 背景檢查頻率：停用、每小時、每日、每週或每月。 |
| Send notifications on errors? | 通知條件：停用、所有錯誤與警告，或僅錯誤。 |
| Avoid spinning up disks for tests? | 選擇一律測試（建議），或略過會喚醒休眠磁碟的測試。 |
| Number of allowed invalid logins per day | 每日允許的無效登入次數。 |
| Log Ignored Errors/Warnings? | 是否將已忽略的錯誤／警告寫入日誌，建議啟用。 |
| Check if Docker containers have updates? | 是否檢查 Docker 容器更新，預設為是。 |
| Permission Fix Excluded On | 權限修正的排除項目；Docker appdata 與 CA 備份目的地會自動排除。 |

錯誤／警告本身的協助可至 Unraid 一般支援區提出問題；外掛功能、誤報及新增檢查需求則使用外掛支援討論串。本次未啟動掃描、確認問題或執行權限修正。

## 網路統計與使用者指令碼

網路統計的 Interfaces to capture 是「要收集統計的網路介面」；Aliases 是「介面別名」；VNSTAT Daemon: Running 是「vnStat 背景服務：執行中」。介面名稱本身是系統識別碼，保留原文。

使用者指令碼的排程選項依序為：停用排程、每小時、每日、每週、每月、陣列啟動時、陣列停止時、僅第一次啟動陣列時，以及自訂。No description 是「尚無說明」，What Is Cron 是「什麼是 Cron」。使用者自行撰寫的指令碼名稱及內容不屬於固定介面翻譯。

## NVIDIA 驅動程式

Driver Update Notification（驅動程式更新通知）會每天在上午 8 點至 10 點間檢查所選分支；若有新版本，便下載驅動程式並通知。**安裝新驅動程式仍需重新啟動伺服器。**

若選擇 latest、Production Branch 或 New Feature Branch，應啟用更新通知以自動下載，或在通知停用時手動使用 Update & Download（更新並下載）。

| 分支 | 原始說明的中文對照 |
| --- | --- |
| latest | 不論分支，一律下載目前最新可用版本。 |
| Production Branch | 產品正式分支，生命週期較長，提供專業應用程式認證、穩定性與效能改善，以及定期安全性更新；舊稱 Optimal Driver for Enterprise（ODE）。 |
| New Feature Branch | 新功能分支，生命週期較短，通常每個分支僅有 1–2 次發行，用來在正式分支之間提供新功能、作業系統及硬體支援；舊稱 Quadro New Feature（QNF）。 |
| Open Source Driver | 使用開放原始碼核心模組，搭配 NVIDIA 專有驅動程式套件中的函式庫與執行檔。此受測外掛說明限定 Turing 或更新架構的 GPU。 |

受測頁面的 NVIDIA-SMI 訊息表示「無法與 NVIDIA 驅動程式通訊，請確認驅動程式已安裝且正在執行」。這是命令輸出及執行狀態，不是語言包的翻譯失效；本次未更新或重載驅動程式。

## unBALANCE、Tailscale 與 Unraid API

unBALANCE 設定頁的 Open Web UI 是「開啟網頁管理介面」；Enable unBALANCE Server 是「啟用 unBALANCE 服務」；Port 是「連接埠」。未進入其獨立應用程式執行磁碟搬移。

Tailscale 的 Accept routes、Accept DNS、Run as exit node、Use exit node、Allow LAN access 與 Tailnet Lock，可分別譯為「接受路由、接受 DNS 設定、作為出口節點、使用出口節點、允許區域網路存取、Tailnet 鎖定」。Taildrop location 是「Taildrop 接收位置」，Funnel 是產品功能名稱，保留原文。其設定、狀態與鎖定頁使用獨立前端詞庫，受測環境仍顯示簡體或英文。

Unraid API 的 Service Status、Refresh Status、Restart API、Developer Sandbox、Allowed OIDC Redirect Origins、OIDC Providers、Authorization Rules、Effective Permissions，可分別譯為「服務狀態、重新整理狀態、重新啟動 API、開發者沙箱、允許的 OIDC 重新導向來源、OIDC 提供者、授權規則、有效權限」。授權規則中的允許電子郵件網域、指定電子郵件地址、允許的使用者 ID 及遠端存取，均為實際存取控制設定；本次只檢查文字，未變更權限。

## 來源

- [WebGUI 開機參數](https://github.com/unraid/webgui/blob/26eb1b5c1d547ddbf44a38e63956ba24f659098b/emhttp/plugins/dynamix/BootParameters.page)。
- [通知代理輸出程式](https://github.com/unraid/webgui/blob/26eb1b5c1d547ddbf44a38e63956ba24f659098b/emhttp/plugins/dynamix/NotificationAgents.page)及同版本 `agents/*.xml`。
- [Appdata Backup 設定原始碼](https://github.com/Commifreak/unraid-appdata.backup/blob/cf336627b85060d296e8dac8df738c7b798cbd2c/src/pages/content/settings.php)。
- [Compose Manager 設定](https://github.com/dcflachs/compose_plugin/blob/074a9af3a29d14b346e5dae8a700a0649cda601c/source/compose.manager/compose.manager.settings.page)。
- [USB Manager 裝置頁](https://github.com/SimonFair/USB_Manager/blob/2874838c0697bc4ef3447c3a908a0368ec8bb47a/source/USBDevices.page)及同版本 `USBDevices.php`、`USBManagerSettings.page`。

其他對照來自本次已登入介面的可見文字。公開原始碼用於確認翻譯掛鉤；未將它當作受測伺服器所有檔案均相同的證明。
