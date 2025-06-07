from .quick_sort import quick_sort
from datetime import datetime

def bucket_sort(arr, bucket_size=None, key=lambda x: x):
    if not arr:
        return []

    def to_numeric(val):
        result = key(val)
        if isinstance(result, bytes):
            return int.from_bytes(result, 'little')
        elif isinstance(result, datetime):
            return result.timestamp()
        return result

    numeric_arr = [(item, to_numeric(item)) for item in arr]
    min_k = min(numeric_arr, key=lambda x: x[1])[1]
    max_k = max(numeric_arr, key=lambda x: x[1])[1]

    if min_k == max_k:
        return [item for item, _ in numeric_arr]

    if bucket_size is None:
        bucket_size = (max_k - min_k) / len(arr)

    bucket_count = min(int((max_k - min_k) / bucket_size) + 1, 1000)
    buckets = [[] for _ in range(bucket_count)]

    for item, num in numeric_arr:
        index = int((num - min_k) / bucket_size)
        index = min(index, bucket_count - 1)
        buckets[index].append(item)

    result = []
    for bucket in buckets:
        quick_sort(bucket, key=key)
        result.extend(bucket)

    return result
