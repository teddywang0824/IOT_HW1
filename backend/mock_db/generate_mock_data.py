"""
generate_mock_data.py
=====================
產生 50 筆隨機溫濕度測試資料並寫入 SQLite 資料庫 (aiotdb.db)。

Table: sensor_data
Columns:
  - id          : INTEGER PRIMARY KEY AUTOINCREMENT
  - temp        : REAL DEFAULT 0.0
  - humid       : REAL DEFAULT 0.0
  - created_at  : DATETIME DEFAULT (datetime('now', 'localtime'))
  - updated_at  : DATETIME DEFAULT (datetime('now', 'localtime'))
"""

import sqlite3
import random
import os
from datetime import datetime, timedelta

# ──────────────────────────── 設定 ────────────────────────────

DB_NAME = "aiotdb.db"
TABLE_NAME = "sensor_data"
NUM_RECORDS = 50

# 溫濕度隨機範圍（模擬 DHT11 實際數值）
TEMP_MIN, TEMP_MAX = 18.0, 35.0    # °C
HUMID_MIN, HUMID_MAX = 30.0, 90.0  # %

# ──────────────────────────── 主程式 ────────────────────────────


def get_db_path() -> str:
    """取得資料庫檔案的絕對路徑（與此腳本同一目錄）。"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, DB_NAME)


def create_table(cursor: sqlite3.Cursor) -> None:
    """建立 sensor_data 資料表（若不存在）。"""
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            id          INTEGER  PRIMARY KEY AUTOINCREMENT,
            temp        REAL     DEFAULT 0.0,
            humid       REAL     DEFAULT 0.0,
            created_at  DATETIME DEFAULT (datetime('now', 'localtime')),
            updated_at  DATETIME DEFAULT (datetime('now', 'localtime'))
        )
    """)


def generate_random_records(n: int) -> list[tuple]:
    """
    產生 n 筆隨機溫濕度資料。
    時間戳記模擬過去 24 小時內的隨機時間點，並依時間排序。
    """
    now = datetime.now()
    records = []

    for _ in range(n):
        # 隨機溫度（保留 1 位小數）
        temp = round(random.uniform(TEMP_MIN, TEMP_MAX), 1)
        # 隨機濕度（保留 1 位小數）
        humid = round(random.uniform(HUMID_MIN, HUMID_MAX), 1)
        # 隨機時間：過去 24 小時內
        random_offset = timedelta(seconds=random.randint(0, 86400))
        timestamp = (now - random_offset).strftime("%Y-%m-%d %H:%M:%S")

        records.append((temp, humid, timestamp, timestamp))

    # 依時間排序（舊 → 新）
    records.sort(key=lambda r: r[2])
    return records


def insert_records(cursor: sqlite3.Cursor, records: list[tuple]) -> None:
    """批次插入資料。"""
    cursor.executemany(f"""
        INSERT INTO {TABLE_NAME} (temp, humid, created_at, updated_at)
        VALUES (?, ?, ?, ?)
    """, records)


def display_records(cursor: sqlite3.Cursor) -> None:
    """查詢並顯示所有資料。"""
    cursor.execute(f"SELECT * FROM {TABLE_NAME} ORDER BY id ASC")
    rows = cursor.fetchall()

    print(f"\n{'='*70}")
    print(f"  📊 aiotdb.db — sensor_data 資料表 ({len(rows)} 筆)")
    print(f"{'='*70}")
    print(f"  {'ID':>4}  {'溫度(°C)':>9}  {'濕度(%)':>8}  {'建立時間':<20}  {'更新時間':<20}")
    print(f"  {'-'*4}  {'-'*9}  {'-'*8}  {'-'*20}  {'-'*20}")

    for row in rows:
        id_, temp, humid, created, updated = row
        print(f"  {id_:>4}  {temp:>8.1f}  {humid:>7.1f}  {created:<20}  {updated:<20}")

    print(f"{'='*70}\n")


def main():
    db_path = get_db_path()
    is_new = not os.path.exists(db_path)

    print(f"📁 資料庫路徑: {db_path}")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # 建立資料表
        create_table(cursor)

        if is_new:
            print(f"✅ 已建立新資料庫與資料表 '{TABLE_NAME}'")
        else:
            # 清除舊資料重新產生
            cursor.execute(f"DELETE FROM {TABLE_NAME}")
            print(f"🔄 已清除舊資料，重新產生...")

        # 產生並插入隨機資料
        records = generate_random_records(NUM_RECORDS)
        insert_records(cursor, records)
        conn.commit()

        print(f"✅ 已成功插入 {NUM_RECORDS} 筆隨機測試資料")

        # 顯示資料
        display_records(cursor)

    except Exception as e:
        print(f"❌ 錯誤: {e}")
        conn.rollback()
    finally:
        conn.close()


if __name__ == "__main__":
    main()
