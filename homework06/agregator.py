from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from bs4 import BeautifulSoup
import Classifier2
import requests as r
from bottle import route, run, template, request, redirect

# Создадим БД и сессию для обращения к ней
Base = declarative_base()
engine = create_engine("sqlite:///news.db")
session = sessionmaker(bind=engine)

# Создадим столбцы таблицы в БД и зададим их тип
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

# Передадим все неразмеченные новости из БД в template, к которому можно обратится по ссылке /news
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

# Запушим все спаршенные новости с сайта на наш сайт localhost через сессию и закоммитим
@route('/recommends')
def news_list_recommend():
    neverAr, maybeAr, goodAr = [], [], []
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    rows_fit = s.query(News).filter(News.label != None).all()
    sents = []
    labels = []
    for elem in rows_fit:
        sents.append(elem.title)
        labels.append(elem.label)
    argues = Classifier2.NaiveBayesClassifier.fit(False, sents, labels)
    for elem in rows:
        cur_label = Classifier2.NaiveBayesClassifier.predict(False, elem.title, argues)
        if cur_label == 'never':
            neverAr.append(elem)
        elif cur_label == 'maybe':
            maybeAr.append(elem)
        elif cur_label == 'good':
            goodAr.append(elem)
    new_rows = []
    for elem in goodAr:
        new_rows.append(elem)
    for elem in maybeAr:
        new_rows.append(elem)
    for elem in neverAr:
        new_rows.append(elem)
    return template('news_template', rows=new_rows, lenth=len(rows))

@route('/news')
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    rows.reverse()
    return template('news_template', rows=rows, lenth=len(rows))

def DBnews():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return [{'title': i.title,
             'author': i.author,
             'url': i.url,
             'comments': i.comments,
             'likes': i.likes,
             'label': i.label}for i in rows]
# Создадим функцию, передающую словарь из немаркерованных новостей из БД

# Создадим функцию, передающую словарь из маркерованных новостей из БД
def DBnewsMarked():
    s = session()
    rows = s.query(News).filter(News.label != None).all()
    return [{'title': i.title,
             'author': i.author,
             'url': i.url,
             'comments': i.comments,
             'likes': i.likes,
             'label': i.label}for i in rows]

# Парсим новостную ленту с 1 страницы hackernews.com
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

# Переход на следующую страницу
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

# Парсим все новости с n страниц новостного сайта
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

# Пополним новостную ленту нашего сайта свежими новостями первоисточника
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

# Добавим определенную метку интересности выбранной новости
@route('/add_label/')
def add_label(id=1, label='active'):
    id, label = request.query.id, request.query.label
    s = session()
    note = s.query(News).filter(News.id == id).all()[0]
    note.label = label
    s.commit()
    redirect('/news')

# Необязательная функция
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
    run(host='localhost', port=8080)