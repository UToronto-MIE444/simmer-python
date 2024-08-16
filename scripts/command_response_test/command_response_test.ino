/*
command_response_test

This Arduino sketch serves as an example to help students understand command data
parsing, response construction, and packetization. It will take any command received
over the serial connection, split out the command ID and data values, and parse the
data value as a floating point number. It will then respond to the command by echoing
back the data value in the correct response format.

*/

String s;
String cmdID;
String dataValue;

// If not debugging, set this to false to suppress debug messages
boolean DEBUG = false;

// Define whether using packed float or string response format
boolean FloatResponse = true;
boolean StringResponse = !FloatResponse;



// Setup Function
void setup() {
  // initialize digital pin LED_BUILTIN as output in case it's needed
  pinMode(LED_BUILTIN, OUTPUT);

  // Use a higher data rate because the VS Code serial monitor uses 115200 as default
  Serial.begin(9600);
  // Set timeout to a low number so responses are quick
  Serial.setTimeout(100);
}

// If DEBUG is true, send some debug messages over the serial port
void debugMessage(String msg1, String msg2) {
  if (DEBUG)
    {
      Serial.println(msg1);
      Serial.println(msg2);
    }
}

// main loop
void loop() {
  if (Serial.available())
  {
    // Get the received command
    Serial.readStringUntil('\x02');
    s = Serial.readStringUntil('\x03');
    s = '\x02' + s;
    debugMessage("Received String:", s);

    // Parse the command string
    if (s.length() >= 3)
    {
      // Get the command ID
      cmdID = s.substring(0,min(2, s.length()));
      debugMessage("Command ID is:", cmdID);


      // A command string 4 characters or longer should have a data value (i.e. 'w0-3.5')
      if (s.length() >= 4)
      {
        // Parse the string as a float
        dataValue = s.substring(3);
        debugMessage("The parsed data string is:", dataValue);
      }
      // A command without data should only be 2 or 3 characters long (i.e. 'u1' or 'u1-')
      else
      {
        // If the string isn't long enough to have a data value
        dataValue = "100.001";
        debugMessage("There is no data in the command to parse, returning:", dataValue);
      }

      Serial.println(dataValue);

    }
  }
}
