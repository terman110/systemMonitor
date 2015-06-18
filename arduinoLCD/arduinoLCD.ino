/*
  16x2 LCD display (Hitachi HD44780)

 * LCD RS pin to digital pin 12
 * LCD Enable pin to digital pin 11
 * LCD D4 pin to digital pin 5
 * LCD D5 pin to digital pin 4
 * LCD D6 pin to digital pin 3
 * LCD D7 pin to digital pin 2
 * LCD R/W pin to ground
 * 10K resistor:
 * ends to +5V and ground
 * wiper to LCD VO pin (pin 3)

 http://www.arduino.cc/en/Tutorial/LiquidCrystalSerial
 */

// include the library code:
#include <LiquidCrystal.h>

#define BAUD 9600
#define WIDTH 16
#define HEIGHT 2
#define SIZE WIDTH*HEIGHT
#define PIN_RS 12
#define PIN_EN 11
#define PIN_D4 5
#define PIN_D5 4
#define PIN_D6 3
#define PIN_D7 2

LiquidCrystal lcd(PIN_RS, PIN_EN, PIN_D4, PIN_D5, PIN_D6, PIN_D7);
char buffer[SIZE];

void setup() {
  lcd.begin(WIDTH, HEIGHT);
  lcd.noBlink();
  lcd.noCursor();
  lcd.noAutoscroll();
  lcd.clear();
  
  Serial.begin(BAUD);
  Serial.println("System status alive");
}

void loop()
{
  if(Serial.available()) {
    delay(100);
    int i = Serial.readBytes(buffer, SIZE);
    if(i!=32) {
      Serial.println("Invalid string transmitted. Only 32 characters allowed.");
    } else {
      lcd.clear();
      lcd.setCursor(0,0);
      for( int i = 0; i < 32; ++i){
        if(i == 16){
          lcd.setCursor(0,1);
        }
        lcd.write(buffer[i]);
      }
      //lcd.print(buffer);
      Serial.print("Recevied: ");
      Serial.println(buffer);
    }
  }
  //lcd.noDisplay();
  //lcd.display();
}
