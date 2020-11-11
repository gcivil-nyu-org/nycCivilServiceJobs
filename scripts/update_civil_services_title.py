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

from examresults.models import CivilServicesTitle

client = Socrata(
    "data.cityofnewyork.us",
    "m7QHRP2U6tqRR7XCge8TzIRUW",
    username="nycCivilService.csgy6063@gmail.com",
    password="team4Pythonpir@tes",
    timeout=30,
)


def update_civil_services_title():
    columns = ["title_code", "title_description"]

    limit = 10000
    record_count = int(client.get("nzjr-3966", select="COUNT(*)")[0]["COUNT"])
    print("Total Records Before Preprocessing: ", record_count)
    offset = 0
    civil_services_title = []
    while offset < record_count:
        try:
            civil_services_title_list = client.get(
                "nzjr-3966",
                select="distinct title, descr",
                where="title is not null",
                offset=offset,
                limit=limit,
            )
        except Exception as e:
            print("API Errors", e)
        else:

            civil_services_title_df = pd.DataFrame.from_records(
                civil_services_title_list
            )
            civil_services_title_df = civil_services_title_df.replace(
                r"^\s*$", None, regex=True
            )
            civil_services_title_df = civil_services_title_df.where(
                civil_services_title_df.notnull(), None
            )
            # civil_services_title_df = civil_services_title_df[civil_services_title_df["title"].notnull()]

            for c in columns:
                if c not in civil_services_title_df.columns:
                    civil_services_title_df[c] = None

            for index, row in civil_services_title_df.iterrows():
                try:
                    # print(row["job_id"])
                    val_in_db = CivilServicesTitle.objects.filter(
                        title_code=row["title"],
                        title_description=civil_service_title_cleanup(row["descr"]),
                    )
                    if not val_in_db.exists():
                        civil_services_title.append(
                            CivilServicesTitle(
                                title_code=row["title"],
                                title_description=civil_service_title_cleanup(
                                    row["descr"]
                                ),
                            )
                        )
                except Exception as e:
                    print("Error", e)

            offset += limit

    print("Found", len(civil_services_title), "new Civil Services Titles")
    if len(civil_services_title) > 0:
        CivilServicesTitle.objects.bulk_create(
            civil_services_title, ignore_conflicts=True
        )
        print("Inserted New Civil Services Titles")
    else:
        print("No new Civil Services Titles to insert")


def civil_service_title_cleanup(s):
    return trim_parenthesis(s)


# Trims dangling parenthesis
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


if __name__ == "__main__":
    update_civil_services_title()
