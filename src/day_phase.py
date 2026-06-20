import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def determining_the_phase_of_the_day() -> str:
    """"Определяет какая сейчас часть суток по условному разграничению"""

    # Условное разграничение суток
    logger.info('Получен шаблон')
    time_list = ['06:00', '11:59', '12:00', '17:59', '18:00', '22:59']


    # Форматирование условного разграничения
    time_list = [datetime.strptime(t, "%H:%M").time() for t in time_list]
    logger.info('Получен набор временных границ')
    for i in range(0, 6, 2):
        if time_list[i] <= datetime.now().time() <= time_list[i + 1]:
            match i:
                case 0:
                    logger.info('Понял где и когда я')
                    return "Доброе утро"
                case 2:
                    logger.info('Понял где и когда я')
                    return "Добрый день"
                case 4:
                    logger.info('Понял где и когда я')
                    return "Добрый вечер"

    logger.info('Понял когда я')
    return "Доброй ночи"