from twisted.internet import reactor, protocol
from twisted.protocols import basic
import os, pickle

class SearchRequestProtocol(basic.LineReceiver):
    
    def __init__(self, command, file_name, user_name, gui):
        self.command = command
        self.file_name = file_name
        self.user_name = user_name
        self.file_handler = None
        self.gui = gui
        
    def connectionMade(self):
        print("Connected to Server..")
        print("Sending Request..")
        self.initiate()
    
    def connectionLost(self, reason):
        pass
    
    def initiate(self):
        line = self.command+' '+self.file_name+' '+self.user_name
        self.sendLine(line)     
    
    def lineReceived(self, line):
        print(line)
        if(line.endswith('Sending Descriptor')):
            self.mode = "descriptor"
            self.file_path = self.file_name+'.desc'
            self.handler = open(self.file_path,'wb')
            self.setRawMode()
        elif(line.endswith('Sending Search List')):
            self.mode = "searchList"
            self.file_path = self.file_name+'.list'
            self.handler = open(self.file_path,'wb')
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
                self.printList(self.file_path)                
                self.setLineMode()
                os.remove(self.file_path)
            else:
                self.handler.write(data)
                
    def printList(self,tempFile):
        result_string = ""
        list = pickle.load(open(tempFile,'rb'))
        for entry in list:
            print("FILE : "+entry[0])
            print("USER : "+entry[1])
            print("\n\n")
            result_string=result_string+entry[0]+'--'+entry[1]
            result_string=result_string+" "
            if self.gui:
                self.gui.setSearchList(result_string)
                       
    
class SearchRequestFactory(protocol.ClientFactory):
    protocol = SearchRequestProtocol
    
    def __init__(self, command, file_name, user_name, gui):
        self.command = command
        self.file_name = file_name
        self.user_name = user_name
        self.gui = gui
        
    def buildProtocol(self, addr):
        return SearchRequestProtocol(self.command, self.file_name, self.user_name,
                                     self.gui)
    
def sendSearchRequest(server_ip, command, file_name, user_name, gui=None):
    reactor.connectTCP(server_ip, 9890,
                        SearchRequestFactory(command, file_name, user_name, gui))