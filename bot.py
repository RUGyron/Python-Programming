import config
import telebot
import requests
from telebot import types
from bs4 import BeautifulSoup


bot = telebot.TeleBot(config.token)
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 YaBrowser/17.10.1.1204 Yowser/2.5 Safari/537.36'}
@bot.message_handler(commands=['start'])
def startBot(message):
    key = types.ReplyKeyboardMarkup()
    key.row('Поиск', 'Совет')
    bot.send_message(message.chat.id, 'Начнём, ' + message.chat.first_name + '?', reply_markup=key)


@bot.message_handler(content_types=['text'])
def inline(message):
    if message.text == 'Совет':
        recommendFilm(message)
    if message.text == 'К началу':
        startBot(message)
    if message.text == 'Поиск':
        searchFilm(message)
    if '-' in message.text:
        getSchedule(getFilmBySearch(message))


def getSchedule(web_page):
    web_page, message = web_page
    web = BeautifulSoup(web_page, "html5lib")

    all_info = web.find("div", attrs={"class": "element most_wanted"}).find('div', attrs={'class': 'info'})

    spec_url = all_info.find("a", attrs={"class": "js-serp-metrika"}).get('href')
    url = 'https://www.kinopoisk.ru'
    url += spec_url

    title = all_info.find("a", attrs={"class": "js-serp-metrika"}).get_text()
    year = all_info.find("span", attrs={'class':'year'}).get_text()
    grey_info = all_info.find_all('span', attrs={'class':'gray'})[:-1]
    alter_name, time = grey_info[0].get_text().split(', ')
    try:
        contry , _ = grey_info[1].get_text().split(', реж')
    except:
        contry, _ = grey_info[1].get_text().split(' реж')
    producer = grey_info[1].find('a', attrs={'data-type':'film'}).get_text()
    _, genres = grey_info[1].get_text().split('(')
    genres, _ = genres.split(')')
    id = web.find("div", attrs={"class": "element most_"
                                               "wanted"}).find('p', attrs={'class': 'pic'}).find('img').get('title')
    _, id = id.split('sm_film/')
    id, _ = id.split('.')
    img_url = 'https://st.kp.yandex.net/images/film_iphone/iphone360_{0}.jpg'.format(id)
    url_yt = 'https://www.youtube.com/results?search_query='
    title_yt = title.replace(' ', '+')
    url_yt += title_yt + '+трейлер'

    film_text = '<b>Информация о фильме:</b>\n\n'
    film_text += '<b>Название: </b>'+title+'\n<b>Жанр: </b>'+genres+'\n<b>Страна: </b>'+contry+\
                '\n<b>Год: </b>'+year+'\n<b>Длительность: </b>'+time+'\n<b>Название (ориг.): </b>'+alter_name+\
                '\n<b>Режиссёр: </b>'+producer+'\n<b>Инфо на "Кинопоиске": </b>'+url+'\n<b>Трейлер на YouTube: </b>'+\
                 url_yt+'\n'

    bot.send_photo(message.chat.id, img_url)
    bot.send_message(message.chat.id, film_text, parse_mode='HTML')


def recommendFilm(message):
    key = types.ReplyKeyboardMarkup()
    key.row('Из топа', 'Слуйчайный')
    key.row('Фильтры')
    key.row('К началу')
    bot.send_message(message.chat.id, 'Выберите 1 из следующих опций:', reply_markup=key)


def searchFilm(message):
    bot.send_message(message.chat.id, 'Введите название фильма, например:'
                                      ' <b>-Гарри Поттер</b>', parse_mode='HTML')

def getFilmBySearch(message):
    nameFilm = message.text[1:]
    response = config.domainSearch + nameFilm
    query = requests.get(response).text
    return query, message

if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except:
            pass
