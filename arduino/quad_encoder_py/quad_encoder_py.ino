
// This is now the DUE version 

#include <Encoder.h>

Encoder myEnc(2,3); // pick your pins, reverse for sign flip

void setup() {
  Serial.begin(115200);
  //SerialUSB.begin(115200); // for real-time feedback
  myEnc.write(0);
}

void loop() {
  long pos;
 
  pos = myEnc.read();
  if (pos != NULL) {
    Serial.println(pos);
  }
}
