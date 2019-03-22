
// Subrutine to test communication
void activateRadioCommunication() {
  Serial.println("Waiting for Control Station to respond");
  unsigned int len = chibiGetData(CHB_MAX_PAYLOAD);

  // wait untill any data is received from Control Station or timeout
  unsigned long timeRunning = millis() + timeOut;
  while (len == 0 && timeRunning > millis()) {
    len = chibiGetData(CHB_MAX_PAYLOAD);
    Serial.println("No data received");
    delay(200);
    chibiTx(BROADCAST_ADDR, "C", 2);
  }
  if (len == 0) {
    Serial.println("Time Out... Sending Data");
  } else {
    Serial.print("Data received!: ");
    Serial.println(len);
    // Answer to Control Station
    chibiTx(BROADCAST_ADDR, TestBuf, 2);
    conectionOK = true;
  }
}

// Subrutine to send data from remote station
void SendData() {
  // Convert sensors value from float to char array and concatenate data into the format P0.000T000.00E000.00F
  /*dtostrf(Tiempo, 8, 0, TiempoChar);
  String str1(TiempoChar);
  
  dtostrf(Pressure, 5, 3, PressureChar);
  String str2(PressureChar);

  dtostrf(Temperature, 6, 2, TemperatureChar);
  String str3(TemperatureChar);

  dtostrf(Thrust, 6, 2, ThrustChar);
  String str4(ThrustChar);
  */
  //String Send = "M" + str1 + "P" + str2 + "T" + str3 + "E" + str4 + "F";
  String Send = "M," + String(Tiempo) + "," + String(int(Pressure*1000)) + "," + String(int(Temperature*100)) + "," + String(int(Thrust*1000)) + ",F";
  
  Len = Send.length()+1;
  Send.toCharArray(Buf, Len);

  // Broadcast data
  chibiTx(BROADCAST_ADDR, Buf, Len);

  // Check what is being broadcasted
  Serial.println(Send);
}

