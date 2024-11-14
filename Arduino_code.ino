#include <LiquidCrystal.h>

const int rs = 12, en = 11, d4 = 5, d5 = 4, d6 = 3, d7 = 2;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);
const int soundSensorPin = 7;
int soundDetected = 0;

void setup() {
  lcd.begin(16, 2);
  Serial.begin(9600);
  pinMode(soundSensorPin, INPUT);
}

void loop() {
  if (Serial.available() > 0) {
    lcd.clear();
    String text = Serial.readStringUntil('\n');  

    lcd.setCursor(0, 0);

    lcd.print(text.substring(0, 16));

    if (text.length() > 16) {
      lcd.setCursor(0, 1);  
      lcd.print(text.substring(16, 32)); 
    }
  }
  soundDetected = digitalRead(soundSensorPin);
  if (soundDetected == HIGH) {
    Serial.println("SOUND_DETECTED");
    delay(500); 
  }
}