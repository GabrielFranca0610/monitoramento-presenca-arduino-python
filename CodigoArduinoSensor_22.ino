int pirPin = 7;          // Define o pino digital 7 para o sensor PIR (entrada de movimento)
int ledPin = 8;          // Define o pino digital 8 para o LED (saída para acender/apagar)

bool bloqueado = false;  // Variável para bloquear novas detecções por um tempo após detectar movimento
unsigned long tempoUltimaDeteccao = 0;  // Armazena o momento da última detecção (em milissegundos)
const unsigned long tempoEspera = 90000;     // Tempo de bloqueio após detecção: 90 segundos (90.000 ms)
const unsigned long tempoLedLigado = 2000;   // Tempo que o LED ficará aceso após detecção: 2 segundos (2.000 ms)

bool ledLigado = false;            // Controla se o LED está aceso ou apagado
unsigned long tempoLedAcendido = 0; // Armazena o momento em que o LED foi ligado

void setup() {
  pinMode(pirPin, INPUT);          // Configura o pino do sensor PIR como entrada digital
  pinMode(ledPin, OUTPUT);         // Configura o pino do LED como saída digital
  Serial.begin(9600);              // Inicializa a comunicação serial a 9600 bps para enviar mensagens ao PC
}

void loop() {
  int movimento = digitalRead(pirPin);  // Lê o valor do sensor PIR (HIGH = movimento detectado, LOW = nada)
  unsigned long agora = millis();        // Pega o tempo atual desde que o Arduino ligou (em ms)

  // Se detectou movimento e ainda não está bloqueado para nova detecção
  if (movimento == HIGH && !bloqueado) {
    Serial.println("Movimento detectado!");  // Envia mensagem para monitor serial avisando movimento
    digitalWrite(ledPin, HIGH);               // Liga o LED para sinalizar presença
    ledLigado = true;                         // Marca que o LED está ligado
    tempoLedAcendido = agora;                  // Salva o tempo em que o LED foi ligado

    tempoUltimaDeteccao = agora;              // Atualiza o tempo da última detecção para controlar bloqueio
    bloqueado = true;                         // Ativa o bloqueio para evitar múltiplas detecções seguidas
  }

  // Se o LED está ligado e já passou o tempo que ele deve ficar aceso, apaga o LED
  if (ledLigado && (agora - tempoLedAcendido >= tempoLedLigado)) {
    digitalWrite(ledPin, LOW);               // Apaga o LED
    ledLigado = false;                       // Marca que o LED está desligado
  }

  // Se está bloqueado e já passou o tempo de espera (90 segundos), libera para nova detecção
  if (bloqueado && (agora - tempoUltimaDeteccao >= tempoEspera)) {
    bloqueado = false;                       // Desbloqueia o sensor para novas detecções
  }

  delay(50);  // Pequena pausa para dar estabilidade e evitar leituras muito rápidas
}
