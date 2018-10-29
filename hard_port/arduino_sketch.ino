define interruptInput A0
#define interrupOutput A1

#define gerconInput 2
#define solenoidOutput 4

#define redPin  11
#define greenPin  10
#define bluePin  9
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
  pinMode(redPin, OUTPUT);
  pinMode(greenPin, OUTPUT);
  pinMode(bluePin, OUTPUT);
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
  if (curState==GOOD_WAITING){
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
    }
  }
    Serial.print("state:"+String(states_str[curState]) + ",");
    /*Serial.print("isWallDamaged():"+String(isWallDamaged()) + ",");
    Serial.print("isGerconOpen():"+String(isGerconOpen()) + ",");*/

    if ((curState==UNLOCKED)&&(isGerconOpen()== true)){
        lock();
        curState = OPENED;
    }

    if ((curState==GOOD_WAITING)||(curState== OPENED)){
        setColor(255 ,0, 0, 300);
    }
    if ((curState==WALL_DAMAGED)||(curState== GERCON_OPEN)||(curState== SAFE_DAMAGED)){
         setColor(0, 255, 0, 300);
    }
    if (curState==UNLOCKED){
        setColor(0 ,0, 255, 300);
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
  digitalWrite(solenoidOutput, HIGH);
}
boolean lock(){
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

void setColor(int red, int green, int blue, int del){
    #ifdef COMMON_ANODE
    red = 255 - red
    green = 255 - green;
    blue = 255 - blue;
    #endif
    analogWrite(redPin, red);
    analogWrite(greenPin, green);
    analogWrite(bluePin, blue);
}