import random

def powmod(num, pow, mod):
    res = 1

    num = num % mod
    while pow > 0:
        if pow & 1:
            res = (res * num) % mod

        pow >>= 1
        num = (num * num) % mod
    
    return res

def millerrabbin(num, k):
    if num <= 1 or num % 2 == 0:
        return False
    if num <= 3:
        return True

    d = num - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s = s + 1

    for i in range(k):
        r = random.randint(2,num-2)
        x = powmod(r,d,num)
        if x == 1 or x == num - 1:
            continue
        for j in range(s):
            x = (x * x) % num
            if x == 1:
                return False
            if x == num-1:
                break

        if x != num-1:
            return False

    return True
