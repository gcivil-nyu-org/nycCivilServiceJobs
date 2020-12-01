import sys
import os
import django

sys.path.append("../nycCivilServiceJobs")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nycCivilServiceJobs.settings")
django.setup()
from faq.models import faq

import csv
import datetime


def get_faqs():
    faq_count_before = faq.objects.count()
    faq_csv = "scripts/FAQ_list.csv"
    entries = []
    with open(faq_csv) as f:
        reader_faq = csv.reader(f, delimiter=",")

        for row in reader_faq:
            try:
                val = faq.objects.filter(question=row[0])
                if val:
                    continue
                else:
                    item=(faq(
                        question = row[0],
                        answer = row[1],
                        date_published = datetime.date.today(),
                    )
                )
                entries.append(item)

            except Exception as e:
                print("Error", e)

    print("FAQ count before adding:", faq_count_before)
    faq.objects.bulk_create(entries, ignore_conflicts=True)
    print("FAQ count  after adding:", faq.objects.count())


if __name__ == "__main__":
    get_faqs()
