import json
import os
from math import log

os.makedirs("charts", exist_ok=True)

with open("results.json", "r") as f:
    results = json.load(f)


import os
import matplotlib.pyplot as plt
from collections import defaultdict

def plot_time_vs_size():
    size_data = defaultdict(lambda: defaultdict(list))

    for test_name, sort_results in results.items():
        if "_" not in test_name:
            continue

        data_type, size = test_name.rsplit("_", 1)
        size = int(size)

        for sort_name, time in sort_results.items():
            if isinstance(time, (float, int)):
                time_microseconds = time * 1_000_000
                size_data[sort_name][data_type].append((size, time_microseconds))

    for sort_name, data_types in size_data.items():
        plt.figure(figsize=(10, 6))

        for data_type, points in data_types.items():
            sizes, times = zip(*sorted(points))
            plt.plot(sizes, times, "o-", label=data_type)

        plt.xlabel("Размер массива")
        plt.ylabel("Время (мкс)")
        plt.title(f"Производительность {sort_name}")
        plt.xscale("log")
        plt.yscale("log")
        plt.legend()
        plt.grid(True, which="both", ls="--")

        os.makedirs("charts", exist_ok=True)
        filename = os.path.join("charts", f"time_vs_size_{sort_name}.png")
        plt.savefig(filename, bbox_inches="tight")
        plt.close()



def plot_relative_performance():
    FAST_SORTS = {
        "intro", "bucket", "heap", "lsd_radix",
        "merge", "msd_radix", "quick", "shell", "tim"
    }

    for data_type in ["random_int", "almost_sorted", "reverse_sorted", "few_unique"]:
        plt.figure(figsize=(12, 6))

        size_data = defaultdict(list)
        perf_data = defaultdict(list)

        for test_name, sort_results in results.items():
            if not test_name.startswith(data_type):
                continue

            size = int(test_name.split("_")[-1])

            for sort_name, time in sort_results.items():
                if sort_name in FAST_SORTS and isinstance(time, (float, int)):
                    size_data[sort_name].append(size)
                    perf_data[sort_name].append(time)

        if not size_data:
            continue

        common_sizes = None
        for sort_name, sizes in size_data.items():
            if common_sizes is None:
                common_sizes = set(sizes)
            else:
                common_sizes.intersection_update(sizes)

        if not common_sizes:
            continue

        common_sizes = sorted(common_sizes)

        filtered_perf_data = defaultdict(list)
        for sort_name in perf_data:
            for size, time in zip(size_data[sort_name], perf_data[sort_name]):
                if size in common_sizes:
                    filtered_perf_data[sort_name].append(time)

        min_times = []
        for i in range(len(common_sizes)):
            min_time = min(times[i] for times in filtered_perf_data.values())
            min_times.append(min_time)

        normalized_data = {}
        for sort_name, times in filtered_perf_data.items():
            normalized_data[sort_name] = [t / min_t for t, min_t in zip(times, min_times)]

        for sort_name, rel_times in normalized_data.items():
            plt.plot(common_sizes, rel_times, "o-", label=sort_name)

        plt.xlabel("Размер массива")
        plt.ylabel("Относительное время")
        plt.title(f"Относительная производительность (только быстрые сортировки: {data_type})")
        plt.xscale("log")
        plt.legend()
        plt.grid(True)

        filename = os.path.join("charts", f"relative_perf_fast_{data_type}.png")
        plt.savefig(filename, bbox_inches="tight")
        plt.close()


def check_complexity():
    fast_sorts = ["intro", "bucket", "heap", "lsd_radix", "merge", "msd_radix", "quick", "shell", "tim"]
    data_type = "random_int"

    plt.figure(figsize=(10, 6))

    for sort_name in fast_sorts:
        sizes = []
        times = []

        for test_name, sort_results in results.items():
            if not test_name.startswith(data_type):
                continue

            size = int(test_name.split("_")[-1])
            if sort_name in sort_results and isinstance(sort_results[sort_name], (float, int)):
                sizes.append(size)
                times.append(sort_results[sort_name])

        if not sizes:
            continue

        n_log_n = [n * log(n) for n in sizes]
        normalized_times = [t / nlogn for t, nlogn in zip(times, n_log_n)]

        plt.plot(sizes, normalized_times, "o-", label=sort_name)

    plt.xlabel("Размер массива")
    plt.ylabel("Время / (n log n)")
    plt.title("Проверка сложности O(n log n)")
    plt.xscale("log")
    plt.legend()
    plt.grid(True, which="both", ls="--")

    filename = os.path.join("charts", "complexity_check.png")
    plt.savefig(filename, bbox_inches="tight")
    plt.close()


def plot_basic_charts():
    for test_name, sort_results in results.items():
        labels = []
        times = []
        errors = []

        for sort_name, value in sort_results.items():
            if isinstance(value, (float, int)):
                labels.append(sort_name)
                times.append(value * 1_000_000)
            else:
                errors.append(sort_name)

        plt.figure(figsize=(12, 6))
        bars = plt.bar(labels, times, color="skyblue")

        for bar, time in zip(bars, times):
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2, height,
                     f"{height:.1f}", ha="center", va="bottom", fontsize=8)

        plt.xlabel("Алгоритм сортировки")
        plt.ylabel("Время (мкс)")
        plt.title(f"Сравнение сортировок: {test_name}")
        plt.xticks(rotation=45)
        plt.tight_layout()

        filename = os.path.join("charts", f"chart_{test_name}.png")
        plt.savefig(filename)
        plt.close()

def plot_slow_sorts_only():
    SLOW_SORTS = {"bubble", "insertion", "selection", "rank"}

    for test_name, sort_results in results.items():
        labels = []
        times = []

        for sort_name, value in sort_results.items():
            if sort_name in SLOW_SORTS and isinstance(value, (float, int)):
                labels.append(sort_name)
                times.append(value * 1_000_000)

        if not labels:
            continue

        plt.figure(figsize=(10, 5))
        bars = plt.bar(labels, times, color="salmon")

        for bar, time in zip(bars, times):
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2, height,
                     f"{height:.1f}", ha="center", va="bottom", fontsize=8)

        plt.xlabel("Медленные сортировки")
        plt.ylabel("Время (мкс)")
        plt.title(f"Только медленные сортировки: {test_name}")
        plt.xticks(rotation=45)
        plt.tight_layout()

        filename = os.path.join("charts", f"slow_chart_{test_name}.png")
        plt.savefig(filename)
        plt.close()

def plot_fast_sorts_only():
    FAST_SORTS = {
        "intro", "bucket", "heap", "lsd_radix",
        "merge", "msd_radix", "quick", "shell", "tim"
    }

    for test_name, sort_results in results.items():
        labels = []
        times = []

        for sort_name, value in sort_results.items():
            if sort_name in FAST_SORTS and isinstance(value, (float, int)):
                labels.append(sort_name)
                times.append(value * 1_000_000)

        if not labels:
            continue

        plt.figure(figsize=(12, 6))
        bars = plt.bar(labels, times, color="mediumseagreen")

        for bar, time in zip(bars, times):
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2, height,
                     f"{height:.1f}", ha="center", va="bottom", fontsize=8)

        plt.xlabel("Быстрые сортировки")
        plt.ylabel("Время (мкс)")
        plt.title(f"Только быстрые сортировки: {test_name}")
        plt.xticks(rotation=45)
        plt.tight_layout()

        filename = os.path.join("charts", f"fast_chart_{test_name}.png")
        plt.savefig(filename)
        plt.close()



if __name__ == "__main__":
    plot_basic_charts()
    plot_time_vs_size()
    plot_relative_performance()
    check_complexity()
    plot_slow_sorts_only()
    plot_fast_sorts_only()