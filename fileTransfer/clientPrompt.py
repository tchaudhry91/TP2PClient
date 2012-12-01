from . import fileClient
import time
import os

def startPrompt(root_dir="/home/tanmay/TEST"):
    time.sleep(1)
    commands = []
    while(True):
        host = raw_input(">>HOST:")
        port = int(raw_input(">>PORT:"))
        private = raw_input(">>PRIVATE:")
        file_name = raw_input(">>FILENAME:")
        get_command = "get " + file_name
        commands = buildCommands(private, get_command)
        file_name = os.path.join(root_dir,file_name)
        fileClient.requestFile(host, commands, file_name, port)
        break
    
def buildCommands(private, get_command):
    commands = []
    if private == "True":
        commands.append('private')
    commands.append(get_command)
    return commands