def longest_consecutive_sequence(arr: list[int]) -> int:
    if len(arr) <= 0:
        return 0
    set_arr = set(arr)
    max_length = 1
    for num in arr:
        current_length = 1
        if num - 1 in set_arr:
            continue
        check_i = num
        while check_i + 1 in set_arr:
            current_length += 1
            check_i = check_i + 1
        max_length = max(max_length, current_length)

    return max_length


if __name__ == "__main__":
    nums = [-5, -1, -3, -2, -4]
    result = longest_consecutive_sequence(nums)
    print(result)

    test_cases = [
        ([100, 4, 200, 1, 3, 2], 4),
        ([0, 3, 7, 2, 5, 8, 4, 6, 0, 1], 9),
        ([], 0),
        ([1], 1),
        ([1, 2, 3, 4, 5], 5),
        ([5, 4, 3, 2, 1], 5),
        ([1, 3, 5, 7], 1),
        ([1, 2, 2, 3, 4], 4),
        ([10, 5, 12, 3, 55, 30, 4, 11, 2], 4),
        ([-3, -2, -1, 0, 1], 5),
        ([-10, -9, -8, 20, 21, 22, 23], 4),
        ([1, 100, 2, 101, 3, 102], 3),
        ([7, 7, 7, 7], 1),
        ([2, 1, 4, 3, 6, 5], 6),
        ([-5, -1, -3, -2, -4], 5),
    ]

    for nums, expected in test_cases:
        result = longest_consecutive_sequence(nums)
        print(
            f"Input: {nums}\n"
            f"Expected: {expected}, Got: {result}\n"
            f"{'✅ PASS' if result == expected else '❌ FAIL'}\n"
        )
