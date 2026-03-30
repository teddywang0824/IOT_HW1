from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3
import os
import asyncio
import random

app = FastAPI(title="AIoT WiFi Sensor Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 資料庫路徑 (與此腳本同目錄下的 aiotdb.db)
DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "aiotdb.db")

# 定義接收的資料結構 (JSON)
class SensorData(BaseModel):
    temp: float
    humid: float

def init_db():
    """初始化資料庫與資料表"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sensor_data (
            id          INTEGER  PRIMARY KEY AUTOINCREMENT,
            temp        REAL     DEFAULT 0.0,
            humid       REAL     DEFAULT 0.0,
            created_at  DATETIME DEFAULT (datetime('now', 'localtime')),
            updated_at  DATETIME DEFAULT (datetime('now', 'localtime'))
        )
    ''')
    conn.commit()
    conn.close()

esp32_active = True
simulation_active = False

async def simulation_loop():
    global simulation_active
    while True:
        if simulation_active:
            temp = round(random.uniform(20.0, 35.0), 2)
            humid = round(random.uniform(40.0, 80.0), 2)
            try:
                conn = sqlite3.connect(DB_FILE)
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO sensor_data (temp, humid) VALUES (?, ?)",
                    (temp, humid)
                )
                conn.commit()
                conn.close()
                print(f"🔄 Simulated Data Saved: Temp={temp}°C, Humid={humid}%")
            except Exception as e:
                print(f"❌ Simulator error: {str(e)}")
        await asyncio.sleep(2)

bg_tasks = set()

@app.on_event("startup")
async def startup_event():
    # 啟動時確保資料表存在
    init_db()
    print(f"📦 Database initialized at {DB_FILE}")
    task = asyncio.create_task(simulation_loop())
    bg_tasks.add(task)

@app.post("/api/simulator/on")
def start_simulator():
    """啟動背景模擬器，每2秒產生一筆模擬溫濕度資料"""
    global simulation_active, esp32_active
    esp32_active = False  # 自動關閉 ESP32
    simulation_active = True
    return {"status": "success", "message": "Simulator started, ESP32 stopped"}

@app.post("/api/simulator/off")
def stop_simulator():
    """停止背景模擬器"""
    global simulation_active
    simulation_active = False
    return {"status": "success", "message": "Simulator stopped"}

@app.post("/api/esp32/on")
def start_esp32():
    """啟動真實硬體 ESP32 的資料接收"""
    global esp32_active, simulation_active
    simulation_active = False  # 自動關閉模擬器
    esp32_active = True
    return {"status": "success", "message": "ESP32 data reception started, Simulator stopped"}

@app.post("/api/esp32/off")
def stop_esp32():
    """停止接收真實硬體 ESP32 的資料"""
    global esp32_active
    esp32_active = False
    return {"status": "success", "message": "ESP32 data reception stopped"}

@app.post("/api/sensor")
def receive_sensor_data(data: SensorData):
    """接收來自 Edge 端 (ESP32) 的溫濕度資料並存入 SQLite"""
    global esp32_active
    if not esp32_active:
        print("⏸️ Ignored ESP32 data: ESP32 switch is OFF.")
        return {"status": "ignored", "message": "Switch is offline"}
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        # 插入資料，created_at 和 updated_at 由 SQLite 預設值處理
        cursor.execute(
            "INSERT INTO sensor_data (temp, humid) VALUES (?, ?)",
            (data.temp, data.humid)
        )
        conn.commit()
        record_id = cursor.lastrowid
        conn.close()
        
        print(f"✅ Received and Saved: ID={record_id}, Temp={data.temp}°C, Humid={data.humid}%")
        return {"status": "success", "id": record_id, "message": "Data saved"}
        
    except Exception as e:
        print(f"❌ Error saving data: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/sensor")
def get_sensor_data(limit: int = 10):
    """取得最近幾筆溫濕度資料 (供測試用)"""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM sensor_data ORDER BY id DESC LIMIT ?", (limit,)
        )
        rows = cursor.fetchall()
        conn.close()
        
        results = [
            {"id": r[0], "temp": r[1], "humid": r[2], "created_at": r[3], "updated_at": r[4]}
            for r in rows
        ]
        return {"status": "success", "data": results}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
