from enum import Enum

DAYS_OF_THE_WEEK = (
    "שלישי",
    "רביעי",
    "חמישי",
    "ראשון",
    "שני"
)

# working day hours
EARLIEST_HOUR = 8
LATEST_HOUR = 20  # inclusive!

# the required number of interviews so that a psychologist will not be considered new
NUM_OF_INTERVIEWS = 50

CANDIDATES_TABLE = "Candidates"
CANDIDATE_AUTHORITY = "authority"
CANDIDATE_FIRST_NAME = "first_name"
CANDIDATE_FAMILY_NAME = "family_name"
CANDIDATE_GENDER = "gender"
CANDIDATE_DATE_OF_BIRTH = "date_of_birth"
CANDIDATE_ID_NUMBER = "id_number"
CANDIDATE_PERSONAL_NUMBER = "personal_number"
CANDIDATE_PHONE_NUMBER = "phone_number"
CANDIDATE_COURSE_TYPE = "course_type"
CANDIDATE_PSYCHOTECHNIC_EVALUATION = "psychotechnic_evaluation"
CANDIDATE_STUDY_YEARS = "study_years"
CANDIDATE_HEBREW_LEVEL = "hebrew_level"
CANDIDATE_NOTES = "notes"
CANDIDATE_REQUIRED_LEVEL = "required_level"
CANDIDATE_EMAIL_ADDRESS = "email_address"
CANDIDATE_AVAILABLE_HOURS = "available_hours"
CANDIDATE_SERVICE_TYPE = "service_type"
CANDIDATE_WEEK = "week"

EXCEL_CANDIDATE_SUBMISSION_DATE = "Test Date"
EXCEL_CANDIDATE_AUTHORITY = "סמכות"
EXCEL_CANDIDATE_FIRST_NAME = "First Name"
EXCEL_CANDIDATE_FAMILY_NAME = "Last Name"
EXCEL_CANDIDATE_GENDER = "Gender"
EXCEL_CANDIDATE_BIRTH_DATE = "Birth Date"
EXCEL_CANDIDATE_ID_NUMBER = "ID"
EXCEL_CANDIDATE_PHONE_NUMBER = "טלפון"
EXCEL_CANDIDATE_COURSE_TYPE = 'סוג קק"צ'
EXCEL_CANDIDATE_SERVICE_TYPE = "סוג שירות"
EXCEL_CANDIDATE_NOTES = "הערות"
EXCEL_CANDIDATE_EMAIL_ADDRESS = "אימייל"
EXCEL_CANDIDATE_PERSONAL_NUMBER = "NID"
EXCEL_CANDIDATE_HEBREW_LEVEL = "עברית"
EXCEL_CANDIDATE_STUDY_YEARS = 'שנו"ל'
EXCEL_CANDIDATE_PSYCHOTECHNIC_EVALUATION = 'דפ"ר'

EXCEL_CANDIDATE_AVAILABLE_HOUR_PERSONAL_NUMBER = "מספר אישי"

CONDITIONS_TABLE = "Conditions"
CONDITION_NAME = "name"
CONDITION_REQUIRED_LEVEL = "required_level"

EXCEL_CONDITION_NAME = "התניות"
EXCEL_CONDITION_REQUIRED_LEVEL = "דרג נדרש"

SERVICE_TYPES_TABLE = "ServiceTypes"
SERVICE_TYPE_NAME = "name"
SERVICE_TYPE_REQUIRED_LEVEL = "required_level"

EXCEL_SERVICE_TYPE_NAME = "סוג שירות"
EXCEL_SERVICE_TYPE_REQUIRED_LEVEL = "דרג נדרש"

PSYCHOLOGISTS_TABLE = "Psychologists"
PSYCHOLOGIST_FIRST_NAME = "first_name"
PSYCHOLOGIST_FAMILY_NAME = "family_name"
PSYCHOLOGIST_ID_NUMBER = "id_number"
PSYCHOLOGIST_LEVEL = "level"
PSYCHOLOGIST_IS_NEW = "is_new"
PSYCHOLOGIST_NUM_OF_INTERVIEWS = "num_of_interviews"
PSYCHOLOGIST_AVAILABLE_HOURS = "available_hours"
PSYCHOLOGIST_WEEK = "week"

EXCEL_WORKING_HOURS_ID_NUMBER = "תעודת זהות"

EXCEL_PSYCHOLOGIST_FIRST_NAME = "שם פרטי"
EXCEL_PSYCHOLOGIST_FAMILY_NAME = "שם משפחה"
EXCEL_PSYCHOLOGIST_ID_NUMBER = "תעודת זהות"
EXCEL_PSYCHOLOGIST_LEVEL = "דרגה"
EXCEL_PSYCHOLOGIST_NUM_OF_INTERVIEWS = "מספר ריאיונות"

MEETINGS_TABLE = "Meetings"
MEETING_PSYCHOLOGIST_ID = "psychologist_id"
MEETING_CANDIDATE_NUMBER = "candidate_personal_number"
MEETING_DAY = "day"
MEETING_HOUR = "hour"
MEETING_WEEK = "week"

FORMS_SEPARATOR = ", "


class IsInSchedule(Enum):
    SUCCESS_WITH_CONDS = 0  # the candidate was listed in the schedule within his available_hours
    SUCCESS_NO_CONDS = 1    # the candidate was listed in the schedule, but not within his available_hours
    FAILED = 2              # the candidate was not listed in the schedule because insufficient amount of psychologist hours
