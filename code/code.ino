#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>

TwoWire i2cPort2 = TwoWire(1);

Adafruit_BNO055 bno1 = Adafruit_BNO055(55);
Adafruit_BNO055 bno2 = Adafruit_BNO055(55, 0x28, &i2cPort2);

void setup(void) 
{
  Serial.begin(115200);
  i2cPort2.begin(32, 33, 100000);
  Serial.println("Knee Angle Flexion Test"); Serial.println("");
  
  /* Initialise the sensor */
  if(!bno1.begin() || !bno2.begin())
  {
    /* There was a problem detecting the BNO055 ... check your connections */
    Serial.print("Ooops, no BNO055 detected ... Check your wiring or I2C ADDR!");
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

  // check if sensors are worn correctly
  // sensorLocationCal();

}

void loop(void) 
{
  // continuously get knee flexion angle averaged across 50 samples
  // Serial.print("Knee flexion angle: ");
  Serial.print(getKneeAngle(10));

  // get force applied from heel
  // Serial.print("\t");
  // getForce();

  Serial.println("");
  delay(100);
}

void sensorLocationCal(void) {
  /* Checks if the sensors are placed in the correct spot. Orientation angles
  are used to approximate if sensors are aligned. */
  
  int count = 0;

  // continues to sample until user correctly places sensors over 1000 consecutive samples
  while (count < 100) {
    float kneeAngle = getKneeAngle(100);
    
    // just for debugging purposes
    Serial.print("Knee angle: ");
    Serial.print(kneeAngle);
    Serial.println("");

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

    float thighZ = event1.orientation.z;
    float shinZ = event2.orientation.z;

    if (thighZ >= 0 && shinZ >= 0) {
      sum += shinZ - thighZ;
    }
    else if (thighZ < 0 && shinZ < 0) {
      sum += (360-abs(shinZ)) - (360-abs(thighZ));
    }
    else if (thighZ < 0 && shinZ > 0) {
      sum += shinZ + abs(thighZ);
    }
    else if (thighZ > 0 && shinZ < 0) {
      sum += (360-abs(shinZ)) - thighZ;
    }
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

  Serial.print("The force sensor value = ");
  Serial.print(analogReading); // print the raw analog reading

  if (analogReading < 3900)   
    Serial.println(" -> no pressure");
  else 
    Serial.println(" -> big squeeze");

}