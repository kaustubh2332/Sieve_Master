import math
from multiprocessing import Pool, cpu_count

def mark_primes_parallel(args):
    """Worker function for marking non-prime numbers in parallel."""
    i_start, i_end, n, is_prime = args
    n_sqrt = int(math.sqrt(n))
    
    for i in range(3, n_sqrt + 1, 2):
        ind_i = (i - 3) // 2
        if not is_prime[ind_i]:
            continue

        for j in range(i * i, n + 1, 2 * i):
            ind_j = (j - 3) // 2
            if ind_j >= i_start and ind_j <= i_end:
                is_prime[ind_j] = False

def count_primes_parallel(args):
    """Worker function for counting primes in a given range."""
    i_start, i_end, is_prime = args
    return sum(is_prime[i_start:i_end + 1])

def sieve2(n):
    """Highly optimized sieve algorithm with parallel processing."""
    if n < 2:
        return 0
    if n == 2:
        return 1

    n_red = n - (n % 2 == 0)
    n_sqrt = int(math.sqrt(n))
    high_ind = (n - 3) // 2
    size = high_ind + 1

    is_prime = [True] * size
    res = 1  # Start with 1 for the prime number 2

    # Parallel marking of non-prime numbers
    num_threads = cpu_count()
    chunk_size = (size + num_threads - 1) // num_threads
    tasks = []

    for i in range(num_threads):
        i_start = i * chunk_size
        i_end = min((i + 1) * chunk_size - 1, size - 1)
        tasks.append((i_start, i_end, n, is_prime))

    with Pool(processes=num_threads) as pool:
        pool.map(mark_primes_parallel, tasks)

    # Parallel counting of primes
    count_tasks = []
    for i in range(num_threads):
        i_start = i * chunk_size
        i_end = min((i + 1) * chunk_size - 1, size - 1)
        count_tasks.append((i_start, i_end, is_prime))

    with Pool(processes=num_threads) as pool:
        results = pool.map(count_primes_parallel, count_tasks)

    res += sum(results)
    return res