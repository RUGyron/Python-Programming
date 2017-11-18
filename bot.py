import config
import telebot
import requests
from bs4 import BeautifulSoup

bot = telebot.TeleBot(config.token)

"""
@bot.message_handler(content_types=["text"])
def repeater(message):  # Название функции не играет никакой роли, в принципе
    bot.send_message(message.chat.id, message.text)
"""

def get_page(week=''):
    if week:
        week = str(week) + '/'
    url = '{domain}/{group}/{week}raspisanie_zanyatiy_{group}.htm'.format(
        domain=config.domain,
        week=week,
        group='K3140')
    response = requests.get(url)
    web_page = response.text
    return web_page


def get_schedule(web_page, day):
    soup = BeautifulSoup(web_page, "html5lib")
    if type(day) == list:
        day = day[0]
    # Получаем таблицу с расписанием на день недели
    schedule_table = soup.find("table", attrs={"id": "1day"})
    if day == '/понедельник' or day == '/воскресенье' or day == '/Понедельник' or day == '/Воскресенье':
        schedule_table = soup.find("table", attrs={"id": "1day"})
    elif day == '/вторник' or day == '/Вторник':
        schedule_table = soup.find("table", attrs={"id": "2day"})
    elif day == '/среда' or day == '/Среда':
        schedule_table = soup.find("table", attrs={"id": "3day"})
    elif day == '/четверг' or day == '/Четверг':
        schedule_table = soup.find("table", attrs={"id": "4day"})
    elif day == '/пятница' or day == '/Пятница':
        schedule_table = soup.find("table", attrs={"id": "5day"})
    elif day == '/суббота' or day == '/Суббота':
        schedule_table = soup.find("table", attrs={"id": "6day"})
    # Время проведения занятий
    times_list = schedule_table.find_all("td", attrs={"class": "time"})
    times_list = [time.span.text for time in times_list]
    # Место проведения занятий
    locations_list = schedule_table.find_all("td", attrs={"class": "room"})
    locations_list = [room.span.text for room in locations_list]

    # Название дисциплин и имена преподавателей
    lessons_list = schedule_table.find_all("td", attrs={"class": "lesson"})
    lessons_list = [lesson.text.split('\n') for lesson in lessons_list]
    lessons_list = [''.join([info for info in lesson_info if info]) for lesson_info in lessons_list]

    return times_list, locations_list, lessons_list


@bot.message_handler(commands=['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье',
                               'Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресеьне'])
def get_day(message):
    if len(message.text.split()) == 2:
        day, week = message.text.split()
        web_page = get_page(week)
    else:
        day = message.text.split()
        web_page = get_page()
    times_lst, locations_lst, lessons_lst = get_schedule(web_page, day)

    resp = ''
    for time, location, lesson in zip(times_lst, locations_lst, lessons_lst):
        resp += '<b>{}</b>, {}, {}\n'.format(time, location, lesson)

    bot.send_message(message.chat.id, resp, parse_mode='HTML')


if __name__ == '__main__':
    bot.polling(none_stop=True)
