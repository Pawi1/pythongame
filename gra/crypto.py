from django.shortcuts import render
from django.conf import settings
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64

# def encrypt_data(data):
#     key = settings.SECRET_KEY[:32] 
#     cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC)
#     ciphertext = cipher.encrypt(pad(str(data).encode('utf-8'), AES.block_size))
#     return base64.b64encode(ciphertext).decode('utf-8')

# def decrypt_data(encrypted_data):
#     key = settings.SECRET_KEY[:32]
#     cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC)
#     decrypted_data = unpad(cipher.decrypt(base64.b64decode(encrypted_data.encode('utf-8'))), AES.block_size)
#     return decrypted_data.decode('utf-8')
def encrypt_data(data):
    key = settings.SECRET_KEY[:32].encode('utf-8')  # Klucz musi być bajtami
    cipher = AES.new(key, AES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(str(data).encode('utf-8'), AES.block_size))
    return base64.b64encode(cipher.iv + ciphertext).decode('utf-8')  # Dodaj wektor inicjalizacyjny do zaszyfrowanych danych

def decrypt_data(encrypted_data):
    key = settings.SECRET_KEY[:32].encode('utf-8')  # Klucz musi być bajtami
    encrypted_bytes = base64.b64decode(encrypted_data.encode('utf-8'))
    iv = encrypted_bytes[:AES.block_size]  # Pierwsze AES.block_size bajtów to wektor inicjalizacyjny
    ciphertext = encrypted_bytes[AES.block_size:]  # Pozostała część to zaszyfrowane dane
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return decrypted_data.decode('utf-8')

def set_encrypted_cookie(request, data):
    encrypted_data = encrypt_data(data)
    response = render(request, 'my_template.html', {'encrypted_data': encrypted_data})
    response.set_cookie('my_encrypted_cookie', encrypted_data)
    return response

def get_decrypted_cookie(request):
    encrypted_data = request.COOKIES.get('my_encrypted_cookie', '')
    decrypted_data = decrypt_data(encrypted_data)
    return render(request, 'my_template.html', {'decrypted_data': decrypted_data})
