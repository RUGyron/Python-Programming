def encrypt_vigenere(plaintext, keyword):
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
    keyword = keyword.lower()
    while len(plaintext) > len(keyword):
        keyword = keyword + keyword
    while len(keyword) > len(plaintext):
        keyword = keyword[: - 1]
    for i in plaintext:
        if i.islower():
            if ord(i) > 96 + 26 - ord(keyword[k]) + 96:
                ciphertext = ciphertext + chr(ord(i) +
                                              ord(keyword[k]) - 97 - 26)
            else:
                ciphertext = ciphertext + chr(ord(i) + ord(keyword[k]) - 97)
        elif i.isupper():
            if ord(i) > 64 + 26 - ord(keyword[k]) + 96:
                ciphertext = ciphertext + chr(ord(i) +
                                              ord(keyword[k]) - 97 - 26)
            else:
                ciphertext = ciphertext + chr(ord(i) + ord(keyword[k]) - 97)
        k = k + 1
    return ciphertext


def decrypt_vigenere(ciphertext, keyword):
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
    keyword = keyword.lower()
    while len(ciphertext) > len(keyword):
        keyword = keyword + keyword
    while len(keyword) > len(ciphertext):
        keyword = keyword[: - 1]
    for i in ciphertext:
        if i.islower():
            if ord(i) < ord(keyword[k]):
                plaintext = plaintext + chr(ord(i) - ord(keyword[k]) + 97 + 26)
            else:
                plaintext = plaintext + chr(ord(i) - ord(keyword[k]) + 97)
        elif i.isupper():
            if ord(i) < ord(keyword[k]) - 32:
                plaintext = plaintext + chr(ord(i) - ord(keyword[k]) + 97 + 26)
            else:
                plaintext = plaintext + chr(ord(i) - ord(keyword[k]) + 97)
        k = k + 1
    return plaintext
