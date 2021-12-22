from load_to_database import Candidate, PsychoInfo, DAYS_OF_THE_WEEK
import pandas as pd
import datetime


def make_schedule(candidates: list, psychologists: list) -> list:
    return_list = []
    psychologists = parse_psychologists(psychologists)
    candidates = sort_candidates(candidates)
    for candidate in candidates:
        temp = assign(candidate, psychologists, True)
        if not temp:
            print('could not assign the candidate {} {} with the current time table'.format(candidate.first_name,
                                                                                            candidate.family_name))
            temp = assign(candidate, psychologists, False)
        return_list.append(temp)

    return return_list


def sort_candidates(candidates: list) -> list:
    l = []
    for candidate in candidates:
        l.append([candidate, sum([len(i) for i in candidate.available_hours])])
    return [i[0] for i in sorted(l, reverse=True, key=lambda x: x[1])]


def assign(candidate, psychologists, adjust_for_candidate_time):
    available_times = calculate_available_times(candidate)
    if candidate.specific_psychologist is not None:
        pass  # TODO implement specific psychologist condition
    if candidate.required_level_for_interview is None or candidate.required_level_for_interview < 3:
        for psy_list in psychologists[0:4]:
            for psy in psy_list:
                day, time = try_to_assign(available_times, psy, adjust_for_candidate_time)
                if day is not None and time is not None:
                    psy.used_hours.append([day, psy.available_hours[day].pop(psy.available_hours[day].index(time))])
                    return [psy, day, time, candidate]
    for psy_list in psychologists[4:]:
        for psy in sorted(psy_list, key=lambda k: k.num_of_interviews, reverse=True):
            day, time = try_to_assign(available_times, psy, adjust_for_candidate_time)
            if day is not None and time is not None:
                return [psy, day, time, candidate]
    return False


def parse_psychologists(psychologists: list) -> list:
    return_list = [[] for i in range(6)]  # number of levels of psychologists
    for psy in psychologists:
        return_list[psy.level - 1].append(psy)
    return return_list


def calculate_available_times(candidate: Candidate) -> list:
    return_list = []
    for day in candidate.available_hours:
        temp = []
        start = 0
        last = 0
        for idx, hour in enumerate(day):
            if start == 0:
                start = hour
            elif hour - last > 1:
                if idx == len(day) - 1:
                    temp.append((start, last))
                    temp.append((hour, hour))
                else:
                    temp.append((start, last))
                    start = hour
            elif idx == len(day) - 1:
                temp.append((start, hour))
            last = hour
        return_list.append(temp)
    return return_list


def try_to_assign(candidate_times: list, psychologist: PsychoInfo, adjust_for_candidate_time: bool):
    day = -1
    for idx, day_p in enumerate(psychologist.available_hours):
        day += 1
        for hour in day_p:
            if not adjust_for_candidate_time:
                return day, hour
            for times in candidate_times[idx]:
                if times[0] <= hour <= times[1] + 1:
                    return day, hour
    return None, None


def time_float_to_string(meeting):
    fix_time = str(datetime.timedelta(hours=meeting[2]))[:-3]
    return fix_time


def to_excel(list_schedule, day_index):
    table_for_excel = [
        ("פסיכולוג", "שעת ראיון", "שם פרטי", "שם משפחה", "מ.א", "הערות", "טלפון", "דפר", "שנו\"ל", "עברית", "מייל")]
    new_list_schedule = []

    for meeting in list_schedule:
        if meeting[1] == day_index:
            meeting[2] = time_float_to_string(meeting)
            new_list_schedule.append(meeting)

    for info_schedule in new_list_schedule:
        list_to_table = [info_schedule[0].first_name, info_schedule[2], info_schedule[3].first_name,
                         info_schedule[3].family_name, info_schedule[3].personal_number, info_schedule[3].notes,
                         info_schedule[3].phone_number, info_schedule[3].psychotechnic_evaluation,
                         info_schedule[3].study_years, info_schedule[3].hebrew_level, info_schedule[3].email_address]

        table_for_excel.append(list_to_table)
    print(table_for_excel)
    return table_for_excel


       # pd.DataFrame(table_for_excel).to_excel(r'{}Schedule.xlsx'.format(DAYS_OF_THE_WEEK[day_index]), header=False,
                #                               index=False)
