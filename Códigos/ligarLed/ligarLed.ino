#define LED_PIN 12

#define ACTIVATE_LED "1"

#define DEACTIVATE_LED "0"

void setup() {
  Serial.begin(9600);
  pinMode(LED_PIN, OUTPUT);
}

void loop() {
  String s = Serial.readString();

  if(s == ACTIVATE_LED){
    digitalWrite(LED_PIN, HIGH);
    Serial.println("led aceso.");
  }
  else if(s == DEACTIVATE_LED){
    digitalWrite(LED_PIN, LOW);
    Serial.println("led apagado.");
  }
}
