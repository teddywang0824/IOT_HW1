# 🗄️ Mock DB — SQLite 測試資料產生器

> 產生模擬 DHT11 感測器的隨機溫濕度資料，寫入 SQLite 資料庫供開發測試使用。

## 📁 專案結構

```
backend/mock_db/
├── generate_mock_data.py   # 主程式：產生隨機資料並寫入 aiotdb.db
├── main.py                 # uv 預設進入點
├── pyproject.toml          # 專案設定
├── README.md               # 本文件
├── .python-version         # Python 版本鎖定 (3.12)
└── aiotdb.db               # (執行後產生) SQLite 資料庫
```

## 📋 資料表結構 (`sensor_data`)

| 欄位         | 型別                                              | 說明           |
| ------------ | ------------------------------------------------- | -------------- |
| `id`         | `INTEGER PRIMARY KEY AUTOINCREMENT`               | 主鍵，自動遞增 |
| `temp`       | `REAL DEFAULT 0.0`                                | 溫度（°C）     |
| `humid`      | `REAL DEFAULT 0.0`                                | 濕度（%）      |
| `created_at` | `DATETIME DEFAULT (datetime('now', 'localtime'))` | 建立時間       |
| `updated_at` | `DATETIME DEFAULT (datetime('now', 'localtime'))` | 更新時間       |

## 🚀 使用方式

### 1. 建立虛擬環境（首次使用）

```bash
cd backend/mock_db
uv sync
```

### 2. 執行資料產生器

```bash
uv run python generate_mock_data.py
```

執行後會：

- 在同目錄下建立 `aiotdb.db`（若已存在則清除舊資料重新產生）
- 插入 **50 筆**隨機溫濕度測試資料
- 在終端顯示格式化的資料表格

### 3. 手動查看資料庫

```bash
# 使用 sqlite3 CLI
sqlite3 aiotdb.db "SELECT * FROM sensor_data;"
```

或使用 VS Code 的 **SQLite Viewer** 擴充套件直接開啟 `aiotdb.db`。

## 🔧 設定參數

在 `generate_mock_data.py` 頂部可調整：

| 參數                      | 預設值          | 說明           |
| ------------------------- | --------------- | -------------- |
| `NUM_RECORDS`             | `50`            | 產生的資料筆數 |
| `TEMP_MIN` / `TEMP_MAX`   | `18.0` / `35.0` | 溫度範圍（°C） |
| `HUMID_MIN` / `HUMID_MAX` | `30.0` / `90.0` | 濕度範圍（%）  |

## 📌 備註

- 使用 Python 內建 `sqlite3` 模組，**不需額外安裝依賴**
- 時間戳記模擬過去 **24 小時**內的隨機時間點
- 每次執行會**清除舊資料**並重新產生，確保資料一致性
