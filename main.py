#from encryptor import Encryptor
from encryptor import Encryptor

if __name__ == "__main__":
	enc = Encryptor()
	# generate and store keys
	#enc.generate_keys()
	#enc.store_keys()

	#load keys
	enc.load_keys()
	enc.read_file_data_for_encryption("monochrome.png")
	enc.encrypt()
