# To Do:
- Clients declare to server data types to be reported
- Server to add client data types to database of sorts
- Server to allow submission of data from registered IP addresses
- Server to serve requested data in json format
- Make client generic so that there is an abstract method which contains the specific implementation
- Work out how to serve multiple clients simultaneously
- Display server database in simple webpage for debugging
- Update client connection system to just have server constantly (every 60s) broadcast json with ip address?

## Done:
- Server to store timestamp of last data submission
- Clients declare to server name
- Server to approve client name or suggest alternative
- Update all client/server interactions to use json