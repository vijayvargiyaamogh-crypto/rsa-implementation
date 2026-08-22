p = 13
q = 67
n = p * q
message = input("Enter the text to be encrypted: ")
unicode = bytearray(message, "utf-8")
encrypt = bytes(pow(c, 65537, n) for c in unicode)
print(f"The encrypted text is: {encrypt.decode('utf-8')}")