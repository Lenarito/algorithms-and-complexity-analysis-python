def msd_radix_sort(arr, digit=None):
    if not arr:
        return arr
    if digit is None:
        max_num = max(arr)
        digit = len(str(max_num))
    if digit <= 0 or len(arr) <= 1:
        return arr
    buckets = [[] for _ in range(10)]
    for num in arr:
        d = (num // (10 ** (digit - 1))) % 10
        buckets[d].append(num)
    result = []
    for bucket in buckets:
        if bucket:
            result += msd_radix_sort(bucket, digit - 1)
    return result
