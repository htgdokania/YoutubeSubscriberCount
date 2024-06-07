#include <ESP8266WiFi.h>
#include <WiFiClientSecureBearSSL.h>
#include <ArduinoJson.h>
#include <Adafruit_SSD1306.h> // Include the Adafruit SSD1306 library for OLED display
#include <Adafruit_GFX.h>
#include <Wire.h>

#define OLED_RESET -1 // Reset pin # (or -1 if sharing Arduino reset pin)
Adafruit_SSD1306 display(128,64,&Wire,OLED_RESET);

const char* ssid = "SWATI";
const char* password = "8585865764";
const char* host = "www.googleapis.com";
const char* apiKey = "YOUTUBE_DATA_API_KEY"; // Replace with your API key
const char* channelId = "YOUTUBE_CHANNEL_ID"; // Replace with your Channel ID note this is not same as channel name.

void setup() {
  Serial.begin(115200);
  
  // Initialize the OLED display with the I2C address 0x3C
  if(!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    Serial.println(F("SSD1306 allocation failed"));
    for(;;);
  }

  // Clear the display buffer
  display.clearDisplay();
  display.display();
  // Clear the display buffer
  display.clearDisplay();

  // Display subscriber count on OLED display
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(30,20);
  display.println("Subscribers:");

  display.display();
  delay(100);

  connectToWiFi();
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    getSubscriberCount();
  } else {
    connectToWiFi();
  }
  delay(10000); // Update subscriber count every 5 minutes
}

void connectToWiFi() {
  Serial.println("Connecting to WiFi...");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting...");
  }
  Serial.println("Connected to WiFi");
}

void getSubscriberCount() {
  BearSSL::WiFiClientSecure client;
  client.setInsecure();
  if (!client.connect(host, 443)) {
    Serial.println("Connection failed");
    return;
  }

  Serial.println("Connected to Google API");

  String url = "/youtube/v3/channels?part=statistics&id=" + String(channelId) + "&key=" + String(apiKey);

  client.print(String("GET ") + url + " HTTP/1.1\r\n" +
               "Host: " + host + "\r\n" +
               "Connection: close\r\n\r\n");

  Serial.println("Request sent");
  Serial.println(host+url);
    String response = "";
  bool headersRead = false;
  bool jsonStarted = false;
  while (client.connected()) {
    String line = client.readStringUntil('\n');
    if (!headersRead) {
      if (line == "\r") {
        headersRead = true;
      }
    } else {
      if (jsonStarted || line.startsWith("{")) {
        jsonStarted = true;
        response += line;
      }
    }
  }

  Serial.println("Response received");
  
  DynamicJsonDocument doc(1024);
  deserializeJson(doc, response);
  JsonObject root = doc.as<JsonObject>();
  long subscriberCount = root["items"][0]["statistics"]["subscriberCount"];

  Serial.print("Subscriber count: ");
  Serial.println(subscriberCount);

  client.stop();

  // Clear the display buffer
  display.clearDisplay();

  // Display subscriber count on OLED display
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(30,20);
  display.println("Subscribers:");
  display.setTextSize(2);
  display.setCursor(40,40);
  display.println(subscriberCount);
  display.display();
}
