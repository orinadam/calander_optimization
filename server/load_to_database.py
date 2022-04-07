import datetime
import sqlite3
import logging
import os
import zipfile

import pandas as pd
from math import inf
from constants import *
from typing import *
from warning_messages import *

# relative path to database
DATABASE_PATH = "database.db"


def float_to_hour(flt):
    """converts hours from 15.5 to 15:30 format"""
    full = int(flt // 1)
    frac = flt - full
    frac *= 60
    frac = int(frac)
    return f"{full}:{str(frac).zfill(2)}"


class Candidate:
    def __init__(self, first_name, family_name, date_of_birth, gender, personal_number, notes, phone_number,
                 study_years,
                 hebrew_level,
                 email_address, authority, required_level_for_interview, psychotechnic_evaluation,
                 id_number, service_type, course_type, specific_psychologist=None, available_hours=None):
        self.first_name = first_name
        self.family_name = family_name
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.id_number = id_number
        try:
            self.personal_number = int(personal_number)
        except (ValueError, TypeError):
            self.personal_number = personal_number
        self.notes = notes
        self.phone_number = phone_number
        self.study_years = study_years
        self.hebrew_level = hebrew_level
        self.email_address = email_address
        self.authority = authority
        self.required_level_for_interview = required_level_for_interview
        self.service_type = service_type
        self.course_type = course_type
        if available_hours is None:
            self.available_hours = [[] for i in range(len(DAYS_OF_THE_WEEK))]
        else:
            self.available_hours = available_hours
        self.psychotechnic_evaluation = psychotechnic_evaluation
        self.specific_psychologist = specific_psychologist
        self.in_schedule = IsInSchedule.FAILED.value

    def available_hours_to_string(self):
        return "\n".join((", ".join(float_to_hour(h) for h in hours) for hours in self.available_hours))

    def errors_inserting(self):
        errors = []
        if not isinstance(self.personal_number, int) or self.personal_number < 0:
            errors.append("שגיאה: המספר האישי " + str(self.personal_number) + " אינו תקין. המועמד לא התווסף.")
        if not isinstance(self.date_of_birth, datetime.datetime):
            errors.append("שגיאה: תאריך הלידה " + str(self.date_of_birth) + " אינו תקין. המועמד שמספרו האישי " + str(
                self.personal_number) + " לא התווסף.")
        return errors

    def non_critical_errors(self):
        errors = []

        id_error = verify_id(self.id_number)
        if id_error:
            errors.append(id_error)
        phone_error = verify_phone_number(self.phone_number)
        if phone_error:
            errors.append(phone_error)
        email_error = verify_email(self.email_address)
        if email_error:
            errors.append(email_error)
        if not self.first_name:
            errors.append("השם הפרטי לא יכול להיות ריק")
        if not self.family_name:
            errors.append("שם המשפחה לא יכול להיות ריק")
        if not self.gender:
            errors.append("ערך המגדר לא יכול להיות ריק")
        if not self.email_address:
            errors.append("כתובת המייל לא יכולה להיות ריק.")
        if not self.authority:
            errors.append("הסמכות לא יכולה להיות ריקה.")
        if not self.service_type:
            errors.append("סוג השירות לא יכול להיות ריק.")
        if not self.course_type:
            errors.append('סוג קק"צ לא יכול להיות ריק')

        try:
            int(self.required_level_for_interview)
        except ValueError:
            errors.append("הדרג הנדרש לריאיון חייב להיות מספר.")

        try:
            int(self.study_years)
        except ValueError:
            errors.append("מספר שנות הלימוד חייב להיות מספר.")
        else:
            if not self.study_years:
                errors.append("מספר שנות הלימוד לא יכול להיות ריק.")

        return errors

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


class Meeting:
    """
    a class containing all data about a meeting
    """

    def __init__(self, candidate: Candidate, psychologist: PsychoInfo, day: int, hour: float):
        """
        constructs a new meeting class
        :param candidate: a candidate (class)
        :param psychologist: a psychologist (class)
        :param day: the day (as an integer!) references the day in DAYS_OF_THE_WEEK[day]
        :param hour: the hour (float, I.E. 17.25 means 17:15)
        """
        self.day: int = day
        self.hour = hour
        self.candidate = candidate
        self.psychologist = psychologist


def initialize_database_tables():
    """
    initializes the tables of the database, if they do not already exist.
    if the database does not exist, creates one
    """

    connection = sqlite3.connect(DATABASE_PATH, detect_types=sqlite3.PARSE_DECLTYPES)
    connection.execute(f"""
    CREATE TABLE IF NOT EXISTS {CANDIDATES_TABLE} (
        {CANDIDATE_AUTHORITY} INTEGER,
        {CANDIDATE_FIRST_NAME} TEXT,
        {CANDIDATE_FAMILY_NAME} TEXT,
        {CANDIDATE_GENDER} TEXT,
        {CANDIDATE_DATE_OF_BIRTH} timestamp NOT NULL,
        {CANDIDATE_ID_NUMBER} INTEGER,
        {CANDIDATE_PERSONAL_NUMBER} INTEGER,
        {CANDIDATE_PHONE_NUMBER} TEXT,
        {CANDIDATE_EMAIL_ADDRESS} TEXT,
        {CANDIDATE_COURSE_TYPE} TEXT,
        {CANDIDATE_SERVICE_TYPE} INTEGER,
        {CANDIDATE_PSYCHOTECHNIC_EVALUATION} INTEGER,
        {CANDIDATE_STUDY_YEARS} INTEGER,
        {CANDIDATE_HEBREW_LEVEL} INTEGER,
        {CANDIDATE_NOTES} TEXT,
        {CANDIDATE_REQUIRED_LEVEL} INTEGER DEFAULT 0,
        {CANDIDATE_AVAILABLE_HOURS} TEXT,
        {CANDIDATE_WEEK} timestamp NOT NULL,
        value,
        PRIMARY KEY ({CANDIDATE_WEEK}, {CANDIDATE_PERSONAL_NUMBER})
    );
    """)

    # boolean values is sqlite are stored as 0 or 1
    # available hours are stored as text
    connection.execute(f"""
    CREATE TABLE IF NOT EXISTS {PSYCHOLOGISTS_TABLE} (
        {PSYCHOLOGIST_FIRST_NAME} TEXT NOT NULL,
        {PSYCHOLOGIST_FAMILY_NAME} TEXT NOT NULL,
        {PSYCHOLOGIST_ID_NUMBER} INTEGER NOT NULL,
        {PSYCHOLOGIST_LEVEL} INTEGER NOT NULL ,
        {PSYCHOLOGIST_IS_NEW} INTEGER NOT NULL DEFAULT 1,
        {PSYCHOLOGIST_NUM_OF_INTERVIEWS} INTEGER NOT NULL DEFAULT 0,
        {PSYCHOLOGIST_AVAILABLE_HOURS} TEXT,
        {PSYCHOLOGIST_WEEK} timestamp NOT NULL,
        value,
        PRIMARY KEY ({PSYCHOLOGIST_WEEK}, {PSYCHOLOGIST_ID_NUMBER})
    );
    """)

    connection.execute(f"""
    CREATE TABLE IF NOT EXISTS {CONDITIONS_TABLE} (
        {CONDITION_NAME} TEXT NOT NULL UNIQUE,
        {CONDITION_REQUIRED_LEVEL} INTEGER NOT NULL
    );
    """)

    connection.execute(f"""
    CREATE TABLE IF NOT EXISTS {SERVICE_TYPES_TABLE} (
        {SERVICE_TYPE_NAME} INTEGER NOT NULL UNIQUE,
        {SERVICE_TYPE_REQUIRED_LEVEL} INTEGER NOT NULL
    );
    """)

    connection.execute(f"""
    CREATE TABLE IF NOT EXISTS {MEETINGS_TABLE} (
        {MEETING_PSYCHOLOGIST_ID} INTEGER NOT NULL,
        {MEETING_CANDIDATE_NUMBER} INTEGER NOT NULL,
        {MEETING_DAY} INTEGER NOT NULL ,
        {MEETING_HOUR} TEXT NOT NULL,
        {MEETING_WEEK} timestamp NOT NULL,
        value,
        PRIMARY KEY ({MEETING_WEEK}, {MEETING_CANDIDATE_NUMBER})
    );
    """)

    connection.close()


def insert_into_table(cursor, table_name, data, replace=True):
    """
    inserts now rows into a given table
    :param replace: if set to true, if entry violates primary key constraints the value will be replaced. Otherwise,
    in case of a PK constraint violation will raise an error.
    :param cursor: the cursor to use when inserting
    :param table_name: the name of the table
    :param data: a dictionary containing pairs of (row: data_to_insert)
    :return:
    """
    # the sql query used to insert data
    # "keys" should be replaced with a list of comma separated column names
    # "values" should be replaced with a list of comma separated question marks, which
    # should then be sanitized by sqlite to prevent injections
    sql_query = """REPLACE INTO {table}
                   ({keys})
                   VALUES ({values});
    """
    keys = []
    values = []
    for key, val in data.items():
        keys.append(key)
        values.append(val)
    sql_query = sql_query.format(table=table_name, keys=", ".join((str(i) for i in keys)),
                                 values=", ".join(list("?" * len(values))))
    cursor.execute(sql_query, tuple(values))


def store_timetable(meetings: List[Meeting], week):
    """
    stores a timetable in the database
    :param meetings: a list of meeting to store
    :param week: the week of the table to store. Weeks are described by a `datetime.datetime` object storing the first
    day of the week (which is tuesday, or day 1 since monday is 0) at midnight.
    """
    connection = sqlite3.connect(DATABASE_PATH, detect_types=sqlite3.PARSE_DECLTYPES)
    cursor = connection.cursor()

    # clear previous data
    cursor.execute(f"DELETE FROM {MEETINGS_TABLE} WHERE {MEETING_WEEK}=?;", (week,))

    for meeting in meetings:
        # convert hour to string
        hour = f"{int(meeting.hour)}:{int(60 * (meeting.hour - int(meeting.hour)))}"
        # load into database
        insert_into_table(cursor, MEETINGS_TABLE, {
            MEETING_DAY: meeting.day,
            MEETING_HOUR: hour,
            MEETING_PSYCHOLOGIST_ID: meeting.psychologist.id_number,
            MEETING_CANDIDATE_NUMBER: meeting.candidate.personal_number,
            MEETING_WEEK: week
        })
    connection.commit()
    connection.close()


def load_timetable_from_database(week):
    """
    loads all meetings from database
    :return: a list of the meetings loaded
    """
    connection = sqlite3.connect(DATABASE_PATH, detect_types=sqlite3.PARSE_DECLTYPES)
    cursor = connection.execute(f"SELECT {MEETING_DAY}, {MEETING_HOUR}, {MEETING_PSYCHOLOGIST_ID}, "
                                f"{MEETING_CANDIDATE_NUMBER} from {MEETINGS_TABLE} WHERE {MEETING_WEEK}=?;",
                                (week,)
                                )
    meetings = []
    candidates_list = get_candidates_list(week)
    psychologists_list = get_psychologists_list(week)
    for row in cursor:  # each row corresponds to a meeting
        day, hour_text, psychologist_id, candidate_personal_number = row
        # convert hour to numeric format (17:30 becomes 17.5)
        idx = pd.DatetimeIndex((hour_text,), dtype='datetime64[ns]')
        hour = list(idx.hour + idx.minute / 60)[0]

        # fetch candidate with correct personal number and psychologist with correct id
        candidate = next(filter(lambda c: (c.personal_number == candidate_personal_number), candidates_list), None)
        psychologist = next(filter(lambda p: (p.id_number == psychologist_id), psychologists_list), None)

        if candidate is None or psychologist is None:
            # TODO raise error, both candidate and psychologist should exist
            pass

        meetings.append(Meeting(candidate=candidate, psychologist=psychologist, day=day, hour=hour))
    connection.close()
    return meetings


def get_service_types(conditions_file_path, clear_previous=False):
    """loads the service types from the given file into the database"""
    errors = []
    try:
        data = pd.read_excel(conditions_file_path, engine='openpyxl')
    except (zipfile.BadZipfile, KeyError):
        errors.append("קובץ סוגי השירות אינו קובץ excel תקין.")
        return errors
    connection = sqlite3.connect(DATABASE_PATH, detect_types=sqlite3.PARSE_DECLTYPES)
    cursor = connection.cursor()

    # clear previous data
    if clear_previous:
        cursor.execute(f"DELETE FROM {SERVICE_TYPES_TABLE};")

    for idx, row in data.iterrows():
        insert_into_table(cursor, SERVICE_TYPES_TABLE, {SERVICE_TYPE_NAME: int(row[EXCEL_SERVICE_TYPE_NAME]),
                                                        SERVICE_TYPE_REQUIRED_LEVEL: int(
                                                            row[EXCEL_SERVICE_TYPE_REQUIRED_LEVEL])
                                                        })
    connection.commit()
    connection.close()
    return errors


def get_service_types_dict():
    """returns a dict of service_types and their required level."""
    out = {}
    connection = sqlite3.connect(DATABASE_PATH, detect_types=sqlite3.PARSE_DECLTYPES)
    cursor = connection.execute(f"SELECT {SERVICE_TYPE_NAME}, {SERVICE_TYPE_REQUIRED_LEVEL} "
                                f"from {SERVICE_TYPES_TABLE};")
    for row in cursor:  # each row corresponds to a psychologist
        service_type, required_level = row
        out[service_type] = required_level
    connection.close()
    return out


def get_conditions(conditions_file_path, clear_previous=False):
    """loads the conditions from the given file into the database"""
    errors = []
    try:
        data = pd.read_excel(conditions_file_path, engine='openpyxl')
    except (zipfile.BadZipfile, KeyError):
        errors.append("קובץ ההתניות אינו קובץ excel תקין.")
        return errors
    connection = sqlite3.connect(DATABASE_PATH, detect_types=sqlite3.PARSE_DECLTYPES)
    cursor = connection.cursor()

    # clear previous data
    if clear_previous:
        cursor.execute(f"DELETE FROM {CONDITIONS_TABLE};")

    for idx, row in data.iterrows():
        insert_into_table(cursor, CONDITIONS_TABLE, {CONDITION_NAME: row[EXCEL_CONDITION_NAME],
                                                     CONDITION_REQUIRED_LEVEL: row[EXCEL_CONDITION_REQUIRED_LEVEL]})
    connection.commit()
    connection.close()
    return errors



def get_psychologists(psychologists_file_path, week, clear_previous=False):
    """reads a file of psychologists into to database"""
    errors = []
    try:
        data = pd.read_excel(psychologists_file_path, engine='openpyxl')
    except (zipfile.BadZipfile, KeyError):
        errors.append("קובץ הפסיכולוגים אינו קובץ excel תקין.")
        return errors
    if not EXCEL_PSYCHOLOGIST_COLUMNS <= set(data.columns.to_list()):
        errors.append("קובץ הפסיכולוגים לא מכיל את העמודות הנכונות.")
        return errors

    connection = sqlite3.connect(DATABASE_PATH, detect_types=sqlite3.PARSE_DECLTYPES)
    cursor = connection.cursor()

    # clear previous data
    if clear_previous:
        clear_psychologists_table()

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
                              PSYCHOLOGIST_IS_NEW: int(row[EXCEL_PSYCHOLOGIST_NUM_OF_INTERVIEWS] < NUM_OF_INTERVIEWS),
                              PSYCHOLOGIST_WEEK: week
                          })
    connection.commit()
    connection.close()
    return errors


def get_required_level_by_service(service, service_types_dict):
    """
    given service, this function calculates the required level for a candidate with the given
    service
    :param service: an integer representing the service
    :param service_types_dict: a dict of pairs (service_type: required_level)
    :return: the required level for a candidate with the service
    """
    if service in service_types_dict:
        return service_types_dict[service]
    # TODO handle error
    return 0


def get_candidates(candidates_file_path, week, clear_previous=False):
    """loads candidates from file into the database"""
    errors = []
    try:
        data = pd.read_excel(candidates_file_path, engine='openpyxl')
    except (zipfile.BadZipfile, KeyError):
        errors.append("קובץ המועמדים אינו קובץ excel תקין.")
        return errors

    if not EXCEL_CANDIDATE_COLUMNS <= set(data.columns.to_list()):
        errors.append("קובץ המועמדים אינו תקין")
        return errors

    data[EXCEL_CANDIDATE_AUTHORITY] = data[EXCEL_CANDIDATE_AUTHORITY].fillna(method='ffill', axis=0)

    # clear previous data
    if clear_previous:
        connection = sqlite3.connect(DATABASE_PATH, detect_types=sqlite3.PARSE_DECLTYPES)
        cursor = connection.cursor()
        cursor.execute(f"DELETE FROM {CANDIDATES_TABLE} WHERE {CANDIDATE_WEEK}=(?);", (week,))
        connection.commit()
        connection.close()

    service_types = get_service_types_dict()
    for idx, row in data.iterrows():
        if not pd.isnull(row[EXCEL_CANDIDATE_PERSONAL_NUMBER]):
            cand = Candidate(
                first_name=row[EXCEL_CANDIDATE_FIRST_NAME],
                family_name=row[EXCEL_CANDIDATE_FAMILY_NAME],
                authority=row[EXCEL_CANDIDATE_AUTHORITY],
                date_of_birth=row[EXCEL_CANDIDATE_BIRTH_DATE].to_pydatetime(),
                gender=row[EXCEL_CANDIDATE_GENDER],
                id_number=row[EXCEL_CANDIDATE_ID_NUMBER],
                phone_number=row[EXCEL_CANDIDATE_PHONE_NUMBER],
                email_address=row[EXCEL_CANDIDATE_EMAIL_ADDRESS],
                notes=row[EXCEL_CANDIDATE_NOTES],
                course_type=row[EXCEL_CANDIDATE_COURSE_TYPE],
                service_type=row[EXCEL_CANDIDATE_SERVICE_TYPE],
                personal_number=row[EXCEL_CANDIDATE_PERSONAL_NUMBER],
                hebrew_level=row[EXCEL_CANDIDATE_HEBREW_LEVEL],
                study_years=row[EXCEL_CANDIDATE_STUDY_YEARS],
                psychotechnic_evaluation=row[EXCEL_CANDIDATE_PSYCHOTECHNIC_EVALUATION],
                required_level_for_interview=get_required_level_by_service(row[EXCEL_CANDIDATE_SERVICE_TYPE],
                                                                           service_types)
            )
            cand_errors = cand.errors_inserting()
            if cand_errors:
                errors.extend(cand_errors)
            else:
                add_single_candidate(cand, week)
    return errors


def clear_candidates_table(week=None):
    _clear_table(CANDIDATES_TABLE, week=week)


def clear_meetings_table(week=None):
    _clear_table(MEETINGS_TABLE, week=week)


def clear_psychologists_table(week=None):
    _clear_table(PSYCHOLOGISTS_TABLE, week=week)


def _clear_table(table_name, week=None):
    connection = sqlite3.connect(DATABASE_PATH, detect_types=sqlite3.PARSE_DECLTYPES)
    cursor = connection.cursor()
    if week is None:
        cursor.execute(f"DELETE FROM {table_name};")
    else:
        cursor.execute(f"DELETE FROM {table_name} WHERE {CANDIDATE_WEEK}=(?);", (week,))
    connection.commit()
    connection.close()


def add_single_candidate(candidate: Candidate, week):
    """adds a single candidate into the database"""
    connection = sqlite3.connect(DATABASE_PATH, detect_types=sqlite3.PARSE_DECLTYPES)
    cursor = connection.cursor()

    candidate_dict = {
        CANDIDATE_FIRST_NAME: candidate.first_name,
        CANDIDATE_FAMILY_NAME: candidate.family_name,
        CANDIDATE_AUTHORITY: candidate.authority,
        CANDIDATE_DATE_OF_BIRTH: candidate.date_of_birth,
        CANDIDATE_GENDER: candidate.gender,
        CANDIDATE_ID_NUMBER: candidate.id_number,
        CANDIDATE_PHONE_NUMBER: candidate.phone_number,
        CANDIDATE_EMAIL_ADDRESS: candidate.email_address,
        CANDIDATE_NOTES: candidate.notes,
        CANDIDATE_COURSE_TYPE: candidate.course_type,
        CANDIDATE_SERVICE_TYPE: candidate.service_type,
        CANDIDATE_PERSONAL_NUMBER: candidate.personal_number,
        CANDIDATE_HEBREW_LEVEL: candidate.hebrew_level,
        CANDIDATE_STUDY_YEARS: candidate.study_years,
        CANDIDATE_PSYCHOTECHNIC_EVALUATION: candidate.psychotechnic_evaluation,
        CANDIDATE_REQUIRED_LEVEL: candidate.required_level_for_interview,
        CANDIDATE_AVAILABLE_HOURS: candidate.available_hours_to_string(),
        CANDIDATE_WEEK: week
    }
    insert_into_table(cursor, CANDIDATES_TABLE,
                      candidate_dict)
    connection.commit()
    connection.close()


def remove_single_candidate(personal_number, week):
    connection = sqlite3.connect(DATABASE_PATH, detect_types=sqlite3.PARSE_DECLTYPES)
    cursor = connection.cursor()
    cursor.execute(f"""DELETE FROM {CANDIDATES_TABLE} WHERE {CANDIDATE_WEEK}=? and {CANDIDATE_PERSONAL_NUMBER}=?""",
                   (week, personal_number))
    connection.commit()
    connection.close()


def check_if_candidate_exists(personal_number, week):
    """checks if a candidate exists"""
    connection = sqlite3.connect(DATABASE_PATH, detect_types=sqlite3.PARSE_DECLTYPES)
    cursor = connection.cursor()
    c = cursor.execute(f"""SELECT EXISTS (SELECT 1 
                                          FROM {CANDIDATES_TABLE}
                                          WHERE {CANDIDATE_WEEK}=? and {CANDIDATE_PERSONAL_NUMBER}=?
                                          LIMIT 1)""", (week, personal_number)).fetchone()[0]
    if c:
        return True
    return False


def get_cond_of_cand(path_to_candidates_conditions_file, week):
    """loads conditions from a file into the database"""
    errors = []
    connection = sqlite3.connect(DATABASE_PATH, detect_types=sqlite3.PARSE_DECLTYPES)
    cursor = connection.execute(f"SELECT {CONDITION_NAME}, {CONDITION_REQUIRED_LEVEL} from {CONDITIONS_TABLE};")
    conditions = {}
    for row in cursor:
        condition, required_level = row
        conditions[condition] = required_level

    data: pd.DataFrame = pd.read_excel(path_to_candidates_conditions_file, engine='openpyxl')

    candidates_to_update = {}

    for cond, level in conditions.items():
        if cond not in data.columns:  # if the condition does not appear in the file
            continue
        for personal_number in data[cond]:  # iterate over all personal numbers with the condition
            if not pd.isnull(personal_number):
                candidates_to_update[personal_number] = max(level, candidates_to_update.get(personal_number, -inf))

    # updates database
    for personal_number, level in candidates_to_update.items():
        check_if_candidate_exists()
        cursor.execute(f"""
            UPDATE {CANDIDATES_TABLE}
            SET {CANDIDATE_REQUIRED_LEVEL}=?
            WHERE {CANDIDATE_PERSONAL_NUMBER} = ? AND {CANDIDATE_REQUIRED_LEVEL} < ? AND {CANDIDATE_WEEK} = ?;
        """, (level, personal_number, level, week))
    connection.commit()
    connection.close()
    return errors


def get_conditions_dict():
    """loads conditions from a file into the database"""
    connection = sqlite3.connect(DATABASE_PATH, detect_types=sqlite3.PARSE_DECLTYPES)
    cursor = connection.execute(f"SELECT {CONDITION_NAME}, {CONDITION_REQUIRED_LEVEL} from {CONDITIONS_TABLE};")
    conditions = {}
    for row in cursor:
        condition, required_level = row
        conditions[condition] = required_level
    connection.commit()
    connection.close()
    return conditions


def get_working_time(path_to_working_hours_file):
    """loads working times of psychologists into the database"""
    errors = []
    try:
        data: pd.DataFrame = pd.read_excel(path_to_working_hours_file, engine='openpyxl')
    except (zipfile.BadZipfile, KeyError):
        errors.append("קובץ שעות העבודה של הפסיכולוגים אינו קובץ excel תקין.")
        return errors
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

    connection = sqlite3.connect(DATABASE_PATH, detect_types=sqlite3.PARSE_DECLTYPES)
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
    return errors


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


def get_psychologists_list(week):
    """
    :return: a list of psychologists
    """
    connection = sqlite3.connect(DATABASE_PATH, detect_types=sqlite3.PARSE_DECLTYPES)
    cursor = connection.execute(f"SELECT {PSYCHOLOGIST_FIRST_NAME}, {PSYCHOLOGIST_FAMILY_NAME}, "
                                f"{PSYCHOLOGIST_ID_NUMBER}, {PSYCHOLOGIST_NUM_OF_INTERVIEWS}, {PSYCHOLOGIST_LEVEL}, "
                                f"{PSYCHOLOGIST_AVAILABLE_HOURS} from {PSYCHOLOGISTS_TABLE} "
                                f"WHERE {PSYCHOLOGIST_WEEK}=?", (week,))
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


def get_candidates_list(week):
    """
    :return: a dictionary of candidates and their info
    """
    connection = sqlite3.connect(DATABASE_PATH, detect_types=sqlite3.PARSE_DECLTYPES)
    cursor = connection.execute(f"SELECT {CANDIDATE_PERSONAL_NUMBER}, {CANDIDATE_FIRST_NAME}, {CANDIDATE_FAMILY_NAME}, "
                                f"{CANDIDATE_NOTES}, {CANDIDATE_PHONE_NUMBER}, {CANDIDATE_PSYCHOTECHNIC_EVALUATION}, "
                                f"{CANDIDATE_STUDY_YEARS}, {CANDIDATE_HEBREW_LEVEL}, {CANDIDATE_EMAIL_ADDRESS}, "
                                f"{CANDIDATE_AUTHORITY}, {CANDIDATE_REQUIRED_LEVEL}, {CANDIDATE_AVAILABLE_HOURS},"
                                f"{CANDIDATE_SERVICE_TYPE}, {CANDIDATE_ID_NUMBER}, {CANDIDATE_DATE_OF_BIRTH}, "
                                f"{CANDIDATE_GENDER}, {CANDIDATE_COURSE_TYPE}"
                                f" from {CANDIDATES_TABLE} WHERE {CANDIDATE_WEEK}=?;", (week,))
    candidates = []
    for row in cursor:  # each row corresponds to a psychologist
        # extracting info from row
        personal_number, first_name, family_name, notes, phone_number, psychotechnic_eval, \
        study_years, hebrew, email, authority, required_level, available_hours_raw, service_type, id_number, \
        date_of_birth, gender, course_type = row
        # parse available_hours
        available_hours = parse_times_list(available_hours_raw)

        # inserting info into candidate class
        candidates.append(Candidate(
            first_name=first_name,
            family_name=family_name,
            personal_number=personal_number,
            id_number=id_number,
            notes=notes,
            phone_number=phone_number,
            study_years=study_years,
            hebrew_level=hebrew,
            email_address=email,
            authority=authority,
            required_level_for_interview=required_level,
            psychotechnic_evaluation=psychotechnic_eval,
            service_type=service_type,
            available_hours=available_hours,
            date_of_birth=date_of_birth,
            gender=gender,
            course_type=course_type
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


def get_candidates_available_hours(available_hours_file, week):
    """loads available times of candidates into the database"""
    errors = []
    try:
        data: pd.DataFrame = pd.read_excel(available_hours_file, header=None, index_col=0, engine='openpyxl').transpose()
    except (zipfile.BadZipfile, KeyError):
        errors.append("קובץ השעות הזמינות של המועמדים אינו קובץ excel תקין.")
        return errors
    connection = sqlite3.connect(DATABASE_PATH, detect_types=sqlite3.PARSE_DECLTYPES)
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
        if not check_if_candidate_exists(candidate_personal_number, week):
            errors.append("המועמד עם המספר האישי {value} לא קיים.".format(value=candidate_personal_number))
        cursor.execute(f"""
            UPDATE {CANDIDATES_TABLE}
            SET {CANDIDATE_AVAILABLE_HOURS} = ?
            WHERE {CANDIDATE_PERSONAL_NUMBER} = ?
            AND {CANDIDATE_WEEK} = ?;
        """, (times, candidate_personal_number, week))
    connection.commit()
    connection.close()
    return errors


if __name__ == "__main__":
    initialize_database_tables()
    get_conditions("../examples/conditions.xlsx")
    print(get_conditions_dict())

    w = datetime.datetime(2022, 1, 1)
    w1 = datetime.datetime(year=2022, month=1, day=1)
    print(get_candidates("../examples/candidates.xlsx", week=w1, clear_previous=True))
    print(get_candidates("/home/ez/Code/calander_optimization/server/requirements.txt", week=w1, clear_previous=True))
    clear_candidates_table(w1)
    print(get_psychologists("../examples/psychologists.xlsx", week=w1))
    cand = Candidate(
        first_name="a",
        family_name="b",
        date_of_birth=w1,
        gender=None,
        personal_number=None,
        notes=None,
        phone_number="d",
        study_years="4",
        hebrew_level=None,
        email_address="e",
        authority="asd",
        required_level_for_interview="d",
        psychotechnic_evaluation="f",
        id_number="g",
        service_type="h",
        course_type="e"
    )
    print(cand.errors_inserting())
    print(cand.non_critical_errors())
    add_single_candidate(cand, w1)
    get_candidates_list(w1)