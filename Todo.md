# To Do:
- Make client generic so that there is an abstract method which contains the specific implementation
- Work out how to serve multiple clients simultaneously (Done?)
- Display server database in simple webpage for debugging
- Update client connection system to just have server constantly (every 60s) broadcast json with ip address?
- Update client server poller to use asyncio rather than threads so that it can work on esp8266 modules
- Reject connection based on name or IP, decide accordingly
- Protect data upload based on name not IP, or both name and IP
- Allow requesting of multiple data types in a single request

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