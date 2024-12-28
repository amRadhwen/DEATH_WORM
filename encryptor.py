# class makes copy of original file the encrypt and decrypt it
# using AES
# libraries


from os import urandom
from Cryptodome.Cipher import AES

class Encryptor:
    def __init__(self) -> None:
        pass
    
    def padd(self, data):
        padding_len = 16 - len(data) % 16
        padding = bytes([padding_len] * padding_len)
        return data + padding
    
    def unpadd(self, data):
        padding_len = data[-1]
        if padding_len < 1 or padding_len > 16:
            raise ValueError("Invalid padding encountred !")
        return data[:-padding_len]
    
    def encrypt(self, input_file, output_file):
        key = urandom(32)
        iv = urandom(16)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        try:
            with open(input_file, 'rb') as f:
                plaintext = f.read()
            padded_plaintext = self.padd(plaintext)
            ciphertext = cipher.encrypt(padded_plaintext)
            with open(output_file, 'wb') as f:
                f.write(ciphertext)
            encoded_key = key.hex()
            encoded_iv = iv.hex()
            return encoded_key, encoded_iv
        except Exception as e:
            print(f'An error occured during encryption: {e}')
            return None, None
        
    def decrypt(self, key, iv, input_file, output_file):
        try:
            decoded_key = bytes.fromhex(key)
            iv_bytes = bytes.fromhex(iv)
            if len(decoded_key) != 32:
                raise ValueError("Incorrect AES key length !")
            cipher = AES.new(decoded_key, AES.MODE_CBC, iv_bytes)
            with open(input_file, 'rb') as f:
                encrypted_data = f.read()
            decrypted_data = self.unpadd(cipher.decrypt(encrypted_data))
            with open(output_file, 'wb') as f:
                f.write(decrypted_data)
        except Exception as e:
                print(f'An error occured during decryption: {e}')
                
                