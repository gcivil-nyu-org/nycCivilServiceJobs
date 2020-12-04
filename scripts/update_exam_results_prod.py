import sys
import os
import django

sys.path.append("../nycCivilServiceJobs")  # here store is root folder(means parent).
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nycCivilServiceJobs.settings")
django.setup()

import pandas as pd
from sodapy import Socrata
from examresults.models import ExamResultsActive
from examresults.models import ExamResultsTerminated
from django.utils import timezone
import datetime


client = Socrata(
    "data.cityofnewyork.us",
    "m7QHRP2U6tqRR7XCge8TzIRUW",
    username="nycCivilService.csgy6063@gmail.com",
    password="team4Pythonpir@tes",
    timeout=30,
)


def update_exam_result_active():
    columns = [
        "exam_no",
        "list_no",
        "first_name",
        "last_name",
        "adj_fa",
        "list_title_code",
        "list_title_desc",
        "group_no",
        "list_agency_code",
        "list_agency_desc",
        "established_date",
        "anniversary_date",
        "mi",
        "published_date",
        "veteran_credit",
        "extension_date",
        "sibling_lgy_credit",
        "list_div_code",
        "parent_lgy_credit",
        "residency_credit",
    ]
    limit = 10000
    record_count = int(client.get("vx8i-nprf", select="COUNT(*)")[0]["COUNT"])
    offset = 0

    entries = []

    while offset < record_count:
        try:
            exam_result_list = client.get("vx8i-nprf", offset=offset, limit=limit)
        except Exception as e:
            print("API Errors", e)
        else:
            exam_result_list_df = pd.DataFrame.from_records(exam_result_list)
            exam_result_list_df = exam_result_list_df.replace(
                r"^\s*$", None, regex=True
            )
            exam_result_list_df = exam_result_list_df.where(
                exam_result_list_df.notnull(), None
            )
            exam_result_list_df = exam_result_list_df[
                exam_result_list_df["first_name"].notnull()
                & exam_result_list_df["last_name"].notnull()
            ]
        for c in columns:
            if c not in exam_result_list_df.columns:
                exam_result_list_df[c] = None
        for index, row in exam_result_list_df.iterrows():
            try:
                val_in_db = ExamResultsActive.objects.filter(
                    exam_number=row["exam_no"],
                    list_title_code=row["list_title_code"],
                    list_number=row["list_no"],
                    first_name=row["first_name"],
                    last_name=row["last_name"],
                    middle_initial=row["mi"],
                )
                if not val_in_db.exists():
                    entries.append(
                        ExamResultsActive(
                            exam_number=row["exam_no"],
                            list_number=row["list_no"],
                            first_name=row["first_name"],
                            last_name=row["last_name"],
                            middle_initial=row["mi"],
                            adjust_final_average=row["adj_fa"],
                            list_title_code=row["list_title_code"],
                            list_title_desc=row["list_title_desc"],
                            group_number=row["group_no"],
                            list_agency_code_promo=row["list_agency_code"],
                            list_agency_code_promo_desc=row["list_agency_desc"],
                            list_div_code_promo=row["list_div_code"],
                            anniversary_date=getAwareDate(row["anniversary_date"]),
                            extension_date=getAwareDate(row["extension_date"]),
                            published_date=getAwareDate(row["published_date"]),
                            veteran_credit=row["veteran_credit"],
                            parent_legacy_credit=row["parent_lgy_credit"],
                            sibling_legacy_credit=row["sibling_lgy_credit"],
                            residency_credit=row["residency_credit"],
                        )
                    )

            except Exception as e:
                print("Error", e)
        offset += limit

    print("Found ", len(entries), "new entries for Active")
    ExamResultsActive.objects.bulk_create(entries, ignore_conflicts=True)


def update_exam_result_terminated():

    try:
        record_count = client.get("qu8g-sxqf", select="COUNT(*)")[0]["COUNT"]
        exam_result_list = client.get(
            "qu8g-sxqf",
            select="distinct exam_no,list_title_code,list_title_desc",
            limit=record_count,
        )
    except Exception as e:
        print("Client Error", e)
    else:
        exam_result_list_df = pd.DataFrame.from_records(exam_result_list)
        exam_result_list_df = exam_result_list_df.where(
            exam_result_list_df.notnull(), None
        )
        columns = ["exam_no", "list_title_code", "list_title_desc"]
        for c in columns:
            if c not in exam_result_list_df:
                exam_result_list_df[c] = None
        entries = []
        for index, row in exam_result_list_df.iterrows():
            try:
                val_in_db = ExamResultsTerminated.objects.filter(
                    exam_number=row["exam_no"],
                    list_title_code=row["list_title_code"],
                    list_title_desc=row["list_title_desc"],
                )
                if not val_in_db.exists():
                    entries.append(
                        ExamResultsTerminated(
                            exam_number=row["exam_no"],
                            list_title_code=row["list_title_code"],
                            list_title_desc=row["list_title_desc"],
                        )
                    )

            except Exception as e:
                print("Error", e)

        print("Found ", len(entries), "new entries in Terminated")
        ExamResultsTerminated.objects.bulk_create(entries, ignore_conflicts=True)


def getAwareDate(inputDate):
    if not inputDate:
        return
    tz = timezone.get_default_timezone()
    aware_datetime = datetime.datetime.fromisoformat(inputDate)
    date_aware = aware_datetime.replace(tzinfo=tz)
    return date_aware


def convertDateFormat(inputDate):
    if not inputDate:
        return None
    return datetime.datetime.strptime(inputDate, "%d-%b-%Y").strftime("%Y-%m-%d")


if __name__ == "__main__":
    update_exam_result_active()
    update_exam_result_terminated()
