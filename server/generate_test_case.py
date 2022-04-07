import random
import pandas as pd
from datetime import date
from constants import *


def generate_candidate_time_conditions(num_of_candidates, x, candidate_ids):
    days = ['יום שלישי בשעה ', 'יום רביעי בשעה ', 'יום חמישי בשעה ', 'יום ראשון בשעה ', 'יום שני בשעה ']
    fd = {
        EXCEL_PERSONAL_NUMBER: []
    }

    for i in days:
        for j in range(8, 21):
            fd[EXCEL_PERSONAL_NUMBER].append(i + str(j) + ':00')
    for i in range(num_of_candidates):
        fd[candidate_ids[i]] = ['V' if (hour + i) % x == 0 else '' for hour in range(13 * 5)]

    return fd



def generate_ranks_for_psychologists(ranks):
    rtrn_list = []
    for idx, i in enumerate(ranks):
        for j in range(i):
            rtrn_list.append(str(idx + 1))
    return rtrn_list


def generate_psychologists_dict(num_of_psychologists, ranks, psychologists_ids):
    fd = {
        EXCEL_CANDIDATE_FIRST_NAME: [],
        EXCEL_CANDIDATE_FAMILY_NAME: [],
        EXCEL_CANDIDATE_ID_NUMBER: [],
        EXCEL_RANK: [],
    }

    for i in range(num_of_psychologists):
        fd[EXCEL_CANDIDATE_FIRST_NAME].append('first')
        fd[EXCEL_CANDIDATE_FAMILY_NAME].append('name')
        fd[EXCEL_CANDIDATE_ID_NUMBER].append(psychologists_ids[i])
        fd[EXCEL_RANK].append(ranks[i])
    return fd


def psychologists_working_hours_to_excel(num_of_psychologists, psychologist_ids):
    psychologists_working_hours = []
    for i in range(num_of_psychologists):
        values_time = [psychologist_ids[i], ", ".join(generate_time()), ", ".join(generate_time()),
                       ", ".join(generate_time()),
                       ", ".join(generate_time()), ", ".join(generate_time())]
        psychologists_working_hours.append(values_time)

    return psychologists_working_hours


def generate_time():
    hours = []
    time_schedule = []
    for i in range(6):
        hour = (random.randrange(8, 21))
        hours.append(hour)
    hours.sort()
    time = list(dict.fromkeys(hours))
    for a in time:
        minutes = str(random.randrange(0, 46, 15))
        if minutes == "0":
            minutes = "00"
        time_schedule.append(str(a) + ":" + minutes)
    return time_schedule


def generate_id_num() -> str:
    id_num = ''
    check_digit = 0
    for i in range(8):
        id_num += str(random.randint(1, 9))
    for idx, i in enumerate(id_num):
        incNum = int(i) * ((idx % 2) + 1)  # Multiply number by 1 or 2
        check_digit += incNum - 9 if (incNum > 9) else incNum  # Sum the digits up and add to total
    id_num += str(10 - (check_digit % 10) if (check_digit % 10) != 0 else 0)
    return id_num


def IDValidator(id_num):
    # print(id_num)
    if len(id_num) != 9:  # Make sure ID is formatted properly
        return False
    my_sum = 0
    for idx, i in enumerate(id_num):
        incNum = int(i) * ((idx % 2) + 1)  # Multiply number by 1 or 2
        my_sum += incNum - 9 if (incNum > 9) else incNum  # Sum the digits up and add to total
    return my_sum % 10 == 0


def generate_candidate_dict(num_of_candidates, candidate_ids):
    dapar = [60, 70, 80, 90]
    fd = {
        EXCEL_CANDIDATE_SUBMISSION_DATE: [],
        EXCEL_CANDIDATE_AUTHORITY: [],
        EXCEL_CANDIDATE_FIRST_NAME: [],
        EXCEL_CANDIDATE_FAMILY_NAME: [],
        EXCEL_CANDIDATE_GENDER: [],
        EXCEL_CANDIDATE_BIRTH_DATE: [],
        EXCEL_CANDIDATE_ID_NUMBER: [],
        EXCEL_CANDIDATE_PHONE_NUMBER: [],
        EXCEL_CANDIDATE_COURSE_TYPE: [],
        EXCEL_CANDIDATE_NOTES: [],
        EXCEL_CANDIDATE_EMAIL_ADDRESS: [],
        EXCEL_CANDIDATE_PERSONAL_NUMBER: [],
        EXCEL_CANDIDATE_HEBREW_LEVEL: [],
        EXCEL_CANDIDATE_STUDY_YEARS: [],
        EXCEL_CANDIDATE_PSYCHOTECHNIC_EVALUATION: []
    }

    for i in range(num_of_candidates):
        fd[EXCEL_CANDIDATE_SUBMISSION_DATE].append(date.today().strftime('%m-%d-%Y'))
        fd[EXCEL_CANDIDATE_AUTHORITY].append('9100')
        fd[EXCEL_CANDIDATE_FIRST_NAME].append('first')
        fd[EXCEL_CANDIDATE_FAMILY_NAME].append('name')
        fd[EXCEL_CANDIDATE_GENDER].append('M' if i % 2 == 0 else 'F')
        fd[EXCEL_CANDIDATE_BIRTH_DATE].append(date.today().strftime('%m-%d-%Y'))
        fd[EXCEL_CANDIDATE_ID_NUMBER].append(candidate_ids[i])
        fd[EXCEL_CANDIDATE_PHONE_NUMBER].append('0541231234')
        fd[EXCEL_CANDIDATE_COURSE_TYPE].append('נחשון/מעוז')
        fd[EXCEL_CANDIDATE_NOTES].append('')
        fd[EXCEL_CANDIDATE_EMAIL_ADDRESS].append('email@email.com')
        fd[EXCEL_CANDIDATE_PERSONAL_NUMBER].append(str(i).zfill(7))
        fd[EXCEL_CANDIDATE_HEBREW_LEVEL].append(9 if i % 2 == 0 else 8)
        fd[EXCEL_CANDIDATE_STUDY_YEARS].append(12)
        fd[EXCEL_CANDIDATE_PSYCHOTECHNIC_EVALUATION].append(dapar[i % 4])
    return fd


def generate_candidate_conditions(num_of_candidates, candidate_ids):
    fd = {
        'התניה לדוגמא': [],
        'התניה נוספת': [],
        'התניה נוספת 1': [],
        'התניה נוספת 2': [],
        'התניה נוספת 3': [],
        'התניה נוספת 4': [],
        'התניה נוספת 5': [],
        'התניה נוספת 6': [],
        'התניה נוספת 7': [],
        'התניה נוספת 8': [],
        'התניה נוספת 9': [],
        'התניה נוספת 10': [],
        'התניה נוספת 11': [],
        'התניה נוספת 12': [],
        'התניה נוספת 13': [],
        'התניה נוספת 14': [],

    }
    for i in range(num_of_candidates):
        if i % 16 == 0:
            fd['התניה לדוגמא'].append(candidate_ids[i])
        elif i % 16 == 1:
            fd['התניה נוספת'].append(candidate_ids[i])
        elif i % 16 == 2:
            fd['התניה נוספת 1'].append(candidate_ids[i])
        elif i % 16 == 3:
            fd['התניה נוספת 2'].append(candidate_ids[i])
        elif i % 16 == 4:
            fd['התניה נוספת 3'].append(candidate_ids[i])
        elif i % 16 == 5:
            fd['התניה נוספת 4'].append(candidate_ids[i])
        elif i % 16 == 6:
            fd['התניה נוספת 5'].append(candidate_ids[i])
        elif i % 16 == 7:
            fd['התניה נוספת 6'].append(candidate_ids[i])
        elif i % 16 == 8:
            fd['התניה נוספת 7'].append(candidate_ids[i])
        elif i % 16 == 9:
            fd['התניה נוספת 8'].append(candidate_ids[i])
        elif i % 16 == 10:
            fd['התניה נוספת 9'].append(candidate_ids[i])
        elif i % 16 == 11:
            fd['התניה נוספת 10'].append(candidate_ids[i])
        elif i % 16 == 12:
            fd['התניה נוספת 11'].append(candidate_ids[i])
        elif i % 16 == 13:
            fd['התניה נוספת 12'].append(candidate_ids[i])
        elif i % 16 == 14:
            fd['התניה נוספת 13'].append(candidate_ids[i])
        elif i % 16 == 15:
            fd['התניה נוספת 14'].append(candidate_ids[i])
    max_len = 0
    for val in fd.values():
        if len(val) > max_len:
            max_len = len(val)
    for key, val in fd.items():
        while len(val) < max_len:
            fd[key].append('')
    return fd


def create_test_case(file_name, df):
    writer = pd.ExcelWriter(file_name, engine='xlsxwriter')
    df = pd.DataFrame.from_dict(df)
    df.to_excel(writer, sheet_name='Sheet1', index=False)
    writer.save()


def generate_id_list(num):
    return [generate_id_num() for i in range(num)]


def generate_full_test(dict_name, test_name, num_of_candidates, num_of_psychologists):
    candidate_ids = generate_id_list(num_of_candidates)
    psychologist_ids = generate_id_list(num_of_psychologists)
    create_test_case(dict_name + '/candidate_time_conditions_' + test_name + '.xlsx',
                     generate_candidate_time_conditions(num_of_candidates, 3, candidate_ids))
    create_test_case(dict_name + '/psychologists_' + test_name + '.xlsx', generate_psychologists_dict(num_of_psychologists,
                                                                                         generate_ranks_for_psychologists(
                                                                                             [10, 2, 3, 1, 3, 2]),
                                                                                         psychologist_ids))
    create_test_case(dict_name + '/candidates_' + test_name + '.xlsx', generate_candidate_dict(num_of_candidates, candidate_ids))
    create_test_case(dict_name + '/candidate_conditions_' + test_name + '.xlsx',
                     generate_candidate_conditions(num_of_candidates, candidate_ids))
    psychologists_working_hours = psychologists_working_hours_to_excel(num_of_psychologists, psychologist_ids)
    pd.DataFrame(psychologists_working_hours, index=[None for i in range(num_of_psychologists)],
                 columns=["ת'ז", "יום שלישי 14.12", "יום רביעי 15.12",
                          "יום חמישי 16.12", "יום ראשון 17.12", "יום שני 18.12"]).to_excel(
        dict_name + '/psychologists_working_hours_' + test_name + '.xlsx', index=False)


if __name__ == '__main__':
    # create_test_case('test3.xlsx', psychologists_working_hours_to_excel(6))
    # create_test_case('test1.xlsx', generate_candidate_dict(100))
    # create_test_case('test1.xlsx', generate_candidate_dict(100))
    generate_full_test('4th_dict_name', '1st_full_test', 100, 20)
