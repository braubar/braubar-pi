//Libraries:

// LCD
#include <LiquidCrystal.h> //Library für LCD
LiquidCrystal lcd(12, 11, 5, 4, 3, 2); //Pins für LCD

// Temperatursensor
#include <OneWire.h> //Library f. Dallas DS18B20
OneWire ds(10); //gelbes Kabel an Pin 10 (Temperatursensor1)
OneWire ds2(13); // blaues Kabel an Pin 13 (Temperatursensor2)

// Funksteuerung
#include <RCSwitch.h> // Library f. Funksender
RCSwitch mySwitch = RCSwitch();

// Variablen:
float soll = 78.25; //Solltemperatur
float ist1; //Isttemperatur1
float ist2; // Isttemperatur2
float diff1; //Temperaturdifferenz1
float diff2; //Temperaturdifferenz2
#define TempUp 9 // Pin für Temperaturerhöhung
#define TempDown 8 // Pin für Temperatursenkung
int StatusUp;
int StatusDown;

// Konstanten
const float Toleranz = 0.1; // Toleranz für Temperaturabweichung in °C.

void setup()
{
  lcd.begin(16, 2); //LCD hat 16 Spalten und 2 Zeilen
  Serial.begin(9600);  //Serielle Übertragung aktivieren mit Baudrate

  mySwitch.enableTransmit(7); //Funksender ist an Pin 7
  pinMode(TempDown, INPUT); // Zum Erniedrigen von Temperatur
  pinMode(TempUp, INPUT); // Zum Erhöhen der Temperatur
}

void loop() {
  ist1 = getTemp(); // Aktuelle Temperatur1
  ist2 = getTemp2();
  Serial.println(soll);
  Serial.println(ist1);
  Serial.println(ist2);
  // Taster abfragen
  StatusUp = digitalRead(TempUp);
  StatusDown = digitalRead(TempDown);
  // ggf. Sollwert ändern
  if (StatusUp == HIGH) {
    soll = soll + 0.25;
  }
  if (StatusDown == HIGH) {
    soll = soll - 0.25;
  }
  // Sollwert seriell ändern
  if (Serial.available() > 0) {
    soll = Serial.parseInt(); // nur int auslesen
  }

  // Ist- und Sollwerte auf LCD anzeigen
  lcd.clear();
  lcd.print("i1:");
  lcd.print(ist1,1);
  lcd.print(" i2:");
  lcd.print(ist2,1);
  lcd.setCursor(0, 1);
  lcd.print("soll:");
  lcd.print(soll);
  lcd.print((char)223);
  lcd.print("C");


  // Regelung
  diff1 = soll - ist1;
  if (diff1 >= Toleranz) {
    mySwitch.switchOn(2, 2);
  }
  else {
    mySwitch.switchOff(2, 2);
  }
  
  diff2 = soll - ist2;
  if (diff2 >= Toleranz) {
    mySwitch.switchOn(3, 3);
  }
  else {
    mySwitch.switchOff(3, 3);
  }


  // Ende Schleife
}

// Temperatur1 aus Sensor erfassen
float getTemp() {
  byte i;
  byte present = 0;
  byte type_s = 0; // für DS18B20
  byte data[12];
  byte addr[8];
  float celsius;

  if ( !ds.search(addr)) {
    //Serial.println("No more addresses.");
    //Serial.println();
    ds.reset_search();
    //delay(2000);
  }

  if (OneWire::crc8(addr, 7) != addr[7]) {
    Serial.println("CRC is not valid!");
  }
  //Serial.println();

  ds.reset();
  ds.select(addr);
  ds.write(0x44, 1); //Konversion starten

  delay(1000); //hier reichen evtl auch 750ms

  present = ds.reset();
  ds.select(addr);
  ds.write(0xBE);

  for ( i = 0; i < 9; i++) { //9 bytes auslesen
    data[i] = ds.read();
  }

  // Daten in Temperatur umwandeln

  int16_t raw = (data[1] << 8) | data[0];
  byte cfg = (data[4] & 0x60);
  if (cfg == 0x00) raw = raw & ~7; //9 bit Auflösung, 93,75ms
  else if (cfg == 0x20) raw = raw & ~3; //10 bit Aufklösung, 187,5ms
  else if (cfg == 0x40) raw = raw & ~1; //11 bit Auflösung, 375ms

  // Sollte es nicht gehen, mit 12 bit Auflösung probieren:

  /*
  if (type_s){
   raw = raw << 3; // noch 9 bit Auflösung
   if (data[7] == 0x10) {
   raw = (raw & 0xFFF0) +12 -data[6];
   }
   }

   */

  celsius = (float)raw / 16.0;


  /*Serial.println(celsius);
   Serial.print((char)176);
   Serial.println("C");
   Serial.println(oeff);
   */

  return (celsius);

}

// Temperatur2 aus Sensor erfassen
float getTemp2() {
  byte i;
  byte present = 0;
  byte type_s = 0; // für DS18B20
  byte data[12];
  byte addr[8];
  float celsius;

  if ( !ds2.search(addr)) {
    //Serial.println("No more addresses.");
    //Serial.println();
    ds2.reset_search();
    //delay(2000);
  }

  if (OneWire::crc8(addr, 7) != addr[7]) {
    Serial.println("CRC is not valid!");
  }
  //Serial.println();

  ds2.reset();
  ds2.select(addr);
  ds2.write(0x44, 1); //Konversion starten

  delay(1000); //hier reichen evtl auch 750ms

  present = ds2.reset();
  ds2.select(addr);
  ds2.write(0xBE);

  for ( i = 0; i < 9; i++) { //9 bytes auslesen
    data[i] = ds2.read();
  }

  // Daten in Temperatur umwandeln

  int16_t raw = (data[1] << 8) | data[0];
  byte cfg = (data[4] & 0x60);
  if (cfg == 0x00) raw = raw & ~7; //9 bit Auflösung, 93,75ms
  else if (cfg == 0x20) raw = raw & ~3; //10 bit Aufklösung, 187,5ms
  else if (cfg == 0x40) raw = raw & ~1; //11 bit Auflösung, 375ms

  // Sollte es nicht gehen, mit 12 bit Auflösung probieren:

  /*
  if (type_s){
   raw = raw << 3; // noch 9 bit Auflösung
   if (data[7] == 0x10) {
   raw = (raw & 0xFFF0) +12 -data[6];
   }
   }

   */

  celsius = (float)raw / 16.0;


  /*Serial.println(celsius);
   Serial.print((char)176);
   Serial.println("C");
   Serial.println(oeff);
   */

  return (celsius);

}





