def convertTime(current: str, correct: str) -> int:
    current_hour = current[0:2]
    current_minutes = current[3:]
    correct_hour = correct[0:2]
    correct_minutes = correct[3:]

    current_total_minutes = 0
    correct_total_minutes = 0

    if int(current_hour[0]) == 0:
        current_total_minutes = int(current_hour[1]) * 60
    else:
        current_total_minutes = int(current_hour) * 60

    if int(current_minutes[0]) == 0:
        current_total_minutes += int(current_minutes[1])
    else:
        current_total_minutes += int(current_minutes)

    #########################################

    if int(correct_hour[0]) == 0:
        correct_total_minutes = int(correct_hour[1]) * 60
    else:
        correct_total_minutes = int(correct_hour) * 60

    if int(correct_minutes[0]) == 0:
        correct_total_minutes += int(correct_minutes[1])
    else:
        correct_total_minutes += int(correct_minutes)

    difference = correct_total_minutes - current_total_minutes

    min_count_one = 0
    min_count_two = 0
    min_count_three = 0

    while difference >= 5:
        print(difference)
        print(min_count_one)
        min_count_one = (difference // 60)
        print(min_count_one)
        difference = difference - (min_count_one * 60)
        print(difference)
        min_count_two = (difference // 15)
        print(min_count_two)
        difference = difference - (min_count_two * 15)
        print(difference)
        min_count_three = (difference // 5)
        print(min_count_three)
        difference = difference - (min_count_three * 5)
        print(difference)

    return min_count_one + min_count_two + min_count_three + difference

if __name__ == "__main__":
    x = "00:00"
    y = "23:59"

    result = convertTime(x,y)

    print(result)