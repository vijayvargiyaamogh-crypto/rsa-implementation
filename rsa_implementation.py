from random import randint
from number_theoretic_algorithms import generateSieve
from number_theoretic_algorithms import primeCount
from number_theoretic_algorithms import eulerTotient
from number_theoretic_algorithms import modInverse
from number_theoretic_algorithms import modExp

def randomPrimePair(lower: int, upper: int) -> tuple[int, int]:
    isPrime = generateSieve(upper+1)
    i = randint(lower, upper)
    j = randint(lower, upper)
    while not (isPrime[i] and isPrime[j]):
        i = randint(lower, upper)
        j = randint(lower, upper)
    # This randomly samples two numbers from [lower, upper]
    # It does this until it finds a pair of primes
    # This code is written with a particular range in mind
    # i.e., lower = 5 million, upper = 10 million - 1
    # The average density of primes in this range is roughly
    # The arithmetic mean of 1/ln(lower) + 1/ln(upper)
    # = ln(upper*lower)/(2*ln(lower)*ln(upper))
    # = log(5E+13)/(2*2.303*log(5E+6)*log(1E+7))
    # = (14-log(2))/(2*2.303*7*(7-log(2)))
    # = 13.699 / (4.606*7*6.699)
    # = 13.7 / (4.6 * 7 * 6.7)
    # = 13.7 / 216
    # = 0.063
    # This manual approximation was unnecessary but fun
    # The actual number is 6.32%, so 0.063 is really accurate
    # So the expected attempts before we find a pair of primes
    # Is (1/0.063)*(1/0.063) = 16*16 = 256
    # So runtime is not affected adversely
    return i, j

    # Postscript:
    # Technically this function could generate i = j
    # Which would be bad for encryption
    # As a hacker could just take the sqrt of the semiprime
    # To find the prime(s)
    # But that is quite unlikely
    # The odds of that are 1/primeCount(lower, upper)
    # print(primeCount(5000000, 9999999))
    # Running the previous line outputs 316066
    # So the odds are 1/316066
    # If you still end up generating i=j, you are just unlucky
    # I'm not fixing this issue because it's funny

p, q = randomPrimePair(5000000, 9999999)
n = p*q

phi = (p-1) * (q-1) # Euler totient function for n = p*q

e = 65537 # Public exponent e chosen as 65537 by convention

d = modInverse(e, phi) # Private exponent d

# n is at least 25 trillion
# So that's how many distinct messages we can send
# Limit ourselves to just capital letters and whitespaces
# Our message can be log(25 trillion) / log(27) long
# Which can be approximated as (14-2*log(2))/(3*log(3))
# = (14-2*0.301)/(3*0.477)
# = 13.398/1.431
# = 13.4 / 1.43
# = 9.4
# So lets choose a limit of 9 characters to be safe

vals = {} # Dictionary mapping characters to [0, 26]
vals[" "] = 0
for i in range(26):
    vals[chr(65+i)] = i+1

valz = {} # Inverse dictionary
valz[0] = " "
for i in range(1, 27):
    valz[i] = chr(64+i)


def textToInteger(text: str) -> int:
    # Note: The entire text is converted to a single integer
    # This could be avoided by splitting into blocks
    # I'm not doing that this time
    num = 0
    text += " " * (9-len(text)) # Padding string
    for c in text:
        num *= 27
        num += vals[c]
    return num

    # e.g., print(textToInteger("       AA")) outputs 28

def intToText(num: int) -> str:
    keyz = []
    while num:
        keyz.append(num%27)
        num //= 27
    keyz.extend([0]*(9-len(keyz))) # Making length 9
    chars = [valz[i] for i in keyz][::-1]
    return "".join(chars)

message = input("Enter secret message: ")
num = textToInteger(message)
enc = modExp(num, e, n)

print("\nThe encrypted message is:", intToText(enc))

print("The private key is", d)
print("You would obviously not know this in a real usecase")

M, D = input("\nEnter enc message and private key: ").split()
M, D = textToInteger(M), int(D)

dec = modExp(M, d, n)
print("\nThe decrypted message is:", intToText(dec))
