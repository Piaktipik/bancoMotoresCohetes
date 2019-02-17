/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//------------------------------------This code reads and sends sensors value in remote station------------------------------------//
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

//------------------------------------------------Library and objets initialization------------------------------------------------//

// chibiArduino RF transceptor library
#include <chibi.h>

// Multi porpuse Arduino libraries
#include <math.h>
#include <string.h>

// No library needed for pressure sensor

// Thermocuople with max6675 module library
#include "max6675.h"

// Strain gauge with HX711 module library
#include "HX711.h"

//----------------------------------------------------------Pin connection----------------------------------------------------------//

// Pressure sensor
// BROWN to +9 - 36V, BLUE to GND, BLACK to Analog I/O (A2)

// Temperature sensor
// RED to T+, BLACK to T-

// MAX6675 module
// RED to +5V, BLACK to GND, GREEN to PWM Digital I/O (11), ORANGE to PWM Digital I/O (10), BROWN to PWM Digital I/O (9)

// Strain gauge sensor
// RED to E+, BLACK to E-, GREEN to A+, WHITE to A-

// HX711 module
// VCC to +5V, GND to GND, DT to PWM Digital I/O (7), SKK to PWM Digital I/O (8)

// Sensores pin definition
#define PressureAOUT A2     // Signal DPH-L114
#define thermoDO 11        // SEL max6675
#define thermoCS 10        // Signal max6675
#define thermoCLK 9        // Clock max6675
#define StrainGaugeDOUT 7  // Signal HX711
#define StrainGaugeCLK 8   // Clock HX711 

// Object cretion
// No object creation needed for pressure sensor

// Thermocouple object creation
MAX6675 thermocouple(thermoCLK, thermoCS, thermoDO);

// Strain gauge object creation
HX711 scale;

//------------------------------------------------------Variables definition-------------------------------------------------------//

// Data to be sent and received
//char Send[21];                     //P0.000T000.00E000.00
char PressureChar[5];
char TemperatureChar[6];
char ThrustChar[6];
byte Receive[CHB_MAX_PAYLOAD];

// Sensors values
float Pressure, Thrust, Temperature;

// Number of data to average Thrust value
int NumToAve = 10;

// Time to wait for communication setup
unsigned int TimeOut = 1;

// Size of data to send
unsigned int Len = 23;

// Data to send
char Buf[23];

// Char to send during communication test
byte TestBuf[] = "R";

// Stop if error with any sensor is detected
boolean Stop = 0;

// Activated errors
char ErrorList[4], oldErrorList[4];

// Sample time
int SampleTime = 0;

//------------------------------------------------------Subrutines definition-------------------------------------------------------//

// Subrutine to test communication
void CommunicationTest() {
  Serial.println("Waiting for Control Station to respond");
  unsigned int len = chibiGetData(Receive);

  // wait untill any data is received from Control Station
  while (len == 0) {
    len = chibiGetData(Receive);
    //Serial.println("No data received");
  }
  //Serial.println("Data received!");
  // Answer to Control Station
  delay(TimeOut * 1000);
  chibiTx(BROADCAST_ADDR, TestBuf, 2);
}

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

// Subrutine to send data from remote station
void SendData() {
  // Convert sensors value from float to char array and concatenate data into the format P0.000T000.00E000.00F
  dtostrf(Pressure, 5, 3, PressureChar);
  String str1(PressureChar);

  dtostrf(Temperature, 6, 2, TemperatureChar);
  String str2(TemperatureChar);

  dtostrf(Thrust, 6, 2, ThrustChar);
  String str3(ThrustChar);

  String Send = "P" + str1 + "T" + str2 + "E" + str3 + "F";

  Send.toCharArray(Buf, Len);

  // Broadcast data
  chibiTx(BROADCAST_ADDR, Buf, Len);

  // Check what is being broadcasted
  //Serial.println(Buf);
}

//----------------------------------------------------------Main program-----------------------------------------------------------//

void setup() {
  // Initialize transceptor
  chibiInit();

  // Begin serial communiation
  Serial.begin(9600);

  // Test communication with control station
  CommunicationTest();
  Serial.println("Communication Stablished");

  // Define Strain Gauge pins
  scale.begin(StrainGaugeDOUT, StrainGaugeCLK);

  // Set scale factor (from calibration)
  scale.set_scale(5526.95);

  // Reset signal to zero
  scale.tare();
  //
  //  CheckSensors();
  //  while (Stop) {
  //    CheckSensors();
  //    if(oldErrorList != ErrorList) chibiTx(BROADCAST_ADDR, ErrorList, 5);
  //    oldErrorList[0] = ErrorList[0];
  //    oldErrorList[1] = ErrorList[1];
  //    oldErrorList[2] = ErrorList[2];
  //    oldErrorList[3] = ErrorList[3];
  //  }

  unsigned int len = 0;
  len = chibiGetData(Receive);
  while (len != 0) {
    len = chibiGetData(Receive);
  }

  while (len == 0) {
    if (chibiDataRcvd() == true) {
      len = chibiGetData(Receive);
      //Serial.println((char *)Receive);
    }
  }
  /*
  for (int j = sizeof(Receive) - 1; j <= 0; j--) {
    SampleTime = (Receive[j] - 48) * pow(10, abs(j - (sizeof(Receive) - 1))) + SampleTime;
  } */
  SampleTime = ((Receive[0]-48)*10)+(Receive[1]-48);
  Serial.println(SampleTime);
  Serial.println("   Pressure \t Temperature \t Thrust");
}

void loop() {
  GetPressureData();
  GetTemperatureData();
  GetThrustData();
  SendData();
  Serial.println("\t" + String(Pressure) + "\t\t" + String(Temperature) + "\t\t" + String(Thrust));
  delay(SampleTime);
}
