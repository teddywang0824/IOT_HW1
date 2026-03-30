# 🌐 AIoT 溫濕度感測與 WiFi 串接專題 (ESP32)

本專案是一個完整的物聯網 (IoT) 實作專題，旨在達成「即時擷取邊緣端感測資料並於本地/雲端展示」。
為因應硬體展示需求與 Live Demo (Vercel) 雲端部署，本專案採用 **「雙軌獨立法」** 進行開發：

- **軌道一：地端真實硬體展示** (`edge/` + `backend/` + `frontend/`)：透過 ESP32 與本地 API 配合，確保真實感測器數據寫入資料庫，以火力展示完整系統。
- **軌道二：雲端純前端展示** (`frontend_vercel/`)：抽離後端 API 依賴，以輕量的 React 原生模擬器在瀏覽器中展示動態儀表板，專司 Vercel Live Demo，滿足雲端存取需求。

---

## 📂 專案總體結構

```
d:\IOT_HW1\
├── .agent/              # AI 代理人 Skill 設定區 (task_logger)
├── frontend_vercel/     # 【雲端軌道】專為 Vercel 打造的純前端模擬 Live Demo (無資料庫依賴)
├── frontend/            # 【地端軌道】銜接本地 FastAPI 與真實 ESP32 數據的全功能 Dashboard
├── backend/             # 後端伺服器與資料庫專案區 (Python / uv)
│   ├── mock_db/         # 產生模擬 SQLite 測試資料的專案
│   └── wifi_iot/        # 接收 ESP32 上傳真實數據的 FastAPI 伺服器
├── edge/                # 邊緣運算硬體專案區 (C++ / PlatformIO)
│   ├── DHT11/           # 單純讀取 DHT11 溫濕度並印在 Serial
│   ├── DHT11_WIFI/      # 【正式串接】讀取 DHT11 溫濕度並透過 WiFi POST 到本地後端
│   └── LED/             # 基礎測試 ESP32 內建 LED
├── 任務紀錄.md            # 開發日誌 (Development Log) 自動紀錄檔
└── README.md            # 本專案總體說明文件
```

---

## 🖥️ 子系統一覽與說明

### 1. 視覺化儀表板 (Frontend)
- **`frontend_vercel/` (雲端 Live Demo 版)**: 
  使用 React + Vite 建構。此版本**不具備任何後端呼叫或硬體連接功能**，依賴前端 `setInterval` 產生定時隨機的溫濕度數據。部署於 Vercel，用於提供外界可隨意訪問且極具動態感的雲端模擬儀表板。
- **`frontend/` (地端全功能版)**: 
  使用 React + Vite 建構。負責輪詢 (Polling) 本地 FastAPI 伺服器，呈現「透過真實 ESP32 開發板」或是「本地軟體模擬器」寫入 SQLite 資料庫的溫濕度資料。

### 2. 應用程式介面與資料庫 (Backend)
- **`backend/wifi_iot/`**: 輕量級 FastAPI 應用程式，專門接收 ESP32 發來的 `/api/sensor` HTTP POST 請求。所有收到的溫濕度均寫入本機 `aiotdb.db` SQLite 資料庫中；同時也提供 API 讓 `frontend/` 讀取資料或控制內部軟體模擬器。

### 3. 微控制器硬體端 (Edge)
- **`edge/DHT11_WIFI/`**: 基於 PlatformIO 開發，硬體支援 ESP32 (`denky32`)。在提供正確的手機熱點 `ssid` 與 本地電腦端 API IP (如 `192.168.x.x:8000`) 的情況下，定期於 GPIO 15 收集 DHT11 感測數值，以 WiFi POST 向伺服器遞交。

---

## 🚀 執行與測試指南 (雙軌)

### 軌道一：部署 Vercel Live Demo
如果你只需觀看雲端模擬版本：
1. 進入 `frontend_vercel/`。
2. 將其存放庫綁定 Vercel 並進行標準 React 部署。
3. 存取 Vercel 提供網址，即刻看到充滿科技感的數據跳動。

### 軌道二：執行地端真實硬體測試
若需親自驗證感測器連線：
1. **啟動後端：** 執行 `uv run -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload` (位於 `backend/wifi_iot/`)。請利用 `ipconfig` 找出該台電腦分配到的手機熱點區網 IP 位址。
2. **啟動前端：** 執行 `npm run dev` (位於 `frontend/`) 查看本機 Dashboard。
3. **燒入韌體：** 開啟 `edge/DHT11_WIFI/src/main.cpp`，填寫正確的 WiFi 憑證與電腦 API 位址。燒錄成功後觀察 ESP32 的 Serial Monitor 輸出即可。

---
_詳細的使用與環境設定，請參考各專案下的 `README.md` 指南。_
