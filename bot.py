# -*- coding: utf-8 -*-
import config
import telebot
import requests
import random
import time
from telebot import types
from bs4 import BeautifulSoup
from pprint import pprint as pp


bot = telebot.TeleBot(config.token)
'''
@bot.message_handler(content_types=['text'])
def echo(message):
    print(message)
    return None
'''
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 YaBrowser/17.10.1.1204 Yowser/2.5 Safari/537.36'}
@bot.message_handler(commands=['start'])
def startBot(message):
    key = types.ReplyKeyboardMarkup()
    key.row('Поиск', 'Совет')
    bot.send_message(message.chat.id, 'Начнём, ' + message.chat.first_name + '?😊', reply_markup=key)


Genre = '0'
YearSt = '0'
YearEn = '0'
Contry = '0'
cnt = 0
@bot.message_handler(content_types=['text'])
def inline(message):
    global cnt
    if message.text == 'Совет':
        if cnt == 0:
            recommendFilm(message)
        else:
            bot.send_message(message.chat.id, 'Сори, сейчас выполняется другой запрос')
    if message.text == 'К началу':
        if cnt == 0:
            startBot(message)
        else:
            bot.send_message(message.chat.id, 'Сори, сейчас выполняется другой запрос')
    if message.text == 'Поиск':
        cnt = 1
        searchFilm(message)
    if '-' in message.text:
        if cnt == 0:
            getScheduleSearch(getFilmBySearch(message))
        else:
            bot.send_message(message.chat.id, 'Сори, сейчас выполняется другой запрос')
    if message.text == 'Случайный':
        if cnt == 0:
            getScheduleRandom(getFilmRandom(), message)
        else:
            bot.send_message(message.chat.id, 'Сори, сейчас выполняется другой запрос')
    if message.text == 'Из топа':
        if cnt == 0:
            getFilmTop(message)
        else:
            bot.send_message(message.chat.id, 'Сори, сейчас выполняется другой запрос')
    if message.text == 'Фильтры':
        if cnt == 0:
            getFilters(message)
        else:
            bot.send_message(message.chat.id, 'Сори, сейчас выполняется другой запрос')
    if 'G:' in message.text:
        if cnt == 0:
            getGenre(message)
        else:
            bot.send_message(message.chat.id, 'Сори, сейчас выполняется другой запрос')
    if '_' in message.text:
        if cnt == 0:
            if Genre == '0':
                bot.send_message(message.chat.id, 'Вы не выбрали жанр, начните сначала 😅')
            getYear(message)
        else:
            bot.send_message(message.chat.id, 'Сори, сейчас выполняется другой запрос')
    if 'C:' in message.text:
        if cnt == 0:
            if Genre == '0' or YearEn == '0' or YearSt == '0':
                bot.send_message(message.chat.id, 'Вы не выбрали жанр или год, начните сначала 😅')
            getContry(message)
        else:
            bot.send_message(message.chat.id, 'Сори, сейчас выполняется другой запрос')



def getFilters(message):
    global cnt
    cnt = 1
    key = types.ReplyKeyboardMarkup()
    key.row('G:Криминал', 'G:Фентези', 'G:Детектив')
    key.row('G:Триллер', 'G:Мультфильм', 'G:Боевик')
    key.row('G:Комедия', 'G:Ужасы', 'G:Драма')
    key.row('К началу')
    bot.send_message(message.chat.id, 'Выберите жанр', reply_markup=key)
    cnt = 0



def getGenre(message):
    global cnt
    global Genre
    cnt = 1
    Genre = message.text
    key = types.ReplyKeyboardMarkup()
    key.row('К началу')
    bot.send_message(message.chat.id, 'Введите веременной период через <b>подчёркивание</b>, '
                                      'например\n<b>1995_2005</b>',parse_mode='HTML', reply_markup=key)
    cnt = 0


def getYear(message):
    global YearSt
    global YearEn
    global cnt
    cnt = 1
    try:
        YearSt, YearEn = message.text.split('_')
        key = types.ReplyKeyboardMarkup()
        key.row('C:Франция', 'C:Испания', 'C:Италия')
        key.row('C:Индия', 'C:Великобритания', 'C:СССР')
        key.row('C:Япония', 'C:США', 'C:Россия')
        key.row('К началу')
        bot.send_message(message.chat.id, 'Выберите страну', reply_markup=key)
    except:
        YearSt, YearEn = '0', '0'
        bot.send_message(message.chat.id, 'Вы ввели некорректные данные, повторите ввод снова')
        getGenre(message)
    cnt = 0


def getContry(message):
    global Contry
    global cnt
    cnt = 1
    Contry = message.text
    getScheduleFilters(getFilmsFilters(message), message)
    cnt = 0


def getFilmsFilters(message):
    global Genre, YearSt, YearEn, Contry
    global cnt
    cnt = 1
    _, genre = Genre.split(':')
    _, contry = Contry.split(':')

    if contry == 'США':
        contry = '1'
    elif contry == 'Франция':
        contry = '8'
    elif contry == 'Россия':
        contry = '2'
    elif contry == 'СССР':
        contry = '13'
    elif contry == 'Испания':
        contry = '15'
    elif contry == 'Италия':
        contry = '14'
    elif contry == 'Индия':
        contry = '29'
    elif contry == 'Великобритания':
        contry = '11'
    elif contry == 'Япония':
        contry = '9'

    if genre == 'Криминал':
        genre = '16'
    elif genre == 'Фентези':
        genre = '5'
    elif genre == 'Детектив':
        genre = '17'
    elif genre == 'Триллер':
        genre = '4'
    elif genre == 'Мультфильм':
        genre = '14'
    elif genre == 'Боевик':
        genre = '3'
    elif genre == 'Комедия':
        genre = '6'
    elif genre == 'Ужасы':
        genre = '1'
    elif genre == 'Драма':
        genre = '8'

    url = config.domainNav.format(genre, contry, YearSt, YearEn)
    print(url)
    try:
        web_page = requests.get(url).text
        web_page = BeautifulSoup(web_page, 'html5lib')
    except:
        bot.send_message(message.chat.id, 'Что-то пошло не так, попробуйте сначала')
    cnt = 0
    return web_page


def getScheduleFilters(Web_page, message):
    global cnt
    cnt = 1
    try:
        web_page = Web_page
        table = web_page.find('div', attrs={'id':'itemList'}).find_all('div', attrs={'class':'item _NO_HIGHLIGHT_'})
        num = random.randint(0, 99)
        text_info = table[num].find('div', attrs={'class':'info'})
        title = text_info.find('div', attrs={'class': 'name'}).find('a').get_text()
        others = text_info.find('div', attrs={'class': 'name'}).find('span').get_text()
        try:
            alter_name, _ = others.split(' (')
        except:
            alter_name = 'Отсутствует'
        year, _ = others.split(')')
        _, year = year.split('(')
        _, time = others.split(') ')
        others = text_info.find('span', attrs={'class': 'gray_text'}).get_text().replace('\n', '')
        contry, _ = others.split('реж.')
        contry = contry.replace(' ', '')
        if ',' in contry:
            contry = contry.replace(',', '')

        producer, _ = others.split('(')
        _, producer = producer.split('реж. ')
        producer = producer.replace('  ', '')
        genres, _ = others.split(')')
        _, genres = genres.split('(')
        url = config.defaultURL + text_info.find('div', attrs={'class': 'name'}).find('a').get('href')
        _, id = table[num].find('img').get('src').split('sm_film/')
        id, _ = id.split('.')
        img_url = 'https://st.kp.yandex.net/images/film_iphone/iphone360_{0}.jpg'.format(id)
        url_yt = 'https://www.youtube.com/results?search_query='
        title_yt = title.replace(' ', '+')
        url_yt += title_yt + '+трейлер'
        hdrezka = config.hdrezkaURL + title.replace(' ', '_')

        film_text = '<b>Информация о фильме:😁</b>\n\n'
        film_text += '<b>Название: </b>' + title + '\n<b>Жанр: </b>' + genres + '\n<b>Страна: </b>' + contry + \
                 '\n<b>Год: </b>' + year + '\n<b>Длительность: </b>' + time + '\n<b>Название (ориг.): </b>' + alter_name + \
                 '\n<b>Режиссёр: </b>' + producer + '\n<b>Инфо на "Кинопоиске": </b>' + url + '\n<b>Трейлер на YouTube: </b>' + \
                 url_yt + '\n<b>Посмотреть на www.hdrezka.ru: </b>' + hdrezka + '\n'

        bot.send_photo(message.chat.id, img_url)
        bot.send_message(message.chat.id, film_text, parse_mode='HTML')
    except:
        bot.send_message(message.chat.id, 'Что-то пошло не так, попробуйте сначала')
    cnt = 0


def getFilmTop(message):
    global cnt
    cnt = 1
    url = config.domainTop
    web_page = requests.get(url).text
    web_page = BeautifulSoup(web_page, 'html5lib')
    table = web_page.find('table', attrs={'id':'itemList'}).find_all('tr')
    num = random.randint(0,99)
    film_info = table[num]
    title = film_info.find('a', attrs={'class':'all'}).get_text()
    others = film_info.find('span', attrs={'style':'color: #888; font-family: arial; font-size: 11px;'
                                                       ' display: block'}).get_text()
    try:
        alter_name, _ = others.split(' (')
    except:
        alter_name = 'Отсутствует'
    year, _ = others.split(')')
    _, year = year.split('(')
    _, time = others.split(') ')
    others = film_info.find('span', attrs={'class', 'gray_text'}).get_text().replace('\n', '')
    contry, _ = others.split('реж.')
    contry = contry.replace(' ', '')
    if ',' in contry:
        contry = contry.replace(',', '')

    producer, _ = others.split('(')
    _, producer = producer.split('реж. ')
    producer = producer.replace('  ', '')
    genres, _ = others.split(')')
    _, genres = genres.split('(')
    url = config.defaultURL + film_info.find('a', attrs={'class':'all'}).get('href')
    _, id = film_info.find('img').get('title').split('sm_film/')
    id, _ = id.split('.')
    img_url = 'https://st.kp.yandex.net/images/film_iphone/iphone360_{0}.jpg'.format(id)
    url_yt = 'https://www.youtube.com/results?search_query='
    title_yt = title.replace(' ', '+')
    url_yt += title_yt + '+трейлер'
    hdrezka = config.hdrezkaURL + title.replace(' ', '_')

    film_text = '<b>Информация о фильме:😁</b>\n\n'
    film_text += '<b>Название: </b>' + title + '\n<b>Жанр: </b>' + genres + '\n<b>Страна: </b>' + contry + \
                 '\n<b>Год: </b>' + year + '\n<b>Длительность: </b>' + time + '\n<b>Название (ориг.): </b>' + alter_name + \
                 '\n<b>Режиссёр: </b>' + producer + '\n<b>Инфо на "Кинопоиске": </b>' + url + '\n<b>Трейлер на YouTube: </b>' + \
                 url_yt + '\n<b>Посмотреть на www.hdrezka.ru: </b>' + hdrezka + '\n'

    bot.send_photo(message.chat.id, img_url)
    bot.send_message(message.chat.id, film_text, parse_mode='HTML')
    cnt = 0


def getScheduleRandom(Web_page, message):
    global cnt
    cnt = 1
    # key = types.ReplyKeyboardMarkup()
    # key.row('По новой "Рандом"')
    # key.row('К началу')

    web_page, url = Web_page

    all_info = web_page.find("div", attrs={"class": "b-object-summary"})

    title = all_info.find('div', attrs={'class': 'b-object-header'}).find('h1').get_text().split()[1:]
    titleNew = ''
    for i in title:
        titleNew += i + ' '

    try:
        alter_title = all_info.find('div', attrs={'class': 'b-object-header'}).find('h2').get_text().split()
        alter_titleNew = ''
        for i in alter_title:
            alter_titleNew += i + ' '
    except:
        alter_titleNew = 'Отсутствует'

    genresN = ''
    genres = all_info.find('div', attrs={'class': 'b-tags'}).get_text().split()
    for i in genres:
        genresN += i + ' '

    producer = all_info.find('div', attrs={'class': 'm-margin-btm'}).find('span').get_text()

    others= all_info.find('span', attrs={'class': 'creation'}).get_text()[:-1].split(', ')
    contry = others[0]
    time = others[-1]
    year = others[-2]


    url_yt = 'https://www.youtube.com/results?search_query='
    title_yt = titleNew.replace(' ', '+')
    url_yt += title_yt + 'трейлер'
    hdrezka = config.hdrezkaURL + titleNew.replace(' ', '_')

    film_text = '<b>Случайный фильм😁: </b>\n\n'
    film_text += '<b>Название: </b>' + titleNew + '\n<b>Жанр: </b>' + genresN + '\n<b>Страна: </b>' + contry + \
                 '\n<b>Год: </b>' + year + '\n<b>Длительность: </b>' + time + '\n<b>Название (ориг.): </b>' + alter_titleNew + \
                 '\n<b>Режиссёр: </b>' + producer + '\n<b>Инфо на "Афише": </b>' + url + '\n<b>Трейлер на YouTube: </b>' + \
                 url_yt + '\n<b>Посмотреть на www.hdrezka.ru: </b>' + hdrezka + '\n'
    web_photo = url + '/photo'
    web_photo = requests.get(web_photo).text
    web_photo = BeautifulSoup(web_photo, 'html5lib')
    try:
        img = web_photo.find('div', attrs={'class':'wrimg selected'}).find('img', attrs={'class':'photo'}).get('src')
        img = img.replace('100x100', '300x300')
        if img is None:
            img = 'http://gpsnew.ru/images/products/no_picture.jpg'
    except:
        img = 'http://gpsnew.ru/images/products/no_picture.jpg'
        print(img)
    bot.send_photo(message.chat.id, img)
    bot.send_message(message.chat.id, film_text, parse_mode='HTML')
    cnt = 0


def getFilmRandom():
    global cnt
    cnt = 1
    url = config.domainRandom + '20'
    randState = str(random.randrange(1000, 10000))
    url += randState
    print(url)
    web_page = requests.get(url).text
    web_page = BeautifulSoup(web_page, 'html5lib')
    ToDpage = web_page.get_text()
    ToD = True
    if 'Увы, такой страницы не существует. Возможно ссылка,' in ToDpage:
        ToD = False
    while not ToD:
        time.sleep(0.5)
        url = config.domainRandom + '20'
        randState = str(random.randrange(1000, 10000))
        url += randState
        print(url)
        web_page = requests.get(url).text
        web_page = BeautifulSoup(web_page, 'html5lib')
        ToDpage = web_page.get_text()
        ToD = True
        if 'Увы, такой страницы не существует. Возможно ссылка,' in ToDpage:
            ToD = False
    cnt = 0
    return web_page, url


def getFilmBySearch(message):
    global cnt
    cnt = 1
    nameFilm = message.text[1:]
    response = config.domainSearch + nameFilm
    query = requests.get(response).text
    cnt = 0
    return query, message


def getScheduleSearch(web_page):
    global cnt
    cnt = 1
    try:
        #К сожалению, по вашему запросу ничего не найдено...
        web_page, message = web_page
        web = BeautifulSoup(web_page, "html5lib")

        all_info = web.find("div", attrs={"class": "element most_wanted"}).find('div', attrs={'class': 'info'})

        spec_url = all_info.find("a", attrs={"class": "js-serp-metrika"}).get('href')
        url = 'https://www.kinopoisk.ru'
        url += spec_url

        title = all_info.find("a", attrs={"class": "js-serp-metrika"}).get_text()
        year = all_info.find("span", attrs={'class':'year'}).get_text()
        grey_info = all_info.find_all('span', attrs={'class':'gray'})[:-1]
        try:
            alter_name, time = grey_info[0].get_text().split(', ')
        except:
            alter_name, time = 'Отсутствует', grey_info[0].get_text()
        try:
            contry , _ = grey_info[1].get_text().split(', реж')
        except:
            contry, _ = grey_info[1].get_text().split(' реж')
        try:
            producer = grey_info[1].find('a', attrs={'data-type': 'film'}).get_text()
        except:
            producer = grey_info[1].find('a', attrs={'data-type': 'series'}).get_text()
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
        hdrezka = config.hdrezkaURL + title.replace(' ', '_')

        film_text = '<b>Информация о фильме😁:</b>\n\n'
        film_text += '<b>Название: </b>'+title+'\n<b>Жанр: </b>'+genres+'\n<b>Страна: </b>'+contry+\
                    '\n<b>Год: </b>'+year+'\n<b>Длительность: </b>'+time+'\n<b>Название (ориг.): </b>'+alter_name+\
                    '\n<b>Режиссёр: </b>'+producer+'\n<b>Инфо на "Кинопоиске": </b>'+url+'\n<b>Трейлер на YouTube: </b>'+\
                     url_yt+'\n<b>Посмотреть на www.hdrezka.ru: </b>' + hdrezka + '\n'

        bot.send_photo(message.chat.id, img_url)
        bot.send_message(message.chat.id, film_text, parse_mode='HTML')
    except:
        bot.send_message(message.chat.id, 'Сори, я не смог найти такой фильм 😓', parse_mode='HTML')
    cnt = 0



def recommendFilm(message):
    global cnt
    cnt = 1
    key = types.ReplyKeyboardMarkup()
    key.row('Из топа', 'Случайный')
    key.row('Фильтры')
    key.row('К началу')
    bot.send_message(message.chat.id, 'Выберите 1 из следующих опций:', reply_markup=key)
    cnt = 0


def searchFilm(message):
    global cnt
    cnt = 1
    bot.send_message(message.chat.id, 'Введите название фильма через <b>дефис</b>, например:'
                                      ' <b>\n-Гарри Поттер</b>', parse_mode='HTML')
    cnt = 0


if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except:
            pass