from datetime import datetime

from day_phase import determining_the_phase_of_the_day


def main(request_time):
    print(determining_the_phase_of_the_day())

    request_time=datetime.strptime(request_time, "%Y-%m-%d %H:%M:%S").strftime("%d-%m-%Y %H:%M:%S")
    card_numbers=[i for i in about_financial_transactions_xlsx('operations.xlsx')]

    print(request_time)







main('2019-05-21 12:49:53')