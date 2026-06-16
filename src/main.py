import json

from day_phase import determining_the_phase_of_the_day
from views import working_with_transactions


def main(request_time: str) -> None:
    s=working_with_transactions(request_time)
    with open('1.json','w',encoding="utf-8") as f:
        json.dump(s,f, indent=4, ensure_ascii=False)




print(main('2019-05-21 12:49:53'))
