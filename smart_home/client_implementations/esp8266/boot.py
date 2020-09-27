import os
if "setup.py" in os.listdir():
    import machine
    import setup
    try:
        setup.do_setup()
        machine.reset()
        print("Setup complete")
    except:
        print("Setup failed. Removing setup file")
        os.remove("setup.py")

from connection import Connection

Connection().checkOrMakeConnection()
