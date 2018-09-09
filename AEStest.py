from Crypto.Cipher import AES
import base64

msg_text = b'test some plain text here'.rjust(32)
secret_key = b'1234567890123456' # create new & store somewhere safe

cipher = AES.new(secret_key,AES.MODE_ECB) # never use ECB in strong systems obviously
encoded = base64.b64encode(cipher.encrypt(msg_text))
# ...
decoded = cipher.decrypt(base64.b64decode(encoded))
print (decoded.strip())
