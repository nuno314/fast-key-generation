# Le Hoang Trong Tin
# 19120682
import numpy as np
import random as rd
import time

# Generate nxn lower matrix 
def gen_lower_matrix(n):
    l_matrix = []
    for i in range(n):
        row = []
        for j in range(n):
            if i==j:
                row.append(1)
            elif i > j:
                row.append(0)
            else: # i < j
                row.append(rd.randint(0,1))
        l_matrix.append(row)
    return l_matrix

# Generate nxn upper matrix
def gen_upper_matrix(n):
    u_matrix = []
    for i in range(n):
        row = []
        for j in range(n):
            if i==j:
                row.append(1)
            elif i < j:
                row.append(0)
            else: # i > j
                row.append(rd.randint(0,1))
        u_matrix.append(row)
    return u_matrix

def gen_fast_key(n, p):
    L = np.array(gen_lower_matrix(n))
    U = np.array(gen_upper_matrix(n))
    key = (L @ U) % p
   # key %= 2
    I = np.identity(n)
    X = []
    Y = []
    
    # Solve L.iY = ie
    for i in range(n):
        Y.append(np.linalg.solve(L, I[i]) % p)

    # Solve U.iX = iY
    for i in range(n):
        X.append(np.linalg.solve(U, Y[i]) % p)

    iKey = (np.transpose(np.array(X)).astype(int))
    
    return np.array(key), iKey

def matrix_to_array(m):
    arr = []
    for i in range(len(m)):
        for j in range(len(m[i])):
            arr.append(m[i][j])

    return arr

def encrypt(plain_text, key, p):

    cipher_text = []
    
    n = len(key)
  
    while len(plain_text) % n != 0:
        plain_text.append(0)
    
    plain_text = [plain_text[i:i +n] for i in range(0, len(plain_text), n)]
    
    for i in range(0,len(plain_text)):
        m = np.array(plain_text[i])
        c = (key @ m) % p
        cipher_text.append(c)

    return np.array(cipher_text)

def decrypt(cipher_text, i_key, p):

    plain_text = []
    
    for i in range(0, len(cipher_text)):
        c = cipher_text[i]
        m = (i_key @ c) % p
        plain_text.append(m)

    return plain_text

# Generate plain text
plain_text = []
for i in range(1024):
    plain_text.append(rd.randint(0,1))

# Init n, p, key, inverse key
n = 10
p = 2

# Fast Key Generation
key_start = time.time()
k, ik = gen_fast_key(n, p)
key_finish = time.time()

# Encryption
encrypt_start = time.time()
cipher_text = encrypt(plain_text, k, p)
encrypt_finish = time.time()

# Decryption
decrypt_start = time.time()
new_plain_text = decrypt(cipher_text, ik, p)
decrypt_finish = time.time()

# Format to compare
new_plain_text = np.array(new_plain_text)
old_plain_text = np.array_split(plain_text, len(plain_text)/n)

# Information
print('Plaintext: ')
print(plain_text)

print('Ciphertext: ')
print(matrix_to_array(cipher_text))
# for i in cipher_text:
#     print(i)

print('Decrypted: ')
print(matrix_to_array(new_plain_text))

print('Fast Key Generation Time: ', format(key_finish - key_start))
print('Encryption Time: ', format(encrypt_finish - key_start))
print('Decryption Time: ', format(decrypt_finish - decrypt_start))

check = old_plain_text == new_plain_text
check = check.all()
print('Correct: ', check)
print(len(new_plain_text))