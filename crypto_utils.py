from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64

KEY = b'ThisIsASecretKey'     # 16 bytes
IV = b'ThisIsAnIV456789'      # 16 bytes

def encrypt_message(msg: str) -> str:
    cipher = AES.new(KEY, AES.MODE_CBC, IV)
    padded = pad(msg.encode(), AES.block_size)
    encrypted = cipher.encrypt(padded)
    return base64.b64encode(encrypted).decode()

def decrypt_message(enc: str) -> str:
    try:
        cipher = AES.new(KEY, AES.MODE_CBC, IV)
        decoded = base64.b64decode(enc)
        decrypted = cipher.decrypt(decoded)
        return unpad(decrypted, AES.block_size).decode()
    except (ValueError, base64.binascii.Error):
        return ""  # Return blank to indicate failure
