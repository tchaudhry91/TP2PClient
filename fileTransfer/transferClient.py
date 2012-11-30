from twisted.internet import reactor, protocol
from twisted.protocols import basic

class FileReceiverProtocol(basic.LineReceiver):
        
    def connectionMade(self):
        self.factory = FileReceiverFactory()
        self.file_handler = open('/home/tanmay/d.pdf','wb')
        print("Connected To:" + self.transport.getPeer().host)
        self.setRawMode()
        self.sendLine('get')
        
    def rawDataReceived(self, data):
        self.file_handler.write(data)
        
    def lineReceived(self, line):
        print(line)
        
class FileReceiverFactory(protocol.ClientFactory):
    protocol = FileReceiverProtocol

if __name__=="__main__":
    connection = reactor.connectTCP('localhost', 9876, FileReceiverFactory())
    reactor.run()
    
    