#include <WiFi.h>
#include <Servo.h>

// Wi-Fi 설정
#define ssid "ConnectValue_C403_2G"  // Wi-Fi SSID
#define password "CVC403!@#$"         // Wi-Fi 비밀번호

// 서보 모터 객체 선언
Servo myservo0; // 진공 펌프 제어용 서보
Servo myservo1; // 솔레노이드 밸브 제어용 서보

void setup() {
  // 시리얼 통신 초기화
  Serial.begin(115200);
  
  // 서보 모터 핀 설정
  myservo0.attach(9);  // 진공 펌프 제어용 서보를 핀 9에 연결
  myservo1.attach(8);  // 솔레노이드 밸브 제어용 서보를 핀 8에 연결
  
  // 서보 초기 상태 설정
  myservo0.write(0);   // 진공 펌프 OFF (서보 초기 위치: 0도)
  myservo1.write(0);   // 솔레노이드 밸브 닫힘 (서보 초기 위치: 0도)

  // Wi-Fi 연결
  WiFi.begin(ssid, password);
  Serial.println("Connecting to Wi-Fi...");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWi-Fi connected!");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  // 소켓 서버 시작
  WiFiServer server(10000);  // 포트 10000에서 서버 시작
  server.begin();
  Serial.println("Server started, waiting for clients...");
}

void loop() {
  WiFiServer server(10000);
  WiFiClient client = server.available();
  
  if (client) {
    Serial.println("Client connected");
    
    // 명령을 받는 부분
    while (client.connected()) {
      if (client.available()) {
        char command = client.read();
        Serial.print("Command received: ");
        Serial.println(command);

        // 명령에 따라 서보 제어
        if (command == '1') {  // 진공 펌프 작동 (모터 1: 시계방향)
          Serial.println("Pump ON, Valve Closed");
          myservo0.write(180);  // 진공 펌프 ON (서보 모터 180도)
          myservo1.write(0);    // 솔레노이드 밸브 닫힘 (서보 모터 0도)
          client.println("Pump ON, Valve Closed");
        } else if (command == '2') {  // 진공 펌프 해제 (모터 1: 반시계방향)
          Serial.println("Pump OFF, Valve Open");
          myservo0.write(0);    // 진공 펌프 OFF (서보 모터 0도)
          myservo1.write(180);  // 솔레노이드 밸브 열림 (서보 모터 180도)
          client.println("Pump OFF, Valve Open");
        } else {
          Serial.println("Invalid command received.");
          client.println("Invalid command");
        }
      }
    }
    client.stop();  // 클라이언트 연결 종료
    Serial.println("Client disconnected");
  }
}
