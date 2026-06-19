from datetime import datetime


def determining_the_phase_of_the_day() -> str:
    """"Определяет какая сейчас часть суток по условному разграничению"""

    # Уссловное разграничение суток
    time_list = ['06:00', '11:59', '12:00', '17:59', '18:00', '22:59']
    # Форматирование условного разграничения
    time_list = [datetime.strptime(t, "%H:%M").time() for t in time_list]

    for i in range(0, 6, 2):
        if time_list[i] <= datetime.now().time() <= time_list[i + 1]:
            match i:
                case 0:
                    return "Доброе утро"
                case 2:
                    return "Добрый день"
                case 4:
                    return "Добрый вечер"

    return "Доброй ночи"