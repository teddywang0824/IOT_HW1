#include <Arduino.h>

// ============================================
// ESP32 LED 閃爍測試程式
// 板子：ESP32 WROOM-32 (denky32)
// 功能：內建 LED 閃爍 + Serial 監控輸出
// ============================================

// ESP32 內建 LED 通常在 GPIO 2
#define LED_PIN 2

// 閃爍間隔（毫秒）
#define BLINK_INTERVAL 500

// 記錄閃爍次數
unsigned long blinkCount = 0;

void setup() {
  // 初始化 Serial 通訊，方便觀察狀態
  Serial.begin(115200);
  delay(1000); // 等待 Serial 穩定

  // 設定 LED 腳位為輸出模式
  pinMode(LED_PIN, OUTPUT);

  Serial.println("===================================");
  Serial.println("  ESP32 LED 閃爍測試程式啟動");
  Serial.println("  LED Pin: GPIO 2 (內建 LED)");
  Serial.printf("  閃爍間隔: %d ms\n", BLINK_INTERVAL);
  Serial.println("===================================");
}

void loop() {
  // LED 亮起
  digitalWrite(LED_PIN, HIGH);
  Serial.printf("[#%lu] LED ON\n", ++blinkCount);
  delay(BLINK_INTERVAL);

  // LED 熄滅
  digitalWrite(LED_PIN, LOW);
  Serial.printf("[#%lu] LED OFF\n", blinkCount);
  delay(BLINK_INTERVAL);
}