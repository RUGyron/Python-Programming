import requests
import os
from bs4 import BeautifulSoup

def get_img(image, user_hash, session):
    upload_url = 'http://atvseries.net/engine/ajax/upload.php'
    data = {
        'news_id': 0,
        'imageurl': image,
        'ftpurl': '',
        't_size': 200,
        't_seite': 0,
        'make_thumb': 1,
        'm_size': 450,
        'm_seite': 0,
        'make_medium': 1,
        'make_watermark': 0,
        'area': '',
        'author': 'admin',
        'subaction': 'upload',
        'user_hash': user_hash
            }

    page = str(BeautifulSoup(session.post(upload_url, data).text, 'html5lib'))
    try: return page.split('atvseries.net')[1].split('"')[0].replace('\/', '/')[:-1].split('posts/')[1]
    except: return ''

def upload_1_news(name_of_file):
    with open(name_of_file, 'r', encoding='utf-8') as file:
        news_dict = eval(file.read())

    url_login = 'http://atvseries.net/admin.php?mod=main'
    url_add_news = 'http://atvseries.net/admin.php?mod=addnews&action=addnews'
    data_login = {
        'username': 'admin',
        'password': 'AAAY122abOn+777',
        'subaction': 'dologin',
        'selected_language': 'Russian',
                  }
    data_login = {
        'username': 'admin',
        'password': 'AAAY122abOn+777',
        'subaction': 'dologin',
        'selected_language': 'Russian',
                  }

    s = requests.Session()  # Creating Session
    s.post(url_login, data_login)  # Authorization as admin on web site
    r1 = s.get(url_add_news)  # GET query to "add_news" page

    web_page = BeautifulSoup(r1.text, 'html5lib')
    user_hash = str(web_page.find('form', attrs={'id': 'addnews'}).find_all('input')[-1].get('value'))

    _ ,php_id = str(web_page.find('div', attrs={'id': 'xfield_holder_image'}).find('script').text).split('PHPSESSID')
    php_id = php_id.split('"')[2]

    genre_id = {
        'BUSH': 22,
        'BUTT': 20,
        'CLIPS': 18,
        'EXPLICIT': 21,
        'FULL FRONTAL': 19,
        'HD VIDEO': 14,
        'LESBIAN': 12,
        'MOVIE NUDITY': 13,
        'SEX': 11,
        'STANDART DEFINITION': 17,
        'TOPLESS': 15,
        'TV NUDITY': 16,
        '2018': 1,
        '2017': 2,
        '2016': 3,
        '2015': 4,
        '2014': 5,
        '2013': 6,
        '2012': 7,
        '2011': 8,
        '2010': 9,
        'UNTIL 2009': 10
    }
    genres = [genre_id[elem] for elem in news_dict['Categories']]
    if not news_dict['Year'] in news_dict['Categories'] and not genre_id['UNTIL 2009'] in genres:
        try:
            genres.append(genre_id[news_dict['Year']])
        except:
            genres.append(genre_id['UNTIL 2009'])

    image = get_img(news_dict['Main Image'], user_hash, s)
    images = [get_img(i, user_hash, s) for i in news_dict['Images']]
    imgs = ''
    for url in images:
        imgs += url + ','
    imgs = imgs[:-1]
    if image == '': image = imgs[0]

    tags_cloud_1 = ''
    for i in news_dict['Starring'].split(','):
        tags_cloud_1 += i + ' Nude, '
    tags_cloud = tags_cloud_1 + news_dict['Movie'] + ' Nude Scenes'
    data_add_news = {
        'title': news_dict['Title'],
        'newdate': '',
        'new_author': 'admin',
        'category[]': genres,
        'short_story': '',
        'full_story': news_dict['Description'],
        'xfield[image]': image,
        'xfield[images]': imgs,
        'xfield[format]': news_dict['Video'],
        'xfield[time]': news_dict['Duration'],
        'xfield[size]': news_dict['Size'],
        'xfield[download_link]': news_dict['Download Link'],
        'xfield[kadri]': '',
        'approve': 1,
        'allow_main': 1,
        'allow_rating': 1,
        'allow_br': 1,
        'allow_comm': 1,
        'vote_title': '',
        'frage': '',
        'vote_body': '',
        'catalog_url': '',
        'alt_name': '',
        'tags': tags_cloud,
        'expires': '',
        'expires_action': 0,
        'password': '',
        'meta_title': 'Watch Online - ' + news_dict['Title'],
        'descr': 'Download nude scenes with ' + news_dict['Starring'] + ' in HD',
        'keywords': tags_cloud_1[:-2],
        'group_extra[2]': 0,
        'group_extra[3]': 0,
        'group_extra[4]': 0,
        'group_extra[5]': 0,
        'mod': 'addnews',
        'action': 'doaddnews',
        'user_hash': user_hash
    }

    r2 = s.post(url=url_add_news, data=data_add_news)

    # if 'была успешно добавлена' in r2.text:
    #     print('Success')
    # else:
    #     print('Failed')

def main():
    titles = [elem for elem in os.listdir() if '.txt' in elem]
    cnt = 0
    for elem in titles:
        cnt += 1
        upload_1_news(elem)
        print('"' + elem + '" ' + 'successfully uploaded! (' + str(cnt) + '/' + str(len(os.listdir())) + ')')

if __name__ == '__main__':
    os.chdir(os.getcwd() + '/txt')
    main()
