from millerrabin import powmod, millerrabbin
import random
from math import gcd
from hashlib import sha256
from binascii import hexlify
from mgf1 import mgf1

def generate_prime(minval, maxval, k):
    res = random.randint(minval,maxval)
    while not millerrabbin(res, k):
        res = random.randint(minval,maxval)
    return res

def egcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        gcd, x, y = egcd(b % a, a)
        return gcd, y - (b // a) * x, x

class RSAOAEP:
    LENGTH = 1024
    k = 20

    #OAEP data
    k0 = 24
    k1 = 24

    def __init__(self):
        self.p = generate_prime(2,2**RSAOAEP.LENGTH, RSAOAEP.k)
        self.q = generate_prime(2,2**RSAOAEP.LENGTH, RSAOAEP.k)
        self.n = self.p * self.q
        self.pn = (self.p-1)*(self.q-1) // gcd(self.p-1,self.q-1)

        self.e = 65537
        while gcd(self.e, self.pn) != 1:
            self.e = self.e + 2

        g_, self.d, y_ = egcd(self.e, self.pn)
        if self.d < 0:
            self.d = self.pn - (-self.d) % self.pn

        # additional data for crt decryption
        self.dp = self.d % (self.p-1)
        self.dq = self.d % (self.q-1)

        self.qinv = pow(self.q,-1,self.p)

    def encrypt(self, m, e, n):
        return powmod(m, e, n)

    def decrypt(self, m):
        return powmod(m, self.d, self.n)

    def crtdecrypt(self, m):
        m1 = pow(m,self.dp,self.p)
        m2 = pow(m,self.dq,self.q)

        h = self.qinv * (m1 - m2)
        m = (m2 + h * self.q) % self.n

        return m

    def publish_public_key(self):
        return self.e, self.n

    def oaepencrypt(self, m, e, n):
        m = m << RSAOAEP.k1
        r = random.randint(2**(RSAOAEP.k0-1),2**RSAOAEP.k0)
        
        rs = str(r)
        rs = hexlify(mgf1(rs.encode(),(RSAOAEP.LENGTH - RSAOAEP.k0) // 8))
        X = m^int(rs,16)

        Xs = str(X)
        Xs = hexlify(mgf1(Xs.encode(), RSAOAEP.k0 // 8, sha256))
        Y = r^int(Xs,16)

        return self.encrypt((X << RSAOAEP.k0) | Y, e, n)

    def oaepdecrypt(self, c):
        m = self.crtdecrypt(c)

        X = m >> RSAOAEP.k0
        Y = m % X

        Xs = str(X)
        Xs = hexlify(mgf1(Xs.encode(), RSAOAEP.k0 // 8, sha256))
        r = Y^int(Xs,16)

        rs = str(r)
        rs = hexlify(mgf1(rs.encode(),(RSAOAEP.LENGTH - RSAOAEP.k0) // 8))
        res = X^int(rs,16)
        res = res >> RSAOAEP.k1

        return res

    def encrypt_text(self, txt, e, n):
        num = ""
        for c in txt:
            t = str(ord(c))
            while len(t) < 3:
                t = "0" + t
            num = num + t
        m = int(num)
        l = len(bin(m)) - 2
        mpadded = m << (RSAOAEP.LENGTH - RSAOAEP.k0 - RSAOAEP.k1 - l)
        mpadded = mpadded^(2**(RSAOAEP.LENGTH - RSAOAEP.k0 - RSAOAEP.k1 - l - 1))
        return self.oaepencrypt(mpadded, e, n)

    def decrypt_text(self, c):
        mpadded = self.oaepdecrypt(c)
        temp = str(bin(mpadded))
        temp = temp.rstrip('0')
        temp = temp[:-1]
        num = int(temp, 2)
        res = ""
        while num > 0:
            c = num % 1000
            res = res + chr(c)
            num = num // 1000
        return res[::-1]


if __name__ == "__main__":
    rsa = RSAOAEP()
    e, n = rsa.publish_public_key()
    enc = rsa.encrypt_text("now longer time", e, n)
    print(enc)
    dec = rsa.decrypt_text(enc)
    print(dec)
