from Tkinter import *
import ttk
from twisted.internet import tksupport
from fileTransfer import fileServer
from fileListing import generate_fl
from fileTransfer import fileClient
from fileListing.descriptor import Descriptor
from fileListing import sendSearchRequest
import os
import pickle

class MainGUI():
    
    def __init__(self):
        self.root = Tk()
        self.root.title("TP2PClient")
        tksupport.install(self.root)
        
        #VARS
        self.user_name = StringVar()
        self.user_name.set("Username")
        
        self.root_directory = StringVar()
        self.root_directory.set("Root Directory")
        
        self.server_ip = StringVar()
        self.server_ip.set("Server IP")
        
        self.search_text = StringVar()
        self.search_text.set("Search")
        
        self.status_label = StringVar()
        self.status_label.set("Status")
                
        self.search_results = StringVar()
        
        self.descriptors = StringVar()
    
    def build(self):
        self.mainframe = ttk.Frame(self.root, padding=" 3 3 12 12")
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(0, weight=1)
        
        #CONNECT
        self.user_name_entry = ttk.Entry(self.mainframe, width=20, 
                                         textvariable=self.user_name
                                         ).grid(column=1,row=2)
        self.root_directory_entry = ttk.Entry(self.mainframe, width=20, 
                                         textvariable=self.root_directory
                                         ).grid(column=2,row=2)
        self.server_ip_entry = ttk.Entry(self.mainframe, width=20, 
                                         textvariable=self.server_ip
                                         ).grid(column=3,row=2)                                 
        self.connect_button = ttk.Button(self.mainframe, text="Connect",
                                         command=self.connect)
        self.connect_button.grid(column=4,row=2)
                                         
        #SEARCH 
        self.search_entry = ttk.Entry(self.mainframe, textvariable=self.search_text
                                      ).grid(column=1, row=3)
        self.search_list = Listbox(self.mainframe, listvariable=self.search_results)
        self.search_list.grid(column=1, row=4)
        self.search_button = ttk.Button(self.mainframe, text="Search",
                                        command=self.search).grid(column=1, row=5)
        
        #GET
        self.get_button = ttk.Button(self.mainframe, text="Get Descriptor",
                                     command=self.get).grid(column=2,row=4)
                                     
        #DOWNLOAD      
        self.descriptor_list = Listbox(self.mainframe, listvariable=self.descriptors)
        self.descriptor_list.grid(column=3,row=4)
        self.download_button = ttk.Button(self.mainframe, text="Download",
                                          command=self.download).grid(column=3,
                                                                      row=5)
        self.refresh_button = ttk.Button(self.mainframe, text="Refresh",
                                         command=self.refreshDescriptorList
                                         ).grid(column=4, row=4)
        
        #STATUS
        ttk.Label(self.root, textvariable=self.status_label).grid()
        
        for child in self.mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)
        

    def connect(self):
        generate_fl.generate_fl(self.root_directory.get(),self.user_name.get()
                                ,self.server_ip.get())
        fileServer.startServer(self.root_directory.get(), 9876)
        self.setStatus("Connected to Server")
        self.connect_button.configure(state=['disabled'])
    
    def search(self):
        sendSearchRequest.sendSearchRequest(self.server_ip.get(),
                                            'search',
                                            self.search_text.get(),
                                            '',self)
        self.setStatus("Search Request Sent")
        
    def get(self):
        results = self.search_results.get().split(' ')
        index = self.search_list.curselection()
        desc_info = results[index[0]].split("'")[1].split('--')
        self.setStatus(desc_info[0]+'--'+desc_info[1]+' Getting Descriptor..')
        sendSearchRequest.sendSearchRequest(self.server_ip.get(),
                                            'get', desc_info[0],
                                                desc_info[1])
        self.setStatus("Descriptor Receieved")
        self.refreshDescriptorList()
    
    def download(self):
        index = self.descriptor_list.curselection()[0]
        descriptor = self.descriptors.get().split(" ")[index]
        descriptor = descriptor.split("'")[1]
        self.dispatchDescriptor(descriptor)
    
    def setSearchList(self, result_list):
        self.search_results.set(result_list)
        
    def setStatus(self, status):
        self.status_label.set(status)
        
    def refreshDescriptorList(self):
        self.setStatus("Refreshing Descriptors")
        tup = os.walk(os.getcwd())
        print(os.getcwd())
        tup = tup.next()
        files = tup[2]
        results = []
        descriptors = ''
        for f in files:
            if isinstance(f, basestring):
                if f.endswith('.desc'):
                    results.append(f)
        for f in results:
            descriptors = descriptors+f
            descriptors = descriptors+' '
        self.descriptors.set(descriptors)
        
    def dispatchDescriptor(self, descriptor_file):
        print("Unpacking Descriptor...")
        descriptor_file = open(descriptor_file, 'rb')
        descriptor = pickle.load(descriptor_file)    
        command = 'download '+descriptor.getFileName()
        fileClient.requestFile(descriptor.getFileHost(),
                           descriptor.getFileName(),
                           [command], 9876)
        self.setStatus("Downloaded File. Check Directory")
            