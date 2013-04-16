from twisted.internet import stdio
from twisted.protocols import basic
from fileTransfer import fileClient
from fileListing.descriptor import Descriptor
from fileListing import sendSearchRequest
import pickle
import sys

class ClientPrompt(basic.LineReceiver):
    from os import linesep as delimiter
    
    def __init__(self, server_ip):
        self.server_ip = server_ip

    def connectionMade(self):
        self.transport.write('>>> ')

    def lineReceived(self, line):
        buildCommand(line, self.server_ip)
        self.transport.write('>>> ')
        
def startPrompt(server_ip):
    stdio.StandardIO(ClientPrompt(server_ip))

def dispatchDescriptor(descriptor_file):
    print("Unpacking Descriptor...")
    descriptor_file = open(descriptor_file, 'rb')
    descriptor = pickle.load(descriptor_file)    
    command = 'download '+descriptor.getFileName()
    fileClient.requestFile(descriptor.getFileHost(), descriptor.getFileName(), [command], 9876)    

def dispatchExit():
    sys.exit(0)
    
def buildCommand(line, server_ip):
    commands = line.split(' ')
    base_command = commands[0]
    if base_command == "download":
        try:
            descriptor = commands[1]
            dispatchDescriptor(descriptor)
        except IndexError:
            print("No Descriptor Provided")
        except IOError:
            print("No Such Descriptor")
    
    if base_command == "exit":
        dispatchExit()
    
    if base_command == "get":
        pass
        
    if base_command == "search":
        try:
            sendSearchRequest.sendSearchRequest(server_ip, base_command, commands[1])
        except IndexError:
            print("No FileName to Search")
        