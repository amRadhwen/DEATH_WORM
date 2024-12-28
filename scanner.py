# scan local filesystem for dir subdir and files the create index
import os
import sys
class Scanner:
    sysinfo = list(os.uname())
    maxln = 0
    def __init__(self) -> None:
        pass
    
    def get_sys_info(self):
        for i in self.sysinfo:
            print("| "+i)
        print(" ", end="")
        for i in range(0, self.maxln):
            print("=", end="")
        
    def find_max_info_ln(self):
        for i in self.sysinfo:
            if len(i) > self.maxln: self.maxln = len(i)
        self.maxln = self.maxln + 2
        return self.maxln
    
        
sc = Scanner()
maxln = sc.find_max_info_ln()
print(" ", end="")
for i in range(0, maxln):
    print("=", end="")
print("")
sc.get_sys_info()