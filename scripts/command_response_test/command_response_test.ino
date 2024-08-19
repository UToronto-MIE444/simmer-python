/*
command_response_test

This Arduino sketch serves as an example to help students understand command data
parsing, response construction, and packetization. It will take any command received
over the serial connection, split out the command ID and data values, and parse the
data value as a floating point number. It will then respond to the command by echoing
back the data value in the correct response format.

*/

/* Declarations and Constants */
// Declare some string variables
String packet;
String cmdID;
String dataValue;

bool DEBUG = false; // If not debugging, set this to false to suppress debug messages
char FRAMESTART = '\x02';
char FRAMEEND = '\x03';
double DIFFERENCE = 1.2;

/* Create a debug message */
void debugMessage(String msg1, String msg2) {
  // If DEBUG is true, send some debug messages over the serial port
  if (DEBUG)
    {
      Serial.println(msg1);
      Serial.println(msg2);
    }
}

/* Serial receive function */
String receiveSerial() {
  // Declare message variable
  String msg;

  // If there's anything available in the serial buffer, get it
  if (Serial.available()) {
    // Read characters until the FRAMESTART character is found, dumping them all
    Serial.readStringUntil(FRAMESTART);
    // If serial characters are still available, read them into msg until the FRAMEEND character is reached
    if (Serial.available()) {
      msg = Serial.readStringUntil(FRAMEEND);
      msg = FRAMESTART + msg;
      debugMessage("Received String:", msg);
      return depacketize(msg);
    }
  }

  // If a correctly packed string isn't found, return an empty string
  return String();
}

/* Remove packet framing information */
String depacketize(String msg) {
  // If the message is correctly framed (packetized), trim framing characters and return it
  if (msg.length() > 0 && msg[0] == FRAMESTART) {
    if (msg[msg.length()] == FRAMEEND) {
      return msg.substring(1, msg.length());
    }
  }

  // If anything doesn't match the expected format, return an empty string
  return String();
}

/* Add packet framing information */
String packetize(String msg) {
  return FRAMESTART + msg + FRAMEEND;
}

/* Handle the received commands (in this case just sending back the command and the data + DIFFERENCE)*/
String parseCmd(String cmdString) {
  String cmdID;
  double data = 0;
  debugMessage("Parsed command: ", cmdString);

  // Get the command ID
  cmdID = cmdString.substring(0,min(2, packet.length()));

  // Get the data, if the command is long enough to contain it
  if (cmdString.length() >= 4) {
    data = packet.substring(3).toDouble();
  }

  // Debug print messages
  debugMessage("Command ID is: ", cmdID);
  debugMessage("The parsed data string is:", String(data));

  /*
  Here you would insert code to do something with the received cmdID and data
  */

  // Create a string response
  return cmdID + '-' + String(data + DIFFERENCE) + ',';

}



/* Setup Function */
void setup() {
  // initialize digital pin LED_BUILTIN as output in case it's needed
  pinMode(LED_BUILTIN, OUTPUT);

  // Use a higher data rate because the VS Code serial monitor uses 115200 as default
  Serial.begin(9600);
  // Set timeout to a quarter second as the max time to listen for a message
  Serial.setTimeout(250);
}

/* Main Loop */
void loop() {

  // Get a string from the serial port
  packet = receiveSerial();

  // Parse a correctly formatted command string
  if (packet.length() >= 3 && packet.length() <= 256)
  {
    // Loop through the received string, splitting any commands by the ',' character and parsing each
    int cmdStartIndex = 0;
    String responseString = String();
    for (int ct = 0; ct < packet.length(); ct++) {
      if (packet[ct] == ',') {
        responseString += parseCmd(packet.substring(cmdStartIndex, ct));
        cmdStartIndex = ct + 1;
      }
    }
    // For the last command (or if there were no ',' characters), parse it as well
    responseString += parseCmd(packet.substring(cmdStartIndex));
    debugMessage("Response String is: ", responseString);

    // Packetize and send the response string (removing the trailing ',')
    Serial.println(packetize(responseString.substring(0,responseString.length())));
  }
}
