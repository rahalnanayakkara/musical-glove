#define R1 6
#define R2 3
#define R3 4
#define R4 5
#define R5 7
#define L1 11
#define L2 8
#define L3 10
#define L4 9
#define L5 12

const int bufferSize = 10;

void setup()
{
    for(int i=3; i<13; i++)
        pinMode(i, OUTPUT);

    Serial.begin(115200);
}

void loop()
{
    while (Serial.available() < bufferSize) {}

    byte buffer[bufferSize];
    Serial.readBytes(buffer, bufferSize);

    int pins[] = {R1, R2, R3, R4, R5, L1, L2, L3, L4, L5};

    for(int i=0; i<bufferSize; i++)
        digitalWrite(pins[i], buffer[i]);
}