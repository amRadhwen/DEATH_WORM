from platform import system
import os as OS
import psutil
import sys, subprocess
from glob import glob


class System:
    __os = None
    __sys_infos = None
    __disks = None
    __partitions = None
    __start_dir = None
    __filename = None
    def __init__(self) -> None:
        pass
    
    # detect os and system informations
    def detect_system(self):
        self.__os = system()
        self.__sys_infos = list(OS.uname())
        return self.__os
    
    # print os and system informations
    def print_system_infos(self):
        print(f"OS: {self.__os}")
        print(f"DIST: {self.__sys_infos[0]}, {self.__sys_infos[3]}")
        print(f"Version: {self.__sys_infos[2]}")
        print(f"Core: {self.__sys_infos[4]}")
        print(f"USER: {self.__sys_infos[1]}")
    
    def detect_system_partition(self, all=False):
        self.__partitions = psutil.disk_partitions(all)
    
    def get_system_partitions(self):
        return self.__partitions
    
    def print_system_partitions(self):
        for i in self.__partitions:
            print(i)
        print("============")
        print(" SDISKPART ")
        print("============")
        for i in range(0, len(self.__partitions)):
            print(f"Device {i}: {self.__partitions[i].device}")
            print(f"---->MountPoint: {self.__partitions[i].mountpoint}")
            print(f"---->FsType: {self.__partitions[i].fstype}")
            print(f"---->Opts: {self.__partitions[i].opts}")
            print(f"---->MaxFile: {self.__partitions[i].maxfile}")
            print(f"---->MaxPath: {self.__partitions[i].maxpath}")
    
    def detect_drives(self):
        if self.os.lower() == "linux":
            self.__disks = subprocess.run(["fdisk", "-l"], stdout=subprocess.PIPE, universal_newlines=True)
    
    def get_drives(self):
        return self.__disks
            
    
    def scan_system_files(self, files_ext=None):
        #filesnames = next(OS.walk("/"))
        #print(filesnames)
        #print(glob("/*.*"))
        start_dir = "/home/r3d1"
        counter = 0
        print("Starting Scan !")
        print("Scanning...wait !")
        for r, d, f in OS.walk(start_dir):
            for file in f:
                if file.endswith(".txt"):
                    counter+=1
                    print(f'{counter}: {OS.path.join(r, file)}')
        print("Scan ended !")
        print(f"Found: {counter} files !")
    
    def scan_dir(self, start_dir=None, files_ext=None):
        if self.__os.lower() == "linux":
            print("Initializin scan !")
            print("Scan starting !")
            result = OS.walk(self.__start_dir)
            files= []
            counter = 0
            print("Scan started !")
            with open(self.__filename, "wt") as fsindex:
                for tpl in result:
                        for i in tpl[2]:
                            counter += 1
                            files.append(tpl[0]+"/"+i)
                            print(tpl[0]+"/"+i)
                            fsindex.write(tpl[0]+"/"+i+"\n")
                print("Scan Finished !")
                print(f'Found {counter} files')
            
    def init_filesystem_index(self, start_dir):
        self.__start_dir = start_dir
        self.__filename = (self.__start_dir+".txt").replace("/", "_")
        print(self.__filename)
        with open(self.__filename, "a") as fsindex:
            fsindex.write("")
        
sc = Scanner()
sc.detect_system()
sc.init_filesystem_index("/home/r3d1/Videos")
#sc.scan_dir()