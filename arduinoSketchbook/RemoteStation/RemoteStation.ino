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
#define PressureAOUT A2    // Signal DPH-L114
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

// -------------------------- Sensors 
char TiempoChar[8];
char PressureChar[5];
char TemperatureChar[6];
char ThrustChar[6];

// Sensors values
unsigned long Tiempo = 0;
float Pressure, Thrust, Temperature;

// Number of data to average Thrust value
int NumToAve = 2;

// -------------------------- Radio 
// Data to be sent and received
//char Send[21];                    //P0.000T000.00E000.00
byte Receive[CHB_MAX_PAYLOAD];      // Vector to capture incomming data
unsigned int timeOut = 5000;        // Time to wait for communication setup
byte TestBuf[] = "R";               // Char to send during communication activation
boolean conectionOK = false;      // Used to identify the conection status
 
unsigned int Len = 23;              // Size of data to send 
char Buf[50];                       // Data to send           
boolean Stop = 0;                   // Stop if error with any sensor is detected
char ErrorList[4], oldErrorList[4]; // Activated errors
int SampleTime = 0;                 // Sample time

// ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ Initial Configurations  ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ 
void setup() {
  // Initialize transceptor
  chibiInit();
  chibiSetChannel(20);
  
  // Begin serial communiation
  Serial.begin(230400);   // Detalle consola arduino doble de la velocidad real 115200

  // Test communication with control station
  activateRadioCommunication();
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

  /*unsigned int len = 0;
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
  
    for (int j = sizeof(Receive) - 1; j <= 0; j--) {
    SampleTime = (Receive[j] - 48) * pow(10, abs(j - (sizeof(Receive) - 1))) + SampleTime;
    } */
  //SampleTime = ((Receive[0] - 48) * 10) + (Receive[1] - 48);

  // Print initial data log
  Serial.println(SampleTime);
  Serial.println("\t Time \t\t Pressure \t\t Temperature \t\t Thrust");
}

// ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ Main Program  ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ 
void loop() {
  // Sensor lectures
  Tiempo = millis();
  GetPressureData();      // Maximo ADC 1000Hz  - Requiere: <1ms
  GetThrustData();        // Maximo 
  GetTemperatureData();   // Maximo solo 10Hz   - Requiere: 32-35ms

  //tiempo = millis()-tiempo;   // usado para medir tiempos

  // Radio comand check
  char len = chibiGetData(CHB_MAX_PAYLOAD);
  if (len != 0) {
    Serial.print("Data received!: ");
    Serial.println(len);
    // Answer to Control Station
    chibiTx(BROADCAST_ADDR, "A", 2);
    delay(2000);
  }
  
  // Radio data Send
  SendData();
  
  // Log
  //Serial.println("\t" + String(Tiempo) +  "\t\t" + String(Pressure) + "\t\t" + String(Temperature) + "\t\t" + String(Thrust));
  //delay(SampleTime); // deactivated in order to take data as fast as posible

  // Ajustamos tiempo muestreo
  while((Tiempo+100)> millis()){
    delayMicroseconds(100);
  }
}



