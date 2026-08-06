import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def determining_the_phase_of_the_day() -> str:
    """"Определяет какая сейчас часть суток по условному разграничению"""

    # Условное разграничение суток
    time_list = ['06:00', '11:59', '12:00', '17:59', '18:00', '22:59']
    logger.info('Получен шаблон временных отрезков')


    # Форматирование условного разграничения
    time_list = [datetime.strptime(t, "%H:%M").time() for t in time_list]
    logger.info('Получен набор временных отрезков')
    for i in range(0, 6, 2):
        if time_list[i] <= datetime.now().time() <= time_list[i + 1]:
            logger.info('Фаза дня определена')
            match i:
                case 0:
                    return "Доброе утро"
                case 2:
                    return "Добрый день"
                case 4:
                    return "Добрый вечер"

    return "Доброй ночи"