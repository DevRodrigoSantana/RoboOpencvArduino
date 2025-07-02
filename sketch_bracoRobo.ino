#include <Servo.h>

Servo servoX;
Servo servoY;
Servo servoZ;  

int posicaoAtualZ = 5;  

void setup() {
  Serial.begin(9600);
  servoX.attach(9);
  servoY.attach(10);
  servoZ.attach(11);  
  servoZ.write(posicaoAtualZ);
}

void loop() {
  if (Serial.available()) {
    String comando = Serial.readStringUntil('\n');
    int separador1 = comando.indexOf(',');
    int separador2 = comando.indexOf(',', separador1 + 1);

    if (separador1 > 0 && separador2 > separador1) {
      
      int anguloX = comando.substring(0, separador1).toInt();
      int anguloY = comando.substring(separador1 + 1, separador2).toInt();
      int statusMaoEsquerda = comando.substring(separador2 + 1).toInt();  // 0 ou 1

      
      anguloX = constrain(anguloX, 0, 180);
      anguloY = constrain(anguloY, 0, 180);

     
      int anguloY_limitado = map(anguloY, 0, 180, 110, 3);
      anguloY_limitado = constrain(anguloY_limitado, 3, 110);

      
      servoX.write(anguloX);
      servoY.write(anguloY_limitado);

      
      int alvoZ = statusMaoEsquerda == 0 ? 20 : 5;

      
      if (posicaoAtualZ != alvoZ) {
        int passo = posicaoAtualZ < alvoZ ? 1 : -1;
        for (int i = posicaoAtualZ; i != alvoZ; i += passo) {
          servoZ.write(i);
          delay(10);  
        }
        posicaoAtualZ = alvoZ;
      }
    }
  }
}
