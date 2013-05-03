import sys
from fileListing import generate_fl
from fileTransfer import fileServer
from cli import clientPrompt
from twisted.internet import reactor
from gui import main_gui
  
if __name__=="__main__": 
    gui = main_gui.MainGUI()
    gui.build()
    """
    try:
        root_dir = sys.argv[1]
        server_ip = sys.argv[2]
    except:
        root_dir = raw_input("Enter Root Directory:")
        server_ip = raw_input("Enter Main Server IP:")
    port = 9876
    user_name = raw_input("Login:")
    generate_fl.generate_fl(root_dir,user_name, server_ip)
    print("File Listing Created..")
    
    fileServer.startServer(root_dir, port)
    clientPrompt.startPrompt(server_ip)
    """
    reactor.run()
    
    