#include <WiFi.h>
#include <ESP32Servo.h>

// Wi-Fi 설정
#define ssid "ConnectValue_C403_2G"        // Wi-Fi SSID
#define password "CVC403!@#$" // Wi-Fi password

// 서보 모터 설정
Servo vacuumServo;   // 진공 펌프 제어 서보
Servo valveServo;    // 솔레노이드 밸브 제어 서보

void setup() {
  Serial.begin(115200);

  // 서보 모터 핀에 연결
  vacuumServo.attach(2);  // 진공 서보를 9번 핀에 연결
  valveServo.attach(4);   // 밸브 서보를 8번 핀에 연결

  // 서보 초기화
  vacuumServo.write(0);   // 진공 펌프 끄기
  valveServo.write(0);    // 밸브 닫기
  delay(1000);

  Serial.println("시스템 초기화 완료");
  Serial.println("진공: OFF, 밸브: 닫힘");

  // Wi-Fi 연결
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("Wi-Fi 연결됨");
  Serial.print("IP 주소: ");
  Serial.println(WiFi.localIP());
}

void loop() {
  WiFiClient client;
  
  // Python 서버에 연결
  if (!client.connect("172.30.1.11", 8882)) {  // 서버의 IP를 적절히 변경하세요.
    Serial.println("서버에 연결 실패. 재시도 중...");
    delay(2000);
    return;
  }
  
  Serial.println("Python 서버에 연결됨.");

  // Python에서 명령을 수신
  while (client.connected()) {
    while (client.available()) {
      String command = client.readString();
      Serial.println("받은 명령: " + command);

      if (command == "Suction ON") {
        vacuumServo.write(180);  // 진공 펌프 ON
        valveServo.write(0);     // 밸브 닫기
        client.println("진공 ON, 밸브 닫힘");
      }
      else if (command == "Suction OFF") {
        vacuumServo.write(0);    // 진공 펌프 OFF
        valveServo.write(180);   // 밸브 열기
        client.println("진공 OFF, 밸브 열림");
      }
      else {
        client.println("알 수 없는 명령");
      }
    }
  }

  client.stop();  // 연결 종료
  delay(100);  // 잠시 대기 후 반복
}

