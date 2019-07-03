#include <Wire.h>

int data[2];
int raw_adc;
double raw_adc_prom;
double voltaje;
double temperatura;
double suma;
double temperaturaFiltrada;
double muestras;
unsigned long tempo;

void setup() {
  Serial.begin(115200);
  Wire.begin();  
  Wire.beginTransmission(0x48); //Direccion del esclavo
  Wire.write(0x01); //Inicar configuracion de registro
  Wire.write(0xC0);  //1 100 000 0
                     //Iniciar conversion simple
                     //AINP = AIN0 and AINN = GND
                     //FSR = ±6.144 V
                     //Modo de conversion continua
  Wire.write(0xE3);  //111 0 0 0 11
                     //860 muestras por segundo (max)
                     //Comparador tradicional
                     //Polaridad de comparador en bajo
                     //Comparador sin enclavamiento
                     //Deshabilitar comparador
  Wire.endTransmission();
  
}

void loop() {
  
  unsigned long t1 = micros();
  Wire.beginTransmission(0x48);
  Wire.write(0x00);
  Wire.endTransmission();
  delayMicroseconds(300);
  Wire.requestFrom(0x48, 2); //Solita 2 bytes de datos al ADS1115
  while (Wire.available()){
    data[0] = Wire.read();
    data[1] = Wire.read();
    delayMicroseconds(100);
  }
  raw_adc = (data[0] * 256) + data[1]; //Convierte bytes a entero
  if (raw_adc > 32767){raw_adc -= 65535;}

  voltaje = raw_adc*0.0001875057F; //Escala voltios por cada bit
  temperatura = (voltaje-1.0)*1300.0/4.0; //Escala °C por cada voltio
  delayMicroseconds(1000);
  unsigned long t2 = micros();  //t2-t1 periodo muestreo aprox 2ms
  Serial.println(temperatura);
}
