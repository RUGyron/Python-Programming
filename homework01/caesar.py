def encrypt_caesar(plaintext, shift):
    """
    >>> encrypt_caesar("PYTHON", 3)
    'SBWKRQ'
    >>> encrypt_caesar("python", 3)
    'sbwkrq'
    >>> encrypt_caesar("", 3)
    ''
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
    return ciphertext


def decrypt_caesar(chipertext, shift):
    """
    >>> decrypt_caesar("SBWKRQ", 3)
    'PYTHON'
    >>> decrypt_caesar("sbwkrq", 3)
    'python'
    >>> decrypt_caesar("", 3)
    ''
    """
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
    return plaintext
