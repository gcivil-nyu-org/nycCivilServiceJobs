import sys, os, django
sys.path.append("../nycCivilServiceJobs") #here store is root folder(means parent).
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nycCivilServiceJobs.settings")
django.setup()

import requests
import json
import pandas as pd
from sodapy import Socrata
import csv
from jobs.models import job_record
from django.utils import timezone
import datetime



'''def getjob_data(restaurant_name, restaurant_location):
    location_list = restaurant_location.split(", ")
    address1 = location_list[0]
    city = location_list[1]
    state = location_list[2]
    country = 'US'

    api_key = 'JaekzvTTKsWGtQ96HUiwAXOUwRt6Ndbqzch4zc2XFnOEBxwTmwr-esm1uWo2QFvFJtXS8nY2dXx51cfAnMqVHpHRcp8N7QtP7LNVCcoxJWV_9NJrmZWSMiq-R_mEX3Yx'
    headers = {'Authorization': 'Bearer %s' % api_key}
    url = 'https://api.yelp.com/v3/businesses/matches'
    params = {'name': restaurant_name, 'address1': address1, 'city': city, 'state': state, 'country': country}

    response = requests.get(url, params=params, headers=headers)
    return response.text.encode("utf8")
'''


def getJobs():
    client = Socrata("data.cityofnewyork.us",
                     "m7QHRP2U6tqRR7XCge8TzIRUW",
                     username="nycCivilService.csgy6063@gmail.com",
                     password="team4Pythonpir@tes")
    results = client.get("kpav-sd4t", limit=25000)

    return results


def save_Jobs():
    jobs_list = getJobs()
    jobs_list_df = pd.DataFrame.from_records(jobs_list)
    #print(jobs_list_df)
    for index, row in jobs_list_df.iterrows():
        try:
            print(row['job_id'])
            # tz=timezone.get_default_timezone()
            # posting_date_aware_datetime = datetime.datetime.fromisoformat(row['posting_date'])
            # posting_date_aware=posting_date_aware_datetime.replace(tzinfo=tz)
           
            jobrecord = job_record( job_id=row['job_id'],
                                agency=row['agency'],
                                posting_type=row['posting_type'],
                                num_positions=row['number_of_positions'],
                                business_title=row['business_title'],
                                civil_service_title=row['civil_service_title'],
                                title_classification=row['title_classification'],
                                title_code_no=row['title_code_no'],
                                level=row['level'],
                                job_category=row['job_category'],
                                full_time_part_time_indicator=row['full_time_part_time_indicator'], # Full-time/Part-time
                                career_level=row['career_level'],
                                salary_range_from=row['salary_range_from'],
                                salary_range_to=row['salary_range_to'],
                                salary_frequency=row['salary_frequency'],
                                work_location=row['work_location'],
                                division_work_unit=row['division_work_unit'],
                                job_description=row['job_description'],
                                minimum_qual_requirements=row['minimum_qual_requirements'],
                                preferred_skills=row['preferred_skills'],
                                additional_information=row['additional_information'],
                                to_apply=row['to_apply'],
                                hours_shift=row['hours_shift'],
                                work_location_1=row['work_location_1'],
                                recruitment_contact=None,
                                residency_requirement=row['residency_requirement'],
                                posting_date=getAwareDate(row['posting_date']),
                                post_until=convertDateFormat(row['post_until']), #if not is_nan(row['post_until']) else None,
                                posting_updated=getAwareDate(row['posting_updated']),
                                process_date=getAwareDate(row['process_date']))
            jobrecord.save()
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
    save_Jobs()