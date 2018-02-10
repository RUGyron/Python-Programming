from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from bs4 import BeautifulSoup
import requests as r
import html5lib
from bottle import route, run, template, request, redirect

Base = declarative_base()
engine = create_engine("sqlite:///news.db")
session = sessionmaker(bind=engine)

class News(Base):
    __tablename__ = "news"
    id = Column(Integer, primary_key = True)
    title = Column(String)
    author = Column(String)
    url = Column(String)
    comments = Column(Integer)
    likes = Column(Integer)
    label = Column(String)

Base.metadata.create_all(bind=engine)


@route('/news')
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    rows.reverse()
    return template('news_template', rows=rows, lenth=len(rows))


def add_news(instance):
    s = session()
    news = News(title=instance['title'],
                author=instance['author'],
                url=instance['url'],
                comments=instance['comments'],
                likes=instance['likes'])
    s.add(news)
    s.commit()
    return None

def DBnews():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return [{'title': i.title,
             'author': i.author,
             'url': i.url,
             'comments': i.comments,
             'likes': i.likes,
             'label': i.label}for i in rows]

def DBnewsMarked():
    s = session()
    rows = s.query(News).filter(News.label != None).all()
    return [{'title': i.title,
             'author': i.author,
             'url': i.url,
             'comments': i.comments,
             'likes': i.likes,
             'label': i.label}for i in rows]

def extract_news(url):
    # Спарсим целиком страницу и преобразуем ее с помощью модуля BS4 с возможностью искать и обращаться к тэгам
    web_page = r.get(url).text
    web_page = BeautifulSoup(web_page, 'html5lib')
    # Сузим область поиска новостей до основных кликбэйтов и подтекста к ним
    main_texts = web_page.find_all('tr', attrs={'class': 'athing'})
    sub_texts = web_page.find_all('td', attrs={'class': 'subtext'})
    # Проверим, что кол-во кликбейтов совпадает с кол-вом подтекстов к ним

    # Создадим пустой список для будущего хранения в нем списка новостей
    news_list = []

    # Создадим счетчик внутри цикла, чтобы парсить по каждой новости за раз
    cnt = 0

    # Создадим бесконечный цикл, выходом из которого будет служить невозможность спарсить новость
    # (конец новостной ленты)
    while True:
        try:
            news_list.append({'url': main_texts[cnt].find('span', attrs={'class': 'sitestr'}).get_text(),
                              'title': main_texts[cnt].find('a', attrs={'class': 'storylink'}).get_text(),
                              'author': sub_texts[cnt].find('a', attrs={'class': 'hnuser'}).get_text(),
                              'likes': sub_texts[cnt].find('span').get_text().split()[0],
                              'comments': sub_texts[cnt].find_all('a')[-1].get_text()})
            cnt += 1
        # Не у каждой новости есть ссылка на сторонний источник, поэтому во избежание ошибок и неполного парсинга
        # создадим исключение для "особенных" новостей
        except:
            try:
                news_list.append({'title': main_texts[cnt].find('a', attrs={'class': 'storylink'}).get_text(),
                                  'url': 'None',
                                  'author': sub_texts[cnt].find('a', attrs={'class': 'hnuser'}).get_text(),
                                  'likes': sub_texts[cnt].find('span').get_text().split()[0],
                                  'comments': sub_texts[cnt].find_all('a')[-1].get_text()})
                cnt += 1
            except:
                break
    for i in range(len(news_list)):
        if news_list[i]['comments'] != 'discuss':
            news_list[i]['comments'], _ = news_list[i]['comments'].split('\xa0')
    return news_list


def extract_next_page(url):
    # Спарсим целиком страницу и преобразуем ее с помощью модуля BS4 с возможностью искать и обращаться к тэгам
    web_page = r.get(url).text
    web_page = BeautifulSoup(web_page, 'html5lib')
    # Добудем ссылку на следующую страницу с самой страницы
    try:
        return 'https://news.ycombinator.com/' +\
               web_page.find_all('td', attrs={'class': 'title'})[-1].find('a').get('href')
    # Создадим исключение на случай, если следующей страницы нет
    except:
        return None

def get_news(url, num_pages=1):
    # Создадим пустой список для хранения новостной ленты
    news_list = []
    # Создадим цикл для добавления новостей с i страниц
    for i in range(num_pages):
        next_page_url = extract_next_page(url)
        # Проверим, не является ли данная страница последней
        if next_page_url != None:
            cur_news_list = extract_news(url)
            for elem in range(len(cur_news_list)):
                news_list.append(cur_news_list[elem])
            url = next_page_url
        else:
            break
    return news_list

@route('/update_news')
def update_news():
    news_list = get_news('https://news.ycombinator.com/newest')
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    rows.reverse()
    bd_title_list = []
    for row in rows:
        bd_title_list.append(row.title)
    for i in news_list:
        if i['title'] not in bd_title_list:
            add_news(i)
    redirect('/news')


@route('/add_label/')
def add_label(id=1, label='active'):
    id, label = request.query.id, request.query.label
    s = session()
    note = s.query(News).filter(News.id == id).all()[0]
    note.label = label
    s.commit()
    redirect('/news')


def add_unread_news(url, num_pages):
    news_list = get_news(url, num_pages)
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    bd_title_list = []
    for row in rows:
        bd_title_list.append(row.title)
    for i in news_list:
        if i['title'] not in bd_title_list:
            add_news(i)


if __name__ == '__main__':
    # add_unread_news('https://news.ycombinator.com/newest', 34)
    # update_news('https://news.ycombinator.com/newest')
    run(host='localhost', port=8080)