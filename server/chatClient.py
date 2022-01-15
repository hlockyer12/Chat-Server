class chatClient:

    # Create an object that stores the username, client (connection) 
    # and list of chatChannel objects the user has joined.
    # Note: thi object does not store any passwords

    def __init__(self, name, connection):
        self.name = name
        self.connection = connection
        self.channelList = []

    def addChannel(self, channel):
        self.channelList.append(channel)

