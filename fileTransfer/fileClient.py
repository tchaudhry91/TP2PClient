from twisted.internet import reactor, protocol
from twisted.protocols import basic

class FileRequestProtocol(basic.LineReceiver):
    def __init__(self, commands, file_name):
        self.commands = commands
        self.file_name = file_name
        
    def connectionMade(self):
        print("CLIENT:Connected To Host:"+self.transport.getPeer().host)
        for command in self.commands:
            self.sendLine(command)
    
    def rawDataReceived(self, data):
        if data.endswith('\r\n'):
            data = data[:-2]
            self.file_handler.write(data)
            self.file_handler.close()
            self.setLineMode()
            print('CLIENT:File Receieved..Exiting')
            self.sendLine('exit')
        else:
            self.file_handler.write(data)
    
    def lineReceived(self, line):
        if line == 'RAW DATA':
            self.setRawMode()
            self.file_handler = open(self.file_name, 'wb')
        else:
            print(line)
    
    def connectionLost(self, reason):
        print('Connection Closed')

class FileRequestFactory(protocol.ClientFactory):
    protocol = FileRequestProtocol
    
    def __init__(self, commands, file_name):
        self.commands = commands
        self.file_name = file_name
    
    def buildProtocol(self, addr):
        return FileRequestProtocol(self.commands, self.file_name)
    
def requestFile(host, file_name, commands, port=9876):
    reactor.connectTCP(host, port, FileRequestFactory(commands, file_name))