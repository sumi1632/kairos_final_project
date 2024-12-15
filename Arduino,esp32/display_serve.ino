#include <SD.h>
#include <LCDWIKI_GUI.h>
#include <LCDWIKI_KBV.h>
#include <TouchScreen.h>

// LCD 초기화
LCDWIKI_KBV my_lcd(ILI9486, A3, A2, A1, A0, A4);

// SD 카드 핀 설정
#define SD_CS 10 // SD 카드의 CS 핀에 연결된 핀 번호

#define YP A3
#define XM A2
#define YM 9
#define XP 8

// 버튼 위치 및 크기
int buttonX = 95;
int buttonY = 180;
int buttonWidth = 300;
int buttonHeight = 100;
#define BTNCOLOR 0xFEC0

#define MINPRESSURE 10
#define MAXPRESSURE 1000

//touch sensitivity for X
#define TS_MINX 906
#define TS_MAXX 116

//touch sensitivity for Y
#define TS_MINY 92
#define TS_MAXY 952

int isReturnning = 0;

// BMP 헤더 크기
#define BMP_SIGNATURE 0x4D42

TouchScreen ts = TouchScreen(XP, YP, XM, YM, 300);

void drawBMP(const char* filename, int x, int y) {
    File bmpFile = SD.open(filename);
    if (!bmpFile) {
        Serial.println("BMP 파일을 열 수 없습니다.");
        return;
    }

    uint16_t signature;
    bmpFile.read((uint8_t*)&signature, 2);
    if (signature != BMP_SIGNATURE) {
        Serial.println("BMP 파일이 아닙니다.");
        bmpFile.close();
        return;
    }

    bmpFile.seek(18); // 이미지 크기 정보 위치로 이동
    int32_t bmpWidth, bmpHeight;
    bmpFile.read((uint8_t*)&bmpWidth, 4);
    bmpFile.read((uint8_t*)&bmpHeight, 4);

    bmpFile.seek(54); // 픽셀 데이터 시작 위치로 이동

    for (int row = 0; row < bmpHeight; row++) {
        for (int col = 0; col < bmpWidth; col++) {
            uint8_t b = bmpFile.read();
            uint8_t g = bmpFile.read();
            uint8_t r = bmpFile.read();
            uint16_t color = my_lcd.Color_To_565(r, g, b);
            my_lcd.Set_Draw_color(color);
            my_lcd.Draw_Pixel(x + col, y + (bmpHeight - row - 1));
        }
    }

    bmpFile.close();
}

void drawSpeechBubble(int x, int y, int width, int height, uint16_t borderColor, uint16_t bgColor, const char* line1, const char* line2) {
    my_lcd.Set_Draw_color(borderColor);
    my_lcd.Fill_Rectangle(x, y, x + width, y + height);

    my_lcd.Set_Draw_color(bgColor);
    int border = 4;
    my_lcd.Fill_Rectangle(x + border, y + border, x + width - border, y + height - border);

    my_lcd.Set_Text_Mode(1);
    my_lcd.Set_Text_Size(2);
    my_lcd.Set_Text_colour(0x0000);
    my_lcd.Print_String(line1, x + 20, y + 20);
    my_lcd.Print_String(line2, x + 20, y + 50);
}

void drawButton(int x, int y, int width, int height, uint16_t textColor, uint16_t fillColor, const char* text) {
    my_lcd.Set_Draw_color(fillColor);
    my_lcd.Fill_Rectangle(x, y, x + width, y + height);

    my_lcd.Set_Text_Mode(1);
    my_lcd.Set_Text_Size(4);
    my_lcd.Set_Text_colour(textColor);
    int textX = x + (width / 2) - 70;
    int textY = y + (height / 2) - 15;
    my_lcd.Print_String(text, textX, textY);
}

void setup() {
    Serial.begin(9600);
    if (!SD.begin(SD_CS)) {
        Serial.println("SD 카드 초기화 실패!");
        while (1);
    }

    my_lcd.Init_LCD();
    my_lcd.Set_Rotation(1);
    my_lcd.Fill_Screen(0xFFFF);

    drawBMP("image.bmp", 20, 20);
    drawSpeechBubble(180, 20, 280, 100, 0xFFE0, 0xFFFF, "Press the button", "after taking food :)");
    drawButton(buttonX, buttonY, buttonWidth, buttonHeight, 0xFFFF, BTNCOLOR, "RETURN");
}

void loop() {
    digitalWrite(13, HIGH);
    TSPoint p = ts.getPoint();
    digitalWrite(13, LOW);
    pinMode(XM, OUTPUT);
    pinMode(YP, OUTPUT);

    if (isReturnning == 0 && p.z > MINPRESSURE && p.z < MAXPRESSURE) {
        int touchX = map(p.x, TS_MINX, TS_MAXX, 0, 320);
        int touchY = map(p.y, TS_MINY, TS_MAXY, 0, 480);

        if (touchX > buttonX && touchX < buttonX + buttonWidth &&
            touchY > buttonY && touchY < buttonY + buttonHeight) {
            drawButton(buttonX, buttonY, buttonWidth, buttonHeight, 0xFFFF, 0xF7B0, "RETURN");
            isReturnning = 1;
            delay(100);
            drawSpeechBubble(180, 20, 280, 100, 0xFFE0, 0xFFFF, "Thank you!", "Enjoy your meal!");
            drawButton(buttonX, buttonY, buttonWidth, buttonHeight, 0xFFFF, BTNCOLOR, "RETURN");
            Serial.println("return");
            delay(3000);
            drawSpeechBubble(180, 20, 280, 100, 0xFFE0, 0xFFFF, "Press the button", "after taking food :)");
            isReturnning = 0;
        }
    }
}
