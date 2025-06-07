import random
import string
from datetime import datetime, timedelta


def generate_random_int_array(length: int, min_value: int = 0, max_value: int = 1000):
    return [random.randint(min_value, max_value) for _ in range(length)]

def generate_random_string_array(length: int, min_len: int = 5, max_len: int = 10):
    return [''.join(random.choices(string.ascii_letters, k=random.randint(min_len, max_len))) for _ in range(length)]

def generate_random_bytes_array(length):
    return [random.randint(0, 9).to_bytes(1, 'little') for _ in range(length)]

def generate_random_date_array(length: int, start: datetime, end: datetime):
    delta = (end - start).days
    return [start + timedelta(days=random.randint(0, delta)) for _ in range(length)]

def generate_reverse_sorted_array(length: int):
    return list(range(length, 0, -1))

def generate_almost_sorted_array(length: int, num_unsorted: int = 10):
    arr = list(range(length))
    for _ in range(num_unsorted):
        i = random.randint(0, length - 1)
        j = random.randint(0, length - 1)
        arr[i], arr[j] = arr[j], arr[i]
    return arr

def generate_few_unique_array(length: int, num_unique: int = 5):
    return [random.randint(1, num_unique) for _ in range(length)]

def generate_tail_random_array(length, random_ratio=0.1):
    base = list(range(length))
    k = int(length * random_ratio)
    base[-k:] = generate_random_int_array(k)
    return base

def generate_insert_random_array(length, insert_count=10):
    base = list(range(length))
    for _ in range(insert_count):
        base.insert(random.randint(0, len(base)), random.randint(0, 1000))
    return base