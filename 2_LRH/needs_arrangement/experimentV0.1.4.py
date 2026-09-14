

def longest_rectangle_in_histogram_left_boundaries(arr: list) -> list[int]:
    left_boundaries = []
    monotonic_stack = []

    for index,value in enumerate(arr):
        while True:
            if len(monotonic_stack) == 0:
                left_boundaries.append(-1)
                monotonic_stack.append(index)
                break

            current_index = index
            current_value = arr[current_index]
            monotonic_stack_current_index = monotonic_stack[-1]
            monotonic_stack_current_value = arr[monotonic_stack_current_index]

            if monotonic_stack_current_value >= current_value:
                monotonic_stack.pop()
                continue

            if monotonic_stack_current_value < current_value:
                top_index = monotonic_stack[-1]
                left_boundaries.append(top_index)
                monotonic_stack.append(index)
                break

    return left_boundaries

if __name__ == "__main__":
    print(longest_rectangle_in_histogram_left_boundaries([2,1,5,6,2,3]))
