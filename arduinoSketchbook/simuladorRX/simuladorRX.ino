
// Data to be sent and received
//char Send[21];                     //P0.000T000.00E000.00
char PressureChar[5];
char TemperatureChar[6];
char ThrustChar[6];
//byte Receive[CHB_MAX_PAYLOAD];

// Sensors values
unsigned long Tiempo = 0;
float Pressure = 0, Thrust = 0, Temperature = 0;

float angle = 0;

void setup() {
  // Begin serial communiation
  Serial.begin(115200);
  // put your setup code here, to run once:

}

void loop() {
  // put your main code here, to run repeatedly:
  Tiempo = millis();
  angle = (float(Tiempo)/1000)*PI;
  Pressure = 100*sin(angle);
  Temperature = 900*sin(angle);
  Thrust = 500*tan(angle);
  delay(20);
  SendData();
}

void SendData() {
  // Convert sensors value from float to char array and concatenate data into the format P0.000T000.00E000.00F

  String Send = "M," + String(Tiempo) + "," + String(long(Pressure*1000)) + "," + String(long(Temperature*100)) + "," + String(long(Thrust*1000)) + ",F";
  
  Serial.println(Send);
  //Send.toCharArray(Buf, Len);

  // Broadcast data
  //chibiTx(BROADCAST_ADDR, Buf, Len);

  // Check what is being broadcasted
  //Serial.println(Buf);
}
