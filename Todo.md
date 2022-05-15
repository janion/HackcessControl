# To Do:
- Display server database in simple webpage for debugging?
- Update client connection system to just have server constantly (every 60s) broadcast json with ip address?
- Add mechanism for arbitrary connection to poll the total database state? (debugging only)
- Server to record tool usage
- Client/server to calculate _actual_ tool usage by a current meter

## Done:
- Clients declare to server name
- Server to approve client name or suggest alternative
- Update all client/server interactions to use json
- Server to serve requested data in json format
- Work out how to serve multiple clients simultaneously
- Update client server poller to not use threads so that it can work on esp8266 modules
- ESP8266 connection code with hard-coded authentication details factored out into json file
- Add script to move files to correct places on ESP8266
- Add mechanism for ESP8266 to be come an access point with a login page when no wifi credentials found
- Handle clients and server disconnecting and reconnecting
- Lock database when client request comes in
- Store names in Interface client thread so that removal of a client removes the actual client, not just the first client with the given IP address
- Store the device name in a .json file so that devices don't change names after a power cut
- Add device name as option on esp8266 login