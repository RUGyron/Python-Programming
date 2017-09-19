def encrypt_caesar(plaintext, shift):
    
    """
    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    
    """
    
    ciphertext = ""
    for i in plaintext:
        if 96 < ord(i) < 123:
            if ord(i) > 96 + 26 - shift:
                ciphertext = ciphertext + chr(ord(i) + shift - 26)
            else:
                ciphertext = ciphertext + chr(ord(i) + shift)
        elif 64 < ord(i) < 91:
            if ord(i) > 64 + 26 - shift:
                ciphertext = ciphertext + chr(ord(i) + shift - 26)
            else:
                ciphertext = ciphertext + chr(ord(i) + shift)
        else:
            return print("Error: incorrect symbol")
    return ciphertext

def decrypt_caesar(chipertext, shift):
    plaintext = ""
    for i in chipertext:
        if 96 < ord(i) < 123:
            if ord(i) < 96 + shift:
                plaintext = plaintext + chr(ord(i) - shift + 26)
            else:
                plaintext = plaintext + chr(ord(i) - shift)
        elif 64 < ord(i) < 91:
            if ord(i) < 64 + shift:
                plaintext = plaintext + chr(ord(i) - shift + 26)
            else:
                plaintext = plaintext + chr(ord(i) - shift)
        else:
            return print("Error: incorrect symbol")
    return plaintext

#print(encrypt_caesar("python",3))
#print(encrypt_caesar("",3))
#print(encrypt_caesar("PYTHON",3))
#print(decrypt_caesar("sbwkrq",3))
#print(decrypt_caesar("",3))
#print(decrypt_caesar("SBWKRQ",3))