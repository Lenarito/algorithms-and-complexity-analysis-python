import time
import copy


def measure_time(sort_func, arr, repeat_count=None, min_total_time=0.1):
    total_time = 0
    repeats = 0

    if repeat_count is not None:
        for _ in range(repeat_count):
            test_arr = copy.deepcopy(arr)
            start = time.perf_counter_ns()
            sort_func(test_arr)
            total_time += (time.perf_counter_ns() - start) / 1e9
        return total_time / repeat_count

    while total_time < min_total_time:
        test_arr = copy.deepcopy(arr)
        start = time.perf_counter_ns()
        sort_func(test_arr)
        total_time += (time.perf_counter_ns() - start) / 1e9
        repeats += 1

    return total_time / repeats
