#from encryptor import Encryptor
from hencryptor import Hencryptor

if __name__ == "__main__":
	enc = Hencryptor()
	# generate and store keys
	#enc.generate_keys()
	#enc.store_keys()
	#load keys
	
	enc.load_keys()
	#enc.generate_aes_key()
	#enc.generate_iv()
	#enc.read_file_data_for_encryption("github.pdf")
	#enc.hybrid_encrypt()
	enc.load_file_data_for_decryption("github.pdf")
	enc.hybrid_decrypt()
	
