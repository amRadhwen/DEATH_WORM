# encryption/decryption labraries
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os


class Hencryptor:
    # generated aes key
    __aes_key = None
    # generated IV
    __iv = None
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
    # output file data (encoded)
    output_file_data = None    
    # loaded file data for decryption
    loaded_file_data = None
    # decrypted file data
    decrypted_file_data = None
    # current directory
    current_dir = os.getcwd()
    
    def __init__(self) -> None:
        pass
    
    def generate_aes_key(self):
        self.__aes_key = os.urandom(32)
        return True

    def generate_iv(self):
        self.__iv = os.urandom(16)

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
        if os.path.exists(filename):
            self.filename = os.path.abspath(filename)
            with open(filename, "rb") as file:
                self.input_file_data = file.read()
            return True
        else:
            print("Invalid path or file !")
            return False
    #encrypt file   
    def encrypt(self):
        try:
            self.output_file_data = self.loaded_public_key.encrypt(
                self.input_file_data,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            print(self.output_file_data)
            return True
        except Exception as e:
            print(e.__str__()+" !")
            return False
    
    def hybrid_encrypt(self):
        #encrypt file
        cipher = Cipher(algorithms.AES(self.__aes_key), modes.CFB(self.__iv))
        encryptor = cipher.encryptor()
        self.output_file_data = encryptor.update(self.input_file_data) + encryptor.finalize()
        # encrypt aes key and iv with rsa
        
        encrypted_key = self.loaded_public_key.encrypt(
            self.__aes_key + self.__iv,
            padding.OAEP(
                mgf = padding.MGF1(algorithm=hashes.SHA256()),
                algorithm = hashes.SHA256(),
                label = None
                )
            )
        encrypted_filename = os.path.basename(self.filename)
        encrypted_filename = encrypted_filename[:encrypted_filename.index(".")]+".bin"
        path = self.filename[:self.filename.index(os.path.basename(self.filename))] + encrypted_filename
        
        # save encrypted key + file
        with open(path, "wb") as enf:
            enf.write(encrypted_key + self.output_file_data)
        
    def hybrid_decrypt(self):
        encrypted_key = self.loaded_file_data[:256]
        encrypted_file_data = self.loaded_file_data[256:]

        # decrypt AES key and IV with RSA
        decrypted_key = self.loaded_private_key.decrypt(
            encrypted_key,
            padding.OAEP(
                mgf = padding.MGF1(algorithm=hashes.SHA256()),
                algorithm = hashes.SHA256(),
                label = None
                )
            )
        # Split key and IV
        aes_key = decrypted_key[:32]
        iv = decrypted_key[32:]
        
        # decrypt file using AES
        cipher = Cipher(
            algorithms.AES(aes_key),
            modes.CFB(iv)
            )
        decryptor = cipher.decryptor()
        decrypted_file_data = decryptor.update(encrypted_file_data) + decryptor.finalize()

        # save decrypted file data
        filename = os.path.abspath(self.filename)
        # TODO: find solution to store encrypted then decrypt and set the file extension
        filename = filename[:filename.index(".")] + ".pdf"
        with open(filename, "wb") as decf:
            decf.write(decrypted_file_data)
        return True


    #write file data after encryption
    def write_file_data_after_encryption(self):
        filename = os.path.abspath("enc_"+os.path.basename(self.filename))
        #ext = len(filename) - filename.index('.')
        #with open(filename[:-ext], "wb") as encf:
        with open(filename, "wb") as encf:
            encf.write(self.output_file_data)
        #self.write_ext_to_index_file(filename[filename.index('.'):])
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
    
        
        
    
    
    
    
    
