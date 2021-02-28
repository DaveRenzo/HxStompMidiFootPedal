/*    
Copyright 2021, Dave Renzo (www.daverenzo.com)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
*/
#include <MIDI.h>
#include <EEPROM.h>


#define DEBUG
#undef PROG_EEPROM

#define SW_0  5
#define SW_1  6
#define SW_2  7
#define SW_3  4
#define SW_4  3
#define SW_5  2
#define T_SW  8

#define NUM_SWITHCES 6

#define LED   13


typedef struct footSwitch
{  
  char  ccNumber;
  char  ccValue;
  char  midiChannel;

  int buttonState = HIGH;
  int lastButtonState = HIGH;

  long lastDebounceTime = 0;
  long debounceDelay = 50;
} footSwitch;



MIDI_CREATE_DEFAULT_INSTANCE();



const byte switchArray[NUM_SWITHCES] = {SW_0,SW_1,SW_2,SW_3,SW_4,SW_5};
footSwitch swithces[NUM_SWITHCES];
char transferBuffer[NUM_SWITHCES * 3];

#ifdef DEBUG
int ledState = HIGH;
#endif

char incomingByte =0;

void setup() 
{
  #ifdef PROG_EEPROM
  //cc nums
  EEPROM.write(0, 60);
  EEPROM.write(1, 61);
  EEPROM.write(2, 62);
  EEPROM.write(3, 63);
  EEPROM.write(4, 64);
  EEPROM.write(5, 65);
  //cc vals
  EEPROM.write(6, 0);
  EEPROM.write(7, 1);
  EEPROM.write(8, 2);
  EEPROM.write(9, 3);
  EEPROM.write(10, 5);
  EEPROM.write(11, 5);
  //midi channels
  EEPROM.write(12, 1);
  EEPROM.write(13, 1);
  EEPROM.write(14, 1);
  EEPROM.write(15, 1);
  EEPROM.write(16, 1);
  EEPROM.write(17, 1);
  #endif
  
  bool bLoop = true;
  
  // put your setup code here, to run once:
  MIDI.begin(MIDI_CHANNEL_OMNI);
  
  pinMode(SW_0, INPUT_PULLUP);
  swithces[0].ccNumber = EEPROM.read(0);
  swithces[0].ccValue = EEPROM.read(6);
  swithces[0].midiChannel = EEPROM.read(12);

  pinMode(SW_1, INPUT_PULLUP);
  swithces[1].ccNumber = EEPROM.read(1);
  swithces[1].ccValue = EEPROM.read(7);
  swithces[1].midiChannel = EEPROM.read(13);
  
  pinMode(SW_2, INPUT_PULLUP);
  swithces[2].ccNumber = EEPROM.read(2);
  swithces[2].ccValue = EEPROM.read(8);
  swithces[2].midiChannel = EEPROM.read(14);
  
  pinMode(SW_3, INPUT_PULLUP);
  swithces[3].ccNumber = EEPROM.read(3);
  swithces[3].ccValue = EEPROM.read(9);
  swithces[3].midiChannel = EEPROM.read(15);

  pinMode(SW_4, INPUT_PULLUP);
  swithces[4].ccNumber = EEPROM.read(4);
  swithces[4].ccValue = EEPROM.read(10);
  swithces[4].midiChannel = EEPROM.read(16);

  pinMode(SW_5, INPUT_PULLUP);
  swithces[5].ccNumber = EEPROM.read(5);
  swithces[5].ccValue = EEPROM.read(11);
  swithces[5].midiChannel = EEPROM.read(17);

  pinMode(T_SW, INPUT_PULLUP);
  pinMode(LED_BUILTIN,OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);

  
//#ifdef DEBUG
//  pinMode(LED, OUTPUT);
//  digitalWrite(LED, ledState);
//#endif

  if (LOW == digitalRead(SW_0))
  {
    while(bLoop)
    {
      if (Serial.available()>0)
      {
        
        incomingByte = Serial.read();
        switch(incomingByte)
        {
          //handshake here to make sure arduino is working
          case 'a':
            Serial.print("Ack");
            break;
          //send current setup  
          case 'b':
            sendSetup();
            //Serial.print("Ack");
            break;
          //write a new setup
          case 'c':
            Serial.print("Ack");
            bLoop = getSetup();
            Serial.print("POO");
            break;
          default:
            Serial.print("Nak");
            break;
        }//end switch
      }//end if
    }//end while
  }//end if
}

void loop() {
  //Serial.print("Hi\r\n");
  // read the state of the switch into a local variable:
  for(int i =0; i < NUM_SWITHCES; i++){
  int reading = digitalRead(switchArray[i]);
 
  // check to see if you just pressed the button
  // (i.e. the input went from LOW to HIGH), and you've waited long enough
  // since the last press to ignore any noise:
 
  // If the switch changed, due to noise or pressing:
  if (reading != swithces[i].lastButtonState) {
    // reset the debouncing timer
    swithces[i].lastDebounceTime = millis();
  }
 
  if ((millis() - swithces[i].lastDebounceTime) > swithces[i].debounceDelay) {
    // whatever the reading is at, it's been there for longer than the debounce
    // delay, so take it as the actual current state:
 
    // if the button state has changed:
    if (reading != swithces[i].buttonState) {
      swithces[i].buttonState = reading;
 
      // only toggle the LED if the new button state is HIGH
      if (swithces[i].buttonState == LOW) {
        #ifdef DEBUG
        ledState = !ledState;
        #endif
        
        
        MIDI.sendControlChange(swithces[i].ccNumber,swithces[i].ccValue,swithces[i].midiChannel);
      }
    }
  }

 #ifdef Debug
  // set the LED:
  digitalWrite(ledPin, ledState);
 #endif
  // save the reading. Next time through the loop, it'll be the lastButtonState:
  swithces[i].lastButtonState = reading;}
}

void sendSetup()
{
 
  for (int i =0; i < NUM_SWITHCES; i++)
  {
      transferBuffer[i] = swithces[i].ccNumber;
      //strncpy(transferBuffer[i], (char)switches[i].ccNumber, 1);
  }
  for (int i =0; i < NUM_SWITHCES; i++)
  {
      transferBuffer[i+6] = swithces[i].ccValue;
      //strncpy(transferBuffer[i + 6], (char)switches[i].ccValue, 1);
  }
  for (int i =0; i < NUM_SWITHCES; i++)
  {
      transferBuffer[i+12] = swithces[i].midiChannel;
      //strncpy(transferBuffer[i + 12], (char)swithces[i].midiChannel, 1);
  }
  Serial.write(transferBuffer,sizeof(transferBuffer));
//    Serial.print("Midi Setup:\r\n");
//    for (int i =0; i < 18; i++)
//    {
//      int temp = transferBuffer[i];
//      Serial.print(temp,DEC);
//      Serial.write(" ");
//    }
}
bool getSetup()
{
  Serial.readBytes(transferBuffer,NUM_SWITHCES*3);
  for (int i = 0; i < NUM_SWITHCES*3; i++)
  {
    EEPROM.write(i, transferBuffer[i]);
  }
//  for (int i =0; i < NUM_SWITHCES; i++)
//  {
//      swithces[i].ccNumber = transferBuffer[i];
//  }
//  for (int i =0; i < NUM_SWITHCES; i++)
//  {
//      swithces[i].ccValue = transferBuffer[i+6];
//  }
//  for (int i =0; i < NUM_SWITHCES; i++)
//  {
//      swithces[i].midiChannel = transferBuffer[i+12];
//  }
  return false;
}
