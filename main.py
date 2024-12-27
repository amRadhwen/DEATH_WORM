from encryptor import Encryptor


if __name__ == "__main__":
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