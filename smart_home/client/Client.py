from  smart_home.client.NewDeviceAnnouncer import NewDeviceAnnouncer


class Client:

    def start(self):
        announcer = NewDeviceAnnouncer()
        server_ip = announcer.connect_to_server()

        while True:
            # Do useful things
            # Recording data, informing server, polling server, etc.
            pass

if __name__ == "__main__":
    client = Client()
    client.start()
