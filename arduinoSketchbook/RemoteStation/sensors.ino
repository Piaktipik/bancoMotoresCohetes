
// Function to map a value x from one range between [FromMin,FromMax] to another range between [ToMin, ToMax] with float variables
float MapValue(float Value, float FromMin, float FromMax, float ToMin, float ToMax) {
  return (Value - FromMin) * (ToMax - ToMin) / (FromMax - FromMin) + ToMin;
}

// Subrutine to acquire pressure value from DPH-L114 sensor
void GetPressureData() {
  // Read pressure value from sensor
  //Pressure = analogRead(PressureAOUT);
  Pressure = analogRead(PressureAOUT);
  // Map value from Arduino's ADC to sensor pressure range
  //Pressure = MapValue(Pressure, 206, 1023, 0.0, 9.8);
  Pressure = MapValue(Pressure, 0, 1023, 0, 9.8);
  //Delay to read next value
  //delay(200);
}

// Subrutine to acquire temperature value from max6675 module
void GetTemperatureData() {
  // Read temperature value from sensor
  Temperature = thermocouple.readCelsius();
  //Temperature = analogRead(A4);
  //Temperature = MapValue(Temperature, 0, 1023, 0, 999.0);
  //Delay to read next value
  //delay(200);
}

// Subrutine to acquire temperature value from max6675 module
void GetThrustData() {
  // Read temperature value from sensor
  Thrust = scale.get_units(NumToAve);
  //Thrust = analogRead(A1);
  //Thrust = MapValue(Thrust, 0, 1023, 0, 999.0);
  //Delay to read next value
  //delay(200);
}

// Subrutine to check if any sensor is failing
void CheckSensors() {

  // Read data from sensors
  GetPressureData();
  GetTemperatureData();
  GetThrustData();

  //Serial.println("\t" + String(Pressure) + "\t\t" + String(Temperature) + "\t\t" + String(Thrust));

  if (Pressure == -2.47) {
    ErrorList[0] = '1'; Stop = 1;
  } else ErrorList[0] = '0';
  if (Thrust < -1) {
    ErrorList[1] = '1'; Stop = 1;
  } else ErrorList[1] = '0';
  if (isnan(Temperature)) {
    ErrorList[2] = '1'; Stop = 1;
  } else ErrorList[2] = '0';
  if (Temperature == 0) {
    ErrorList[3] = '1'; Stop = 1;
  } else ErrorList[3] = '0';
  if (ErrorList[0] == '0' && ErrorList[1] == '0' && ErrorList[2] == '0' && ErrorList[3] == '0') Stop = 0;
}

