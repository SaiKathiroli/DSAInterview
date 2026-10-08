
def manual_int_to_string_conversion(string):
    sign = string[0]
    start_index = 0
    transformed_result = 0
    if sign == "-":
        start_index = 1
        multiply_by = -1
    else:
        multiply_by = 1
    for char in string[start_index:len(string)]:
        digit = ord(char) - ord('0')
        transformed_result = (transformed_result * 10) + digit
    return transformed_result * multiply_by



def myAtoi(s: str) -> int:
    new_string = ""
    sign_count = 0
    for ch in s:
        if ch == " " and len(new_string) < 1:
            continue
        if ch == " " and len(new_string) >= 1:
            break
        if (ch == "+" or ch == "-") and (sign_count == 0) and len(new_string) < 1:
            new_string += ch
            sign_count += 1
            continue
        if (ch == "+" or ch == "-") and len(new_string) >= 1:
            break
        if ch.isalpha():
            break
        if ch == ".":
            break
        if ch.isdigit():
            new_string += ch
            continue

    if len(new_string) >= 1 and new_string.strip("+").isdigit():
        result = manual_int_to_string_conversion(new_string.strip("+"))
    elif len(new_string) >= 1 and new_string.strip("-").isdigit():
        result = manual_int_to_string_conversion(new_string)
    else:
        result = 0

    if result > (2 ** 31 - 1):
        return 2 ** 31 - 1
    elif result < (-(2 ** 31)):
        return -(2 ** 31)
    else:
        return result


print(myAtoi("+-12"))
print(myAtoi("-42"))
print(myAtoi("1337c0d3"))
print(myAtoi("0-1"))
print(myAtoi("words and 987"))

