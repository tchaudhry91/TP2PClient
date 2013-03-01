from twisted.internet import reactor, protocol
from twisted.protocols import basic
import os

class SearchRequestProtocol(basic.LineReceiver):
    
    def __init__(self, file_name):
        self.file_name = file_name
        self.file_handler = None
        
    def connectionMade(self):
        print("Connected to Server..")
        print("Sending Request..")
        self.initiate()
    
    def connectionLost(self, reason):
        pass
    
    def initiate(self):
        self.sendLine(self.file_name)     
    
    def lineReceived(self, line):
        print(line)
        if(line.endswith('Sending Descriptor')):
            self.handler = open(self.file_name+'.desc','wb')
            self.setRawMode()
    
    def rawDataReceived(self, data):
        if data.endswith('\r\n'):
            data[:-2]
            self.handler.write(data)
            self.handler.close()
            print("Descriptor Received..To Download File use 'get'")
        else:
            self.handler.write(data)   

class SearchRequestFactory(protocol.ClientFactory):
    protocol = SearchRequestProtocol
    
    def __init__(self,file_name):
        self.file_name = file_name
        
    def buildProtocol(self, addr):
        return SearchRequestProtocol(self.file_name)
    
def sendSearchRequest(server_ip, file_name):
    reactor.connectTCP(server_ip, 9890,
                        SearchRequestFactory(file_name))