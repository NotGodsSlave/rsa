from millerrabin import powmod, millerrabbin
import random
from math import gcd

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

class RSA:
    LENGTH = 1024
    k = 20

    def __init__(self):
        self.p = generate_prime(2,2**RSA.LENGTH, RSA.k)
        self.q = generate_prime(2,2**RSA.LENGTH, RSA.k)
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

    def encrypt_text(self, txt, e, n):
        num = ""
        for c in txt:
            t = str(ord(c))
            while len(t) < 3:
                t = "0" + t
            num = num + t
        return self.encrypt(int(num), e, n)

    def decrypt_text(self, c):
        num = self.crtdecrypt(c)
        res = ""
        while num > 0:
            c = num % 1000
            res = res + chr(c)
            num = num // 1000
        return res[::-1]


if __name__ == "__main__":
    rsa = RSA()
    e, n = rsa.publish_public_key()
    enc = rsa.encrypt_text("Hello World!", e, n)
    dec = rsa.decrypt_text(enc)
    print(f"Encrypted text: {enc}, decrypted text: {dec}")