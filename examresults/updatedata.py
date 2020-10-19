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
import numpy as np
from examresults.models import ExamResultsActive,ExamResultsTerminated
from django.utils import timezone
import datetime
from getdata import *



def update_exam_result_active():
    columns = ['exam_no', 'list_no', 'first_name', 'last_name', 'adj_fa',
       'list_title_code', 'list_title_desc', 'group_no', 'list_agency_code',
       'list_agency_desc', 'established_date', 'anniversary_date', 'mi',
       'published_date', 'veteran_credit', 'extension_date',
       'sibling_lgy_credit', 'list_div_code', 'parent_lgy_credit','residency_credit']

    exam_result_list = get_exam_result_active()
    exam_result_list_df = pd.DataFrame.from_records(exam_result_list)
    exam_result_list_df= exam_result_list_df.where(exam_result_list_df.notnull(),None)

    for c in columns:
        if c not in exam_result_list_df:
            exam_result_list_df[c] = None

    entries = []
    count = 0
    for index, row in exam_result_list_df.iterrows():
        try:
            count+=1
            new = False
            filtered_results = ExamResultsActive.objects.filter(exam_number=row['exam_no'])
            if filtered_results:
                val = filtered_results.filter(list_title_code=row['list_title_code'],
                                                list_number=row['list_no'],
                                                first_name=row['first_name'],
                                                last_name=row['last_name'],
                                                middle_initial = row['mi'])
                if not val:
                    new = True
            else:
                new = True
            if new:
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
                                    list_div_code_promo= row['list_div_code'] ,
                                    anniversary_date=getAwareDate(row['anniversary_date']),
                                    extension_date=getAwareDate(row['extension_date']),
                                    veteran_credit= row['veteran_credit'],
                                    parent_legacy_credit= row['parent_lgy_credit'],
                                    sibling_legacy_credit=row['sibling_lgy_credit'],
                                    residency_credit= row['residency_credit']))

        except Exception as e:
            print('Error',e)
    print("Found ",len(entries),"new entries")
    ExamResultsActive.objects.bulk_create(entries,ignore_conflicts=True)


def update_exam_result_terminated():
    columns = ['exam_no','list_title_code','list_title_desc']

    exam_result_list = get_exam_result_terminated()
    exam_result_list_df = pd.DataFrame.from_records(exam_result_list)
    exam_result_list_df= exam_result_list_df.where(exam_result_list_df.notnull(),None)

    for c in columns:
        if c not in exam_result_list_df:
            exam_result_list_df[c] = None
    entries = []
    for index, row in exam_result_list_df.iterrows():
        try:
            val = ExamResultsTerminated.objects.filter(exam_number=row['exam_no'],
                                    list_title_code=row['list_title_code'],
                                    list_title_desc=row['list_title_desc'])
            if not val.exists():
                entries.append(ExamResultsTerminated(exam_number=row['exam_no'],
                                    list_title_code=row['list_title_code'],
                                    list_title_desc=row['list_title_desc']))

        except Exception as e:
            print('Error',e)

    print("Found ",len(entries),"new entries")
    ExamResultsTerminated.objects.bulk_create(entries,ignore_conflicts=True)


if __name__ == '__main__':
    update_exam_result_active()
    update_exam_result_terminated()
