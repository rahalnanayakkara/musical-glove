void setup()
{
    for(int i=3; i<13; i++)
        pinMode(i, OUTPUT);
    delay(1000);
}

void loop()
{
    for(int i=3; i<13; i++)
    {
        digitalWrite(i, HIGH);
        delay(500);
        digitalWrite(i, LOW);
        delay(1000);
    }
    delay(5000);
}