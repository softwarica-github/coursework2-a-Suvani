import numpy as np
import random
from math import sqrt
XA = 1
q = 1
a = 1
def setXA(num):
    XA = num
def getXA():
    return XA
def setq(num):
    q = num
def getq():
    return q
def seta(num):
    a = num
def geta():
    return a
def power(x, y, p):
    res = 1
    x = x % p
    while y > 0:
        if y & 1:
            res = (res * x) % p
        y = y >> 1
        x = (x * x) % p
    return res

def findPrimefactors(s, n):
    while n % 2 == 0:
        s.add(2)
        n = n // 2
    for i in range(3, int(sqrt(n)), 2):
        while n % i == 0:
            s.add(i)
            n = n // i
    if n > 2:
        s.add(n)

def findPrimitive(n):
    s = set()
    phi = n - 1
    findPrimefactors(s, phi)
    for r in range(2, phi + 1):
        flag = False
        for it in s:
            if power(r, phi // it, n) == 1:
                flag = True
                break
        if flag == False:
            return r
    return -1

def generate_public_key():
    while 1:
        q = random.randrange(100, 999)
        i = q - 1
        ct = 0
        while i >= 5:
            if q % i == 0:
                ct += 1
                break
            i -= 1
        if ct == 0:
            break
    a = 15
    seta(a)
    XA = random.randrange(0, q - 1)
    temp = a ** XA
    YA = temp % q
    publickey = [q, a, YA, XA]
    return publickey

def incrypt_gamal(q, a, YA, text):
    text = list(text)
    asc = []
    for i in range(len(text)):
        asc.append(ord(text[i]))
    M = asc
    k = random.randrange(0, q)
    temp = YA ** k
    K = temp % q
    temp = a ** k
    C1 = temp % q
    C2 = []
    for i in range(len(M)):
        temp = K * M[i]
        out = temp % q
        C2.append(out)
    returnedvalue = ""
    returnedvalue += str(C1) + ","
    for i in range(len(C2)):
        returnedvalue += str(C2[i]) + ","
    returnedvalue += str(q)
    return returnedvalue
def decrept_gamal(messagecopy, XA):
    tempmessage = messagecopy.split(",")
    C1 = int(tempmessage[0])
    q = int(tempmessage[-1])
    C2 = []
    for i in range(len(tempmessage)):
        if i != 0 and i != len(tempmessage) - 1:
            C2.append(int(tempmessage[i]))
    temp = C1 ** XA
    K = temp % q
    kinverse = K
    ct = 1
    while (kinverse * ct) % q != 1:
        ct += 1
    kinverse = ct
    output = []
    for i in range(len(C2)):
        temp = C2[i] * kinverse
        letter = temp % q
        output.append(letter)
    decryptedText = ""
    for i in range(len(output)):
        temp = chr(output[i])
        decryptedText = decryptedText + temp
    return decryptedText
