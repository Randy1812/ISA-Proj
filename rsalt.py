def gcd(a, b):
    if b == 0:
        return a
    else:
        return gcd(b, a % b)


def encrypt():
    p = 13
    q = 31
    r = 157
    s = 173
    n = p * q * r
    totient = (p - 1) * (q - 1) * (r - 1)*(s-1)
    e = d = -1
    ct = 0
    for i in range(2, totient):
        if ct == 1:
            break
        if gcd(i, totient) == 1:
            e = i
            ct += 1
    ed = 1
    while True:
        ed = ed + totient
        if ed % e == 0:
            d = int(ed / e)
            break
    with open("input.txt", "r", encoding='utf-8') as fin:
        message = fin.read()
    print(f"The message in the file is :\n{message}")
    msg = [ord(i) for i in message]
    enc = [pow(i, e, n) for i in msg]
    print("\nThe encrypted message is :")
    with open("encrypted.txt", "w", encoding='utf-8') as fout:
        for i in enc:
            fout.write(chr(i))
            print(chr(i), end="")


def decrypt():
    p = 13
    q = 31
    r = 157
    s = 173
    n = p * q * r
    totient = (p - 1) * (q - 1) * (r - 1)*(s-1)
    e = d = -1
    ct = 0
    for i in range(2, totient):
        if ct == 1:
            break
        if gcd(i, totient) == 1:
            e = i
            ct += 1
    ed = 1
    while True:
        ed = ed + totient
        if ed % e == 0:
            d = int(ed / e)
            break
    with open("encrypted.txt", "r", encoding='utf-8') as fin:
        encmsg = fin.read()
    print(f"The encrypted message is :\n{encmsg}")
    enc = [ord(i) for i in encmsg]
    dec = [pow(i, d, n) for i in enc]
    print("\nThe decrypted message is :")
    with open("decrypted.txt", "w", encoding='utf-8') as fout:
        for i in dec:
            fout.write(chr(i))
            print(chr(i), end="")


choice = int(input("MENU\n1.Encryption\n2.Decryption\n\nEnter your choice : "))
if choice == 1:
    encrypt()
elif choice == 2:
    decrypt()
