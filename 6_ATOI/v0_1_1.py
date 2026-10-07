
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
        result = int(new_string)
    elif len(new_string) >= 1 and new_string.strip("-").isdigit():
        result = int(new_string)
    else:
        result = 0

    if result > (2 ** 31 - 1):
        return 2 ** 31 - 1
    elif result < (-(2 ** 31)):
        return -(2 ** 31)
    else:
        return result


print(myAtoi("+-12"))
print(myAtoi("-042"))
print(myAtoi("1337c0d3"))
print(myAtoi("0-1"))
print(myAtoi("words and 987"))
