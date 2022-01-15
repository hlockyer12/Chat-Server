class chatChannel:

    # Create an object that stores the name and list of users
    # that have currently joined the channel as chatClient objects

    def __init__(self, name):
        self.name = name
        self.users = []

    def addUser(self, user):
        self.users.append(user)

