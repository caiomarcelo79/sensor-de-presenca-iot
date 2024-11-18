#include <SoftwareSerial.h>

// RX no pino 2, TX no pino 3
SoftwareSerial esp8266(2, 3);

// Constantes de rede e dados
const char* ssid = "nome_da_rede";
const char* password = "senha_da_rede";
const char* server = "ip_do_servidor";
const int port = 5000;
const char* endpoint = "/end_point_formato_post";

// Corpo da mensagem JSON
String jsonData = "{\"mov\": \"Detecção de movimento\"}";

String sendATCommand(String command, const int timeout, boolean debug) {
  String response = "";
  esp8266.print(command);
  long int time = millis();
  while ((time + timeout) > millis()) {
    while (esp8266.available()) {
      char c = esp8266.read();
      response += c;
    }
  }
  if (debug) {
    Serial.print(response);
  }
  return response;
}

void setup() {
  Serial.begin(9600);
  esp8266.begin(115200);
  pinMode(13, OUTPUT);
  pinMode(9, INPUT);
  delay(2000);

  sendATCommand("AT+RST\r\n", 2000, true);
  delay(2000);
  
  sendATCommand("AT+CWMODE=1\r\n", 1000, true);
  String connectCmd = "AT+CWJAP=\"" + String(ssid) + "\",\"" + String(password) + "\"\r\n";
  sendATCommand(connectCmd, 5000, true);
  delay(5000);

  sendATCommand("AT+CIFSR\r\n", 1000, true);
  delay(1000);
}

void loop() {
  if (digitalRead(9) == HIGH) {
    String connectTCP = "AT+CIPSTART=\"TCP\",\"" + String(server) + "\"," + String(port) + "\r\n";
    sendATCommand(connectTCP, 100, true);
    delay(100);

    String httpRequest = "POST " + String(endpoint) + " HTTP/1.1\r\n";
    httpRequest += "Host: " + String(server) + "\r\n";
    httpRequest += "Content-Type: application/json\r\n";
    httpRequest += "Content-Length: " + String(jsonData.length()) + "\r\n";
    httpRequest += "Connection: close\r\n\r\n";
    httpRequest += jsonData;

    String sendLength = "AT+CIPSEND=" + String(httpRequest.length()) + "\r\n";
    sendATCommand(sendLength, 100, true);
    delay(100);

    sendATCommand(httpRequest, 100, true);
    delay(100);

    sendATCommand("AT+CIPCLOSE\r\n", 100, true);
    delay(100);
  }
  else if (digitalRead(9) == LOW) {
    
  }
  delay(1500);  // Atraso para evitar múltiplas leituras em rápida sucessão
}
