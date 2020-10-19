import sys, os, django
from django.core import serializers
sys.path.append("../nycCivilServiceJobs")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nycCivilServiceJobs.settings")
django.setup()

import requests
import json
import pandas as pd
from sodapy import Socrata
import csv
import numpy as np
from examresults.models import ExamResultsActive
from examresults.models import ExamResultsTerminated
from django.utils import timezone
import datetime


def get_exam_result_active():
    client = Socrata("data.cityofnewyork.us",
                     "m7QHRP2U6tqRR7XCge8TzIRUW",
                     username="nycCivilService.csgy6063@gmail.com",
                     password="team4Pythonpir@tes",timeout=30)
    record_count = client.get("vx8i-nprf",select="COUNT(*)")[0]['COUNT']
    results = client.get("vx8i-nprf",limit=record_count)

    return results


def get_exam_result_terminated():
    client = Socrata("data.cityofnewyork.us",
                     "m7QHRP2U6tqRR7XCge8TzIRUW",
                     username="nycCivilService.csgy6063@gmail.com",
                     password="team4Pythonpir@tes",timeout=30)
    record_count = client.get("qu8g-sxqf",select="COUNT(*)")[0]['COUNT']
    results = client.get("qu8g-sxqf", select = 'distinct exam_no,list_title_code,list_title_desc',limit=record_count)

    return results

def save_exam_result_active():
    ExamResultsActive.objects.all().delete()
    print("Deleted Previous Entries")
    exam_result_list = get_exam_result_active()
    exam_result_list_df = pd.DataFrame.from_records(exam_result_list)
    exam_result_list_df= exam_result_list_df.where(exam_result_list_df.notnull(),None)

    entries = []
    for index, row in exam_result_list_df.iterrows():
        try:
            entries.append(ExamResultsActive(exam_number=row['exam_no'],
                                list_number=row['list_no'],
                                first_name=row['first_name'],
                                last_name=row['last_name'],
                                middle_initial = row['mi'],
                                adjust_final_average=row['adj_fa'],
                                list_title_code=row['list_title_code'],
                                list_title_desc=row['list_title_desc'],
                                group_number=row['group_no'],
                                list_agency_code_promo=row['list_agency_code'],
                                list_agency_code_promo_desc=row['list_agency_desc'],
                                list_div_code_promo= row['list_div_code'] ,                               anniversary_date=getAwareDate(row['anniversary_date']),
                                extension_date=getAwareDate(row['extension_date']),
                                veteran_credit= row['veteran_credit'],
                                parent_legacy_credit= row['parent_lgy_credit'],
                                sibling_legacy_credit=row['sibling_lgy_credit'],
                                residency_credit= row['residency_credit']))


        except Exception as e:
            print('Error',e)

    print("Created Objects")
    ExamResultsActive.objects.bulk_create(entries,ignore_conflicts=True)

    return



def save_exam_result_terminated():
    ExamResultsTerminated.objects.all().delete()
    exam_result_list = get_exam_result_terminated()
    exam_result_list_df = pd.DataFrame.from_records(exam_result_list)
    exam_result_list_df= exam_result_list_df.where(exam_result_list_df.notnull(),None)
    entries = []
    for index, row in exam_result_list_df.iterrows():
        try:

            entries.append(ExamResultsTerminated(exam_number=row['exam_no'],
                                list_title_code=row['list_title_code'],
                                list_title_desc=row['list_title_desc']))
        except Exception as e:
            print('Error',e)

    print("Created Objects")
    ExamResultsTerminated.objects.bulk_create(entries,ignore_conflicts=True)

def getAwareDate(inputDate):
    if not inputDate:
        return
    tz=timezone.get_default_timezone()
    aware_datetime = datetime.datetime.fromisoformat(inputDate)
    date_aware=aware_datetime.replace(tzinfo=tz)
    return date_aware

def convertDateFormat(inputDate):
    if not inputDate:
        return None
    return datetime.datetime.strptime(inputDate, '%d-%b-%Y').strftime("%Y-%m-%d")


if __name__ == '__main__':
    save_exam_result_active()
    save_exam_result_terminated()
