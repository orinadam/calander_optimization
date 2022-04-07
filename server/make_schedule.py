from load_to_database import Candidate, PsychoInfo, DAYS_OF_THE_WEEK, IsInSchedule
import pandas as pd
import datetime
import sys
PSYCH_NUMBER_OF_LEVELS = 6
ASSIGNED_ERR_CODE = 0
ASSIGNED_BUT_NOT_ADJUST = 1
NOT_ASSIGNED = 2


def make_schedule(candidates: list, psychologists: list) -> list:
    """
    :param candidates: list of candidates :param psychologists: list of psychologists :return: A list of lists,
    in this format: [[psychologist: PsyInfo, day of meeting: int, time of meeting: float, candidate: Candidate,
    adjusted_for_candidate_time: bool] ...] :param errors: errors occurred while loading data. if empty,
    no errors occurred.
    """
    return_list = []
    print("A", file=sys.stderr)
    psychologists = parse_psychologists(psychologists)
    print("B", file=sys.stderr)
    candidates = sort_candidates(candidates)
    print("C", file=sys.stderr)
    for candidate in candidates:
        temp = assign(candidate, psychologists, True)  # try to assign candidate, temp == False if failed
        if not temp:
            print('Could not assign the candidate {} {} with the current time table'.format(candidate.first_name,
                                                                                            candidate.family_name))
            candidate.in_schedule = IsInSchedule.SUCCESS_NO_CONDS.value
            temp = assign(candidate, psychologists, False)  # try to assign candidate, temp == False if failed
            if not temp:
                print('Could not assign the candidate {} {} at all'.format(candidate.first_name,
                                                                           candidate.family_name))
                candidate.in_schedule = IsInSchedule.FAILED.value
                temp = [None, None, None, candidate, NOT_ASSIGNED]
        else:
            candidate.in_schedule = IsInSchedule.SUCCESS_WITH_CONDS.value
        return_list.append(temp)  # add meeting to list
        # TODO: add all meetings that wasn't filled, will be used for adding a single candidate after creating schedule

    return return_list


def sort_candidates(candidates: list) -> list:
    """
    :param candidates: list of candidates
    :return: list of candidates sorted from least hours available to most.
    """
    lst = []
    for candidate in candidates:
        lst.append([candidate,
                    sum([len(i) for i in candidate.available_hours])])  # candidate and number of his available hours
    return [i[0] for i in sorted(lst, reverse=True, key=lambda x: x[1])]


def assign(candidate: Candidate, psychologists: list, adjust_for_candidate_time: bool):
    """
    :param candidate: candidate to assign
    :param psychologists: list of psychologists
    :param adjust_for_candidate_time: should the function apply the candidate's available time
    :return: list with the meeting information if the candidate was assigned successfully, False otherwise.
    """
    err_code = ASSIGNED_ERR_CODE  # if we adjust for candidate time, err_code = 0, if not = 1, if not assigned = 2.
    if not adjust_for_candidate_time:
        err_code = ASSIGNED_BUT_NOT_ADJUST
    available_times = calculate_available_times(candidate)
    if candidate.specific_psychologist is not None:
        pass  # TODO implement specific psychologist condition (not for MVP)
    if candidate.required_level_for_interview is None or candidate.required_level_for_interview < 3:
        for psy_list in psychologists[
                        0:PSYCH_NUMBER_OF_LEVELS // 2 + 1]:  # check the first half of the list, consisting of low-level psychologists.
            for psy in psy_list:
                day, time = try_to_assign(available_times, psy, adjust_for_candidate_time)
                if day is not None and time is not None:  # if the function assigned a meeting successfully.
                    psy.used_hours.append([day, psy.available_hours[day].pop(
                        psy.available_hours[day].index(time))])  # add chosen hour to used hours list.
                    return [psy, day, time, candidate, err_code]
    for psy_list in psychologists[
                    PSYCH_NUMBER_OF_LEVELS // 2 + 1:]:  # check the other half of the list, consisting of high-level psychologists
        for psy in sorted(psy_list, key=lambda k: k.num_of_interviews,
                          reverse=True):  # TODO get a better way to sort the psychologists.
            day, time = try_to_assign(available_times, psy, adjust_for_candidate_time)
            if day is not None and time is not None:  # if the function assigned a meeting successfully.
                psy.used_hours.append([day, psy.available_hours[day].pop(
                    psy.available_hours[day].index(time))])  # add chosen hour to used hours list.
                return [psy, day, time, candidate, err_code]
    return False


def parse_psychologists(psychologists: list) -> list:
    """
    :param psychologists: list of psychologist.
    :return: list with 6 lists inside, one for each of the psychologists levels.
    """
    return_list = [[] for i in range(PSYCH_NUMBER_OF_LEVELS)]
    for psy in psychologists:
        return_list[psy.level - 1].append(psy)
    return return_list


def calculate_available_times(candidate: Candidate) -> list:
    """
    :param candidate: A candidate.
    :return: list with a range of available hours.
    :Output Example: [[(8, 10), (12, 12)], [(8, 10), (13, 15), (17, 18)], [(8, 10)], [(8, 10)], [(8, 10)]]
    :Example Explanation: Tuesday - from 8 to 10 (including 10) and from 12 to 12 (including 12).
    """
    return_list = []
    for day in candidate.available_hours:
        temp = []
        start = 0
        last = 0
        for idx, hour in enumerate(day):
            if start == 0:
                start = hour
            elif hour - last > 1:  # if a gap has been found between the available hours.
                if idx == len(day) - 1:  # if this is the last hour
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
    """
    :param candidate_times: list of available times from calculate_available_times
    :param psychologist: Chosen psychologist for the candidate.
    :param adjust_for_candidate_time: should the function take the candidate's hours into account
    :return: chosen day and hour if a meeting was successfully assigned, (None, None) otherwise.
    """
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


def time_float_to_string(meeting) -> str:
    """
    :param meeting: list with meeting info.
    :return: hour converted from float to minutes. Example: 10.25 -> 10:15
    """
    fix_time = str(datetime.timedelta(hours=meeting[2]))[:-3]
    return fix_time


def to_excel(list_schedule, day_index):
    """
    outputs the schedule to a given day.
    :param list_schedule: built schedule for the entire week.
    :param day_index: index of the day, 0=Tuesday.
    :return: None
    """
    table_for_excel = [("פסיכולוג","יום", "שעת ראיון", "שם פרטי", "שם משפחה", "מ.א", "הערות", "טלפון", "דפר", "שנו\"ל", "עברית", "מייל", "code")]
    new_list_schedule = []

    for meeting in list_schedule:
        if meeting[1] == day_index:
            meeting[2] = time_float_to_string(meeting)
            new_list_schedule.append(meeting)


    for info_schedule in new_list_schedule:
        list_to_table = [info_schedule[0].first_name, DAYS_OF_THE_WEEK[info_schedule[1]] ,info_schedule[2], info_schedule[3].first_name,
                         info_schedule[3].family_name, info_schedule[3].personal_number, info_schedule[3].notes,
                         info_schedule[3].phone_number, info_schedule[3].psychotechnic_evaluation,
                         info_schedule[3].study_years, info_schedule[3].hebrew_level, info_schedule[3].email_address, info_schedule[4]]

        table_for_excel.append(list_to_table)

        pd.DataFrame(table_for_excel).to_excel(r'{}Schedule.xlsx'.format(DAYS_OF_THE_WEEK[day_index]), header=False,
                                               index=False)
    return table_for_excel
