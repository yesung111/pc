int tri = 13;
int ech = 12;

void setup()
{
  Serial.begin(9600);
  pinMode(tri, OUTPUT);
  pinMode(ech, INPUT);
}

void loop()
{
    float cycle;
    float dist;
    digitalWrite(tri, HIGH);
    delay(10);
    digitalWrite(tri, LOW);

    cycle = pulseIn(ech, HIGH);

    dist = ((340 * cycle) / 10000) / 2;


    if (dist < 30)
    {
      Serial.println(1);
    }
    else if (dist >= 30)
    {
      Serial.println(0);
    }
     
    delay(1000);
}
