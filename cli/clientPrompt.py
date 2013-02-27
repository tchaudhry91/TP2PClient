from twisted.internet import stdio
from twisted.protocols import basic
from fileTransfer import fileClient
from fileListing.descriptor import Descriptor
import pickle

class ClientPrompt(basic.LineReceiver):
    from os import linesep as delimiter

    def connectionMade(self):
        self.transport.write('>>> ')

    def lineReceived(self, line):
        buildCommand(line)
        self.transport.write('>>> ')
        
def startPrompt():
    stdio.StandardIO(ClientPrompt())

def dispatchDescriptor(descriptor_file):
    print("Unpacking Descriptor...")
    descriptor_file = open(descriptor_file, 'rb')
    descriptor = pickle.load(descriptor_file)    
    command = 'get '+descriptor.getFileName()
    fileClient.requestFile(descriptor.getFileHost(), descriptor.getFileName(), [command], 9876)    

def dispatchExit():
    pass
    
def buildCommand(line):
    commands = line.split(' ')
    base_command = commands[0]
    if base_command == "get":
        descriptor = commands[1]
        dispatchDescriptor(descriptor)
    
    if base_command == "exit":
        dispatchExit()