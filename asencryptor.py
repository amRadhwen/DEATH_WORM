# encryption/decryption labraries
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
#os file system
import os

class Asencryptor:
    
    # genrated public key
    public_key = None
    #generated private key
    private_key = None
    # load private key
    loaded_private_key = None
    # load public key
    loaded_public_key = None
    # filename for encode
    filename = None
    # input file data for encode
    input_file_data = None
    # output file date (encoded)
    output_file_data = None    
    # loaded file data for decryption
    loaded_file_data = None
    # decrypted file data
    decrypted_file_data = None
    # current directory
    current_dir = os.getcwd()
    
    def __init__(self) -> None:
        pass
    
    # gen private key
    def generate_private_key(self):
        self.private_key = rsa.generate_private_key(
            public_exponent=65537, 
            key_size=2048, 
            backend=default_backend
        )
        return True
    
    #gen public key
    def generate_public_key(self):
        self.public_key = self.private_key.public_key()
        return True
        
    #generate private and public key
    def generate_keys(self):
        self.generate_private_key()
        self.generate_public_key()
        return True
        
    #keys storage
    #store private key
    def store_private_key(self):
        pem = self.private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        with open("privateKey.pem", "wb") as prk:
            prk.write(pem)
        return True
    
    #store public key
    def store_public_key(self):
        pem = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        with open("publicKey.pem", "wb") as pbk:
            pbk.write(pem)
        return True
    
    #store public and private keys
    def store_keys(self):
        self.store_private_key()
        self.store_public_key()
        return True
    
    #reading keys
    #ready private key
    def load_private_key(self):
        if os.path.exists(self.current_dir+"/privateKey.pem"):
            with open("privateKey.pem", "rb") as prk:
                self.loaded_private_key = serialization.load_pem_private_key(
                    prk.read(),
                    password=None,
                    backend=default_backend()
                )
            return True
        else:
            print("Invalid path or file !")
            return False
    
    def load_public_key(self):
        if os.path.exists(self.current_dir+"/publicKey.pem"):
            with open("publicKey.pem", "rb") as pbk:
                self.loaded_public_key = serialization.load_pem_public_key(
                    pbk.read(),
                    backend=default_backend()
                )
            return True
        else:
            print("Invalid path or file !")
            return False
    #load keys
    def load_keys(self):
        self.load_private_key()
        self.load_public_key()
        return True
    
    #encryption
    #open file to encryption
    def read_file_data_for_encryption(self, filename):
        if os.path.exists(self.current_dir+"/"+filename):
            self.filename = filename
            with open(filename, "rb") as f:
                self.input_file_data = f.read()
            return True
        else:
            print("Invalid path or file !")
            return False
    #encrypt file   
    def encrypt(self):
        self.output_file_data = self.loaded_public_key.encrypt(
            self.input_file_data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return True
    
    #write file data after encryption
    def write_file_data_after_encryption(self):
        filename = "enc_"+self.filename
        ext = len(filename) - filename.index('.')
        with open(filename[:-ext], "wb") as encf:
            encf.write(self.output_file_data)
        self.write_ext_to_index_file(filename[filename.index('.'):])
        return True

    #Decrypt
    #read file data for decryption
    def load_file_data_for_decryption(self, filename):
        if os.path.exists(self.current_dir+"/"+filename):
            self.filename = filename
            with open(filename, "rb") as encf:
                self.loaded_file_data = encf.read()
            return True
        else:
            print("Invalid path or file !")
            return False
    
    # decrypt loaded file data
    def decrypt(self):
        self.decrypted_file_data = self.loaded_private_key.decrypt(
            self.loaded_file_data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return True
    
    # write file data after decryption
    def write_file_data_after_decryption(self):
        with open(self.filename[4:], "wb") as encf:
            encf.write(self.decrypted_file_data)
        return True
        
    
    # remove original file after encryption
    def remove_orgfile_after_encryption(self):
        os.remove(self.filename)
        return True
    
    def remove_encrypted_file_after_decryption(self):
        os.remove(self.filename)
        return True
    
    def generate_files_ext_index(self):
        with open("indexes.txt", "w") as indexes:
            indexes.write("")
        return True
            
    def write_ext_to_index_file(self, ext):
        with open("indexes.txt", "a") as indexes:
            indexes.write(ext)
    
        
        
    
    
    
    
    