import random
import math


def is_prime(n):
    """
    >>> is_prime(2)
    True
    >>> is_prime(11)
    True
    >>> is_prime(8)
    False
    """
    if (math.factorial(n - 1) + 1) % n != 0:
        return False
    else:
        return True


def gcd(a, b):
    """
    >>> gcd(12, 15)
    3
    >>> gcd(3, 7)
    1
    """
    while b != 0:
        a, b = b, a % b
    return a


def generate_keypair(p, q):
    if not (is_prime(p) and is_prime(q)):
        print('Both numbers must be prime.')
    elif p == q:
        print('p and q cannot be equal')
    n = p * q
    phi = (p - 1) * (q - 1)
    e = random.randrange(1, phi)
    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)
    d = multiplicative_inverse(e, phi)
    return ((e, n), (d, n))


def multiplicative_inverse(B, A):
    """
    >>> multiplicative_inverse(7, 40)
    23
    """
    L = []
    while A % B != 0:
        div = A // B
        mod = A % B
        L.append([A, B, mod, div])
        A = B
        B = mod
        if A % B == 0:
            div = A // B
            mod = A % B
            L.append([A, B, mod, div])
    x0 = 0
    y0 = 1
    i = len(L) - 1
    while i != 0:
        x1 = y0
        y1 = x0 - y0*L[i - 1][- 1]
        x0 = x1
        y0 = y1
        i -= 1
    d = y1 % L[0][0]
    return d


def encrypt(pk, plaintext):
    key, n = pk
    cipher = [(ord(char) ** key) % n for char in plaintext]
    return cipher


def decrypt(pk, ciphertext):
    key, n = pk
    plain = [chr((char ** key) % n) for char in ciphertext]
    return ''.join(plain)

if __name__ == '__main__':
    print("RSA Encrypter/ Decrypter")
    p = int(input("Enter a prime number (17, 19, 23, etc): "))
    q = int(input("Enter another prime number (Not one you entered above): "))
    print("Generating your public/private keypairs now . . .")
    public, private = generate_keypair(p, q)
    print("Your public key is ", public, " and your private key is ", private)
    message = input("Enter a message to encrypt with your private key: ")
    encrypted_msg = encrypt(private, message)
    print("Your encrypted message is: ")
    print(''.join(map(lambda x: str(x), encrypted_msg)))
    print("Decrypting message with public key ", public, " . . .")
    print("Your message is:")
    print(decrypt(public, encrypted_msg))
