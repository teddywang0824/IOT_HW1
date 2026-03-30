# ☁️ Frontend Vercel (Live Demo)

> **這是一個「純前端」建置的模擬儀表板！專門為 Vercel 雲端 Live Demo 打造！**

## 🎯 專案特色與用途
因應 HW1「展示雲端 Live Demo」的需求，但同時又要保障本地硬體傳輸不致於因為雲端無狀態資料庫而過度複雜。本專案 (`frontend_vercel`) 從最初的 `frontend` 複製分支而出：
- **徹底拔除了後端 API `fetch` 依賴**，避免部署到 Vercel 報發 CORS Error 或是找不到 `localhost:8000` 伺服器。
- **純前端模擬器**：透過原生 React 的 `useEffect` 與 `setInterval` 來自動定時 (5 秒) 產出合乎現實範圍的隨機溫濕度 (Temp: 20~35°C, Humid: 40~80%)。
- **移除硬體按鈕**：介面中封裝好了 Cloud Simulator 介面按鈕，並已將會控制真實硬體的 API 邏輯移除。

## 🚀 部署指南

### 在本地預覽
如果你想先在個人電腦上看看樣子：
```bash
cd frontend_vercel
npm install
npm run dev
```

### 發布至 Vercel (Github 版)
1. 建立一個全新的 GitHub Repository (或者利用現有的庫建立新分支)。
2. 確保只將 `frontend_vercel/` 作為主專案資料夾推送 (或是告訴 Vercel 你的 root directory 是 `frontend_vercel`)。
3. 在 Vercel 匯入 Repository，Framework Protocol 設定為 **Vite**。
4. 按下 Deploy 即可立刻獲得專屬的 Live Demo 網址！
