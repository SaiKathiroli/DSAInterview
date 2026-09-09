"""
Given an array of bar heights in a histogram, find the area of the largest rectangle that can be formed.
Input:  heights = [2, 1, 5, 6, 2, 3]
Output: 10   → rectangle spanning bars 3 and 4 (height 5, width 2)
"""


def longest_rectangle_histogram(param: list[int]) -> int:

    if len(param) == 0:
        return 0

    area = max(param)

    for index, value in enumerate(param):
        scoped_bars = [value]
        temp_index = index
        while temp_index < len(param):
            rectangle_height = min(scoped_bars)
            rectangle_width = len(scoped_bars)
            area = max(area, rectangle_width * rectangle_height)
            if temp_index + 1 >= len(param):
                break
            scoped_bars.append(param[temp_index + 1])
            temp_index += 1

    return area


def test_longest_rectangle_histogram():
    test_cases = [
        # (input, expected_output, description)

        # Basic / edge cases
        ([], 0, "Empty histogram"),
        ([0], 0, "Single bar with zero height"),
        ([5], 5, "Single positive bar"),

        # Two bars
        ([2, 3], 4, "Two increasing bars"),
        ([3, 2], 4, "Two decreasing bars"),
        ([3, 3], 6, "Two equal bars"),
        ([0, 5], 5, "Zero followed by positive bar"),
        ([5, 0], 5, "Positive bar followed by zero"),

        # All bars equal
        ([1, 1, 1, 1], 4, "All bars height 1"),
        ([5, 5, 5, 5], 20, "All bars same height"),

        # Strictly increasing
        ([1, 2, 3, 4, 5], 9, "Strictly increasing histogram"),

        # Strictly decreasing
        ([5, 4, 3, 2, 1], 9, "Strictly decreasing histogram"),

        # Given example
        ([2, 1, 5, 6, 2, 3], 10, "Classic example"),

        # Valley patterns
        ([5, 1, 5], 5, "Deep valley"),
        ([5, 2, 5], 6, "Valley where width matters"),
        ([4, 2, 4], 6, "Symmetric valley"),

        # Peak patterns
        ([1, 5, 1], 5, "Single tall peak"),
        ([1, 2, 3, 2, 1], 6, "Symmetric mountain"),
        ([2, 4, 6, 4, 2], 12, "Larger symmetric mountain"),

        # Zeros split the histogram
        ([2, 0, 2], 2, "Zero separates equal bars"),
        ([2, 2, 0, 3, 3], 6, "Multiple independent regions"),
        ([0, 0, 0], 0, "All zeros"),

        # Maximum rectangle uses full width
        ([2, 2, 2, 2, 2], 10, "Maximum spans entire histogram"),
        ([1, 2, 1], 3, "Small height across full width"),

        # Maximum rectangle is internal
        ([1, 4, 4, 4, 1], 12, "Maximum rectangle in middle"),
        ([1, 2, 5, 5, 5, 2, 1], 15, "Wide plateau in middle"),

        # Duplicate heights
        ([2, 2, 1, 2, 2], 5, "Duplicate bars around low center"),
        ([3, 3, 2, 3, 3], 10, "Minimum height wins across width"),

        # Alternating heights
        ([1, 3, 1, 3, 1], 5, "Alternating low/high bars"),
        ([2, 5, 2, 5, 2], 10, "Alternating pattern with useful baseline"),

        # Large values
        ([1000], 1000, "Single large bar"),
        ([1000, 1000, 1000], 3000, "Multiple large equal bars"),

        # Other known tricky examples
        ([2, 4], 4, "Small classic case"),
        ([6, 2, 5, 4, 5, 1, 6], 12, "Classic textbook example"),
        ([2, 1, 2], 3, "Width beats individual taller bars"),
    ]

    for heights, expected, description in test_cases:
        actual = longest_rectangle_histogram(heights)

        assert actual == expected, (
            f"FAILED: {description}\n"
            f"Input:    {heights}\n"
            f"Expected: {expected}\n"
            f"Actual:   {actual}"
        )

        print(f"PASS: {description}")

    print(f"\nAll {len(test_cases)} test cases passed!")


if __name__ == "__main__":
    test_longest_rectangle_histogram()