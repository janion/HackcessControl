# To Do:
- Display server database in simple webpage for debugging
- Update client connection system to just have server constantly (every 60s) broadcast json with ip address?
- Reject connection based on name or IP, decide accordingly
- Protect data upload based on name not IP, or both name and IP
- Allow requesting of multiple data types in a single request
- Handle missing data when polling
- Allow request for all data types available
- Add script to move files to correct places on ESP8266
- Handle clients disconnecting and reconnecting
- Add mechanism for ESP8266 to be come an access point with a login page when no wifi credentials found

## Done:
- Server to store timestamp of last data submission
- Clients declare to server name
- Server to approve client name or suggest alternative
- Update all client/server interactions to use json
- Server to serve requested data in json format
- Clients declare to server data types to be reported
- Server to add client data types to database
- Server to allow submission of data from registered IP addresses
- Return timestamp with polled data
- Make client generic so that there is an abstract method which contains the specific implementation
- Work out how to serve multiple clients simultaneously
- Update client server poller to not use threads so that it can work on esp8266 modules
- Make Epoch time polling client example
- Make micropython compliant client
- ESP8266 button pressed client
- ESP8266 connection code with hard-coded authentication details factored out into json file