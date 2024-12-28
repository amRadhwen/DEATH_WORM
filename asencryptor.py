# encryption/decryption labraries
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
#os file system
import os

class Asencryptor:
    
    # genrated public key
    generated_public_key = None
    #generated private key
    generated_private_key = None
    # load private key
    load_private_key = None
    # load public key
    load_public_key = None
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
                self.readed_private_key = serialization.load_pem_private_key(
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
                self.readed_public_key = serialization.load_pem_public_key(
                    pbk.read(),
                    backend=default_backend()
                )
            return True
        else:
            print("Invalid path or file !")
            return False
    
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
        self.output_file_data = self.public_key.encrypt(
            self.input_file_data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return True
    
    #write file data for encryption
    def write_file_data_for_encryption(self):
        filename = "enc_"+self.filename
        with open(filename) as encf:
            encf.write(self.output_file_data)
        return True

    #Decrypt
    #read file data for decryption
    def load_file_data_for_decryption(self, filename):
        if os.path.exists(self.current_dir+"/"+filename):
            with open(filename) as encf:
                self.loaded_file_data = encf.read()
            return True
        else:
            print("Invalid path or file !")
            return False
    
    # decrypt loaded file data
    def decrypt(self):
        self.decrypted_file_data = self.private_key.decrypt(
            self.loaded_file_data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return True
        
        
    
        
        
    
    
    
    
    