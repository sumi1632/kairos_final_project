#include <WiFi.h>
#include <Stepper.h>

// Wi-Fi 설정
#define ssid "ConnectValue_C403_2G"      // Wi-Fi SSID
#define password "CVC403!@#$"           // Wi-Fi 비밀번호

// 스텝 모터 설정
const int stepsPerRevolution = 2048;    // 모터 한 바퀴당 스텝 수

// 모터 1 핀 설정 (GPIO 25, 27, 26, 14)
Stepper motor1(stepsPerRevolution, 25, 27, 26, 14);

// 모터 2 핀 설정 (GPIO 32, 4, 33, 5)
Stepper motor2(stepsPerRevolution, 32, 4, 33, 5);

void setup() {
    Serial.begin(115200);
    Serial.println("Starting ESP32...");
    motor1.setSpeed(3); // 스텝 모터 속도 설정
    motor2.setSpeed(3); // 스텝 모터 속도 설정
    // Wi-Fi 연결
    WiFi.begin(ssid, password);
    Serial.println("Connecting to Wi-Fi...");
    int attempts = 0;
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
        attempts++;
        if (attempts > 40) { // 연결 시도 제한
            Serial.println("\nFailed to connect to Wi-Fi.");
            return;
        }
    }
    Serial.println("\nWi-Fi connected!");
    Serial.print("IP address: ");
    Serial.println(WiFi.localIP());
}

void loop() {
    WiFiClient client;

    // Python 서버에 연결
    if (!client.connect(IPAddress(172, 30, 1, 78), 10000)) {  // Python 서버 IP와 포트
        Serial.println("Failed to connect to Python server. Retrying...");
        delay(2000);
        return;
    }

    Serial.println("Connected to Python server.");

    // 명령 처리
    while (client.connected()) {
        while (client.available()) {
            char command = client.read();
            Serial.print("Command received: ");
            Serial.println(command);

            // 명령에 따라 모터 제어
            if (command == '1') {  // 모터 1 시계 방향
                Serial.println("Motor 1: Rotating Clockwise");
                motor1.step(stepsPerRevolution / 6); // 모터 1 시계 방향으로 60도 회전
                client.println("Motor 1 CW completed");
            } else if (command == '2') {  // 모터 1 반시계 방향
                Serial.println("Motor 1: Rotating Counter-Clockwise");
                motor1.step(-stepsPerRevolution / 6); // 모터 1 반시계 방향으로 60도 회전
                client.println("Motor 1 CCW completed");
            } else if (command == '3') {  // 모터 2 시계 방향
                Serial.println("Motor 2: Rotating Clockwise");
                motor2.step(stepsPerRevolution / 6); // 모터 2 시계 방향으로 60도 회전
                client.println("Motor 2 CW completed");
            } else if (command == '4') {  // 모터 2 반시계 방향
                Serial.println("Motor 2: Rotating Counter-Clockwise");
                motor2.step(-stepsPerRevolution / 6); // 모터 2 반시계 방향으로 60도 회전
                client.println("Motor 2 CCW completed");
            } else {
                Serial.println("Invalid command received.");
                client.println("Unknown command");
            }
        }
    }

    client.stop();  // 연결 종료
    delay(100);
}
