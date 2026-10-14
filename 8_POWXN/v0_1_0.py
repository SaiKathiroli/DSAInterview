import math
import time


class Solution:
    def myPow(self, x: float, n: int) -> float:
        """
        50. Pow(x, n)
        Calculates x raised to the power n (i.e., x^n).

        Constraints:
        - -100.0 < x < 100.0
        - -2^31 <= n <= 2^31 - 1
        - n is an integer.
        - Either x is not zero or n > 0.
        - -10^4 <= x^n <= 10^4
        """
        # ==========================================
        # TODO: Write your implementation here
        # ==========================================
        def helper(x, n):
            if x == 0: return 0
            if n == 0: return 1

            res = helper(x, n // 2)
            res = res * res
            return x * res if n % 2 else res

        result = helper(x, abs(n))
        return result if n >= 0 else (1 / result)


def run_tests():
    solver = Solution()

    # Format: (description, x, n, expected_output)
    test_cases = [
        # --- LeetCode Official Examples ---
        ("Example 1: Standard positive power", 2.00000, 10, 1024.00000),
        ("Example 2: Fractional base", 2.10000, 3, 9.26100),
        ("Example 3: Negative exponent", 2.00000, -2, 0.25000),

        # --- Zero & Identity Cases ---
        ("Zero exponent with positive base", 5.43210, 0, 1.00000),
        ("Zero exponent with negative base", -99.99000, 0, 1.00000),
        ("Zero base with positive exponent", 0.00000, 5, 0.00000),
        ("Exponent of 1 (Identity)", -13.75000, 1, -13.75000),
        ("Exponent of -1 (Reciprocal)", 4.00000, -1, 0.25000),

        # --- Negative Base Sign-Flip Cases ---
        ("Negative base, even positive exponent", -2.00000, 4, 16.00000),
        ("Negative base, odd positive exponent", -2.00000, 3, -8.00000),
        ("Negative base, even negative exponent", -2.00000, -4, 0.06250),
        ("Negative base, odd negative exponent", -2.00000, -3, -0.12500),

        # --- Fractional Base with Negative Exponent (Growth) ---
        ("Small base (< 1) with negative power", 0.50000, -10, 1024.00000),

        # --- Extreme Boundary & Stress Cases (n = -2^31 to 2^31 - 1) ---
        ("Max 32-bit signed int (2^31 - 1), base 1.0", 1.00000, 2147483647, 1.00000),
        ("Min 32-bit signed int (-2^31), base 1.0", 1.00000, -2147483648, 1.00000),
        ("Max 32-bit odd exponent, base -1.0", -1.00000, 2147483647, -1.00000),
        ("Min 32-bit even exponent, base -1.0", -1.00000, -2147483648, 1.00000),
        ("Extreme negative exponent underflow to 0", 2.00000, -2147483648, 0.00000),
        ("Near-1 base with huge exponent", 1.000000001, 2147483647, 8.56322),
    ]

    passed = 0
    total = len(test_cases)
    tolerance = 1e-5  # LeetCode judges float answers within 10^-5

    print("=" * 75)
    print(f"Running {total} Test Cases for LeetCode 50: Pow(x, n)")
    print("=" * 75)

    for i, (desc, x, n, expected) in enumerate(test_cases, 1):
        start_time = time.perf_counter()
        try:
            actual = solver.myPow(x, n)
            elapsed_ms = (time.perf_counter() - start_time) * 1000

            if actual is None:
                status = "⏳ TODO"
                detail = "Function returned None (not implemented yet)"
            elif isinstance(actual, (int, float)) and math.isclose(
                    actual, expected, rel_tol=tolerance, abs_tol=tolerance
            ):
                status = "✅ PASS"
                passed += 1
                detail = f"Output: {actual:.5f} ({elapsed_ms:.3f} ms)"
            else:
                status = "❌ FAIL"
                detail = (
                    f"Expected: {expected:.5f} | Got: {actual} ({elapsed_ms:.3f} ms)"
                )

        except RecursionError:
            status = "💥 TLE/ERR"
            detail = "RecursionError: Maximum recursion depth exceeded"
        except Exception as e:
            status = "💥 ERROR"
            detail = f"{type(e).__name__}: {e}"

        print(f"Test {i:02d} [{status}] {desc}")
        print(f"        Input:    x = {x}, n = {n}")
        print(f"        Result:   {detail}\n")

    print("=" * 75)
    print(f"Summary: {passed}/{total} tests passed.")
    print("=" * 75)


if __name__ == "__main__":
    run_tests()
