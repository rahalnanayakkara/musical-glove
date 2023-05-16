#define F1 4
#define F2 3
#define F3 5
#define F4 2
#define F5 6

const int bufferSize = 5;

void setup()
{
    pinMode(F1, OUTPUT);
    pinMode(F2, OUTPUT);
    pinMode(F3, OUTPUT);
    pinMode(F4, OUTPUT);
    pinMode(F5, OUTPUT);

    Serial.begin(115200);
}

void loop()
{
    while (Serial.available() < bufferSize) {}

    byte buffer[bufferSize];
    Serial.readBytes(buffer, bufferSize);

    int pins[] = {F1, F2, F3, F4, F5};

    for(int i=0; i<5; i++)
        digitalWrite(pins[i], buffer[i]);
}