from load_to_database import *
import make_schedule as ms
import extra_funcs


def main():
    initialize_database_tables()
    # get_conditions(os.path.join("examples", "conditions.xlsx"))
    # get_candidates(os.path.join("examples", "candidates.xlsx"))
    get_cond_of_cand(os.path.join("examples", "test_case_3.xlsx"))
    # get_psychologists(os.path.join("examples", "psychologists.xlsx"))
    get_working_time(os.path.join("examples", "psychologists_working_hours_test_case.xlsx"))
    # get_candidates_available_hours(os.path.join("examples", "candidates_available_hours.xlsx"))

    schedule = ms.make_schedule(get_candidates_list(), get_psychologists_list())
    for i in schedule:
        print(i[0].first_name, i[1], i[2], i[3].first_name, i[0].level, i[3].required_level_for_interview)
    for i in range(len(DAYS_OF_THE_WEEK)):
        ms.to_excel(schedule, i)

    # authority = input("authority:")
    # print(extra_funcs.luz_authority(schedule, authority))



if __name__ == '__main__':
    main()
