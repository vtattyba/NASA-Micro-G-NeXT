// ---------------------------------------------------------------------------
// author - Tamaghan Maurya, Micro G
// ---------------------------------------------------------------------------

#include <NewPing.h>
#include <MedianFilter.h>
#include <Wire.h>


#define trig  2  // Arduino trigger pin to 2
#define LED  13  // Arduino trigger pin to 13
#define echo  3  // Arduino echo pin to 3
#define MAX_DISTANCE 450 // maximum distance stated

NewPing sonar(trig, echo, MAX_DISTANCE); // NewPing setup of pins and maximum distance.
MedianFilter filter(31,0);

unsigned int distance;

bool stop;

void setup() {
  Serial.begin(115200); // Open serial monitor at 115200 baud to see ping results.
  pinMode(LED,OUTPUT);
}

int n1 = 0;
int n2 = 0;
int n3 = 0;
int n4 = 0;
int n5 = 0;
void loop() {
digitalWrite(LED,LOW);
delay(50);                   // Wait 50ms between pings (about 20 pings/sec).
n1 = n2;
n2 = n3;
n3 = n4;
n4 = n5;
unsigned int duration = sonar.ping(); // duration time 
  filter.in(duration);
  distance = filter.out()/ US_ROUNDTRIP_CM;

  if(distance > 100 ){
           Serial.print("SENSOR IS RUNNING Dis - "); // for display purpose
           Serial.println(distance);
           n5 = 0;
        }
      
        if(distance < 100 && distance > 0 ){
            Serial.print("***WARNING*** - ");  // minimum distance attained
            Serial.println(distance);
            n5 = 1;                      
        }
        if(n1 == 1 && n2 == 1 && n3 == 1 && n4 == 1 && n5 ==1){
          Serial.print("SAVER STOPPED AT ");
          Serial.print("Distance = ");
          Serial.print(distance);
          Serial.println(" cm");
          digitalWrite(LED,HIGH);
          stop = true;                  // output variable for motors to use 
          for(;;){}               // break;
        }
}
