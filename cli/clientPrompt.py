from twisted.internet import stdio
from twisted.protocols import basic

class ClientPrompt(basic.LineReceiver):
    from os import linesep as delimiter

    def connectionMade(self):
        self.transport.write('>>> ')

    def lineReceived(self, line):
        buildCommand(line)
        self.transport.write('>>> ')
        
def startPrompt():
    stdio.StandardIO(ClientPrompt())

def dispatchDescriptor(descriptor):
    pass

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