from load_to_database import *
import make_schedule as ms
import extra_funcs
import os
import sys
import logging


def loadFiles():
    initialize_database_tables()
    get_conditions("conditions.xlsx")
    get_candidates("candidates.xlsx", 0)
    get_cond_of_cand("candidates_conditions.xlsx")
    get_psychologists("psychologists.xlsx", 0)
    get_working_time("working_hours.xlsx")
    get_candidates_available_hours("candidates_available_hours.xlsx", 0)
    schedule = ms.make_schedule(get_candidates_list(0), get_psychologists_list(0))
    return ms.to_excel(schedule, 0) # 0 - today



