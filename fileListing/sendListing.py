from twisted.internet import reactor, protocol
from twisted.protocols import basic
import os

class SendListingProtocol(basic.LineReceiver):
    
    def __init__(self, listing_handler, user):
        self.listing_handler = listing_handler
        self.user = user
    
    def connectionMade(self):
        print("LISTING SENDER : Connected To Listing Server..")
        print("Preparing to Send..")
        self.setLineMode()
        self.initiate()
        
    def loseConnection(self, reason):
        print("Disconnected from Listing Server")  
        self.listing_handler.close()      
        
    def initiate(self):
        self.sendLine("ListingSendRequest "+self.user)        
    
    def lineReceived(self, line):
        if line == "proceed":
            self.setRawMode()
            self.transport.write(self.listing_handler.read())
            self.transport.write('\r\n')
            self.setLineMode()
            print("Listing Sent To Server")
            self.transport.loseConnection()
            
class SendListingFactory(protocol.ClientFactory):
    protocol = SendListingProtocol
    
    def __init__(self, listing_handler, user):
        self.listing_handler = listing_handler
        self.user = user
        
    def buildProtocol(self, addr):
        return SendListingProtocol(self.listing_handler, self.user)
    
def sendListing(server_host, root_dir, user):
    os.chdir(root_dir)
    listing_handler = open(user+".fls")
    reactor.connectTCP(server_host, 9880,
                        SendListingFactory(listing_handler, user))
    