def longest_common_subsequence(arr: list[int]) -> int:
    if len(arr) <= 0:
        return 0
    set_arr = set(arr)
    lcs = 1
    for i in arr:
        curr_lcs = 1
        if i - 1 in set_arr:
            continue
        check_i = i
        while check_i + 1 in set_arr:
            curr_lcs += 1
            check_i = check_i + 1
        lcs = max(lcs, curr_lcs)

    return lcs


if __name__ == "__main__":
    nums = [-5, -1, -3, -2, -4]
    result = longest_common_subsequence(nums)
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
        result = longest_common_subsequence(nums)
        print(
            f"Input: {nums}\n"
            f"Expected: {expected}, Got: {result}\n"
            f"{'✅ PASS' if result == expected else '❌ FAIL'}\n"
        )
