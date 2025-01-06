from os import remove
from os.path import exists

class IndexHandler:
    
    __indexfile = None
    __data = None
    
    def __init__(self) -> None:
        pass
    
    def check_override(self, filename):
        override  = input(f"File \"{filename}\" already exists override ? (Y/N): ")
        while override.lower() not in ["y", "n"]:
            override = input(f"File \"{filename}\" already exists override ? (Y/N): ")
        if override.lower() == "y": return True
        else: return False

    def check_rem_confirmation(self, filename):
        confirm = input(f"Delete file \"{filename}\" ? (Y/N): ")
        while confirm.lower() not in ["y", "n"]:
            confirm = input(f"Delete file \"{filename}\" ? (Y/N): ")
        if confirm.lower() == "y": return True
        else: return False

    def create_index(self, filename):
        if not exists(filename):# or (exists(filename) and self.check_override(filename)):
            try:
                with open(filename, "w") as indexfile:
                    indexfile.write("")
                    self.__indexfile = indexfile
                    return True
            except Exception as e:
                print(e)
                return False
        else:
            return False
    
    def remove_index(self, filename):
        if exists(filename):# and self.check_rem_confirmation(filename):
            try:
                remove(filename)
                return True
            except Exception as e:
                print(e)
                return False
    
    def open_index_for_write(self, filename):
        try:
            self.__indexfile = open(filename, "w")
            return True
        except Exception as e:
            print(e)
            return False
    
    def open_index_for_append(self, filename):
        try:
            self.__indexfile = open(filename, "a")
            return True
        except Exception as e:
            print(e)
            return False
            
    def write_to_index(self, data, sep):
        try:
            self.__indexfile.write(data+sep)
        except Exception as e:
            print(e)
            return False
    
    def read_data_from_index(self, filename):
        try:
            with open(filename, "r") as indexfile:
                self.__data = indexfile.read()
                return True
        except Exception as e:
            print(e)
            return False
    
    def close_index(self):
        if self.__indexfile:
            self.__indexfile.close()
            return True
        else:
            return False
        
    def get_data(self):
        return self.__data


#ih = IndexHandler()
#ih.create_index("indexfile.txt")
#ih.open_index_for_write("indexfile.txt")
#data1 = "hello world !"
#data2 = "Welcome to the underground :p"
#ih.write_to_index(data1, ";")
#ih.write_to_index(data2, ";")
#ih.close_index()
#ih.read_data_from_index("indexfile.txt")
#print(ih.get_data())