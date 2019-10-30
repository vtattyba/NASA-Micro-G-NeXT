// Author : Imon Tatar

int scale = 3; //scale of the accelerometer measured in g
boolean micro_is_5v = true;

void setup() {
  Serial.begin(115200);

}



void loop() {
  //get raw data for each axis in the form of voltage outputs
   int rawX,rawY,rawZ;
   float scaledX,scaledY,scaledZ;
   if (micro_is_5v)
   {
      scaledX = mapf(rawX, 0, 675, -scale, scale);
      scaledY = mapf(rawY, 0, 675, -scale, scale);
      scaledZ = mapf(rawZ, 0, 675, -scale, scale);
   }
   else
   {
      scaledX = mapf(rawX, 0, 1023, -scale, scale);
      scaledY = mapf(rawY, 0, 1023, -scale, scale);
      scaledZ = mapf(rawZ, 0, 1023, -scale, scale);
   }


  float magnitude;
  magnitude = sqrt(sq(scaledX)+sq(scaledY)+sq(scaledZ));
  
  Serial.print("Magnitude: "); Serial.print(magnitude);Serial.println(" g");
   
  if (magnitude > 3){   //magnitude threshold subject to change
    Serial.print("Collision Detected");
    //in the final project, when a collision is detected it'll
    //switch a boolean value, for example collision, from false to true
    //and the system will initiate
  }
  

}

double mapf(double val, double in_min, double in_max, double out_min, double out_max) {
    return (val - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}
