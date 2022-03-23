import pandas as pd
from datetime import date
from constants import *


def generate_candidate_dict(num_of_candidates):
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
        fd[EXCEL_CANDIDATE_ID_NUMBER].append(str(i).zfill(7))
        fd[EXCEL_CANDIDATE_PHONE_NUMBER].append('0541231234')
        fd[EXCEL_CANDIDATE_COURSE_TYPE].append('נחשון/מעוז')
        fd[EXCEL_CANDIDATE_NOTES].append('')
        fd[EXCEL_CANDIDATE_EMAIL_ADDRESS].append('email@email.com')
        fd[EXCEL_CANDIDATE_PERSONAL_NUMBER].append(str(i).zfill(7))
        fd[EXCEL_CANDIDATE_HEBREW_LEVEL].append(9 if i % 2 == 0 else 8)
        fd[EXCEL_CANDIDATE_STUDY_YEARS].append(12)
        fd[EXCEL_CANDIDATE_PSYCHOTECHNIC_EVALUATION].append(dapar[i % 4])
    return fd


def create_test_case(file_name, df):
    writer = pd.ExcelWriter(file_name, engine='xlsxwriter')
    df = pd.DataFrame(df)
    df.to_excel(writer, sheet_name='Sheet1', index=False)
    writer.save()


if __name__ == '__main__':
    create_test_case('test1.xlsx', generate_candidate_dict(100))
