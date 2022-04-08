import make_schedule as ms
import json


def luz_authority(schedule, authority):
    """הפונקציה מקבלת את המערכת שעות ואת הסמכות
    ומחזירה כפלט את המערכת שעות של הסכמות הרצויה
    :param schedule: רשימה של פגישות
    :return: רשימה של פגישות של אותה סמכות
    """
    # authority_list = [["סמכות"], ["שם פסיכולוג", "יום", "שעה", "שם מועמד"], []]
    authority_list = [["שם פסיכולוג", "יום", "שעה", "שם מועמד", "code"]]

    for meeting in schedule:  # every meeting is [name_psycho, day, time, name_candidate, error code]
        if meeting[6] == authority:
            # meeting[2] = ms.time_float_to_string(meeting)
            authority_list.append(meeting)

    return authority_list



def candidates_available_for_exchange(personal_number, schedule):
    """הפונקציה מקבלת מספר אישי ואת
    המערכת שעות של השבוע ומחזירה בתור פלט
    את הפגישות שניתן להחליף איתן
    :param personal_number: מספר אישי של המועמד
    :param schedule: רשימת הפגישות
    :return: הפגישות שאיתן ניתן להחליף
    """
    candidates_available = [["שם פסיכולוג", "יום", "שעה", "שם מועמד"]]

    for meeting in schedule:
        if meeting[4] == personal_number:
            cur_meeting = meeting
            break
    print(cur_meeting)
    for meeting in schedule:
        if meeting[5] <= cur_meeting[1][5]:
            for available_hour in meeting[cur_meeting[1][1]]:
                if int(cur_meeting[1][2]) == available_hour:

                    if cur_meeting[5] <= meeting[5]:
                        for available_hour1 in cur_meeting[meeting[1][1]]:
                            if int(cur_meeting[1]) == available_hour1:
                                candidates_available.append(meeting)

    return candidates_available


def same_psychologist(name_psycho, schedule):
    """ הפונקציה מקבלת שם פסיכולוג (קלט משתמש)      פגישות כללית
    ומחזירה את המערכת של אותו הפסיכולוג
    :param name_psycho: שם פסיכולוג
    :param schedule: לוז כללי
    :return: לוז של אותו פסיכולוג
    """
    schedule_psychologist = [["שם פסיכולוג", "יום", "שעה", "שם מועמד"]]
    for meeting in schedule:
        print(meeting[0])
        if name_psycho == meeting[0]:  # TODO: לבדוק איך השם של הפסיכולוג מופיע בכל פגישה
            schedule_psychologist.append(meeting)
    return schedule_psychologist


def specific_candidate(first_name_candidate, family_name_candidate, schedule):
    """הפונקציה מקבלת שם פרטי + משפחה, רשימת פגישות ומחזירה
    את הפגישה המתאימה
    :param first_name_candidate: שם פרטי שמתקבל כקלט
    :param family_name_candidate: שם משפחה שמתקבל כקלט
    :param schedule: רשימת הפגישות
    :return: הפגישה המתאימה
    """
    for meeting in schedule:
        if meeting[3] == first_name_candidate:
            if meeting[4] == family_name_candidate:
                return meeting


def filter_by_day(schedule, day):
    authority_list = [["שם פסיכולוג", "יום", "שעה", "שם מועמד", "קוד שגיאה"]]
    for meeting in schedule:  # every meeting is [name_psycho, day, time, name_candidate]
        if meeting[1] == day:
            authority_list.append(meeting)
    return authority_list
