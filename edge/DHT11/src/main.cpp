#include <Arduino.h>
#include <DHT.h>

// ============================================
// ESP32 DHT11 溫濕度感測器測試程式
// 板子：ESP32 WROOM-32 (denky32)
// 功能：讀取 DHT11 溫濕度並透過 Serial 輸出
// ============================================

// DHT11 資料腳位接在 D15 (GPIO 15)
#define DHT_PIN 15
#define DHT_TYPE DHT11

// 讀取間隔（毫秒），DHT11 最快約 1 秒讀一次
#define READ_INTERVAL 2000

// 建立 DHT 物件
DHT dht(DHT_PIN, DHT_TYPE);

// 記錄讀取次數
unsigned long readCount = 0;

void setup() {
  // 初始化 Serial 通訊
  Serial.begin(115200);
  delay(1000); // 等待 Serial 穩定

  // 初始化 DHT 感測器
  dht.begin();

  Serial.println("===================================");
  Serial.println("  ESP32 DHT11 溫濕度測試程式啟動");
  Serial.printf("  DHT Pin: GPIO %d\n", DHT_PIN);
  Serial.printf("  讀取間隔: %d ms\n", READ_INTERVAL);
  Serial.println("===================================");
  Serial.println();
}

void loop() {
  // 讀取溫濕度
  float humidity = dht.readHumidity();
  float tempC = dht.readTemperature();       // 攝氏
  float tempF = dht.readTemperature(true);   // 華氏

  readCount++;

  // 檢查是否讀取失敗
  if (isnan(humidity) || isnan(tempC) || isnan(tempF)) {
    Serial.printf("[#%lu] ❌ 讀取失敗！請檢查接線與感測器。\n", readCount);
    delay(READ_INTERVAL);
    return;
  }

  // 計算體感溫度 (Heat Index)
  float heatIndexC = dht.computeHeatIndex(tempC, humidity, false);

  // 輸出結果
  Serial.printf("[#%lu] 🌡️  溫度: %.1f°C (%.1f°F) | 💧 濕度: %.1f%% | 🔥 體感: %.1f°C\n",
                readCount, tempC, tempF, humidity, heatIndexC);

  delay(READ_INTERVAL);
}