#from encryptor import Encryptor
from asencryptor import Asencryptor


asenc = Asencryptor()
asenc.generate_files_ext_index()
asenc.generate_keys()
asenc.store_keys()
asenc.load_keys()
asenc.read_file_data_for_encryption("helloworld.txt")
asenc.encrypt()
asenc.write_file_data_after_encryption()
asenc.remove_orgfile_after_encryption()
asenc.load_file_data_for_decryption("enc_helloworld")
asenc.decrypt()
asenc.write_file_data_after_decryption()
asenc.remove_encrypted_file_after_decryption()

if __name__ == "__main__":
    '''
	enc = Encryptor()
	input_file = "helloworld.txt"
	encrypted_file = "enc_helloworld"
	decrypted_file = "dec_helloworld.txt"
 
	#encryption
	key, iv = enc.encrypt(input_file, encrypted_file)
	if key and iv:
		print("File encrypted successfully :)")
		print(f"Key: {key}")
		print(f"IV: {iv}")
		#decryption
		enc.decrypt(key, iv, encrypted_file, decrypted_file)
		print("File decrypted successfully :)")
	else:
		print("Encryption Failed !")
  	'''
	