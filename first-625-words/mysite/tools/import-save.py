#!/usr/bin/env python

import csv


from first625words.models import Theme

from django.conf import settings


def main():
    """Read the *.csv files and update the tables on the database"""

    settings.configure(DEBUG=True)

    # Read files and update tables on database
    with open("./data-files/themes.csv") as file:
        themes = csv.reader(file)
        count = 0
        for theme in themes:
            print(theme[0])
            t = Theme(name=theme[0], sort_number=count)
            t.save()
            count += 1


if __name__ == "__main__":
    main()
