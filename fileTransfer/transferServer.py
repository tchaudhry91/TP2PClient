from twisted.internet import reactor, protocol
from twisted.protocols import basic

class FileSenderProtocol(basic.LineReceiver):
    
    def connectionMade(self):
        self.transport.write("Connected")
        print("Connection From:"+self.transport.getPeer().host)
        
    def connectionLost(self, reason):
        print("Connection Lost")
    
    def lineReceived(self, line):
        line = cleanAndSplit(line)
        if line[0] == "get":
            print("Attempting Sending file..")
            self.setRawMode()
            for chunk in readLocalFile('/home/tanmay/a.pdf'):
                self.transport.write(chunk)
            self.setLineMode()
        else:
            self.transport.write('wrong')
            
class FileSenderFactory(protocol.Factory):
    protocol = FileSenderProtocol
    

def readLocalFile(file_name, chunk_size = 1024):
    with open(file_name,'rb') as local_file:
        while(True):
            chunk = local_file.read()
            if chunk:
                yield chunk
            else:
                    break
        
def cleanAndSplit(line):
    line = line.strip()
    line = line.split(' ')
    return line

def startServer():
    reactor.listenTCP(9876,FileSenderFactory())
    reactor.run()
    
if __name__=="__main__":
    startServer()
    