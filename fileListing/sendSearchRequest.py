from twisted.internet import reactor, protocol
from twisted.protocols import basic
import os

class SearchRequestProtocol(basic.LineReceiver):
    
    def __init__(self, command, file_name):
        self.command = command
        self.file_name = file_name
        self.file_handler = None
        
    def connectionMade(self):
        print("Connected to Server..")
        print("Sending Request..")
        self.initiate()
    
    def connectionLost(self, reason):
        pass
    
    def initiate(self):
        line = self.command+' '+self.file_name
        self.sendLine(line)     
    
    def lineReceived(self, line):
        print(line)
        if(line.endswith('Sending Descriptor')):
            self.mode = "descriptor"
            self.handler = open(self.file_name+'.desc','wb')
            self.setRawMode()
        elif(line.endswith('Sending Search List')):
            self.mode = "searchList"
            self.handler = open(self.file_name+'.list','wb')
            self.setRawMode()
    
    def rawDataReceived(self, data):
        if self.mode=="descriptor":
            if data.endswith('\r\n'):
                data[:-2]
                self.handler.write(data)
                self.handler.close()
                print("Descriptor Received..To Download File use 'download'")
                self.setLineMode()
            else:
                self.handler.write(data)
                    
        elif self.mode=="searchList":
            if data.endswith('\r\n'):
                data[:-2]
                self.handler.write(data)
                self.handler.close()
                print("Search List Received..Printing")
                #PRINT HERE
                self.setLineMode()
            else:
                self.handler.write(data)

class SearchRequestFactory(protocol.ClientFactory):
    protocol = SearchRequestProtocol
    
    def __init__(self, command, file_name):
        self.command = command
        self.file_name = file_name
        
    def buildProtocol(self, addr):
        return SearchRequestProtocol(self.command, self.file_name)
    
def sendSearchRequest(server_ip, command, file_name):
    reactor.connectTCP(server_ip, 9890,
                        SearchRequestFactory(command, file_name))