#define analogPin A0 // аналоговый выход MQ135 подключен к пину A0 Arduino
#define digitalPin 3 // цифровой выход подключен к пину 3
int redPin = 11;
int greenPin = 10;
int bluePin = 9;

float analogValue; // для аналогового значения
byte digitalValue; // для цифрового значения, можно, кстати и boolean, но не суть

void setup() {

  Serial.begin(9600); // инициализация последовательного порта
  pinMode(analogPin, INPUT); // режим работы аналогового пина
  pinMode(digitalPin, INPUT); // режим работы цифрового пина
  
  pinMode(redPin, OUTPUT);
  pinMode(greenPin, OUTPUT);
  pinMode(bluePin, OUTPUT); 
  delay(1000); // устаканимся
  }

void loop() {

  /*sudo chown maxim  /dev/ttyACM0
  sudo ln -s /dev/ttyACM0 /dev/ttyUSB0*/
  delay(500);
  analogValue = analogRead(analogPin); // чтение аналогового значения
  digitalValue = digitalRead(3); // чтение цифрового значения
  // вывод аналогового значения в последовательный порт

  state(analogValue);
  delay(500); // задержка, чтобы не мельтешило перед глазами
}

void state(float _analogValue){
  if (_analogValue>500){
        setColor(255, 0, 0, 300); // красный
        Serial.print("{\"signal\":\"" +String(_analogValue,0) + "\","+
                       "\"state\": \"fire\","+
                       "\"from\": \"fire_sensor\"}");
  } else {
        Serial.print("{\"signal\":\"" +String(_analogValue,0) + "\","+
                       "\"state\": \"ok\","+
                       "\"from\": \"fire_sensor\"}");
  }
}

void setColor(int red, int green, int blue, int del)
{
    #ifdef COMMON_ANODE
    red = 255 - red
    green = 255 - green;
    blue = 255 - blue;
    #endif
    analogWrite(redPin, red);
    analogWrite(greenPin, green);
    analogWrite(bluePin, blue);
    delay(del);
    analogWrite(redPin, 0);
    analogWrite(greenPin, 0);
    analogWrite(bluePin, 0);
    
}
