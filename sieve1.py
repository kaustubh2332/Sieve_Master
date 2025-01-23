import math
from multiprocessing import Pool, cpu_count

def mark_primes(is_prime, n):
    """Marks non-prime numbers in the range [0, n]."""
    i_limit = int(math.sqrt(n))
    is_prime[0] = is_prime[1] = False

    for i in range(2, i_limit + 1):
        if not is_prime[i]:
            continue
        for j in range(i * i, n + 1, i):
            is_prime[j] = False

def get_first_prime_multiple_after_n(n, prime):
    """Finds the first multiple of `prime` greater than or equal to `n`."""
    if prime * prime >= n:
        return prime * prime
    else:
        return n if n % prime == 0 else n + (prime - n % prime)

def sieve1_worker(args):
    """Worker function for parallel computation of primes."""
    i_low_global, i_high_global, val_low_global, val_high_global, is_prime, curr_primes = args
    size = i_high_global - i_low_global + 1
    is_prime_loc = [True] * size

    for curr_prime in curr_primes:
        if not is_prime[curr_prime]:
            continue

        first = get_first_prime_multiple_after_n(val_low_global, curr_prime)
        if first % 2 == 0:
            first += curr_prime

        for num_global in range(first, val_high_global + 1, curr_prime * 2):
            num_ind_local = (num_global - val_low_global) // 2
            is_prime_loc[num_ind_local] = False

    # Count local primes
    return sum(is_prime_loc)

def sieve1(n):
    """Optimized sieve algorithm with parallelization."""
    if n < 2:
        return 0
    if n == 2:
        return 1

    n_red = n - (n % 2 == 0)
    n_sqrt = int(math.sqrt(n))
    i_max = (n_red - 3) // 2
    res = 1  # Start with 1 for the prime number 2

    is_prime = [True] * (n_sqrt + 1)
    mark_primes(is_prime, n_sqrt)

    # Split the work across threads
    num_threads = cpu_count()
    pool = Pool(processes=num_threads)
    chunk_size = (i_max + 1) // num_threads

    tasks = []
    for tid in range(num_threads):
        i_low_global = tid * chunk_size
        i_high_global = min((tid + 1) * chunk_size - 1, i_max)
        val_low_global = i_low_global * 2 + 3
        val_high_global = i_high_global * 2 + 3

        tasks.append((i_low_global, i_high_global, val_low_global, val_high_global, is_prime, range(3, n_sqrt + 1, 2)))

    # Collect results from all workers
    results = pool.map(sieve1_worker, tasks)
    pool.close()
    pool.join()

    res += sum(results)
    return res
