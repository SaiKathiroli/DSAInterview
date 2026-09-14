def longest_rectangle_in_histogram_right_boundaries(arr: list) -> list[int]:
    right_boundaries = []
    monotonic_stack = []

    for index, value in enumerate(arr):
        while True:
            if len(monotonic_stack) == 0:
                right_boundaries.append(len(arr))
                monotonic_stack.append(index)
                break

            current_value = arr[index]
            monotonic_stack_top_value = arr[monotonic_stack[-1]]

            if monotonic_stack_top_value >= current_value:
                monotonic_stack.pop()
                continue

    return right_boundaries


if __name__ == "__main__":
    print(longest_rectangle_in_histogram_right_boundaries([2, 1, 5, 6, 2, 3]))
    # [1,6,4,4,6,6]
