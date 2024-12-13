#include <WiFi.h>
#include <ESP32Servo.h>

// Wi-Fi 설정
#define ssid "ConnectValue_C403_2G"        // Wi-Fi SSID
#define password "CVC403!@#$" // Wi-Fi password

// 서보 모터 설정
Servo vacuumServo;   // 진공 펌프 제어 서보
Servo valveServo;    // 솔레노이드 밸브 제어 서보

WiFiServer server(8882);  // 소켓 서버 설정

void setup() {
  Serial.begin(115200);

  // 서보 초기화
  vacuumServo.attach(2);  // 진공 펌프 서보 핀
  valveServo.attach(4);   // 밸브 서보 핀
  vacuumServo.write(0);   // 초기화: 진공 펌프 OFF
  valveServo.write(0);    // 초기화: 밸브 닫기

  // Wi-Fi 연결
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWi-Fi Connected");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());

  // 소켓 서버 시작
  server.begin();
  Serial.println("Socket server started on port 8882");
}

void loop() {
  WiFiClient client = server.available();  // 클라이언트 연결 대기

  if (client) {  // 클라이언트가 연결되었는지 확인
    Serial.println("Client connected");
    while (client.connected()) {
      if (client.available()) {  // 클라이언트 데이터 수신 대기
        String command = client.readStringUntil('\n');  // 명령 읽기
        command.trim();  // 공백 제거
        Serial.println("Received Command: " + command);

        // 명령 처리
        if (command == "Suction ON") {
          vacuumServo.write(180);  // 진공 펌프 ON
          valveServo.write(0);     // 밸브 닫기
          client.println("Suction ON, Valve Closed");
        } else if (command == "Suction OFF") {
          vacuumServo.write(0);    // 진공 펌프 OFF
          valveServo.write(180);   // 밸브 열기
          client.println("Suction OFF, Valve Opened");
        } else {
          client.println("Invalid Command");
        }
      }
    }
    client.stop();  // 클라이언트 연결 종료
    Serial.println("Client disconnected");
  }
}



