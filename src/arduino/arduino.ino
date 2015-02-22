// Sweep
// by BARRAGAN <http://barraganstudio.com> 
// This example code is in the public domain.


#include <Servo.h> 
 
Servo servo_claw; // ?
Servo servo_wrist; // 0 - 180
Servo servo_twist; // 0 - 180
Servo servo_elbow; // 40 - 150
Servo servo_shoulder; // ? - 150
Servo servo_base; // 800 - 2200 uSec, 1500 neutral

int pos = 0;    // variable to store the servo position 
int potpin = 0; 
int minpos = 100;
int maxpos = 100;

void setup() 
{ 
  Serial.begin(9600);
  
  servo_claw.attach(3);  // attaches the servo on pin 9 to the servo object 
  servo_wrist.attach(5);
  servo_twist.attach(6);
  servo_elbow.attach(9);
  servo_shoulder.attach(10);
  servo_base.attach(11);
 
} 
 
 
void loop() 
{ 
  servo_base.writeMicroseconds(1500);
  
//  for(pos = minpos; pos < maxpos; pos += 1)  // goes from 0 degrees to 180 degrees 
//  {                                  // in steps of 1 degree 
//    servo_elbow.write(pos);              // tell servo to go to position in variable 'pos' 
//    delay(30);        
//  } 
//  for(pos = maxpos; pos>=minpos; pos-=1)     // goes from 180 degrees to 0 degrees 
//  {                                
//    servo_elbow.write(pos);              // tell servo to go to position in variable 'pos' 
//    delay(30);      
//    
//  } 
//  
//  int val = analogRead(potpin);
//  val = map(val,0,1023,0,179);
//  servo_shoulder.write(val);
//  servo_twist.write(val);
//  delay(15);
} 
