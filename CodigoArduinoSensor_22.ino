int pirPin = 7; 
int ledPin = 8;

bool bloqueado = false;
unsigned long tempoUltimaDeteccao = 0;
const unsigned long tempoEspera = 90000;     // 90 segundos (1min30s)
const unsigned long tempoLedLigado = 2000;   // LED acende por 2 segundos

bool ledLigado = false;
unsigned long tempoLedAcendido = 0;

void setup() {
  pinMode(pirPin, INPUT);
  pinMode(ledPin, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  int movimento = digitalRead(pirPin);
  unsigned long agora = millis();

  // Se detectou movimento e ainda não está bloqueado
  if (movimento == HIGH && !bloqueado) {
    Serial.println("Movimento detectado!");
    digitalWrite(ledPin, HIGH);
    ledLigado = true;
    tempoLedAcendido = agora;

    tempoUltimaDeteccao = agora;
    bloqueado = true;
  }

  // Desliga o LED após o tempo definido
  if (ledLigado && (agora - tempoLedAcendido >= tempoLedLigado)) {
    digitalWrite(ledPin, LOW);
    ledLigado = false;
  }

  // Após 90 segundos, libera para nova detecção
  if (bloqueado && (agora - tempoUltimaDeteccao >= tempoEspera)) {
    bloqueado = false;
  }

  delay(50);  // pequena pausa para estabilidade
}