import sys, os, django
from django.core import serializers
sys.path.append("../nycCivilServiceJobs") #here store is root folder(means parent).
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nycCivilServiceJobs.settings")
django.setup()

import requests
import json
import pandas as pd
from sodapy import Socrata
import csv
from examresults.models import ExamResultsActive
from examresults.models import ExamResultsTerminated
from django.utils import timezone
import datetime


def get_exam_result_active():
    client = Socrata("data.cityofnewyork.us",
                     "m7QHRP2U6tqRR7XCge8TzIRUW",
                     username="nycCivilService.csgy6063@gmail.com",
                     password="team4Pythonpir@tes")
    results = client.get("vx8i-nprf")

    return results


def get_exam_result_terminated():
    client = Socrata("data.cityofnewyork.us",
                     "m7QHRP2U6tqRR7XCge8TzIRUW",
                     username="nycCivilService.csgy6063@gmail.com",
                     password="team4Pythonpir@tes")
    results = client.get("qu8g-sxqf", select = 'distinct exam_no')

    return results

def save_exam_result_active():
    exam_result_list = get_exam_result_active()
    exam_result_list_df = pd.DataFrame.from_records(exam_result_list)
    for index, row in exam_result_list_df.iterrows():
        try:
            #print(row) 
            # print(row['exam_no']) 
            exam_result_active = ExamResultsActive(exam_number=row['exam_no'],
                                list_number=row['list_no'],
                                first_name=row['first_name'],
                                last_name=row['last_name'],
                                middle_initial = row['mi'],
                                adjust_final_average=row['adj_fa'],
                                list_title_code=(row['list_title_code'] if 'list_title_code' in row.index and not is_nan(row['list_title_code']) else None),
                                list_title_desc=(row['list_title_desc'] if 'list_title_desc' in row.index and not is_nan(row['list_title_desc']) else None),
                                group_number=row['group_no'],
                                list_agency_code_promo=row['list_agency_code'],
                                list_agency_code_promo_desc=row['list_agency_desc'],
                                list_div_code_promo= (row['list_div_code'] if 'list_div_code' in row.index and not is_nan(row['list_div_code']) else None),
                                anniversary_date=getAwareDate(row['anniversary_date']),
                                extension_date=(getAwareDate(row['extension_date']) if 'extension_date' in row.index and not is_nan(row['extension_date']) else None),
                                veteran_credit= (row['veteran_credit'] if 'veteran_credit' in row.index and not is_nan(row['veteran_credit']) else None),
                                parent_legacy_credit= (row['parent_lgy_credit'] if 'parent_lgy_credit' in row.index and not is_nan(row['parent_lgy_credit']) else None),
                                sibling_legacy_credit=(row['sibling_lgy_credit'] if 'sibling_lgy_credit' in row.index and not is_nan(row['sibling_lgy_credit']) else None),
                                residency_credit= (row['residency_credit'] if 'residency_credit' in row.index and not is_nan(row['residency_credit']) else None))
            exam_result_active.save()
        except Exception as e:
            print('Error',e)
            # break
    return



def save_exam_result_terminated():
    exam_result_list = get_exam_result_terminated()
    exam_result_list_df = pd.DataFrame.from_records(exam_result_list)
    for index, row in exam_result_list_df.iterrows():
        try:
            print(row['exam_no'])
           
            exam_result_terminated = ExamResultsTerminated(exam_number=row['exam_no'],
                                list_title_code=None,
                                list_title_desc=None)
                                
            exam_result_terminated.save()
        except Exception as e:
            #print()
            print('Error',e)
            # break
    return

def is_nan(x):
    return (x != x)

def getAwareDate(inputDate):
    #print(inputDate)
    if(is_nan(inputDate)):
        #print('if')
        return 
    tz=timezone.get_default_timezone()
    aware_datetime = datetime.datetime.fromisoformat(inputDate)
    date_aware=aware_datetime.replace(tzinfo=tz)
    return date_aware

def convertDateFormat(inputDate):
    #print(inputDate)
    if(is_nan(inputDate)):
        #print('if')
        return None
    y= datetime.datetime.strptime(inputDate, '%d-%b-%Y').strftime("%Y-%m-%d")
    return y


if __name__ == '__main__':
    save_exam_result_active()
    save_exam_result_terminated()