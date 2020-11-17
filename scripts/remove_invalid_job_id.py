import sys
import os
import django

sys.path.append("../nycCivilServiceJobs")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nycCivilServiceJobs.settings")
django.setup()
from jobs.models import job_record

import csv
import datetime


def get_job_ids():
    job_count_before = job_record.objects.count()
    print("Jobs count before cleanup of Invalid Jobs Ids: ", job_count_before)
    job_ids_csv = "scripts/invalid_job_ids.csv"
    with open(job_ids_csv) as f:
        reader_exams = csv.reader(f, delimiter=",")

        for row in reader_exams:
            try:
                val_in_db = job_record.objects.filter(job_id=row[0]).delete()
            except Exception as e:
                print("Error", e)

    print("Jobs count after cleanup of Invalid Jobs Ids: ", job_record.objects.count())
    print("Totoal Jobs removed: ", job_count_before - job_record.objects.count())


if __name__ == "__main__":
    get_job_ids()
