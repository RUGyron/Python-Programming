from cs102.homework05 import config
import datetime
import telebot
import requests
import time
from bs4 import BeautifulSoup

bot = telebot.TeleBot(config.token)

"""

@bot.message_handler(content_types=["text"])
def repeater(message):  # Название функции не играет никакой роли, в принципе
     bot.send_message(message.chat.id, message.text)

"""


def get_page(week='', group='K3140'):
    if week:
        week = str(week) + '/'
    if week == '0/':
        week = ''
    url = '{domain}/{group}/{week}raspisanie_zanyatiy_{group}.htm'.format(
        domain=config.domain,
        week=week,
        group=group
    )
    response = requests.get(url)
    web_page = response.text
    return web_page


def get_schedule(web_page, day):
    soup = BeautifulSoup(web_page, "html5lib")
    # Получаем таблицу с расписанием на день недели
    schedule_table = soup.find("table", attrs={"id": "1day"})
    if day == '/monday' or day == '/sunday' or day == '/Monday' or day == '/Sunday':
        schedule_table = soup.find("table", attrs={"id": "1day"})
    elif day == '/tuesday' or day == '/Tuesday':
        schedule_table = soup.find("table", attrs={"id": "2day"})
    elif day == '/wednesday' or day == '/Wednesday':
        schedule_table = soup.find("table", attrs={"id": "3day"})
    elif day == '/thursday' or day == '/Thursday':
        schedule_table = soup.find("table", attrs={"id": "4day"})
    elif day == '/friday' or day == '/Friday':
        schedule_table = soup.find("table", attrs={"id": "5day"})
    elif day == '/saturday' or day == '/Saturday':
        schedule_table = soup.find("table", attrs={"id": "6day"})
    # Время проведения занятий
    times_list = schedule_table.find_all("td", attrs={"class": "time"})
    times_list = [time.span.text for time in times_list]
    # Место проведения занятий
    locations_list = schedule_table.find_all("td", attrs={"class": "room"})
    locations_list = [room.span.text for room in locations_list]

    # Название дисциплин и имена преподавателей
    lessons_list = schedule_table.find_all("td", attrs={"class": "lesson"})
    lessons_list = [lesson.text.replace('\n', '').replace('\t', '') for lesson in lessons_list]

    return times_list, locations_list, lessons_list


@bot.message_handler(commands=['all'])
def get_week(message):
    if len(message.text.split()) != 1:
        _, week, group = message.text.split()
        web_page = get_page(week, group)
        if int(week) == 1:
            resp = '<b>Расписание на четную неделю:</b>\n\n'
        elif int(week) == 2:
            resp = '<b>Расписание на нечетную неделю:</b>\n\n'
        elif int(week) == 0:
            resp = '<b>Расписание на любую неделю:</b>\n\n'
    week_list = ['/monday', '/tuesday', '/wednesday', '/thursday', '/friday', '/saturday']
    visual_list = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']
    for i in range(6):
        resp += '<b>' + visual_list[i] + '</b>' + ':\n'
        times_lst, locations_lst, lessons_lst = get_schedule(web_page, week_list[i])

        for time, location, lesson in zip(times_lst, locations_lst, lessons_lst):
            resp += '<b>{}</b>, {}, {}\n'.format(time, location, lesson)
        resp += '\n'
    bot.send_message(message.chat.id, resp, parse_mode='HTML')


@bot.message_handler(commands=['tomorrow'])
def get_tomorrow(message):
    _, group = message.text.split()
    if int(datetime.datetime.today().strftime('%U')) % 2 == 1:
        week = 2
    else:
        week = 1
    web_page = get_page(week, group)
    today = datetime.datetime.now()
    tomorrow = today
    if today.weekday() == 5:
        tomorrow += datetime.timedelta(days=2)
    else:
        tomorrow += datetime.timedelta(days=1)
    if tomorrow.weekday() == 0:
        tomorrow = '/monday'
    elif tomorrow.weekday() == 1:
        tomorrow = '/tuesday'
    elif tomorrow.weekday() == 2:
        tomorrow = '/wednesday'
    elif tomorrow.weekday() == 3:
        tomorrow = '/thursday'
    elif tomorrow.weekday() == 4:
        tomorrow = '/friday'
    elif tomorrow.weekday() == 5:
        tomorrow = '/saturday'
    times_lst, locations_lst, lessons_lst = get_schedule(web_page, tomorrow)
    resp = '<b>Расписание на завтра:\n\n</b>'
    for time, location, lesson in zip(times_lst, locations_lst, lessons_lst):
        resp += '<b>{}</b>, {}, {}\n'.format(time, location, lesson)

    bot.send_message(message.chat.id, resp, parse_mode='HTML')


@bot.message_handler(commands=['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday',
                               'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
def get_day(message):
    day, week, group = message.text.split()
    web_page = get_page(week, group)
    times_lst, locations_lst, lessons_lst = get_schedule(web_page, day)

    resp = ''
    for time, location, lesson in zip(times_lst, locations_lst, lessons_lst):
        resp += '<b>{}</b>, {}, {}\n'.format(time, location, lesson)

    bot.send_message(message.chat.id, resp, parse_mode='HTML')


@bot.message_handler(commands=['near'])
def get_next_lesson(message):
    _, group = message.text.split()
    today = datetime.datetime.now().weekday()
    if today != 6:
        if today == 0:
            today = '/monday'
        elif today == 1:
            today = '/tuesday'
        elif today == 2:
            today = '/wednesday'
        elif today == 3:
            today = '/thursday'
        elif today == 4:
            today = '/friday'
        elif today == 5:
            today = '/saturday'
    else:
        bot.send_message(message.chat.id, 'Сегодня нет пар ;)')

    if int(datetime.datetime.today().strftime('%U')) % 2 == 1:
        week = 2
    else:
        week = 1
    web_page = get_page(week, group)
    times_list, locations_lst, lessons_lst = get_schedule(web_page, today)
    cnt = 0
    state = 0
    for i in times_list:
        _, time = i.split('-')
        t1, t2 = time.split(':')
        time = int(t1 + t2)
        cur_time = int(str(datetime.datetime.now().hour) + str(datetime.datetime.now().minute))
        if cur_time < time:
            resp = '<b>Ближайшая пара сегодня:</b>\n'
            resp += '<b>{}</b>, {}, {}\n'.format(times_list[cnt], locations_lst[cnt], lessons_lst[cnt])
            bot.send_message(message.chat.id, resp, parse_mode='HTML')
            state = 1
            break
        cnt +=1
    if not state:
        bot.send_message(message.chat.id, 'Все пары на сегодня закончились')


# if __name__ == '__main__':
#     bot.polling(none_stop=True)
while True:
    try:
      bot.polling(none_stop=True)
    except:
        time.sleep(5)
