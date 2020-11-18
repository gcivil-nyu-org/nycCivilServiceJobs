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


def get_cst():

    try:
        cst = client.get(
            "kpav-sd4t", select="distinct civil_service_title, title_code_no"
        )
    except Exception as e:
        print("Client Error", e)
    else:
        CivilServicesTitle.objects.all().delete()
        print("\nDeleted Previous Entries for Civil Services Titles")
        cst_df = pd.DataFrame.from_records(cst)

        entries = []

        for index, row in cst_df.iterrows():
            try:

                entries.append(
                    CivilServicesTitle(
                        title_code=row["title_code_no"],
                        title_description=civil_service_title_cleanup(
                            row["civil_service_title"]
                        ),
                    )
                )
            except Exception as e:
                print("Error", e)

        CivilServicesTitle.objects.bulk_create(entries, ignore_conflicts=True)
        print(".", end="", flush=True)
    print(
        "\nCreated Objects in Civil Services Titles: ",
        CivilServicesTitle.objects.count(),
    )


def civil_service_title_cleanup(s):
    return trim_parenthesis(s).rstrip()


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
    get_cst()
