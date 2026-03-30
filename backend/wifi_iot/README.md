# 🌐 AIoT WiFi 後端測試專案 (Backend)

> 作為主控中樞的 FastAPI 伺服器，負責與 SQLite 資料庫互動，接收真實邊緣裝置的數據，或自行於背景執行模擬器。

## 📋 專案架構概觀

本專案 (`wifi_iot`) 作為雙軌法的「地端後端」，提供了一組完整的 HTTP API (.POST, .GET)，用於：
1. **硬體資料接收**：隨時監聽 ESP32 在同個網域上傳的資料。
2. **背景軟體模擬**：內建非同步 (Asynchronous) 的模擬器自動對 SQLite 塞入溫濕度值。
3. **前端圖表供應**：提供資料歷史紀錄給本地端的 React App (`frontend/`) 做視覺化。

### 資料庫結構 (`sensor_data` 表)
- `id`: INTEGER PRIMARY KEY AUTOINCREMENT
- `temp`: REAL DEFAULT 0.0
- `humid`: REAL DEFAULT 0.0
- `created_at`: DATETIME DEFAULT (datetime('now', 'localtime'))
- `updated_at`: DATETIME DEFAULT (datetime('now', 'localtime'))

## 🚀 環境安裝與啟動

在電腦上開啟終端機，執行以下：

### 1. 啟動虛擬環境與安裝依賴
這裡使用 Python 最新的包管理器 `uv` (或是你的 `pip`)：
```bash
cd backend/wifi_iot
uv add fastapi uvicorn
```

### 2. 啟動伺服器
我們將 Host 設定為 `0.0.0.0`，意即「所有在此網路 (含你手機熱點) 的裝置」都能連接：
```bash
uv run -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

> **🔥 找尋你的開發 IP (給 ESP32 用)：**
> 1. 打開手機熱點。
> 2. 電腦連上該熱點。
> 3. 打開另一台終端機輸入 `ipconfig` (Windows) 或 `ifconfig` (Mac/Linux)。
> 4. 在 WiFi 網卡介面中找到 `IPv4 位址` (例如 192.168.43.100)。
> 5. 你的真實對外 API 網址即為：`http://192.168.43.100:8000/api/sensor`。把它填給 `edge/DHT11_WIFI/src/main.cpp` 就對了！

## 📡 提供之 API Endpoint
- `/api/simulator/on` & `/off`：啟動/關閉背景資料模擬。
- `/api/esp32/on` & `/off`：開啟硬體的資料接收功能（與模擬器**互斥**保護）。
- `/api/sensor` [POST]：給 ESP32 端用來上傳 JSON `{"temp": 24, "humid": 60}`。
- `/api/sensor` [GET]：給前端用來抓取最新 50 筆紀錄畫圖。
