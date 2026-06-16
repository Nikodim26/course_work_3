import json

from views import working_with_transactions


def main(request_time: str) -> None:
    with open('1.json','w',encoding="utf-8") as f:
        json.dump(working_with_transactions(request_time),f, indent=4, ensure_ascii=False)




print(main('2018-05-28 12:49:53'))
