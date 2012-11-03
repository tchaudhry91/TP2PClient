class FileListing():
# Basic File Listing Object
    def __init__(self):
        self.username = ""
        self.friends = []
        self.files_open = []
        self.meta_open = {}
        self.files_priv = []
        self.meta_priv = {}
    
    def setUsername(self,username):
        self.username = username
    
    def addFriend(self,friend):
        self.friends.append(friend)
    
    def addOpenFile(self,f_file, size=0):
        self.files_open.append(f_file)
        self.meta_open[f_file] = (size,)
        
    def addPrivFile(self,f_file, size=0):
        self.files_priv.append(f_file)
        self.meta_priv[f_file] = (size,)

    def getIp(self):
        return self.ip_add
    
    def getFriends(self):
        return self.friends
    
    def getOpenFiles(self):
        return self.files_open
    
    def getPrivateFiles(self):
        return self.files_priv
    
    def getOpenMeta(self):
        return self.meta_open
    
    def getPrivMeta(self):
        return self.meta_priv    
        