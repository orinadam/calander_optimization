ID_IS_NOT_A_NUMBER = " שגיאה: הערך {value} אינו מספר תקין."
ID_EMPTY = "שגיאה: שדה תעודת זהות ריק."
ID_NOT_CORRECT_LENGTH = "שגיאה: הערך {value} אינו מספר בן 9 ספרות (מספר ת.ז. כולל ספרת ביקורת)"
ID_INVALID_CHECK_DIGIT = "שגיאה: הערך {value} אינו מספר תעודת זהות תקין. טעות בספרת הביקורת."


def verify_id(id_number):
    """
    checks if a given id number is valid
    :param id_number: the id number to check
    :return: an empty string if id_number is valid, otherwise a string detailing the error
    """
    try:
        id_number_str = str(int(id_number))
    except ValueError:
        return ID_IS_NOT_A_NUMBER.format(value=id_number.__repr__())

    if len(id_number_str) == 0:
        return ID_EMPTY

    if len(id_number_str) != 9:
        return ID_NOT_CORRECT_LENGTH.format(value=id_number.__repr__())
    orig_value = id_number_str

    check_digit = int(id_number_str[-1])
    id_number_str = id_number_str[:-1]

    odd_placed_digits = [int(i) for i in id_number_str[::2]]
    even_placed_digits = [int(i) for i in id_number_str[1::2]]

    values = odd_placed_digits + [2*i for i in even_placed_digits]
    values = "".join((str(i) for i in values))
    expected_check = 10 - sum([int(i) for i in values]) % 10

    if check_digit != expected_check:
        return ID_INVALID_CHECK_DIGIT.format(value=orig_value.__repr__())

    return ""


if __name__ == "__main__":
    while True:
        print(verify_id(input("Enter ID: ")))
