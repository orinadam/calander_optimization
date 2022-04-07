from load_to_database import *
import make_schedule as ms
import extra_funcs
import os
import sys
import logging




def loadFiles():
    errors = []
    initialize_database_tables()
    errors += get_conditions("conditions.xlsx")
    errors += get_candidates("candidates.xlsx",0)
    errors += get_cond_of_cand("candidates_conditions.xlsx", 0)
    errors += get_psychologists("psychologists.xlsx", 0)
    errors += get_working_time("working_hours.xlsx")
    errors += get_candidates_available_hours("candidates_available_hours.xlsx", 0)
    if errors == []:
        return [], errors
    schedule = ms.make_schedule(get_candidates_list(0), get_psychologists_list(0))
    return ms.to_excel(schedule, 0), [] # 0 - today
