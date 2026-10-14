import copy
import time
from typing import List


class Solution:
    """
    56. Merge Intervals (Medium)

    Given an array of intervals where intervals[i] = [start_i, end_i],
    merge all overlapping intervals, and return an array of the
    non-overlapping intervals that cover all the intervals in the input.

    Constraints:
    - 1 <= intervals.length <= 10^4
    - intervals[i].length == 2
    - 0 <= start_i <= end_i <= 10^4
    """

    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        # TODO: Implement your solution here

        if len(intervals) <= 1:
            return intervals

        intervals.sort(key=lambda x: x[0])

        index = 0

        while index <= len(intervals) - 2:
            first = intervals[index][1]
            second = intervals[index + 1][0]
            value = first - second
            if value >= 0:
                right_1 = intervals[index][1]
                right_2 = intervals[index + 1][1]
                if right_2 >= right_1:
                    correct_right = right_2
                else:
                    correct_right = right_1
                new_child_list = [intervals[index][0], correct_right]
                intervals.pop(index + 1)
                intervals[index] = new_child_list
            else:
                index += 1

        return intervals


# =====================================================================
# Local Test Harness
# =====================================================================
def run_tests():
    test_cases = [
        {
            "name": "Example 1: Standard partial overlaps",
            "intervals": [[1, 3], [2, 6], [8, 10], [15, 18]],
            "expected": [[1, 6], [8, 10], [15, 18]],
        },
        {
            "name": "Example 2: Touching boundaries (end_1 == start_2)",
            "intervals": [[1, 4], [4, 5]],
            "expected": [[1, 5]],
        },
        {
            "name": "Example 3: Unsorted touching boundaries",
            "intervals": [[4, 7], [1, 4]],
            "expected": [[1, 7]],
        },
        {
            "name": "Edge Case 1: Single interval (minimum length constraint)",
            "intervals": [[5, 10]],
            "expected": [[5, 10]],
        },
        {
            "name": "Edge Case 2: Zero-length point intervals at 0",
            "intervals": [[0, 0], [0, 0]],
            "expected": [[0, 0]],
        },
        {
            "name": "Edge Case 3: Disjoint point interval and range (unsorted)",
            "intervals": [[1, 4], [0, 0]],
            "expected": [[0, 0], [1, 4]],
        },
        {
            "name": "Edge Case 4: Point interval inside a larger interval",
            "intervals": [[1, 4], [2, 2]],
            "expected": [[1, 4]],
        },
        {
            "name": "Edge Case 5: Completely nested / absorbed intervals",
            "intervals": [[1, 10], [2, 5], [6, 8]],
            "expected": [[1, 10]],
        },
        {
            "name": "Edge Case 6: Late umbrella interval absorbing all previous disjoint ones",
            "intervals": [[2, 3], [4, 5], [6, 7], [8, 9], [1, 10]],
            "expected": [[1, 10]],
        },
        {
            "name": "Edge Case 7: Strictly reverse-sorted input",
            "intervals": [[15, 18], [8, 10], [2, 6], [1, 3]],
            "expected": [[1, 6], [8, 10], [15, 18]],
        },
        {
            "name": "Edge Case 8: Already disjoint (no overlaps at all)",
            "intervals": [[1, 2], [4, 5], [7, 8], [10, 12]],
            "expected": [[1, 2], [4, 5], [7, 8], [10, 12]],
        },
        {
            "name": "Edge Case 9: Identical duplicate intervals & shared start times",
            "intervals": [[1, 4], [1, 4], [1, 5], [1, 2]],
            "expected": [[1, 5]],
        },
        {
            "name": "Edge Case 10: Maximum constraint boundary values (0 to 10^4)",
            "intervals": [[5000, 10000], [0, 5000], [10000, 10000]],
            "expected": [[0, 10000]],
        },
    ]

    solver = Solution()
    passed = 0
    total = len(test_cases)

    print("=" * 70)
    print("Running LeetCode 56: Merge Intervals Test Suite")
    print("=" * 70)

    start_time = time.perf_counter()

    for idx, tc in enumerate(test_cases, 1):
        # Deep copy so in-place sorting/mutations don't corrupt test output display
        input_copy = copy.deepcopy(tc["intervals"])
        expected = tc["expected"]

        try:
            actual = solver.merge(input_copy)
        except Exception as e:
            print(f"[ERROR] Test {idx}: {tc['name']}")
            print(f"   Input:     {tc['intervals']}")
            print(f"   Exception: {type(e).__name__}: {e}\n")
            continue

        # Normalize order only if output is a valid list of lists
        is_valid_type = (
            isinstance(actual, list)
            and all(isinstance(x, list) and len(x) == 2 for x in actual)
        )
        is_correct = is_valid_type and sorted(actual) == sorted(expected)

        if is_correct:
            passed += 1
            print(f"[PASS]  Test {idx}: {tc['name']}")
        else:
            print(f"[FAIL]  Test {idx}: {tc['name']}")
            print(f"   Input:    {tc['intervals']}")
            print(f"   Expected: {expected}")
            print(f"   Actual:   {actual}\n")

    elapsed_ms = (time.perf_counter() - start_time) * 1000
    print("=" * 70)
    print(f"Summary: {passed}/{total} tests passed in {elapsed_ms:.2f} ms")
    print("=" * 70)


if __name__ == "__main__":
    run_tests()