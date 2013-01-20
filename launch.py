import sys
from fileListing import generate_fl
from fileTransfer import fileServer
from cli import clientPrompt
from twisted.internet import reactor
  

if __name__=="__main__": 
    root_dir = sys.argv[1]
    port = 9876
    
    generate_fl.generate_fl(root_dir,"tuxybuzz")
    print("File Listing Created..")
    
    fileServer.startServer(root_dir, port)
    clientPrompt.startPrompt()
    reactor.run()
    
    