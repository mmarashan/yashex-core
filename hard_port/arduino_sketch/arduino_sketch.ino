#define interruptInput A0
#define interrupOutput A1

#define gerconInput 2
#define solenoidOutput 4

#define ledPin  9
#define buzzerPin  10
const char* const states_str[]={"GOOD_WAITING","GERCON_OPEN","WALL_DAMAGED","UNLOCKED","SAFE_DAMAGED","OPENED"};
enum state {GOOD_WAITING, GERCON_OPEN, WALL_DAMAGED, UNLOCKED, SAFE_DAMAGED, OPENED};
// Текущее состояния (запускаем систему, когда дверь открыта
//изменить на Opened!!!
enum state curState = OPENED;

String inputString;

void setup()
{
  Serial.begin(9600); // инициализация последовательного порта
  // соленои инициализация
  pinMode(solenoidOutput, OUTPUT);
  //обрыв инициализация
  pinMode(interrupOutput, OUTPUT);
  pinMode(interruptInput, INPUT);
  //геркон инициальзация
  pinMode(gerconInput, INPUT);
  digitalWrite(gerconInput, HIGH);

  //лампочки инициализация
  pinMode(ledPin, OUTPUT);
  pinMode(buzzerPin, OUTPUT);
  delay(1000); // устаканимся
}

void loop(){

  //если все хорошо
  if ((isWallDamaged()== false)&&(isGerconOpen()==false)&&(curState==GOOD_WAITING)){
    curState = GOOD_WAITING;
  } else {
      //стейты с повреждением
      if (isWallDamaged()== true){
        curState = WALL_DAMAGED;
      }
      if ((isGerconOpen()== true)&&(curState!=UNLOCKED)&&(curState!=OPENED)){
        curState = GERCON_OPEN;
      }
      if ((isGerconOpen()== true)&&(curState!=UNLOCKED)&&(curState!=OPENED)&&(isWallDamaged()== true)){
        curState = SAFE_DAMAGED;
      }

  }

  //если все хорошо, проверяем, если ли команда на открытие
  //if (curState==GOOD_WAITING){
    if(Serial.available() > 0)
    {
        inputString = Serial.readStringUntil('\n');
        
        if (inputString == "unlock"){
          curState = UNLOCKED;
          unlock();

        }
        if (inputString == "lock"){
          curState = GOOD_WAITING;
          lock();

        }

        if (inputString == "sayState"){
          Serial.print("{ \"state\": \""+String(states_str[curState]) + "\"," +
                       "\"GERCON_OPENED\" : \""+String(isGerconOpen()) + "\"" +
                       "\"WALL_DAMAGED\" : \""+String(isWallDamaged()) + "\"}");
        }
    }
  //}
    //Serial.print("state:"+String(states_str[curState]) + ",");

    if ((curState==UNLOCKED)&&(isGerconOpen()== true)){
        lock();
        curState = OPENED;
        ledOff();
        buzzerOff();
    }

    if ((curState==GOOD_WAITING)||(curState== OPENED)){
        ledOn();
        buzzerOff();
    }
    if ((curState==WALL_DAMAGED)||(curState== GERCON_OPEN)||(curState== SAFE_DAMAGED)){
         buzzerSwing();
         ledSwing();
    }
    if (curState==UNLOCKED){
        buzzerOn();
        ledOff();
    }

    //Если был открыт, а теперь закрыт
    if ((curState==OPENED)&&(isGerconOpen()== false)){
        lock();
        curState = GOOD_WAITING;
    }
    delay(1000);


}

//открыть замок
boolean unlock(){
  ledSwing();
  digitalWrite(solenoidOutput, HIGH);
  delay(10000);
}
boolean lock(){
  ledSwing();
  digitalWrite(solenoidOutput, LOW);
}


//Повреждена ли стенка?
boolean isWallDamaged(){
  analogWrite(interrupOutput, 100);
  float analogValue = analogRead(interruptInput); // чтение аналогового значения
  if (analogValue!=0){return true;}
   else{return false;}
}

//разомкнут ли геркон?
boolean isGerconOpen(){
   int digitalValue = digitalRead(gerconInput);
   if (digitalValue==0){return false;}
   else{return true;}
}

void ledOn(){
    digitalWrite(ledPin, HIGH);
}

void ledSwing(){
    digitalWrite(ledPin, LOW);
    delay(500);
    digitalWrite(ledPin, HIGH);
    delay(500);
    digitalWrite(ledPin, LOW);
}

void buzzerOn(){
    tone(buzzerPin, 1000); 
}

void buzzerSwing(){
    tone (buzzerPin, 500);
    delay(100); 
    tone(buzzerPin, 1000); 
    delay(100);
    tone(buzzerPin, 2000);
    delay(100);
}

void ledOff(){
    digitalWrite(ledPin, LOW);
}

void buzzerOff(){
    digitalWrite(buzzerPin, LOW);
}
