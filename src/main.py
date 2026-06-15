from day_phase import determining_the_phase_of_the_day
from views import working_with_transactions


def main(request_time: str, period: int = 0) -> None:
    print(determining_the_phase_of_the_day())

    working_with_transactions(request_time, period)


main('2019-05-21 12:49:53')
