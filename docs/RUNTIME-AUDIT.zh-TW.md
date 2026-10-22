# Unraid 7.3.3 實機介面稽核（2026-10-22）

## 範圍與方式

透過使用者已登入的瀏覽器，檢查 58 個頁面路徑，包含 13 個主要頁面、31 個設定頁、12 個工具頁及 2 個詳細設定頁。主頁另展開長篇說明，虛擬機器與 USB 頁面等待非同步清單載入後再次檢查。

檢查使用實際畫面、輔助功能樹及唯讀 DOM。未套用伺服器設定，未啟動／停止陣列、容器或虛擬機器，也未執行格式化、刪除、掛載、修復、更新、金鑰變更或資料上傳。檢查時展開的說明及語言開發者檢視均已收起。報告不保留伺服器硬體序號、使用者認證資訊或私人檔案內容。

## 已確認的主要問題

| 問題 | 實機證據 | 本機處理與驗證狀態 |
| --- | --- | --- |
| 語言代碼不是 zh_TW | 顯示設定的可見語言欄位，DOM 選取值為 `zh_CN`；已安裝清單只有 English 與中文。開發者清單中的中文也只有 `zh_CN`，未提供 `zh_TW` | 屬於 Unraid 的語言登錄及新版元件支援限制；未變更遠端語言設定。**ZIP 檔名不會決定安裝後的語言代碼** |
| 新版元件顯示簡體 | 頁首、更新、降級、註冊及 Tailscale 顯示「在线时间、专业版、许可证、配置」等簡體文字 | 傳統 `.txt` 語言包無法直接覆寫這些獨立元件的內建詞庫；需元件提供繁體中文與對應語言識別支援 |
| 星期與月份對照表缺少空白 | 自動更新頁的星期選項整串顯示為「星期天Monday=星期一Tuesday=…」 | 修復 `Days_array`／`Months_array` 的空白分隔格式，並新增依實際 `parse_str` 規則驗證的測試。**待重新匯入後實機複驗** |
| 主頁嵌入的 UD 翻譯未載入 | 主頁的 `HISTORICAL`、`SHARE TYPE`、新增遠端共享按鈕及兩段完整說明仍為英文，儘管外掛語言檔已有譯文 | 官方載入器依 URI 載入語言檔；UD 的主頁模組沒有呼叫 `parse_plugin()`。封裝時將 UD 缺少的鍵及區塊補入 `main.txt`，保留 Main 原有譯文優先權。已測試扁平匯入後的字典與區塊；**待重新匯入後實機複驗** |
| 語境錯譯 | 商店 `Credits` 顯示「信用」；手冊連結顯示「手動」；Docker `Resume All` 顯示「全部還原」；通知 `Notices` 顯示「聲明」；VM 磁碟的 Serial 顯示「序列埠」 | 分別改為「致謝、手冊、全部繼續、一般通知、序號」。同時調整來源、磁碟區對應、識別資訊等用語。**待重新匯入後實機複驗** |
| 新版鍵未收錄於英文參照 | 開機參數、電源選項、通知代理欄位、USB／Compose 標籤、CA 熱門外掛及部分 UD 警告仍是英文 | 依實際文字及官方 `_()` 正規化規則補入相容鍵；JavaScript 字典另補圖表與動態標籤。部分外掛可能未經翻譯函式處理，新增鍵不等同保證顯示已修復 |
| PHP 設定說明未翻譯 | 工具頁的整段用途、日誌與回報等級說明為英文 | 官方頁面具有 `:php_settings_plug:`，參照語系缺少此區塊；已補譯至 `tools.txt`。**待重新匯入後實機複驗** |
| 系統資訊外掛單位與總量異常 | 顯示 `KiiB`、`MiiB`、`GiiB`，並將已安裝記憶體的總量顯示為 `0 MiB`；儀表板記憶體總量正常 | 需追查該外掛的單位拼接及硬體資訊解析；未為修正單一頁面而破壞全域 SI／IEC 前綴 |
| Docker 人類可讀時間混用英文 | 某容器的運作時間顯示 `About a 分鐘` | 舊版時間翻譯分支只替換單位，未處理 `About a` 片語；需要時間格式化程式支援，單純增加一般查找鍵不保證生效 |
| 窄視窗水平捲動 | 主要選單、部分表格及應用程式卡片在窄側欄寬度產生水平捲動 | 已記錄為版面限制；未修改遠端主題或縮放設定 |

## 語言代碼限制

本機的 `zh_TW.zip` 是台灣繁體中文翻譯成品的檔名。Unraid 開發者上傳表單會依「選擇語言」欄位的值安裝，並不依 ZIP 檔名建立新語言代碼。

在本次受測的 Unraid 7.3.3 中，只能從內建清單選到 `zh_CN` 中文；因此目前安裝的繁體 `.txt` 與新版元件的簡體內建字典混用。**請勿把重新命名 ZIP，或再次選取「中文」，視為已安裝獨立的 zh_TW 語系。**完整解決需要 Unraid 加入台灣繁體中文的語言登錄，並讓新版元件與外掛支援相應詞庫。

## 已檢查路徑

| 類別 | 路徑 |
| --- | --- |
| 主要頁面（13） | `/Main`、`/Dashboard`、`/USB`、`/Favorites`、`/Shares`、`/Users`、`/Settings`、`/Plugins`、`/Docker`、`/VMs`、`/Apps`、`/Stats`、`/Tools` |
| 系統與網路設定（16） | `/Settings/DisplaySettings`、`DateTime`、`DiskSettings`、`DockerSettings`、`BootParameters`、`PowerMode`、`ShareSettings`、`UPSsettings`、`VMSettings`、`CPUset`、`Identification`、`NetworkSettings`、`ManagementAccess`、`SMB`、`NFS`、`OutgoingProxy` |
| 偏好與排程（5） | `/Settings/Confirmations`、`Console`、`Scheduler`、`Notifications`、`SyslogSettings` |
| 外掛設定（10） | `/Settings/AutoUpdateApps`、`ca_settings`、`SleepSettings`、`StatSettings`、`TempSettings`、`UnassignedDevicesSettings`、`USBManagerSettings`、`Tailscale`、`compose.manager.settings`、`CleanUpAppdata` |
| 工具（12） | `/Tools/Language`、`Update`、`Registration`、`PageMap`、`Preclear`、`SystemProfiler`、`HardwareProfile`、`NewConfig`、`NewPerms`、`PHPsettings`、`SysDrivers`、`Downgrade` |
| 詳細頁面（2） | `/Shares/Share` 的既有共享資料夾設定、`/Users/UserEdit` 的使用者欄位；未儲存變更 |

商店與外掛列表中的應用程式名稱、作者、遠端目錄說明，以及使用者自訂的共享名稱、備註、容器名稱，不當作本語言包的固定介面字串。未逐一開啟商店所有應用程式、每個外掛的所有子分頁，亦未執行任何破壞性操作以驗收其執行結果。

## 程式來源佐證

- [官方翻譯載入器與鍵名正規化](https://github.com/unraid/webgui/blob/26eb1b5c1d547ddbf44a38e63956ba24f659098b/emhttp/plugins/dynamix/include/Translations.php)：依 URI 分段載入；`parse_array()` 將空白與冒號轉為查詢字串分隔符號；PHP 與 JavaScript 字典分別載入。
- [官方語言清單](https://github.com/unraid/webgui/blob/26eb1b5c1d547ddbf44a38e63956ba24f659098b/emhttp/plugins/dynamix/include/languages.key)：含 `zh_CN`，未列 `zh_TW`。
- [官方語言上傳表單](https://github.com/unraid/webgui/blob/26eb1b5c1d547ddbf44a38e63956ba24f659098b/emhttp/plugins/dynamix/Language.page)：使用選取語言值作為安裝識別碼。
- [官方上傳處理](https://github.com/unraid/webgui/blob/26eb1b5c1d547ddbf44a38e63956ba24f659098b/emhttp/plugins/dynamix/include/FileUpload.php)：ZIP 內路徑會被攤平，檔名轉小寫；上傳會清除翻譯快取。
- [UD 主頁模組](https://github.com/unraid/unassigned.devices/blob/7bdcd03cccb67320598e95a1cab38821182f633b/source/unassigned.devices/usr/local/emhttp/plugins/unassigned.devices/UnassignedDevices.page)與 [UD 程式庫](https://github.com/unraid/unassigned.devices/blob/7bdcd03cccb67320598e95a1cab38821182f633b/source/unassigned.devices/usr/local/emhttp/plugins/unassigned.devices/include/lib.php)：模組具有說明替換標記，但未呼叫 `parse_plugin()` 載入該模組語言檔。
- [官方開機參數頁](https://github.com/unraid/webgui/blob/26eb1b5c1d547ddbf44a38e63956ba24f659098b/emhttp/plugins/dynamix/BootParameters.page)：部分標籤支援 `_()`，但開頭介紹等文字直接寫在頁面中；只有語言查找鍵無法覆蓋未提供掛鉤的內容。

以上公開原始碼為查核時的儲存庫提交，不能視為已讀取伺服器上每個程式檔；實機畫面與 DOM 才是本次環境的直接證據。

## 本機驗證與下一次驗收

- 官方參照：51/51 語言檔、5,170/5,170 精確鍵、633/633 參照說明區塊。
- 本機：5,595 筆單行翻譯、零留白值，另含補入的 PHP 說明區塊。
- 12 項回歸測試通過，包括星期／月份對照表、Unraid 扁平匯入模擬、嵌入主頁的 UD 翻譯及檔名衝突檢查。
- `dist/zh_TW.zip` 已重建；內含 51 個檔案，`main.txt` 含封裝時產生的 UD 補充內容。其餘檔案保持各自原始譯文。
- 本次**尚未重新上傳新版 ZIP**；遠端畫面的上述問題仍以檢查當時為準。重新匯入後，應複查星期選項、主頁 UD 按鈕及說明、商店致謝、Docker 繼續操作文字與 PHP 說明。
