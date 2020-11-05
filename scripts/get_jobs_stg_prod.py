import sys
import os
import django
import pandas as pd
from sodapy import Socrata
from django.utils import timezone
import datetime
import ftfy

sys.path.append("../nycCivilServiceJobs")  # here store is root folder(means parent).
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nycCivilServiceJobs.settings")
django.setup()

from jobs.models import job_record

client = Socrata(
    "data.cityofnewyork.us",
    "m7QHRP2U6tqRR7XCge8TzIRUW",
    username="nycCivilService.csgy6063@gmail.com",
    password="team4Pythonpir@tes",
    timeout=30,
)


def getJobs():
    record_count = client.get("kpav-sd4t", select="COUNT(*)")[0]["COUNT"]
    results = client.get("kpav-sd4t", limit=record_count)

    return results


def save_Jobs():

    job_record.objects.all().delete()
    print("Deleted Previous Entries for Jobs")

    columns = [
        "job_id",
        "agency",
        "posting_type",
        "num_positions",
        "business_title",
        "civil_service_title",
        "title_classification",
        "title_code_no",
        "level",
        "job_category",
        "full_time_part_time_indicator",
        "career_level",
        "salary_range_from",
        "salary_range_to",
        "salary_frequency",
        "work_location",
        "division_work_unit",
        "job_description",
        "minimum_qual_requirements",
        "preferred_skills",
        "additional_information",
        "to_apply",
        "hours_shift",
        "work_location_1",
        "recruitment_contact",
        "residency_requirement",
        "posting_date",
        "post_until",
        "posting_updated",
        "process_date",
    ]

    limit = 10000
    record_count = int(client.get("kpav-sd4t", select="COUNT(*)")[0]["COUNT"])
    print("Total Records Before Preprocessing: ", record_count)
    offset = 0
    while offset < record_count:
        try:
            jobs_list = client.get("kpav-sd4t", offset=offset, limit=limit)
        except Exception as e:
            print("API Errors", e)
        else:

            jobs_list_df = pd.DataFrame.from_records(jobs_list)
            jobs_list_df = jobs_list_df.replace(r"^\s*$", None, regex=True)
            jobs_list_df = jobs_list_df.where(jobs_list_df.notnull(), None)
            jobs_list_df = jobs_list_df[jobs_list_df["job_id"].notnull()]

            for c in columns:
                if c not in jobs_list_df.columns:
                    jobs_list_df[c] = None

            jobrecord = []
            for index, row in jobs_list_df.iterrows():
                try:
                    jobrecord.append(
                        job_record(
                            job_id=row["job_id"],
                            agency=row["agency"],
                            posting_type=row["posting_type"],
                            num_positions=row["number_of_positions"],
                            business_title=fix_text_encoding(row["business_title"]),
                            civil_service_title=civil_service_title_cleanup(
                                row["civil_service_title"]
                            ),
                            title_classification=title_classification_cleanup(
                                row["title_classification"]
                            ),
                            title_code_no=row["title_code_no"],
                            level=row["level"],
                            job_category=row["job_category"],
                            full_time_part_time_indicator=full_time_part_time_indicator_cleanup(
                                row["full_time_part_time_indicator"]
                            ),  # Full-time/Part-time
                            career_level=row["career_level"],
                            salary_range_from=row["salary_range_from"],
                            salary_range_to=row["salary_range_to"],
                            salary_frequency=row["salary_frequency"],
                            work_location=fix_text_encoding(row["work_location"]),
                            division_work_unit=row["division_work_unit"],
                            job_description=fix_text_encoding(row["job_description"]),
                            minimum_qual_requirements=fix_text_encoding(
                                row["minimum_qual_requirements"]
                            ),
                            preferred_skills=fix_text_encoding(row["preferred_skills"]),
                            additional_information=fix_text_encoding(
                                row["additional_information"]
                            ),
                            to_apply=fix_text_encoding(row["to_apply"]),
                            hours_shift=row["hours_shift"],
                            work_location_1=fix_text_encoding(row["work_location_1"]),
                            recruitment_contact=fix_text_encoding(
                                row["recruitment_contact"]
                            ),
                            residency_requirement=fix_text_encoding(
                                row["residency_requirement"]
                            ),
                            posting_date=getAwareDate(row["posting_date"]),
                            post_until=convertDateFormat(
                                row["post_until"]
                            ),  # if not is_nan(row['post_until']) else None,
                            posting_updated=getAwareDate(row["posting_updated"]),
                            process_date=getAwareDate(row["process_date"]),
                        )
                    )
                except Exception as e:
                    print("Error", e)

            offset += limit
            job_record.objects.bulk_create(jobrecord, ignore_conflicts=True)
            print(".", end="", flush=True)

    print("\nInserted Job records: ", job_record.objects.count())


def is_nan(x):
    return x != x


def getAwareDate(inputDate):
    if not inputDate:
        return
    tz = timezone.get_default_timezone()
    aware_datetime = datetime.datetime.fromisoformat(inputDate)
    date_aware = aware_datetime.replace(tzinfo=tz)
    return date_aware


def convertDateFormat(inputDate):
    if not inputDate:
        return
    return datetime.datetime.strptime(inputDate, "%d-%b-%Y").strftime("%Y-%m-%d")


# if column is NULL then tag as Fulltime
def full_time_part_time_indicator_cleanup(s):
    if s is None:
        s = "F"
    return s


def civil_service_title_cleanup(s):
    return trim_parenthesis(s)


def trim_parenthesis(s):
    stack = []
    for i in range(len(s)):
        if s[i] == "(":
            stack.append(i)
        elif s[i] == ")":
            stack.pop()

    if len(stack) != 0:
        index = stack.pop(0)
        return s[:index]

    return s


def fix_text_encoding(s):
    if s is not None:
        return ftfy.fix_text(s)
    return s


def title_classification_cleanup(s):
    s = s[: len(s) - 2]
    return s


if __name__ == "__main__":
    save_Jobs()
