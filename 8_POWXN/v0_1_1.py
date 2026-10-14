def myPow(x: float, n: int) -> float:
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


print(myPow(2.0,10))