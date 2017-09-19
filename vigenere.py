def encrypt_vigenere(plaintext,keyword):
    
    """
    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """    
    
    k = 0
    ciphertext = ""
    if plaintext.islower():
        keyword = keyword.lower()
    elif plaintext.isupper():
        keyword = keyword.upper()
    else:
        return print("Symbols have to be the same size")
    while len(plaintext) > len(keyword):
        keyword = keyword + keyword
    while len(keyword) > len(plaintext):
        keyword=keyword[:-1]
    for i in plaintext:
        if plaintext.islower():
            if ord(i) > 96 + 26 - ord(keyword[k]) + 96: 
                ciphertext = ciphertext + chr(ord(i) + ord(keyword[k]) - 97 - 26)
            else:
                ciphertext = ciphertext + chr(ord(i) + ord(keyword[k]) - 97)
        elif plaintext.isupper():
            if ord(i) > 64 + 26 - ord(keyword[k]) + 64:
                ciphertext = ciphertext + chr(ord(i) + ord(keyword[k]) - 65 - 26)
            else:
                ciphertext = ciphertext + chr(ord(i) + ord(keyword[k]) - 65)
        k = k+1                
    return ciphertext

def decrypt_vigenere(ciphertext,keyword):
    
    """
    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """    
    
    plaintext = ""
    k = 0   
    if ciphertext.islower():
        keyword = keyword.lower()
    elif ciphertext.isupper():
        keyword = keyword.upper()
    else:
        return print("Symbols have to be the same size")
    while len(ciphertext) > len(keyword):
        keyword = keyword + keyword
    while len(keyword) > len(ciphertext):
        keyword=keyword[:-1]
    for i in ciphertext:
        if ciphertext.islower():
            if ord(i) < ord(keyword[k]):
                plaintext = plaintext + chr(ord(i) - ord(keyword[k]) + 97 + 26)
            else:
                plaintext = plaintext + chr(ord(i) - ord(keyword[k]) + 97)
        elif ciphertext.isupper():
            if ord(i) < ord(keyword[k]):
                plaintext = plaintext + chr(ord(i) - ord(keyword[k]) + 65 + 26)
            else:
                plaintext = plaintext + chr(ord(i) - ord(keyword[k]) + 65)
        k = k+1
    return plaintext