import math

def sieve0(n):
    if n < 2:
        return 0
    if n == 2:
        return 1

    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False 

    n_sqrt = int(math.sqrt(n))
    res = 0

    # Sieve of Eratosthenes algorithm
    for i in range(2, n_sqrt + 1):
        if is_prime[i]:
            for j in range(i * i, n + 1, i):
                is_prime[j] = False

    # Count prime numbers
    res = sum(is_prime)
    return res
