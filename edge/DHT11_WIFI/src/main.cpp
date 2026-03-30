#include <Arduino.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <DHT.h>

// ============================================
// ESP32 DHT11 + WiFi 溫濕度發送測試程式
// 板子：ESP32 WROOM-32 (denky32)
// 功能：讀取溫濕度並透過 WiFi 發送 HTTP POST 到後端 API
// ============================================

// ──────────────────────────── 設定區 ────────────────────────────

// 1. 手機熱點 (WiFi) 設定
const char* ssid     = "Eggeggwe 2.4GHz";     // 替換為你的手機熱點名稱
const char* password = "YuelaiOrz"; // 替換為你的手機熱點密碼

// 2. 後端伺服器 (Backend) 設定
// 請在連接手機熱點的電腦上，開啟終端機輸入 `ipconfig`，找出 "IPv4 位址"
// 將其填入下方的 X.X，例如 "192.168.43.100"
const char* serverUrl = "http://192.168.1.133:8000/api/sensor"; 

// 3. DHT11 感測器設定
#define DHT_PIN 15          // DHT11 資料腳位接在 GPIO 15 (D15)
#define DHT_TYPE DHT11      
#define READ_INTERVAL 5000  // 每 5 秒讀取並傳送一次資料

// ────────────────────────────────────────────────────────────────

DHT dht(DHT_PIN, DHT_TYPE);
unsigned long lastReadTime = 0;
unsigned long sendCount = 0;

void setup() {
  Serial.begin(115200);
  delay(10);
  
  dht.begin();
  
  // 連接手機 WiFi 熱點
  Serial.println("\n===================================");
  Serial.println("  ESP32 WiFi + DHT11 測試程式啟動");
  Serial.print("  正在連接 WiFi: ");
  Serial.println(ssid);
  Serial.println("===================================");
  
  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  
  Serial.println("\n✅ WiFi 連接成功！");
  Serial.print("📡 ESP32 的 IP 地址: ");
  Serial.println(WiFi.localIP());
  Serial.println("===================================\n");
}

void loop() {
  if (millis() - lastReadTime >= READ_INTERVAL) {
    lastReadTime = millis();
    sendCount++;
    
    // 1. 讀取感測器
    float h = dht.readHumidity();
    float t = dht.readTemperature();
    
    if (isnan(h) || isnan(t)) {
      Serial.printf("[#%lu] ❌ 讀取失敗！請檢查 DHT11 接線。\n", sendCount);
      return;
    }
    
    Serial.printf("[#%lu] 🌡️ 溫度: %.1f°C | 💧 濕度: %.1f%% ... 準備發送\n", sendCount, t, h);
    
    // 2. 透過 WiFi 發送資料
    if (WiFi.status() == WL_CONNECTED) {
      HTTPClient http;
      
      http.begin(serverUrl);
      http.addHeader("Content-Type", "application/json"); // 告訴後端資料格式為 JSON
      
      // 組合 JSON 字串 (例如: {"temp": 25.5, "humid": 60.5})
      String payload = "{\"temp\":" + String(t) + ", \"humid\":" + String(h) + "}";
      
      // 發送 HTTP POST 請求
      int httpResponseCode = http.POST(payload);
      
      if (httpResponseCode > 0) {
        String response = http.getString();
        Serial.printf("  > 伺服器回應碼: %d\n", httpResponseCode);
        Serial.printf("  > 伺服器回傳: %s\n", response.c_str());
      } else {
        Serial.printf("  > ❌ HTTP POST 失敗，錯誤碼: %d\n", httpResponseCode);
        Serial.println("  > （請確認 IP 地址正確，且後端伺服器已啟動 & 防火牆允許存取！）");
      }
      
      // 釋放資源
      http.end();
    } else {
      Serial.println("  > ❌ WiFi 已斷線！");
    }
    Serial.println("-----------------------------------");
  }
}