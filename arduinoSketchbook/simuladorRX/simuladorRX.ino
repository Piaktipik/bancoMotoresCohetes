
// Data to be sent and received
//char Send[21];                     //P0.000T000.00E000.00
char PressureChar[5];
char TemperatureChar[6];
char ThrustChar[6];
//byte Receive[CHB_MAX_PAYLOAD];

// Sensors values
float Pressure = 0, Thrust = 0, Temperature = 0;

void setup() {
  // Begin serial communiation
  Serial.begin(38400);
  // put your setup code here, to run once:

}

void loop() {
  // put your main code here, to run repeatedly:
  Pressure = random(1, 1000);
  Temperature = random(15, 300);
  Thrust = random(0, 200);
  delay(500);
  SendData();
}

void SendData() {
  // Convert sensors value from float to char array and concatenate data into the format P0.000T000.00E000.00F
  dtostrf(Pressure, 5, 3, PressureChar);
  String str1(PressureChar);
 
  dtostrf(Temperature, 6, 2, TemperatureChar);
  String str2(TemperatureChar);

  dtostrf(Thrust, 6, 2, ThrustChar);
  String str3(ThrustChar);

  String Send = "P" + str1 + "T" + str2 + "E" + str3 + "F";

  Serial.println(Send);
  //Send.toCharArray(Buf, Len);

  // Broadcast data
  //chibiTx(BROADCAST_ADDR, Buf, Len);

  // Check what is being broadcasted
  //Serial.println(Buf);
}
