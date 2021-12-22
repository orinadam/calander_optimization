import sqlite3
import os
import pandas as pd
from math import inf
from constants import *

# relative path to database
DATABASE_PATH = "database.db"


class Candidate:
    def __init__(self, first_name, family_name, personal_number, notes, phone_number, study_years, hebrew_level,
                 email_address, authority, required_level_for_interview, psychotechnic_evaluation,
                 specific_psychologist=None, available_hours=None):
        self.first_name = first_name
        self.family_name = family_name
        self.personal_number = personal_number
        self.notes = notes
        self.phone_number = phone_number
        self.study_years = study_years
        self.hebrew_level = hebrew_level
        self.email_address = email_address
        self.authority = authority
        self.required_level_for_interview = required_level_for_interview
        if available_hours is None:
            self.available_hours = [[] for i in range(len(DAYS_OF_THE_WEEK))]
        else:
            self.available_hours = available_hours
        self.psychotechnic_evaluation = psychotechnic_evaluation
        self.specific_psychologist = specific_psychologist

    # to allow easy debugging
    def __repr__(self):
        return str(self.__dict__)


class PsychoInfo:
    def __init__(self, first_name, family_name, id_number, level, num_of_interviews, available_hours=None):
        self.first_name = first_name
        self.family_name = family_name
        self.id_number = id_number
        self.level = level
        self.num_of_interviews = num_of_interviews
        if available_hours is None:
            self.available_hours = [[] for i in range(len(DAYS_OF_THE_WEEK))]
        else:
            self.available_hours = available_hours
        self.is_new = num_of_interviews <= NUM_OF_INTERVIEWS
        self.used_hours = []  # hours in this list should be removed

    # to allow easy debugging
    def __repr__(self):
        return str(self.__dict__)


def initialize_database_tables():
    """
    initializes the tables of the database, if they do not already exist.
    if the database does not exist, creates one
    """

    connection = sqlite3.connect(DATABASE_PATH)
    connection.execute(f"""
    CREATE TABLE IF NOT EXISTS {CANDIDATES_TABLE} (
        {CANDIDATE_AUTHORITY} INTEGER,
        {CANDIDATE_FIRST_NAME} TEXT,
        {CANDIDATE_FAMILY_NAME} TEXT,
        {CANDIDATE_GENDER} TEXT,
        {CANDIDATE_DATE_OF_BIRTH} DATE,
        {CANDIDATE_ID_NUMBER} INTEGER,
        {CANDIDATE_PERSONAL_NUMBER} INTEGER,
        {CANDIDATE_PHONE_NUMBER} TEXT,
        {CANDIDATE_EMAIL_ADDRESS} TEXT,
        {CANDIDATE_COURSE_TYPE} TEXT,
        {CANDIDATE_PSYCHOTECHNIC_EVALUATION} INTEGER,
        {CANDIDATE_STUDY_YEARS} INTEGER,
        {CANDIDATE_HEBREW_LEVEL} INTEGER,
        {CANDIDATE_NOTES} TEXT,
        {CANDIDATE_REQUIRED_LEVEL} INTEGER,
        {CANDIDATE_AVAILABLE_HOURS} TEXT
    );
    """)

    # boolean values is sqlite are stored as 0 or 1
    # available hours are stored as text
    connection.execute(f"""
    CREATE TABLE IF NOT EXISTS {PSYCHOLOGISTS_TABLE} (
        {PSYCHOLOGIST_FIRST_NAME} TEXT,
        {PSYCHOLOGIST_FAMILY_NAME} TEXT,
        {PSYCHOLOGIST_ID_NUMBER} INTEGER,
        {PSYCHOLOGIST_LEVEL} INTEGER,
        {PSYCHOLOGIST_IS_NEW} INTEGER,
        {PSYCHOLOGIST_NUM_OF_INTERVIEWS} INTEGER,
        {PSYCHOLOGIST_AVAILABLE_HOURS} TEXT
    );
    """)

    connection.execute(f"""
    CREATE TABLE IF NOT EXISTS {CONDITIONS_TABLE} (
        {CONDITION_NAME} TEXT,
        {CONDITION_REQUIRED_LEVEL} INTEGER
    );
    """)

    connection.close()


def insert_into_table(cursor, table_name, data):
    """
    inserts now rows into a given table
    :param cursor: the cursor to use when inserting
    :param table_name: the name of the table
    :param data: a dictionary containing pairs of (row: data_to_insert)
    :return:
    """
    # the sql query used to insert data
    # "keys" should be replaced with a list of comma separated column names
    # "values" should be replaced with a list of comma separated question marks, which
    # should then be sanitized by sqlite to prevent injections
    sql_query = """INSERT INTO {table}
                   ({keys})
                   VALUES ({values});
    """
    keys = []
    values = []
    for key, val in data.items():
        keys.append(key)
        values.append(val)
    sql_query = sql_query.format(table=table_name, keys=", ".join((str(i) for i in keys)),
                                 values=", ".join(list("?"*len(values))))
    cursor.execute(sql_query, tuple(values))


def get_conditions(conditions_file_path):
    """loads the conditions from the given file into the database"""
    data = pd.read_excel(conditions_file_path, engine='openpyxl')
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    # clear previous data
    cursor.execute(f"DELETE FROM {CONDITIONS_TABLE};")

    for idx, row in data.iterrows():
        insert_into_table(cursor, CONDITIONS_TABLE, {CONDITION_NAME: row[EXCEL_CONDITION_NAME],
                                                     CONDITION_REQUIRED_LEVEL: row[EXCEL_CONDITION_REQUIRED_LEVEL]})
    connection.commit()
    connection.close()


def get_psychologists(psychologists_file_path):
    """reads a file of psychologists into to database"""
    data = pd.read_excel(psychologists_file_path, engine='openpyxl')
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    # clear previous data
    cursor.execute(f"DELETE FROM {PSYCHOLOGISTS_TABLE};")

    for idx, row in data.iterrows():
        insert_into_table(cursor, PSYCHOLOGISTS_TABLE,
                          {
                              PSYCHOLOGIST_FIRST_NAME: row[EXCEL_PSYCHOLOGIST_FIRST_NAME],
                              PSYCHOLOGIST_FAMILY_NAME: row[EXCEL_PSYCHOLOGIST_FAMILY_NAME],
                              PSYCHOLOGIST_ID_NUMBER: row[EXCEL_PSYCHOLOGIST_ID_NUMBER],
                              PSYCHOLOGIST_LEVEL: row[EXCEL_PSYCHOLOGIST_LEVEL],
                              PSYCHOLOGIST_NUM_OF_INTERVIEWS: row[EXCEL_PSYCHOLOGIST_NUM_OF_INTERVIEWS],
                              # a psychologist is considered new if he/she conducted less than NUM_OF_INTERVIEWS
                              # interviews
                              PSYCHOLOGIST_IS_NEW: int(row[EXCEL_PSYCHOLOGIST_NUM_OF_INTERVIEWS] < NUM_OF_INTERVIEWS)
                          })
    connection.commit()
    connection.close()


def get_candidates(candidates_file_path):
    """loads candidates from file into the database"""
    data = pd.read_excel(candidates_file_path, engine='openpyxl')
    data[EXCEL_CANDIDATE_AUTHORITY] = data[EXCEL_CANDIDATE_AUTHORITY].fillna(method='ffill', axis=0)
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    # clear previous data
    cursor.execute(f"DELETE FROM {CANDIDATES_TABLE};")

    for idx, row in data.iterrows():
        if not pd.isnull(row[EXCEL_CANDIDATE_SUBMISSION_DATE]):
            insert_into_table(cursor, CANDIDATES_TABLE,
                              {CANDIDATE_FIRST_NAME: row[EXCEL_CANDIDATE_FIRST_NAME],
                               CANDIDATE_FAMILY_NAME: row[EXCEL_CANDIDATE_FAMILY_NAME],
                               CANDIDATE_AUTHORITY: row[EXCEL_CANDIDATE_AUTHORITY],
                               CANDIDATE_DATE_OF_BIRTH: str(row[EXCEL_CANDIDATE_BIRTH_DATE]),
                               CANDIDATE_GENDER: row[EXCEL_CANDIDATE_GENDER],
                               CANDIDATE_ID_NUMBER: row[EXCEL_CANDIDATE_ID_NUMBER],
                               CANDIDATE_PHONE_NUMBER: row[EXCEL_CANDIDATE_PHONE_NUMBER],
                               CANDIDATE_EMAIL_ADDRESS: row[EXCEL_CANDIDATE_EMAIL_ADDRESS],
                               CANDIDATE_NOTES: row[EXCEL_CANDIDATE_NOTES],
                               CANDIDATE_COURSE_TYPE: row[EXCEL_CANDIDATE_COURSE_TYPE],
                               CANDIDATE_PERSONAL_NUMBER: row[EXCEL_CANDIDATE_PERSONAL_NUMBER],
                               CANDIDATE_HEBREW_LEVEL: row[EXCEL_CANDIDATE_HEBREW_LEVEL],
                               CANDIDATE_STUDY_YEARS: row[EXCEL_CANDIDATE_STUDY_YEARS],
                               CANDIDATE_PSYCHOTECHNIC_EVALUATION: row[EXCEL_CANDIDATE_PSYCHOTECHNIC_EVALUATION]
                             })
    connection.commit()
    connection.close()


def get_cond_of_cand(path_to_candidates_conditions_file):
    """loads conditions from a file into the database"""
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.execute(f"SELECT {CONDITION_NAME}, {CONDITION_REQUIRED_LEVEL} from {CONDITIONS_TABLE};")
    conditions = {}
    for row in cursor:
        condition, required_level = row
        conditions[condition] = required_level

    # reads the Excel file as though it is transposed
    data: pd.DataFrame = pd.read_excel(path_to_candidates_conditions_file, header=None, index_col=0, engine='openpyxl').transpose()

    candidates_to_update = {}

    for cond, level in conditions.items():
        if cond not in data.columns:  # if the condition does not appear in the file
            continue
        for personal_number in data[cond]:  # iterate over all personal numbers with the condition
            if not pd.isnull(personal_number):
                candidates_to_update[personal_number] = max(level, candidates_to_update.get(personal_number, -inf))

    # updates database
    for personal_number, level in candidates_to_update.items():
        cursor.execute(f"""
            UPDATE {CANDIDATES_TABLE}
            SET {CANDIDATE_REQUIRED_LEVEL}=?
            WHERE {CANDIDATE_PERSONAL_NUMBER} = ?;
        """, (level, personal_number))
    connection.commit()
    connection.close()


def get_working_time(path_to_working_hours_file):
    """loads working times of psychologists into the database"""
    data: pd.DataFrame = pd.read_excel(path_to_working_hours_file, engine='openpyxl')
    days = []
    # Tries to match the days to the columns in the loaded data. For each day (in order), if a column name matches the
    # day, it is appended to the list of days, otherwise, and empty string is appended instead.
    for day in DAYS_OF_THE_WEEK:
        for col in data.columns:
            if day in col:
                days.append(col)
                break
        else:
            days.append("")
    # is_col contains the name of the column containing the id number of the psychologists
    id_col = [i for i in data.columns if EXCEL_WORKING_HOURS_ID_NUMBER in i][0]

    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    for idx, row in data.iterrows():
        # the format of the working_time stored in the database is as follows:
        # each day is represented by a line, containing all the available hours in that day, separated by ", ",
        # the days are separated by newlines, and there is no newline at the end.
        working_time = "\n".join([row[day] if day and not pd.isnull(row[day]) else "" for day in days])
        cursor.execute(f"""
            UPDATE {PSYCHOLOGISTS_TABLE}
            SET {PSYCHOLOGIST_AVAILABLE_HOURS} = ?
            WHERE {PSYCHOLOGIST_ID_NUMBER} = ?
        """, (working_time, row[id_col]))
    connection.commit()
    connection.close()


def parse_times_list(times):
    times_list = []
    if times:
        for day in times.split("\n"):
            # converts hours in HH:MM format to float (For example, "14:30" becomes 14.5)
            idx = pd.DatetimeIndex(day.split(), dtype='datetime64[ns]')
            day_list = list(idx.hour + idx.minute / 60)
            times_list.append(day_list)
    else:  # if a psychologist/candidate did not specify times, he is unavailable
        times_list = [[] for i in range(len(DAYS_OF_THE_WEEK))]
    return times_list


def get_psychologists_list():
    """
    :return: a list of psychologists
    """
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.execute(f"SELECT {PSYCHOLOGIST_FIRST_NAME}, {PSYCHOLOGIST_FAMILY_NAME}, "
                                f"{PSYCHOLOGIST_ID_NUMBER}, {PSYCHOLOGIST_NUM_OF_INTERVIEWS}, {PSYCHOLOGIST_LEVEL}, "
                                f"{PSYCHOLOGIST_AVAILABLE_HOURS} from {PSYCHOLOGISTS_TABLE};")
    psychologists = []
    for row in cursor:  # each row corresponds to a psychologist
        first_name, family_name, id_number, num_of_interviews, level, times = row
        times_list = parse_times_list(times)
        psychologists.append(PsychoInfo(
            first_name=first_name,
            family_name=family_name,
            id_number=id_number,
            level=level,
            num_of_interviews=num_of_interviews,
            available_hours=times_list
        ))
    connection.close()
    return psychologists


def get_candidates_list():
    """
    :return: a dictionary of candidates and their info
    """
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.execute(f"SELECT {CANDIDATE_PERSONAL_NUMBER}, {CANDIDATE_FIRST_NAME}, {CANDIDATE_FAMILY_NAME}, "
                                f"{CANDIDATE_NOTES}, {CANDIDATE_PHONE_NUMBER}, {CANDIDATE_PSYCHOTECHNIC_EVALUATION}, "
                                f"{CANDIDATE_STUDY_YEARS}, {CANDIDATE_HEBREW_LEVEL}, {CANDIDATE_EMAIL_ADDRESS}, "
                                f"{CANDIDATE_AUTHORITY}, {CANDIDATE_REQUIRED_LEVEL}, {CANDIDATE_AVAILABLE_HOURS}"
                                f" from {CANDIDATES_TABLE};")
    candidates = []
    for row in cursor:  # each row corresponds to a psychologist
        # extracting info from row
        personal_number, first_name, family_name, notes, phone_number, psychotechnic_eval, \
            study_years, hebrew, email, authority, required_level, available_hours_raw = row
        # parse available_hours
        available_hours = parse_times_list(available_hours_raw)

        # inserting info into candidate class
        candidates.append(Candidate(
            first_name=first_name,
            family_name=family_name,
            personal_number=personal_number,
            notes=notes,
            phone_number=phone_number,
            study_years=study_years,
            hebrew_level=hebrew,
            email_address=email,
            authority=authority,
            required_level_for_interview=required_level,
            psychotechnic_evaluation=psychotechnic_eval,
            available_hours=available_hours
        ))
    connection.close()
    return candidates


def search_list(lst, subtexts):
    """
    searches list for elements containing subtext
    :param lst: the list to search
    :param subtexts: the subtexts that must appear in the list for it to be considered a match
    :return: the lst element if found, None otherwise
    """
    for element in lst:
        if all((subtext in element for subtext in subtexts)):
            return element
    return None


def get_candidates_available_hours(available_hours_file):
    """loads available times of candidates into the database"""
    data: pd.DataFrame = pd.read_excel(available_hours_file, header=None, index_col=0, engine='openpyxl').transpose()

    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    for idx, row in data.iterrows():  # each candidate has a dedicated row
        candidate_personal_number = row[EXCEL_CANDIDATE_AVAILABLE_HOUR_PERSONAL_NUMBER]
        available_times = []
        for day in DAYS_OF_THE_WEEK:
            day_times = []
            for hour in range(EARLIEST_HOUR, LATEST_HOUR + 1):
                # gets the column name corresponding to {day} at {hour}
                column = search_list(data.columns, (day, f"{hour}:00"))
                if column:  # if such a column exists
                    if not pd.isnull(row[column]):
                        day_times.append(f"{hour}:00")
            available_times.append(", ".join(day_times))

        # convert available times to the expected format, I.E. comma separated hours for each day, days are separated
        # by newlines and there are no newline at the end
        times = "\n".join(available_times)
        # update database
        cursor.execute(f"""
            UPDATE {CANDIDATES_TABLE}
            SET {CANDIDATE_AVAILABLE_HOURS} = ?
            WHERE {CANDIDATE_PERSONAL_NUMBER} = ?
        """, (times, candidate_personal_number))
    connection.commit()
    connection.close()


if __name__ == "__main__":
    initialize_database_tables()
    get_conditions(os.path.join("examples", "conditions.xlsx"))
    get_candidates(os.path.join("examples", "candidates.xlsx"))
    get_cond_of_cand(os.path.join("examples", "candidates_conditions.xlsx"))
    get_psychologists(os.path.join("examples", "psychologists.xlsx"))
    get_working_time(os.path.join("examples", "working_hours.xlsx"))
    get_candidates_available_hours(os.path.join("examples", "candidates_available_hours.xlsx"))

    print(get_psychologists_list())
    print(get_candidates_list())
