import re

ID_IS_NOT_A_NUMBER = " שגיאה: הערך {value} אינו מספר תעודת זהות תקין."
ID_EMPTY = "שגיאה: שדה תעודת זהות ריק."
ID_INVALID_CHECK_DIGIT = "שגיאה: הערך {value} אינו מספר תעודת זהות תקין. טעות בספרת הביקורת."
ID_INVALID_LENGTH = "שגיאה: הערך {value} אינו מספר תעודת זהות תקין. האורך אינו תקין."
PHONE_NUMBER_INVALID_START = "שגיאה: הטלפון לא מתחיל בספרות 05"
PHONE_NUMBER_NOT_CORRECT_LENGTH = "שגיאה: בערך {value} אינו מספר בן 10 ספרות (מספר טלפון)"
PHONE_NUMBER_EMPTY = "שגיאה: השדה מספר טלפון ריק."


EMAIL_EMPTY = "ערך האימייל ריק."
INVALID_EMAIL = "ערך האימייל {value} אינו חוקי"

email_regex = re.compile("([\w\.\-]+)@([\w\-]+)((\.(\w)+)+)$")


def verify_id(id_number):
    """
    checks if a given id number is valid
    :param id_number: the id number to check
    :return: an empty string if id_number is valid, otherwise a string detailing the error
    """
    if not id_number:
        return ID_EMPTY
    try:
        id_number_str = str(int(id_number)).zfill(9)
    except ValueError:
        return ID_IS_NOT_A_NUMBER.format(value=id_number.__repr__())

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


def check_id(id_number):
    check = lambda id: 10 - (reduce(lambda a, b: a + b, list(map(int, id[0: -1: 2]))) + reduce(
        lambda a, b: a + (0, 2, 4, 6, 8, 1, 3, 5, 7, 9)[b], list(map(int, '0' + id[1:: 2])))) % 10 == int(id[-1])
    return check(id_number)


def verify_phone_number(phone_number: str) -> str:
    """
      checks if a given phone number is valid
      :param phone_number: the id number to check
      :return: an empty string if phone_number is valid, otherwise a string detailing the error
      """
    phone_number = str(phone_number)

    phone_number = phone_number.replace('-', "")
    if not phone_number.startswith("05"):
        return PHONE_NUMBER_INVALID_START

    if len(phone_number) == 0:
        return PHONE_NUMBER_EMPTY

    if not len(phone_number) == 10:
        return PHONE_NUMBER_NOT_CORRECT_LENGTH.format(value=phone_number.__repr__())

    return ""


def verify_email(email: str) -> str:
    if not email:
        return EMAIL_EMPTY
    if not isinstance(email, str) or not re.match(email_regex, email):
        return INVALID_EMAIL.format(value=email)
    return ""

if __name__ == "__main__":
    while True:
        print(verify_email(input("Enter Email: ")))
