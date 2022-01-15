#!/bin/python
import signal
import os
import sys
import socket
import multiprocessing
import hashlib
import select
from chatChannel import chatChannel
from chatClient import chatClient

####################
# GLOBAL VARIABLES #
####################

#Use this variable for your loop
daemon_quit = False
serverHost = '127.0.0.1'

loginPath = "/tmp/server_secrets"   # Path to file storing usernames and hashed passwords
channelList = []                    # A list of currently active chatChannel objects
activeClients = []                  # Used to make sure each client can only log into one account
loggedInNames = []                  # Used to quickly check if a user is already logged in
loggedInUsers = []                  # A record of currently logged in chatClient objects

###################
# EXTRA FUNCTIONS #
###################

# Do not modify or remove this handler
def quit_gracefully(signum, frame):
    global daemon_quit
    daemon_quit = True

###################
# SERVER FUNCTION #
###################

def talkTime(host, port):
# Main function for the server
# - Sets up sockets
# - Allows for multiple connects and non-blocking IO using select.select
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    looper = True
    try:
        server.bind((host, port))
        server.setblocking(False)
        server.listen(50)

        reading = [server]
        writing = [server]
    except OSError:
        errormess = "PORT {} STILL OPEN.\n".format(port)
        sys.stderr.write(errormess)
        looper = False

    while not daemon_quit and looper:
        try:
            readable, writable, errors = select.select(reading, writing, reading, 0.5)
        except ValueError:
            continue

        for sock in readable:
            try:
                if sock == server:
                    client, address = sock.accept()
                    client.setblocking(False)
                    reading.append(client)
                else:
                    data = sock.recv(1024)
                    if data:
                        parseData(sock, data.decode("utf-8"))
                    else:
                        sock.close()
                        reading.remove(sock)
            except Exception as ex:
                errormess = "An exception as occured: {} (Args: {})".format(type(ex).__name__, ex.args)
                sys.stderr.write(errormess)
    server.close()


##################
# PARSE FUNCTION #
##################


def parseData(client, message):
# Interprets what action the user has sent to the server
# - Sends the arguments to the correct function to complete
# - Send the result of the function back to the user
    message = message.strip("\n").split(" ")
    action = message[0]

    # LOGIN :USERNAME :PASSWORD
    if action == "LOGIN":
        if len(message) < 3:
            result = "RESULT LOGIN 0\n"
        else:
            result = loginUser(message[1], message[2], client)

    # REGISTER :USERNAME :PASSWORD
    elif action == "REGISTER":
        if len(message) < 3:
            result = "RESULT REGISTER 0\n"
        else:
            result = regsiterNewUser(message[1], message[2])
        
    # JOIN :CHANNEL
    elif action == "JOIN":
        if len(message) < 2:
            result = "RESULT JOIN 0\n"
        else:
            result = joinChannel(message[1], client)

    # CREATE :CHANNEL
    elif action == "CREATE":
        if len(message) < 2:
            result = "RESULT CREATE 0\n"
        else:
            result = newChannel(message[1])

    # SAY :CHANNEL :MESSAGE
    elif action == "SAY":
        if len(message) < 3:
            result = "RESULT SAY 0\n"
        else:
            toSend = ""
            i = 2
            while i < len(message):
                toSend = toSend + message[i] + " "
                i = i + 1
            toSend = toSend.strip(" ")
            result = say(message[1], client, toSend)

    # CHANNELS
    elif action == "CHANNELS":
        result = getChannels()
    client.send(str.encode(result))

############################
# LOGIN/REGISTER FUNCTIONS #
############################

def regsiterNewUser(name, password):
# Attempts to register a new user
# - Checks if the user already exists
# - Hashes the password using SHA-256 and stores it in the "server_secrets" file
# - server_secrets uses the format <USERNAME>,<HASHED-PASSWORD> on each line
    lines = getLoginLines()
    i = 0
    while i < len(lines):
        user = lines[i].strip("\n").split(",")
        if name in user:
            result = "RESULT REGISTER 0\n"
            return result
        i = i + 1
    hashpass = hashlib.sha256(str.encode(password))
    addUserToLogin(name, str(hashpass.hexdigest()))
    result = "RESULT REGISTER 1\n"
    return result

def loginUser(name, password, client):
# Attempts to log into user account
# - Checks if the user exists
# - Checks if the password provided matches the one stored
# - Creates a chatClient object and adds the user to the loggedInUsers list
    hashpass = hashlib.sha256(str.encode(password))
    lines = getLoginLines()
    i = 0
    while i < len(lines):
        user = lines[i].strip("\n").split(",")
        if user[0] == name and name not in loggedInNames and client not in activeClients:
            if user[1] == hashpass.hexdigest():
                loggedInNames.append(name)
                newClient = chatClient(name, client)
                loggedInUsers.append(newClient)
                activeClients.append(client)
                result = "RESULT LOGIN 1\n"
                return result
            else:
                result = "RESULT LOGIN 0\n"
                return result
        i = i + 1
    result = "RESULT LOGIN 0\n"
    return result

def getLoginLines():
# Return the list of usernames and hashed passwords from server_secrets
    file = open(loginPath, "r")
    lines = file.readlines()
    file.close()
    return lines

def addUserToLogin(name, password):
# Add the user's name and hashed password to server_secrets
    file = open(loginPath, "a")
    file.write("{},{}\n".format(name, password))
    file.close()

#####################
# CHANNEL FUNCTIONS #
#####################

def newChannel(name):
# Attempts to create a new channel
# - Checks if a channel with the same name already exists
    for c in channelList:
        if name == c.name:
            result = "RESULT CREATE {} 0\n".format(name)
            return result
    channel = chatChannel(name)
    channelList.append(channel)
    result = "RESULT CREATE {} 1\n".format(name)
    return result

def joinChannel(name, client):
# Attempts to add the user to the specified channel
# - Checks if the client is logged in and retrieves the chatClient for user
# - Checks if the channel exists and retrieves the chatChannel
# - Checks if the client is already part of the channel
# - Adds the client to the channel
    clientCheck = None
    for c in loggedInUsers:
        if c.connection == client:
            clientCheck = c
            break
    if clientCheck == None:
        result = "RESULT JOIN {} 0\n".format(name)
        return result
    channelCheck = None
    for c in channelList:
        if c.name == name:
            channelCheck = c
            break
    if channelCheck == None:
        result = "RESULT JOIN {} 0\n".format(name)
        return result
    for c in channelCheck.users:
        if c.name == clientCheck.name:
            result = "RESULT JOIN {} 0\n".format(name)
            return result
    channelCheck.addUser(clientCheck)
    clientCheck.addChannel(channelCheck)
    result = "RESULT JOIN {} 1\n".format(name)
    return result

def getChannels():
# Returns a message containing the names of all currently active channels
    channelNames = []
    for c in channelList:
        channelNames.append(c.name)
    channelNames.sort()
    toSend = ""
    for c in channelNames:
        toSend = toSend + c + ", "
    toSend = toSend.strip(", ")
    return "RESULT CHANNELS " + toSend + "\n"

####################
# MESSAGE FUNCTION #
####################

def say(channelName, client, message):
# Attempt to send a message to all users in the provided channel
# - Find the chatChannel from the channel name
# - Find the chatClient from the client connection
# - Make sure the client has joined the channel
# - Send the message to everyone in the channel (apart from sender)
    channelCheck = None
    for c in channelList:
        if c.name == channelName:
            channelCheck = c
            break
    if channelCheck == None:
        result = "RESULT SAY 0\n"
        return result
    clientCheck = None
    for c in loggedInUsers:
        if c.connection == client:
            clientCheck = c
            break
    if clientCheck == None:
        result = "RESULT SAY 0\n"
        return result
    clientInChannel = False
    for c in channelCheck.users:
        if c.name == clientCheck.name:
            clientInChannel = True
            break
    if clientInChannel == False:
        result = "RESULT SAY 0\n"
        return result
    clientName = clientCheck.name
    result = "RECV {} {} {}\n".format(clientName, channelName, message)
    for c in channelCheck.users:
        if c.name != clientName:
            c.connection.send(str.encode(result))
    return result

#################
# MAIN FUNCTION #
#################

def run():
    #Do not modify or remove this function call
    signal.signal(signal.SIGINT, quit_gracefully)

    mainloop = True

    if len(sys.argv) < 2:
        # No port provided, print error and exit
        errormess = "No port number provided.\n"
        sys.stderr.write(errormess)
    else:
        # Create new login file or wipe existing file
        logins = open(loginPath, 'w')
        logins.close()

        # Retreive the port number from command line arguments
        serverPort = int(sys.argv[1])

        # Set up multiple processes to allow for multiple clients
        try:
            multiserv = multiprocessing.Process(target=talkTime, args=[serverHost, serverPort], daemon=True)
        except ValueError:
            pass
        multiserv.start()

        # Exit gracefully
        multiserv.join()
        multiserv.terminate()
        multiserv.close()


if __name__ == '__main__':
    run()

