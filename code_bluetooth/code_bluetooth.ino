#include "BluetoothSerial.h"

#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>

TwoWire i2cPort2 = TwoWire(1);

Adafruit_BNO055 bno1 = Adafruit_BNO055(55);
Adafruit_BNO055 bno2 = Adafruit_BNO055(55, 0x28, &i2cPort2);

BluetoothSerial SerialBT;

void setup(void) 
{

  SerialBT.begin("EsP32 Bluetooth - Team 11");
  Serial.begin(115200);
  i2cPort2.begin(32, 33, 100000);
  SerialBT.println("Knee Angle Flexion Test"); Serial.println("");
  
  /* Initialise the sensor */
  if(!bno1.begin() || !bno2.begin())
  {
    /* There was a problem detecting the BNO055 ... check your connections */
    SerialBT.print("Ooops, no BNO055 detected ... Check your wiring or I2C ADDR!");
    while(1);
  }
  
  // set crystals
  bno1.setExtCrystalUse(true);
  bno2.setExtCrystalUse(true);

  // pin 27 - red LED, pin 14 - green LED
  pinMode(27, OUTPUT);
  pinMode(14, OUTPUT);

  // initially set led lights
  digitalWrite(27, HIGH);
  digitalWrite(14, LOW);

  // check if system is calibrated
  systemCal();

  // check if sensors are worn correctly
  sensorLocationCal();
}

void loop(void) 
{
  // continuously get knee flexion angle averaged across 50 samples
  SerialBT.print("Knee flexion angle: ");
  SerialBT.print(getKneeAngle(10));

  // get force applied from heel
  SerialBT.print("\t");
  getForce();

  SerialBT.println("");
}

void systemCal(void) {
  /* Checks if system is calibrated - the system value must be greater than 1. 
  System not calibrated - red LED ON, green LED OFF
  System calibrated - red LED OFF, green LED ON */

  uint8_t system1, gyro1, accel1, mag1;
  system1 = gyro1 = accel1 = mag1 = 0;

  uint8_t system2, gyro2, accel2, mag2;
  system2 = gyro2 = accel2 = mag2 = 0;

  // if not calibrated, keep waiting
  while (system1 <= 1 || system2 <= 1) {
    // get calibration status
    bno1.getCalibration(&system1, &gyro1, &accel1, &mag1);
    bno2.getCalibration(&system2, &gyro2, &accel2, &mag2);
  }

  // if calibrated, turn off red, turn on green
  digitalWrite(27, LOW);
  digitalWrite(14, HIGH);

  // ensure user sees led
  delay(5000);

  digitalWrite(27, HIGH);
  digitalWrite(14, LOW);
}

void sensorLocationCal(void) {
  /* Checks if the sensors are placed in the correct spot. Orientation angles
  are used to approximate if sensors are aligned. */
  
  int count = 0;

  // continues to sample until user correctly places sensors over 1000 consecutive samples
  while (count < 100) {
    float kneeAngle = getKneeAngle(10);
    
    // just for debugging purposes
    SerialBT.print("Knee angle: ");
    SerialBT.print(kneeAngle);
    SerialBT.println("");

    // if absolute difference less than 5 degrees, add to count
    if (abs(kneeAngle) <= 5) {
      count += 1;
    }
    // restart     
    else {
      count = 0;
    }  
  }
  
  // if properly placed, turn on green, turn off red
  digitalWrite(27, LOW);
  digitalWrite(14, HIGH);
}

float getKneeAngle(int numSamples) {
  /* Gets knee angle average across numSamples */
  sensors_event_t event1; 
  sensors_event_t event2; 
  float sum = 0;

  for (int i=0; i<=numSamples; i++) {
    bno1.getEvent(&event1);
    bno2.getEvent(&event2);
    sum += event2.orientation.x - event1.orientation.x;
  }

  // for debugging purposes
  // Serial.print("\tX: ");
  // Serial.print(event1.orientation.x, 4);
  // Serial.print("\tY: ");
  // Serial.print(event1.orientation.y, 4);
  // Serial.print("\tZ: ");
  // Serial.print(event1.orientation.z, 4);
  // Serial.print("\n");
  // Serial.print("\tX2: ");
  // Serial.print(event2.orientation.x, 4);
  // Serial.print("\tY2: ");
  // Serial.print(event2.orientation.y, 4);
  // Serial.print("\tZ2: ");
  // Serial.print(event2.orientation.z, 4);
  // Serial.print("\n");
  
  return sum/numSamples;
}

void getForce(void) {
  int analogReading = analogRead(36);

  SerialBT.print("The force sensor value = ");
  SerialBT.print(analogReading); // print the raw analog reading

  if (analogReading < 3900)       // from 0 to 9
    SerialBT.println(" -> no pressure");
  else // from 800 to 1023
    SerialBT.println(" -> big squeeze");

}
