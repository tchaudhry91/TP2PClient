import os
from twisted.internet import reactor, protocol
from twisted.protocols import basic

class FileServerProtocol(basic.LineReceiver):
    
    def __init__(self, root_dir):
        self.file_handler = None
        self.root_dir = root_dir
        self.root_dir_new = os.path.join(self.root_dir, "Open")
        self.setLineMode()
    
    def connectionMade(self):
        os.chdir(self.root_dir)
        print("SERVER:Incoming Connection:"+self.transport.getPeer().host)
    
    def connectionLost(self, reason):
        print("SERVER:Connection Lost..")
    
    def lineReceived(self, line):
        line = cleanAndSplit(line)
        if validateCommand(line):
            if line[0] == 'exit':
                self.transport.loseConnection()
            elif line[0] == 'private':
                self.root_dir_new = os.path.join(self.root_dir, 'Private')
                print("SERVER:Changed to Private Directory")
            elif line[0] == 'get':
                try:
                    self.file_handler = open(os.path.join(self.root_dir_new, line[1]))
                    self.sendLine('RAW DATA')
                    self.setRawMode()
                    for chunk in readChunks(self.file_handler):
                        self.transport.write(chunk)
                    self.transport.write('\r\n')
                    self.setLineMode()                    
                except(IOError):
                    self.sendLine("Invalid File")                
        else:
            self.sendLine('Invalid Command')

class FileServerFactory(protocol.ServerFactory):
    protocol = FileServerProtocol
    
    def buildProtocol(self, addr):
        return FileServerProtocol(self.root_dir)
    
    def __init__(self, root_dir):
        self.root_dir = root_dir

def cleanAndSplit(line):
    line.strip()
    line = line.split(' ')
    return line

def readChunks(file_handler, chunk_size=1024000):
    while(True):
        chunk = file_handler.read(chunk_size)
        if chunk:
            yield chunk
        else:
            break
        

def validateCommand(line):
    if line[0].lower() == 'exit':
        return True
    elif line[0].lower() == 'get':
        if line[1]:        
            return True
    elif line[0].lower() == 'private':
        return True
    
def startServer(root_dir, port=9876):
    reactor.listenTCP(port, FileServerFactory(root_dir))
    print("Server Started")
    print("Listening On:"+str(port)+"\nDirectory Served:"+root_dir)
