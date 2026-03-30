# 🏠 Frontend (Local 全功能版)

> **這是能夠銜接本地 FastAPI 伺服器、監看 ESP32 真實硬體數據的「正規全能 Dashboard」！**

## 🎯 專案特色與用途
為了展示「真實硬體」以及後端 (FastAPI + SQLite) 的連動火力，這個版本的 React App 負責擔綱我們於個人筆電上的監控台。
- **真實資料輪詢 (Polling)**：每兩秒便使用 `fetch` 輪詢後端 `localhost:8000`，即時反饋包含真實歷史資料的折線圖 (`Recharts`)。
- **軟硬體智慧互斥按鈕**：介面上設計有【Software Simulator】與【ESP32 Hardware】這兩組互斥啟動按鈕。只要你在此操作介面中指令啟動硬體連線，後端與前端就會自動暫停一切模擬行為，專心等待。

## 🚀 使用指南

### 1. 背景條件
你必須事先啟動後端的 API 伺服器與資料庫，否則此網頁將無法運作 (報錯網路無法連線)。
- 進入 `backend/wifi_iot/` 資料夾，執行 FastAPI (`uv run -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload`)。

### 2. 開啟儀表板
```bash
cd frontend
npm install
npm run dev
```
點擊終端機內 Vite 提供的 local URL (通常是 `http://localhost:5173`)。

### 3. 操作模式
- 當你想測試後端，尚未開啟 ESP32 之前，可先開啟 **Software Simulator ON**，觀察 SQLite 寫入與折線圖更新是否順利。
- 當你幫 ESP32 上電後，請先切換回 **ESP32 Hardware ON**。你會看見圖表開始接收來自 `edge/DHT11_WIFI` 回傳的真實物理溫濕度數值！
