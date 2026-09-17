def longest_rectangle_histogram(left, right, arr) -> int:
    if len(arr) == 0:
        return 0

    maximum = 0

    for index, value in enumerate(arr):
        l_i = left[index]
        r_i = right[index]
        width = r_i - l_i - 1
        height = arr[index]
        maximum = max(maximum, height * width)

    return maximum


def right_boundaries_histogram(arr: list):
    monotonic_stack = []
    right_boundaries = []

    for index in range(len(arr) - 1, -1, -1):
        while True:
            if len(monotonic_stack) == 0:
                right_boundaries.append(len(arr))
                monotonic_stack.append(index)
                break

            top_value = arr[monotonic_stack[-1]]
            current_value = arr[index]

            if top_value >= current_value:
                monotonic_stack.pop()
                continue

            if top_value < current_value:
                right_boundaries.append(monotonic_stack[-1])
                monotonic_stack.append(index)
                break

    return right_boundaries[::-1]


def left_boundaries_histogram(arr: list) -> list:
    monotonic_stack = []
    left_boundaries = []

    for index, value in enumerate(arr):
        while True:
            if len(monotonic_stack) == 0:
                left_boundaries.append(-1)
                monotonic_stack.append(index)
                break

            top_value = arr[monotonic_stack[-1]]
            current_value = arr[index]

            if current_value <= top_value:
                monotonic_stack.pop()
                continue

            if current_value > top_value:
                left_boundaries.append(monotonic_stack[-1])
                monotonic_stack.append(index)
                break

    return left_boundaries


if __name__ == "__main__":
    lefter_boundaries = left_boundaries_histogram([2, 4, 6, 4, 2])
    righter_boundaries = right_boundaries_histogram([2, 4, 6, 4, 2])
    print(lefter_boundaries)
    print(righter_boundaries)
    answer = longest_rectangle_histogram(lefter_boundaries, righter_boundaries, [2, 4, 6, 4, 2])
    print(answer)
