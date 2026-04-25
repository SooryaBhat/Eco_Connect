#include "HX711.h"
#include <WiFi.h>
#include <HTTPClient.h>

// WiFi credentials
const char* ssid = "moto g73 5G_2441";
const char* password = "Sooryabhat123";

// Flask backend URL
const char* serverUrl = "https://eco-connect-1-cy88.onrender.com/update_weight";

// Bin code
const char* bin_code = "BIN005";

// Recyclable load cell pins (HX711 #1)
#define REC_DT 4
#define REC_SCK 5

// Non-recyclable load cell pins (HX711 #2)
#define NONREC_DT 18
#define NONREC_SCK 19

// Create HX711 objects
HX711 scale_rec;        
HX711 scale_nonrec;     

// Calibration factors
float CAL_REC = 54.4;
float CAL_NONREC = 22.4;

// Weight variables
float recyclable_weight = 0;
float non_recyclable_weight = 0;

unsigned long lastSendTime = 0;
const unsigned long sendInterval = 5000; // 5 seconds

void connectWiFi() {
  Serial.println("\nConnecting to WiFi...");
  WiFi.begin(ssid, password);
  int tries = 0;

  while (WiFi.status() != WL_CONNECTED && tries < 30) {
    delay(500);
    Serial.print(".");
    tries++;
  }
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\n✓ WiFi Connected!");
    Serial.print("IP Address: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println("\n✗ WiFi FAILED!");
  }
}

void setup() {
  Serial.begin(115200);
  delay(500);

  connectWiFi();

  // Initialize HX711 scales
  Serial.println("\nInitializing Load Cells...");

  scale_rec.begin(REC_DT, REC_SCK);
  scale_nonrec.begin(NONREC_DT, NONREC_SCK);

  if (scale_rec.is_ready() && scale_nonrec.is_ready()) {
    Serial.println("✓ Both Load Cells Ready!");

    scale_rec.set_scale(CAL_REC);
    scale_nonrec.set_scale(CAL_NONREC);

    Serial.println("Taring both load cells...");
    delay(3000);

    scale_rec.tare();
    scale_nonrec.tare();

    Serial.println("Tare Complete!");
  } else {
    Serial.println("✗ ERROR: One or both HX711 modules not detected!");
  }
}

void loop() {
  if (scale_rec.is_ready() && scale_nonrec.is_ready()) {

    // Read raw weights
    recyclable_weight = scale_rec.get_units(10);
    non_recyclable_weight = scale_nonrec.get_units(10);

    // ---- FIX NEGATIVE WEIGHT + DEADZONE ----
    
    // Deadzone (ignore noise below ±50g)
    if (abs(recyclable_weight) < 50) recyclable_weight = 0;
    if (abs(non_recyclable_weight) < 50) non_recyclable_weight = 0;

    // Prevent negative values
    if (recyclable_weight < 0) recyclable_weight = 0;
    if (non_recyclable_weight < 0) non_recyclable_weight = 0;

    // Display for debugging
    Serial.println("==================================");
    Serial.print("Recyclable: ");
    Serial.print(recyclable_weight, 2);
    Serial.println(" g");

    Serial.print("Non-Recyclable: ");
    Serial.print(non_recyclable_weight, 2);
    Serial.println(" g");
    Serial.println("==================================\n");
  }

  // Send values every 5 seconds
  if (millis() - lastSendTime > sendInterval) {
    sendToBackend();
    lastSendTime = millis();
  }

  delay(500);
}

void sendToBackend() {
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("WiFi Lost — Reconnecting...");
    connectWiFi();
    return;
  }

  HTTPClient http;
  http.begin(serverUrl);
  http.addHeader("Content-Type", "application/json");

  // Prepare JSON payload
  String payload = "{";
  payload += "\"bin_code\":\"" + String(bin_code) + "\",";
  payload += "\"recyclable_weight\":" + String(recyclable_weight, 2) + ",";
  payload += "\"non_recyclable_weight\":" + String(non_recyclable_weight, 2);
  payload += "}";

  Serial.println("\nSending to backend:");
  Serial.println(payload);

  int code = http.POST(payload);

  Serial.print("Response Code: ");
  Serial.println(code);

  if (code > 0) {
    Serial.println("Server Response:");
    Serial.println(http.getString());
  }

  http.end();
}