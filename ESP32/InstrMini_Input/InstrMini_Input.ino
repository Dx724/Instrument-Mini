#define analogCount 2
#define digitalCount 4
#define totalCount (analogCount + digitalCount)

int analogPins[analogCount] = {13, 12}; // Joystick X, Joystick Y
int digitalPins[digitalCount] = {14, 33, 18, 19}; // Joystick Z, Switch and two Buttons
// Note that the switch can only be in two states, so we can determine the state
// by verifying the connection state from a single side.

void setup() {
  Serial.begin(115200);

  // Set up pins
  for (int p : analogPins) {
    pinMode(p, INPUT);
  }
  for (int d : digitalPins) {
    pinMode(d, INPUT_PULLUP);
  }
}

// [joystickX, joystickY, joystickZ, switch, button1, button2]
int data[totalCount] = {};

void loop() {
  for (int i = 0; i < analogCount; i++) {
    data[i] = analogRead(analogPins[i]);
  }
  for (int i = analogCount; i < totalCount; i++) {
    data[i] = digitalRead(digitalPins[i-analogCount]);
  }

  for (int i = 0; i < totalCount; i++) {
    Serial.print(data[i]);
    Serial.print(i == totalCount - 1 ? "\n" : " ");
  }
  
  delay(100);
}
