import make_schedule as ms


def luz_authority(schedule, authority):
    """

    :param schedule: רשימה של פגישות
    :return: רשימה של פגישות של אותה סמכות
    """
    authority_list = []
    for meeting in schedule:
        if meeting[3].authority == authority:
            meeting[2] = ms.time_float_to_string(meeting)
            authority_list.append(meeting)

    return authority_list
