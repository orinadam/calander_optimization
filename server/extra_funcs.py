import make_schedule as ms
import json


def luz_authority(schedule, authority):
    """הפונקציה מקבלת את המערכת שעות ואת הסמכות
    ומחזירה כפלט את המערכת שעות של הסכמות הרצויה
    :param schedule: רשימה של פגישות
    :return: רשימה של פגישות של אותה סמכות
    """
    authority_list = [["סמכות"], ["שם פסיכולוג", "יום", "שעה", "שם מועמד"], []]
    for meeting in schedule:  # every meeting is [name_psycho, day, time, name_candidate]
        if meeting[3].authority == authority:
            meeting[2] = ms.time_float_to_string(meeting)
            authority_list.append(meeting)

    return json.dumps(authority_list)


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
        if meeting[3].personal_number == personal_number:
            cur_meeting = meeting
            break

    for meeting in schedule:
        if meeting[3].required_level_for_interview <= cur_meeting[0].level:
            for available_hour in meeting[3].available_hours[cur_meeting[1]]:
                if int(cur_meeting[2]) == available_hour:

                    if cur_meeting[3].required_level_for_interview <= meeting[0].level:
                        for available_hour1 in cur_meeting[3].available_hours1[meeting[1]]:
                            if int(cur_meeting[2]) == available_hour1:
                                candidates_available.append(meeting)

    return json.dumps(candidates_available)


def same_psychologist(name_psycho, schedule):
    """ הפונקציה מקבלת שם פסיכולוג (קלט משתמש) ומערכת פגישות כללית
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