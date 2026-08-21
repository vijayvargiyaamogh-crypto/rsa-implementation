# Some useful functions that can be imported elsewhere

import math

def isPrime(n: int) -> bool:
    # Returns True if n is prime, False otherwise

    if n < 2:
        return False
    # Also returns False for negatives of primes (-2, -3, etc.)

    if n < 4:
        return True
    # Acknowledges 2 and 3 as prime in a single expression

    if not n&1:
        return False
    # The bitwise-AND expression n&1 is 1 iff n is odd
    # This block precludes even numbers from primality testing

    for d in range(3, int(math.sqrt(n))+1, 2):
        # Only odd divisors are required since n is odd
        # Only divisors up to sqrt(n) are required
        # If n % d == 0 where d > sqrt(n), n % (n//d) == 0
        # Here n//d < sqrt(n), hence d up to sqrt(n) is enough
        if n % d == 0:
            return False
    # If nothing has been returned yet, n must be prime
    return True

def generateSieve(n: int) -> list[bool]:
    # Sieve refers to the sieve of Eratosthenes' algorithm
    # Precomputes whether each number i < n is prime or not
    # Returns a list where list[i] is True iff i is prime
    # Running isPrime(i) for each individual i < n is too slow
    # That would have a time complexity of order n*sqrt(n)
    # This has a time complexity of only n*log(log(n))
    # The reason for this is provided along the way

    isPrime = [True for i in range(n)]
    # Every number i is prime until proven otherwise

    isPrime[0] = isPrime[1] = False
    # 0 and 1 are conventionally non-prime

    for i in range(4, n, 2):
        isPrime[i] = False
    # Since no even number > 2 can be prime
    # This loop does not execute for n <= 4
    # But no one would use such a sieve anyway
    # The code hereafter assumes a reasonable user

    for p in range(3, int(math.sqrt(n))+1, 2):
        # This loop scans the sieve with each odd divisor p
        # Going only up to sqrt(n) for aforementioned reasons
        if isPrime[p]:
            # The divisor p must also be prime
            # If a potential divisor was eliminated, then
            # Its multiples would have already been eliminated
            # So no need to bother with it
            for i in range(p*p, n, p):
                # Ignoring multiples from p*2 to p*(p-1)
                # Since they'd've been already eliminated
                # By a divisor less than p
                # The range is just p*p, p*(p+1), p*(p+2), ...
                isPrime[i] = False
    return isPrime
            
    # Postscript 1:
    # math.sqrt(n) can be precomputed for further optimization

    # Postscript 2: (On time complexity)
    # The number of steps is roughly n//2 + n//3 + n//5 + ...
    # This is n times the prime harmonic series
    # Since the density of primes around x ~ 1/log(x)
    # The prime harmonic series sums to roughly log(log(n))
    # Hence the time complexity is n*log(log(n))

def primeCount(a: int, b: int | None = None) -> int:
    # Prime-counting function that takes 1 or 2 arguments

    if b is None:
        lower = 0
        upper = a
    # If 1 argument given, return number of primes <= a

    else:
        lower = a
        upper = b
    # If 2 arguments given, return number of primes in [a, b]
    # Renamed a and b to lower and upper for clarity
    # Note: The range [a, b] includes both a and b

    sieve = generateSieve(upper+1)
    # The previous function comes to the rescue

    return sum(1 for i in range(lower, upper+1) if sieve[i])
    # Counts primes by assigning 1 to each and then summing
    # Returns an error if no primes are found
    # Hopefully this doesn't happen

def primeFactorize(n: int) -> dict[int, int]:
    # Returns the prime factorization of n as a dictionary
    # The keys are the primes and the values are the exponents
    # For example, primeFactorize(60) -> {2: 2, 3: 1, 5: 1}

    factorization = {}

    if not n&1:
        # Equivalent to "if n % 2 == 0" or "if n is even"
        factorization[2] = 0
        # The prime 2 has been included in its factorization
        # Now all that remains is to compute its exponent
        while not n&1:
            factorization[2] += 1
            n //= 2
        # The loop terminates once n is no longer even
        # In other words, all its 2s have been factored out

    d = 3
    while d*d <= n:
        # Alternative to d < int(math.sqrt(n))+1
        if n%d == 0:
            # d divides n
            factorization[d] = 0
            # Include d in its factorization
            while n % d == 0:
                factorization[d] += 1
                n //= d
            # All instances of d have been factored out
        d += 2
        # Note: The if condition can only be met by a prime d
        # If n used to be divisible by a prime p < d, then
        # All instances of p have already been factored out
        # By the repeated n //= p operation
    return factorization

def divisorCount(n: int) -> int:
    # Counts number of divisors using a combinatorial trick
    # Includes 1 and n

    factorization = primeFactorize(n)
    # This will come in handy
    # If n = (p_1 ^ a_1)(p_2 ^ a_2)(p_3 ^ a_3)..., then
    # There are (a_i + 1) choices for the exponent of p_i
    # Each set of choices describes a unique divisor of n
    # Then just apply the multiplication principle of counting

    count = 1 # Initialize product to 1
    for exponent in factorization.values():
        count *= exponent+1
    return count

def gcd(a: int, b: int) -> int:
    # Returns the greatest common divisor (GCD) of a and b
    # Also known as the highest common factor (HCF)

    if a == 0:
        return b
        # b is its own greatest divisor and obviously divides 0
    return gcd(b%a, a)
    # Because gcd(a, b) = gcd(b%a, a) but uses smaller numbers
    # 0 <= b%a < a-1 and the first argument keeps shrinking

def lcm(a: int, b: int) -> int:
    # Returns the least common multiple (LCM) of a and b
    # Uses the property that GCD * LCM = product of a and b

    return (a*b) // gcd(a, b)

def extendedGCD(a: int, b: int) -> tuple[int, int, int]:
    # Returns three integers gcd, x, y
    # The pair (x, y) is one solution to Bezout's identity
    # Bezout's identity: a*x + b*y = gcd(a, b)

    if a == 0:
        return b, 0, 1 # Because 0*a + 1*b = gcd(a, b) = b
    # gcd(a, b) not invoked as its an unnecessary dependency

    gcd, x, y = extendedGCD(b%a, a) # Just like standard gcd()

    return gcd, y - (b//a)*x, x
    # Take this on faith

    # The modular multiplicative inverse of a modulo m
    # Can be written as x % m when it exists
    # Where x is just extendedGCD(a, m)[1]
    # Hence this function is useful later also

def modInverse(a: int, m: int) -> int:
    # Returns the modular multiplicative inverse of a modulo m
    # i.e., returns x in [1, m-1] such that a*x = 1 (mod m)
    # a and m must be co-prime for inverse to exist
    # gcd(a, m) == 1 condition can be checked for this

    gcd, x, y = extendedGCD(a, m)
    return x % m # Brings x into [1, m-1] range

def modExp(base: int, exp: int, m: int) -> int:
    # Does exactly the same thing as Python's inbuilt pow()
    # Calculates (base ^ exp) % m without base ^ exp
    # Essentially uses the property (a*b) % m = (a%m) * (b%m)
    # Called the modular exponentiation function

    # Breaks down higher powers into squares
    # e.g., 3^27 = (3^13)^2 * 3 = ((3^6)^2 * 3)^2 * 3 and so on
    # Time complexity ~ log(exp) because of divide-and-conquer

    if exp == 0:
        # Base case
        return 1

    if exp & 1:
        # Odd exponent
        return (modExp(base, exp-1, m) * base) % m
    # Even exponent otherwise
    return (modExp(base, exp//2, m) ** 2) % m

def eulerTotient(n: int) -> int:
    # Returns count of numbers in [1, n] co-prime with n

    factorization = primeFactorize(n).keys()
    # Creates a view of all distinct prime factors of n

    for p in factorization:
        n -= n//p
    return n
    # This is a standard method