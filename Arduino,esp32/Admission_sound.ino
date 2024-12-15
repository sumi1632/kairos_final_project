#include <Arduino.h>
#include "DYPlayerArduino.h"

// DYPlayer 모듈 초기화
DY::Player player;

// 센서 핀 정의
#define SENSOR_A0 A0
#define SENSOR_A1 A1

// 센서 감지 임계값
#define THRESHOLD 400

// 상태 변수
enum State { IDLE, A0_DETECTED, A1_DETECTED };
State currentState = IDLE;

void setup() {
    // DYPlayer 초기화
    player.begin();
    player.setVolume(30);

    // 센서 핀 설정
    pinMode(SENSOR_A0, INPUT);
    pinMode(SENSOR_A1, INPUT);

    Serial.begin(9600);
}

void loop() {
    // 센서 값 읽기
    int sensorValueA0 = analogRead(SENSOR_A0);
    int sensorValueA1 = analogRead(SENSOR_A1);

    switch (currentState) {
        case IDLE:
            if (sensorValueA0 > THRESHOLD) {
                Serial.println("A0 detected!");
                currentState = A0_DETECTED;
            } else if (sensorValueA1 > THRESHOLD) {
                Serial.println("A1 detected!");
                currentState = A1_DETECTED;
            }
            break;

        case A0_DETECTED:
            if (sensorValueA1 > THRESHOLD) {
                Serial.println("Entrance detected! Playing track 1.");
                player.playSpecified(1); // 1번 트랙 재생
                delay(5000); // 트랙 재생 대기
                currentState = IDLE; // 상태 초기화
            }
            break;

        case A1_DETECTED:
            if (sensorValueA0 > THRESHOLD) {
                Serial.println("Exit detected! Playing track 2.");
                player.playSpecified(2); // 2번 트랙 재생
                delay(5000); // 트랙 재생 대기
                currentState = IDLE; // 상태 초기화
            }
            break;
    }
}
