from typing import List

import pandas as pd
from datetime import timedelta, date

CONFIRMED_CASES_URL = f"https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data" \
                      f"/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv "

"""
When downloading data it's better to do it in a global scope instead of a function.
This speeds up the tests significantly
"""
confirmed_cases = pd.read_csv(CONFIRMED_CASES_URL, error_bad_lines=False)


def poland_cases_by_date(day: int, month: int, year: int = 2020) -> int:
    """
    Returns confirmed infection cases for country 'Poland' given a date.

    Ex.
    >>> poland_cases_by_date(7, 3, 2020)
    5
    >>> poland_cases_by_date(11, 3)
    31

    :param year: 4 digit integer representation of the year to get the cases for, defaults to 2020
    :param day: Day of month to get the cases for as an integer indexed from 1
    :param month: Month to get the cases for as an integer indexed from 1
    :return: Number of cases on a given date as an integer
    """
    
    # Your code goes here (remove pass)
    dt = date(year=year, month=month, day=day)
    dt_str = dt.strftime('%-m/%-d/%y')

    if dt < date(2020, 1, 22):  # date before 2020-01-22 -> no cases
        return 0
    elif dt >= date.today() or dt_str not in confirmed_cases.columns:  # date after last notification -> get last column
        return confirmed_cases[confirmed_cases['Country/Region'] == 'Poland'].iloc[:, -1].sum()
    else:
        return confirmed_cases[confirmed_cases['Country/Region'] == 'Poland'][dt_str].sum()


def top5_countries_by_date(day: int, month: int, year: int = 2020) -> List[str]:
    """
    Returns the top 5 infected countries given a date (confirmed cases).

    Ex.
    >>> top5_countries_by_date(27, 2, 2020)
    ['China', 'Korea, South', 'Cruise Ship', 'Italy', 'Iran']
    >>> top5_countries_by_date(12, 3)
    ['China', 'Italy', 'Iran', 'Korea, South', 'France']

    :param day: 4 digit integer representation of the year to get the countries for, defaults to 2020
    :param month: Day of month to get the countries for as an integer indexed from 1
    :param year: Month to get the countries for as an integer indexed from 1
    :return: A list of strings with the names of the coutires
    """

    # Your code goes here (remove pass)
    dt = date(year=year, month=month, day=day)
    dt_str = dt.strftime('%-m/%-d/%y')

    if dt < date(2020, 1, 22):  # date before 2020-01-22 -> empty list
        return []
    elif dt >= date.today() or dt_str not in confirmed_cases.columns:  # date after last notification -> get last column
        return confirmed_cases[['Country/Region', confirmed_cases.columns[-1]]]\
            .groupby('Country/Region')[confirmed_cases.columns[-1]].sum().sort_values(ascending=False).head().index\
            .tolist()
    else:
        return confirmed_cases[['Country/Region', dt_str]].groupby('Country/Region')[dt_str].sum()\
            .sort_values(ascending=False).head().index.tolist()


def no_new_cases_count(day: int, month: int, year: int = 2020) -> int:
    """
    Returns the number of countries/regions where the infection count in a given day was the same as the previous day.

    Ex.
    >>> no_new_cases_count(11, 2, 2020)
    35
    >>> no_new_cases_count(3, 3)
    57

    :param day: 4 digit integer representation of the year to get the cases for, defaults to 2020
    :param month: Day of month to get the countries for as an integer indexed from 1
    :param year: Month to get the countries for as an integer indexed from 1
    :return: Number of countries/regions where the count has not changed in a day
    """

    # Your code goes here (remove pass)
    dt = date(year=year, month=month, day=day)  # date today
    dty = dt + timedelta(days=-1)  # date yesterday
    dt_str = dt.strftime('%-m/%-d/%y')
    dty_str = dty.strftime('%-m/%-d/%y')

    if dt < date(2020, 1, 22):
        # date before 2020-01-22 -> 0
        return 0
    elif dt == date(2020, 1, 22):
        # date from beginning of all notifications -> number of cs/rs with cases
        return confirmed_cases[confirmed_cases['1/22/20'] > 0]['Country/Region'].count()
    elif dt >= date.today() or dt_str not in confirmed_cases.columns:
        # date after last notification (no knowledge about new cases) -> 0
        return 0
    else:
        return confirmed_cases[confirmed_cases[dt_str] - confirmed_cases[dty_str] != 0]['Country/Region'].count()
