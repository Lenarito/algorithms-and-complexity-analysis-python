import json
from utils.generator_data import *
from utils.timer_wrapper import measure_time
from algorithms.bubble_sort import bubble_sort
from algorithms.bucket_sort import bucket_sort
from algorithms.heap_sort import heap_sort
from algorithms.insertion_sort import insertion_sort
from algorithms.intro_sort import intro_sort
from algorithms.least_significant_digit_radix_sort import radix_sort_lsd
from algorithms.merge_sort import merge_sort
from algorithms.most_significant_digit_radix_sort import msd_radix_sort
from algorithms.quick_sort import quick_sort
from algorithms.rank_sort import rank_sort
from algorithms.selection_sort import selection_sort
from algorithms.shell_sort import shell_sort
from algorithms.tim_sort import tim_sort

from datetime import datetime

SLOW_SORTS = {
    "bubble": bubble_sort,
    "insertion": insertion_sort,
    "selection": selection_sort,
    "rank": rank_sort,

}

FAST_SORTS = {
    "intro": intro_sort,
    "bucket": bucket_sort,
    "heap": heap_sort,
    "lsd_radix": radix_sort_lsd,
    "merge": merge_sort,
    "msd_radix": msd_radix_sort,
    "quick": quick_sort,
    "shell": shell_sort,
    "tim": tim_sort,
}

array_generators = {
    "random_int": generate_random_int_array,
    "reverse_sorted": generate_reverse_sorted_array,
    "almost_sorted": generate_almost_sorted_array,
    "few_unique": generate_few_unique_array,
    "random_string": generate_random_string_array,
    "random_bytes": generate_random_bytes_array,
    "random_date": lambda l: generate_random_date_array(l, datetime(2000, 1, 1), datetime(2025, 1, 1)),
    "tail_random": lambda l: generate_tail_random_array(l),
    "insert_random": lambda l: generate_insert_random_array(l),
}

results = {}

for name, gen_func in array_generators.items():
    print(f"\nТест: {name}")
    lengths = [10, 100, 1000, 10000, 100000]

    for length in lengths:
        print(f"\nТест: {name} | длина: {length}")
        if name == "random_bytes":
            arr = gen_func(length)
            key_func = lambda x: x
        else:
            arr = gen_func(length)
            key_func = None

        results[f"{name}_{length}"] = {}
        current_sorts = FAST_SORTS if length > 1000 else {**FAST_SORTS, **SLOW_SORTS}

        for sort_name, sort_func in current_sorts.items():
            try:
                if key_func:
                    avg_time = measure_time(lambda a: sort_func(a, key=key_func), arr.copy())
                else:
                    repeat_count = 50 if length <= 1000 else 1
                    avg_time = measure_time(sort_func, arr.copy(), repeat_count=repeat_count)

                time_str = f"{avg_time:.9f}".rstrip('0').rstrip('.') if avg_time < 1 else f"{avg_time:.3f}"
                print(f"{sort_name:15} | {time_str} сек")

                results[f"{name}_{length}"][sort_name] = avg_time
            except Exception as e:
                print(f"{sort_name:15} | ОШИБКА: {e}")
                results[f"{name}_{length}"][sort_name] = f"error: {str(e)}"

with open("results.json", "w") as f:
    json.dump(results, f, indent=4, default=str)
