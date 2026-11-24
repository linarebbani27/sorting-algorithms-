# ============================================================
# Sorting Algorithms Assignment - Python
# Bubble, Selection, Insertion, Merge, Quick Sort
# Benchmark: execution time and peak traced memory
# ============================================================

import random
import time
import tracemalloc
import csv
import os

# -------------------- 1. SORTING ALGORITHMS --------------------

def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(n - 1 - i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:  # Early exit if this pass made no swaps
            break
    return arr



def selection_sort(arr):
    n = len(arr)
    for i in range(n):
        min_index = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_index]:
                min_index = j
        arr[i], arr[min_index] = arr[min_index], arr[i]
    return arr



def insertion_sort(arr):
    n = len(arr)
    for i in range(1, n):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr



def merge(left, right):
    result = []
    i = 0
    j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result


def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    middle = len(arr) // 2
    left_half = merge_sort(arr[:middle])
    right_half = merge_sort(arr[middle:])
    return merge(left_half, right_half)


def quick_sort(arr):
    # Pivot strategy: median of the first, middle, and last values.
    # Three-way partition helps when the input contains many duplicates.
    if len(arr) <= 1:
        return arr

    first = arr[0]
    middle = arr[len(arr) // 2]
    last = arr[-1]

    # Find the median using comparisons (no built-in sorting function).
    if (first <= middle <= last) or (last <= middle <= first):
        pivot = middle
    elif (middle <= first <= last) or (last <= first <= middle):
        pivot = first
    else:
        pivot = last

    left = []
    equal = []
    right = []

    for value in arr:
        if value < pivot:
            left.append(value)
        elif value == pivot:
            equal.append(value)
        else:
            right.append(value)

    return quick_sort(left) + equal + quick_sort(right)


# Keep algorithms in menu/comparison order
ALGORITHMS = {
    "Bubble Sort": bubble_sort,
    "Selection Sort": selection_sort,
    "Insertion Sort": insertion_sort,
    "Merge Sort": merge_sort,
    "Quick Sort": quick_sort,
}

# -------------------- 2. DATA GENERATION --------------------

def generate_array(size, data_type="random", seed=42):
    rng = random.Random(seed)

    if data_type == "random":
        return [rng.randint(0, 100000) for _ in range(size)]
    if data_type == "sorted":
        return list(range(size))
    if data_type == "reverse":
        return list(range(size, 0, -1))
    if data_type == "duplicates":
        return [rng.randint(0, 10) for _ in range(size)]

    raise ValueError("Unknown data type")


def choose_data_type():
    print("\nInput data type:")
    print("1. Random")
    print("2. Already sorted")
    print("3. Reverse sorted")
    print("4. Many duplicates")
    choice = input("Choose data type: ").strip()
    return {"1": "random", "2": "sorted", "3": "reverse", "4": "duplicates"}.get(choice, "random")

# -------------------- 3. TIME & MEMORY BENCHMARK --------------------

def benchmark(sort_function, data, repetitions=5):
    elapsed_times = []
    peak_memories_kb = []

    for _ in range(repetitions):
        working_array = data.copy()  # Copy before measuring

        tracemalloc.start()
        try:
            start_time = time.perf_counter()
            sorted_result = sort_function(working_array)
            elapsed = time.perf_counter() - start_time
            current_bytes, peak_bytes = tracemalloc.get_traced_memory()
        finally:
            tracemalloc.stop()

        # Check that the algorithm really sorted the input correctly.
        if sorted_result != sorted(data):
            raise ValueError(f"{sort_function.__name__} produced an incorrect result")

        elapsed_times.append(elapsed * 1000)  # milliseconds
        peak_memories_kb.append(peak_bytes / 1024)  # kilobytes


    average_time_ms = sum(elapsed_times) / len(elapsed_times)
    average_memory_kb = sum(peak_memories_kb) / len(peak_memories_kb)
    return average_time_ms, average_memory_kb


# -------------------- 4. DISPLAY & COMPARISON --------------------

def print_results_table(results):
    print("\n" + "=" * 78)
    print(f"{'Algorithm':<18} {'Size':>10} {'Time (ms)':>16} {'Peak Memory (KB)':>20}")
    print("-" * 78)
    for row in results:
        name, size, time_ms, memory_kb = row
        print(f"{name:<18} {size:>10} {time_ms:>16.3f} {memory_kb:>20.2f}")
    print("=" * 78)


def compare_all(data, names=None):
    results = []
    selected_names = names if names is not None else list(ALGORITHMS.keys())

    for name in selected_names:
        function = ALGORITHMS[name]
        print(f"Running {name} on {len(data)} elements ...")
        average_time, average_memory = benchmark(function, data)
        results.append((name, len(data), average_time, average_memory))

    print_results_table(results)
    return results


# -------------------- 5. CSV EXPORT --------------------

def save_results(results, filename="results/results.csv", append=False):
    os.makedirs(os.path.dirname(filename) or ".", exist_ok=True)
    mode = "a" if append else "w"
    file_exists = False
    try:
        with open(filename, "r", newline=""):
            file_exists = True
    except FileNotFoundError:
        pass

    with open(filename, mode, newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if not append or not file_exists:
            writer.writerow(["Algorithm", "Array Size", "Average Time (ms)", "Average Peak Memory (KB)"])
        writer.writerows(results)

    print(f"Results saved to {filename}")


# -------------------- 6. GRAPH --------------------

def plot_csv_results(filename="results/all_sizes_results.csv"):
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib is not installed. Install it with: pip install matplotlib")
        return


    try:
        with open(filename, newline="", encoding="utf-8") as file:
            rows = list(csv.DictReader(file))
    except FileNotFoundError:
        # If the multi-size benchmark has not been run, use regular saved results.
        fallback_filename = "results/results.csv"
        if filename != fallback_filename and os.path.exists(fallback_filename):
            filename = fallback_filename
            with open(filename, newline="", encoding="utf-8") as file:
                rows = list(csv.DictReader(file))
        else:
            print("CSV file not found. Run option 7 or save a comparison first.")
            return


    if not rows:
        print("The CSV file contains no results.")
        return

    # Plot execution time; separate lines per algorithm, with array size on x-axis.
    names = list(dict.fromkeys(row["Algorithm"] for row in rows))
    plt.figure()
    for name in names:
        points = [row for row in rows if row["Algorithm"] == name]
        points.sort(key=lambda row: int(row["Array Size"]))
        x = [int(row["Array Size"]) for row in points]
        y = [float(row["Average Time (ms)"]) for row in points]
        plt.plot(x, y, marker="o", label=name)

    plt.xlabel("Array size")
    plt.ylabel("Average execution time (ms)")
    plt.title("Sorting Algorithms - Execution Time")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# -------------------- 7. TESTS --------------------

def test_algorithms():
    test_cases = [
        [],
        [1],
        [7, 3, 9, 2, 5],
        [5, 4, 3, 2, 1],
        [1, 2, 3, 4, 5],
        [4, 2, 4, 1, 2, 4],
    ]

    print("\nTesting sorting algorithms...")
    all_passed = True
    for name, function in ALGORITHMS.items():
        passed = True
        for case in test_cases:
            result = function(case.copy())
            if result != sorted(case):
                passed = False
                break
        print(f"{name:<18}: {'PASS' if passed else 'FAIL'}")
        all_passed = all_passed and passed

    print("All tests passed!" if all_passed else "Some tests failed.")

# -------------------- 8. MENU OPTIONS --------------------

def run_one_algorithm(name):
    try:
        size = int(input("Enter array size (positive integer): "))
        if size <= 0:
            print("Array size must be greater than zero.")
            return
    except ValueError:
        print("Invalid size. Please enter an integer.")
        return


    data_type = choose_data_type()
    data = generate_array(size, data_type)
    function = ALGORITHMS[name]



    print(f"\nRunning {name} ...")
    average_time, average_memory = benchmark(function, data)
    result = [(name, size, average_time, average_memory)]
    print_results_table(result)

    save_choice = input("Save this result to results.csv? (y/n): ").strip().lower()
    if save_choice == "y":
        save_results(result, append=True)



def run_comparison():
    try:
        size = int(input("Enter array size (positive integer): "))
        if size <= 0:
            print("Array size must be greater than zero.")
            return
    except ValueError:
        print("Invalid size. Please enter an integer.")
        return


    data_type = choose_data_type()
    data = generate_array(size, data_type)

    if size > 10000:
        print("Warning: Bubble, Selection and Insertion Sort may take a very long time on this size.")
        confirm = input("Continue with all five algorithms? (y/n): ").strip().lower()
        if confirm != "y":
            # For large arrays, run the efficient algorithms only.
            names = ["Merge Sort", "Quick Sort"]
            results = compare_all(data, names)
        else:
            results = compare_all(data)
    else:
        results = compare_all(data)

    save_choice = input("Save comparison to results.csv? (y/n): ").strip().lower()
    if save_choice == "y":
        save_results(results, append=True)


def run_multiple_sizes():
    # Quadratic algorithms are limited to 10,000 elements for practical runtime.
    sizes = [1000, 5000, 10000, 50000, 100000]
    data_type = choose_data_type()
    all_results = []

    for size in sizes:
        print(f"\n### Array size: {size} ###")
        data = generate_array(size, data_type, seed=42)
        if size <= 10000:
            names = list(ALGORITHMS.keys())
        else:
            print("Skipping quadratic algorithms at this size; running Merge and Quick Sort only.")
            names = ["Merge Sort", "Quick Sort"]

        results = compare_all(data, names)
        all_results.extend(results)

    save_results(all_results, "results/all_sizes_results.csv")
    print("Multi-size experiment completed. Results saved to results/all_sizes_results.csv")


def main():
    while True:
        print("\n========== SORTING ALGORITHMS ==========")
        print("1. Bubble Sort")
        print("2. Selection Sort")
        print("3. Insertion Sort")
        print("4. Merge Sort")
        print("5. Quick Sort")
        print("6. Compare all algorithms")
        print("7. Benchmark several array sizes")
        print("8. Plot results from CSV")
        print("9. Test algorithms")
        print("0. Exit")

        choice = input("Your choice: ").strip()

        if choice == "0":
            print("Program terminated. Goodbye!")
            break
        elif choice in ["1", "2", "3", "4", "5"]:
            name = list(ALGORITHMS.keys())[int(choice) - 1]
            run_one_algorithm(name)
        elif choice == "6":
            run_comparison()
        elif choice == "7":
            run_multiple_sizes()
        elif choice == "8":
            plot_csv_results()
        elif choice == "9":
            test_algorithms()
        else:
            print("Invalid choice. Please select a number from the menu.")


if __name__ == "__main__":
    main()
