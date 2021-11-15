from rsa import RSA
from rsaoaep import RSAOAEP
import datetime

if __name__ == "__main__":
    #initialization time
    start = datetime.datetime.now()
    rsa1 = RSA()
    end = datetime.datetime.now()
    elapsed = end - start
    print(f"RSA initialization time: {int(elapsed.total_seconds() * 1000)}ms")

    start = datetime.datetime.now()
    rsa2 = RSAOAEP()
    end = datetime.datetime.now()
    elapsed = end - start
    print(f"RSAOAEP initialization time: {int(elapsed.total_seconds() * 1000)}ms")

    #encryption and decryption time for RSA
    start = datetime.datetime.now()
    enc = rsa1.encrypt_text("1st level wizard dies of 1d4 damage", rsa1.e, rsa1.n)
    end = datetime.datetime.now()
    elapsed = end - start
    print(f"Encrypted message: {enc}\nTime elapsed: {int(elapsed.total_seconds() * 1000)}ms")

    start = datetime.datetime.now()
    dec = rsa1.decrypt_text(enc)
    end = datetime.datetime.now()
    elapsed = end - start
    print(f"Decrypted message: {dec}\nTime elapsed: {int(elapsed.total_seconds() * 1000)}ms")

    # the same but for RSAOAEP
    start = datetime.datetime.now()
    enc = rsa2.encrypt_text("1st level wizard dies of 1d4 damage", rsa2.e, rsa2.n)
    end = datetime.datetime.now()
    elapsed = end - start
    print(f"Encrypted message: {enc}\nTime elapsed: {int(elapsed.total_seconds() * 1000)}ms")

    start = datetime.datetime.now()
    dec = rsa2.decrypt_text(enc)
    end = datetime.datetime.now()
    elapsed = end - start
    print(f"Decrypted message: {dec}\nTime elapsed: {int(elapsed.total_seconds() * 1000)}ms")