from typing import List


class Solution:
    def maxArea(self, height: List[int]) -> int:
        """
        Finds two lines that together with the x-axis form a container,
        such that the container contains the most water.

        :param height: List[int] - array of vertical line heights
        :return: int - maximum amount of water a container can store
        """

        # TODO: Implement your algorithm here
        # Return 0 to prevent NoneType errors before you start writing

        if len(height) == 0:
            return 0

        if len(height) == 1:
            return height[0]

        max_area = 0

        left = 0
        right = len(height) - 1

        while left < right:
            current_area_width = right - left
            current_area_height = min(height[left], height[right])
            current_area = current_area_height * current_area_width
            max_area = max(current_area,max_area)
            if height[left] <= height[right]:
                left += 1
            else:
                right -=1

        return max_area


# =====================================================================
# TEST RUNNER & EDGE CASES
# =====================================================================

def run_tests():
    solution = Solution()

    # Test cases format: (Description, Input Array, Expected Output)
    test_cases = [
        (
            "Standard Case (from LeetCode)",
            [1, 8, 6, 2, 5, 4, 8, 3, 7],
            49
        ),
        (
            "Minimum Constraints (Only 2 elements)",
            [1, 1],
            1
        ),
        (
            "Zeros in the array",
            [0, 2, 0],
            0
        ),
        (
            "All heights are the same",
            [5, 5, 5, 5, 5],
            20  # area = height(5) * width(4)
        ),
        (
            "Large peak in the middle (Tall & Narrow)",
            [1, 2, 100, 100, 2, 1],
            100  # area = height(100) * width(1)
        ),
        (
            "Strictly Decreasing Heights",
            [9, 8, 7, 6, 5, 4, 3, 2, 1],
            20  # max is between index 0 (height 9) and index 4 (height 5) -> area = 5 * 4 = 20
        ),
        (
            "Strictly Increasing Heights",
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
            20  # max is between index 4 and index 8 -> area = 5 * 4 = 20
        ),
        (
            "Wide but short vs narrow but tall trap",
            [2, 3, 4, 5, 18, 17, 6],
            17  # max area is between the two tall ones: min(18, 17) * 1 = 17
        )
    ]

    passed = 0
    total = len(test_cases)

    print("Running tests for LeetCode #11 - Container With Most Water...\n")
    print("-" * 60)

    for i, (desc, height, expected) in enumerate(test_cases, 1):
        try:
            # Pass a copy of the list height[:] to avoid mutation side-effects
            result = solution.maxArea(height[:])

            if result == expected:
                print(f"✅ Test {i} PASSED: {desc}")
                passed += 1
            else:
                print(f"❌ Test {i} FAILED: {desc}")
                print(f"   Input:    {height}")
                print(f"   Expected: {expected}")
                print(f"   Got:      {result}")
        except Exception as e:
            print(f"⚠️️ Test {i} ERROR: {desc}")
            print(f"   Exception: {e}")

    print("-" * 60)
    print(f"Results: {passed} out of {total} tests passed.")
    if passed == total:
        print("🎉 Great job! All test cases passed.")
    else:
        print("Keep going! Look at the failed test cases to debug your logic.")


if __name__ == "__main__":
    run_tests()
