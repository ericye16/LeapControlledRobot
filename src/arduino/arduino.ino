// Sweep
// by BARRAGAN <http://barraganstudio.com> 
// This example code is in the public domain.


#include <Servo.h> 

#define kLeapClawValN 50
#define kLeapWristValN 0
#define kLeapTwistValN 179
#define kLeapElbowValN -15
#define kLeapShoulderValN 0
#define kLeapBaseValN 0

Servo servo_claw; // ?80 - ?100
Servo servo_wrist; // 0 - 180
Servo servo_twist; // 0 - 180
Servo servo_elbow; // 40 - 150
Servo servo_shoulder; // 100 - 130
Servo servo_base; // 800 - 2200 uSec, 1500 neutral, 1400-1600 Ideal

int leapClawVal = 50; //fistedness: 0 - 100
int leapWristVal = 0; //WristYaw: -80 - 80
int leapTwistVal = 179; //WristRotation:  -130 - -180, 180 to 0
int leapElbowVal = -15; //wristPitch: -100 - 70
int leapShoulderVal = 0; //ArmPitch: -80 - 80
int leapBaseVal = 0; // -50 - 50

int pos = 0;    // variable to store the servo position 
int potpin = 0; 
int ledPin = 13;
int minpos = 100;
int maxpos = 130;

void setup() { 
  Serial.begin(9600);
  pinMode(ledPin,OUTPUT);
  
  servo_claw.attach(3);  // attaches the servo on pin 9 to the servo object 
  servo_wrist.attach(5);
  servo_twist.attach(6);
  servo_elbow.attach(9);
  servo_shoulder.attach(10);
  servo_base.attach(11);
 
} 
 
 
void loop() { 
  if (Serial.available() <= 0) {
    digitalWrite(ledPin, HIGH);
    //delay(50);
    return;
  }
  
  int startByte = Serial.read();
  if (startByte != '\x02') {
    digitalWrite(ledPin, HIGH);
    //delay(50); 
    return;
  }
  
  leapElbowVal = readNextInteger(kLeapElbowValN);
  leapTwistVal = readNextInteger(kLeapTwistValN);
  leapWristVal = readNextInteger(kLeapWristValN);
  leapClawVal = readNextInteger(kLeapClawValN);
  leapShoulderVal = readNextInteger(kLeapShoulderValN);
  leapBaseVal = readNextInteger(kLeapBaseValN);
  
  char leapBytes[100] = {0};
  Serial.readBytesUntil('\x03', leapBytes, sizeof(leapBytes));
  
  leapClawVal = map(leapClawVal, 0, 100, 100, 35);
  leapWristVal = map(leapWristVal, -80, 80, 0, 180);
  
  // New Range: -50 - 180
  if (leapTwistVal < 0) {
    leapTwistVal = -leapTwistVal - 180;  
  } else {
    leapTwistVal = -leapTwistVal + 180;
  }
  leapTwistVal = map(leapTwistVal, -50, 180, 180, 0);

  leapElbowVal = map(leapElbowVal, -100, 70, 40, 150);
  leapShoulderVal = map(leapShoulderVal, -80, 80, 100, 130);
  leapBaseVal = map(leapBaseVal, -50, 50, 1550, 1450);
  
  servo_claw.write(leapClawVal);
  servo_wrist.write(leapWristVal);
  servo_twist.write(leapTwistVal);
  servo_elbow.write(leapElbowVal);
  servo_shoulder.write(leapShoulderVal);
  servo_base.writeMicroseconds(leapBaseVal);

} 


int readNextInteger(int defaultVal) {
    int nextInteger = Serial.parseInt();
    if (nextInteger == 0) {
      return defaultVal;
    }
    
    int newLine = Serial.read();
    if (newLine != '\n') {
      digitalWrite(ledPin, HIGH);
      // delay(20000);
    }
    return nextInteger;
 }


void testing() {
  // FOR TESTING ONLY
  for(pos = minpos; pos < maxpos; pos += 1)  // goes from 0 degrees to 180 degrees 
  {                                  // in steps of 1 degree 
    servo_shoulder.write(pos);              // tell servo to go to position in variable 'pos' 
    delay(90);        
  } 
  for(pos = maxpos; pos>=minpos; pos-=1)     // goes from 180 degrees to 0 degrees 
  {                                
    servo_shoulder.write(pos);              // tell servo to go to position in variable 'pos' 
    delay(90);      
  } 
}


// if (startByte == '\x02') {
//    digitalWrite(ledPin, HIGH);
//    delay(500);
//    digitalWrite(ledPin, LOW);
//    delay(500);
//  }
