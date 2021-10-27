#include "I2Cdev.h"
#include "MPU6050.h"
#include "Wire.h"

//------------------------//
//I2C:                    //
//  SDA - D2 GPIO4 yellow //
//  SCL - D1 GPIO5 green  //
//------------------------//
//ADDRESS WIRE COLORS:    //
//  shoulder - gray       //
//  wrist - brown         //
//  hand - white          //
//------------------------//
//WEMOS D1 MINI GPIO:     //
//  D5 - 14               //
//  D6 - 12               //
//  D7 - 13               //
//  D8 - 15               //
//------------------------//
//OUTPUT_DATA:
//  shoulderX/shoulderZ/absoluteX/absoluteY/wristX/handX/handY/gripPercent
//  shoulderX/shoulderZ/absoluteX/absoluteY/wristX/E/Q/F
//------------------------//

#define SHOULDER D6
#define WRIST D8
#define HAND D7

#define TO_DEG 57.2957f

#define TIME_GYRO 2000
#define CALIBRATE_NUM 200
#define SENSORS_AMOUNT 3

#define FK 0.2

char output[100];
String output_str;

long int timer;

float testFilterY = 0.0;

float returned_zero_gx, returned_zero_gy, returned_zero_gz; //возвращаемые функцией getAngle() значения
//калибровочные значения гироскопа
float shoulder_zero_gx, shoulder_zero_gy, shoulder_zero_gz; //плеча
float wrist_zero_gx, wrist_zero_gy, wrist_zero_gz; //предплечья
float hand_zero_gx, hand_zero_gy, hand_zero_gz; //кисти

float returned_gx, returned_gy, returned_gz; //возвращаемые функцией getAngle() значения
//глобальные значения гироскопов
float shoulder_gx, shoulder_gy, shoulder_gz; //плеча
float wrist_gx, wrist_gy, wrist_gz; //предплечья
float hand_gx, hand_gy, hand_gz; //кисти

MPU6050 accgyro(0x69);

float filter(float newVal){
  static float filtVal = 0;
  filtVal += (newVal - filtVal) * 0.09;
  return filtVal;
  }

//функция калибровки гироскопа
void callibrateMPU() {
  int i = 0;
  int16_t raw_gx, raw_gy, raw_gz;

  while (i < CALIBRATE_NUM) {
    if (timer < micros()) {
      timer = micros() + TIME_GYRO;
      accgyro.getRotation(&raw_gx, &raw_gy, &raw_gz);
      returned_zero_gx += raw_gx;
      returned_zero_gy += raw_gy;
      returned_zero_gz += raw_gz;
      i++;
    }
  }
  returned_zero_gx /= CALIBRATE_NUM;
  returned_zero_gy /= CALIBRATE_NUM;
  returned_zero_gz /= CALIBRATE_NUM;
}

void setup() {
  pinMode(SHOULDER, OUTPUT);
  pinMode(WRIST, OUTPUT);
  pinMode(HAND, OUTPUT);

  Wire.begin();
  Serial.begin(9600);

  digitalWrite(SHOULDER, 1);
  digitalWrite(WRIST, 1);
  digitalWrite(HAND, 1);
  accgyro.initialize();

  digitalWrite(SHOULDER, 1);
  digitalWrite(WRIST, 0);
  digitalWrite(HAND, 0);
  callibrateMPU();
  shoulder_zero_gx = returned_zero_gx;
  shoulder_zero_gy = returned_zero_gy;
  shoulder_zero_gz = returned_zero_gz;

  digitalWrite(SHOULDER, 0);
  digitalWrite(WRIST, 1);
  digitalWrite(HAND, 0);
  callibrateMPU();
  wrist_zero_gx = returned_zero_gx;
  wrist_zero_gy = returned_zero_gy;
  wrist_zero_gz = returned_zero_gz;

  digitalWrite(SHOULDER, 0);
  digitalWrite(WRIST, 0);
  digitalWrite(HAND, 1);
  callibrateMPU();
  hand_zero_gx = returned_zero_gx;
  hand_zero_gy = returned_zero_gy;
  hand_zero_gz = returned_zero_gz;
}

void getAngle(byte num, float last_gx, float last_gy, float last_gz, float zero_gx, float zero_gy, float zero_gz) {
  //получение сырых данных
  int16_t raw_ax, raw_ay, raw_az;
  int16_t raw_gx, raw_gy, raw_gz;
  accgyro.getMotion6(&raw_ax, &raw_ay, &raw_az, &raw_gx, &raw_gy, &raw_gz);

  //получение угла с акселлерометра
  float ax, ay, az;
  float angle_ax, angle_ay, angle_az;

  ax = raw_ax / 16384.0;
  ay = raw_ay / 16384.0;
  az = raw_az / 16384.0;

  angle_ax = TO_DEG * atan2(ay, az);
  angle_ay = TO_DEG * atan2(ax, az);

  //получение угла с гироскопа
  float gx, gy, gz;

  gx = (raw_gx - zero_gx) / 131.0;
  gy = (raw_gy - zero_gy) / 131.0;
  gz = (raw_gz - zero_gz) / 131.0;

  returned_gx = last_gx + gx * TIME_GYRO / 1000000.0;
  returned_gy = last_gy + gy * TIME_GYRO / 1000000.0;
  returned_gz = last_gz + gz * TIME_GYRO / 1000000.0;

  // комплиентарный фильтр
  returned_gx = returned_gx * (1 - FK) + angle_ax * FK;
  returned_gy = returned_gy * (1 - FK) + angle_ay * FK;

  // абсолютные координаты
  const int shoulderLenght = 330, wristLenght = 320, handLenght = 170;
  static float absX, absY = 400, absZ, ZAngle;
  
  switch (num) {
    case 0:// shoulder
      absX += shoulderLenght * cos(radians(returned_gy));
      absY += shoulderLenght * sin(radians(-returned_gy));
      ZAngle = returned_gz * 60;
      output_str += String(-returned_gy, 2); output_str += String("/");
      output_str += String(ZAngle, 2); output_str += String("/");
      break;
    case 1:// wrist
      absX += wristLenght * cos(radians(returned_gy));
      absY += wristLenght * sin(radians(-returned_gy));
      
      output_str += String(-returned_gy, 2); output_str += String("/");
      break;
    case 2:// hand
      absX += handLenght * cos(radians(returned_gy));
      absY += handLenght * sin(radians(-returned_gy));
      absZ = absX * sin(radians(ZAngle));
      absX *= cos(radians(ZAngle));
      output_str += String(absX, 2); output_str += String("/");
      output_str += String(absY, 2); output_str += String("/");
      output_str += String(absZ, 2); output_str += String("/");

      absX = 0; absY = 400;
    
      output_str += String(-returned_gy, 2); output_str += String("/");

      if (returned_gx > 21 || returned_gx < -18) {
        if (returned_gx > 21) output_str += String(constrain(map(returned_gx-21, -10, 110, 0, 100), 0, 100));
        else output_str += String(constrain(map(returned_gx+18, -50, -10, -50, 0), -50, 0));
      }
      else output_str += String(0.00);
      output_str += String("/");

      output_str += String(int(filter(constrain(map(analogRead(A0), 150, 200, 100, 0), 0, 100)))); output_str += String("/");
      output_str.toCharArray(output, 100);
      
      Serial.println(output);
      output_str.remove(0);
      delay(100);
      break;
  }

}

void loop() {
  if (timer < micros()) {
    timer = micros() + TIME_GYRO;

    for (byte i = 0; i < SENSORS_AMOUNT; i++) {
      switch (i) {
        case 0:
          digitalWrite(SHOULDER, 1);
          digitalWrite(WRIST, 0);
          digitalWrite(HAND, 0);

          getAngle(i, shoulder_gx, shoulder_gy, shoulder_gz, shoulder_zero_gx, shoulder_zero_gy, shoulder_zero_gz);

          shoulder_gx = returned_gx;
          shoulder_gy = returned_gy;
          shoulder_gz = returned_gz;
          break;
        case 1:
          digitalWrite(SHOULDER, 0);
          digitalWrite(WRIST, 1);
          digitalWrite(HAND, 0);

          getAngle(i, wrist_gx, wrist_gy, wrist_gz, wrist_zero_gx, wrist_zero_gy, wrist_zero_gz);

          wrist_gx = returned_gx;
          wrist_gy = returned_gy;
          wrist_gz = returned_gz;
          break;
        case 2:
          digitalWrite(SHOULDER, 0);
          digitalWrite(WRIST, 0);
          digitalWrite(HAND, 1);

          getAngle(i, hand_gx, hand_gy, hand_gz, hand_zero_gx, hand_zero_gy, hand_zero_gz);

          hand_gx = returned_gx;
          hand_gy = returned_gy;
          hand_gz = returned_gz;
          break;
      }
    }
  }
}
