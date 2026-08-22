p = 67
q = 71
n = p * q
phi = (p-1) * (q-1)
e = 65537
d = pow(e, -1, phi)
message = input("Enter the message to be encrypted: ")
unicode = bytearray(message, "utf-8")
encrypted = [pow(c, e, n) for c in unicode]
print(f"The encrypted message is: {encrypted}")
encrypted = [int(c) for c in input("Enter the message to be decrypted: ").split()]
decrypted = bytes(pow(c, d, n) for c in encrypted)
print(f"The decrypted message is: {decrypted.decode('utf-8')}")