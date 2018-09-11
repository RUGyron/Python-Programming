import requests as r
import os
from bs4 import BeautifulSoup

domain = 'http://nudecelebvideo.net'

def get_news_from_page(url):
    web_page = BeautifulSoup(r.get(url).text, 'html5lib')

    all_info = web_page.find('div', attrs={'class': 'full-in'})
    title = all_info.find('h1').get_text()

    gallery = all_info.find_all('center')[0].find('ul', attrs={'class': 'xfieldimagegallery images'})
    try:
        gallery = gallery.find_all('li')
        images = []
        for i in gallery:
            str1 = i.find('img').get('src')
            if len(str1.split('-')[-1]) == 11:
                string = ''
                for elem in str1.split('-')[:-1]:
                    string += elem + '-'
                images.append(domain + string[:-1] + '.jpg')
            else:
                images.append(domain + str1)
        if len(images) > 6:
            images = [images[-1], images[0], images[4], images[5], images[3], images[2]]
    except:
        images = []

    str1 = all_info.find('img').get('src')
    # cur_img_url_ar = cur_img_url.split('-')
    # if len(cur_img_url_ar) == 2:
    #     main_img = domain + cur_img_url
    # elif len(cur_img_url_ar) == 1:
    #     main_img = domain + cur_img_url
    # elif len(cur_img_url_ar) > 2:
    #     main_img = ''
    #     for i in cur_img_url_ar[:-1]:
    #         main_img += i + '-'
    #     main_img = domain + main_img[:-1] + '.jpg'
    if len(str1.split('-')[-1]) == 11:
        string = ''
        for elem in str1.split('-')[:-1]:
            string += elem + '-'
        main_img = domain + string[:-1] + '.jpg'
    else:
        main_img = domain + str1

    try:
        _, Movie = title.split('-')
    except:
        try:
            _, Movie = title.split('–')
        except:
            if len(title.split('-')) == 1:
                Movie = ''
                movie = title.split('–')
                for i in range(len(movie) - 1):
                    Movie += movie[i+1]
            else:
                Movie = ''
                movie = title.split('-')
                for i in range(len(movie) - 1):
                    Movie += movie[i+1]
    try:
        Movie, _ = Movie.split(' (20')
    except:
        try:
            Movie, _ = Movie.split(' (19')
        except:
            try:
                Movie, _ = Movie.split(' ( 20')
            except:
                try:
                    Movie, _ = Movie.split(' ( 19')
                except:
                    Movie = Movie.split(' (')[0]


    if 's0' in Movie:
        Movie = Movie.split('s0')[0]
    if 'S0' in Movie:
        Movie = Movie.split('S0')[0]
    if '[' in Movie:
        Movie = Movie.split('[')[0]

    try:
        starring, _ = title.split('-')
    except:
        try:
            starring, _ = title.split('–')
        except:
            if len(title.split('-')) == 1:
                starring = ''
                Starring = title.split('–')
                for i in range(len(Starring) - 1):
                    starring += '–' + Starring[i]
            else:
                starring = ''
                Starring = title.split('-')
                for i in range(len(Starring) - 1):
                    starring += '-' + Starring[i]
            starring = starring[1:]

    if 's0' in starring:
        starring = starring.split('-')[0].split('–')[0]
    if 'S0' in starring:
        starring = starring.split('-')[0].split('–')[0]
    if 'etc' in starring:
        starring = starring.split('etc')[0]
    if 'others' in starring:
        starring = starring.split('others')[0]
    if ':Behind The Scenes' in starring:
        starring = starring.split(':Behind The Scenes')[0]
    if 'Season' in starring:
        starring = starring.split('Season')[0]
    if 'with BD' in starring:
        starring = starring.split('with BD')[0]
    while starring[-1] == ' ':
        starring = starring[:-1]
    if starring[-1] == ',':
        starring = starring[:-1]
    while starring[0] == ' ':
        starring = starring[1:]

    if 'etc' in Movie:
        Movie = Movie.split('etc')[0]
    if 'others' in Movie:
        Movie = Movie.split('others')[0]
    if ': Behind The Scenes' in Movie:
        Movie = Movie.split(': Behind The Scenes')[0]
    if 'Season' in Movie:
        Movie = Movie.split('Season')[0]
    if 'with BD' in Movie:
        Movie = Movie.split('with BD')[0]
    while Movie[-1] == ' ':
        Movie = Movie[:-1]
    while Movie[0] == ' ':
        Movie = Movie[1:]

    g = all_info.find('div', attrs={'class': 'full-tags'}).find_all('a')
    genres = []
    for i in g:
        genres.append(i.get_text())

    technical_info = all_info.find('div', attrs={'class': 'btn-dl nc-link'}).get_text().split()
    try:
        video = technical_info[1] + ' ' + technical_info[2]
        duration = technical_info[5]
        size = technical_info[-2] + ' ' + technical_info[-1]
    except:
        video = 'None'
        duration = 'None'
        size = 'None'

    download_url = all_info.find_all('a')[1].get('href')
    # download_url = urllib.request.urlopen(download_url).geturl()

    name_of_file = title + '.txt'
    if ('/' in name_of_file): name_of_file = name_of_file.replace('/', ' ')
    if ('|' in name_of_file): name_of_file = name_of_file.replace('|', ' ')
    if ('*' in name_of_file): name_of_file = name_of_file.replace('*', ' ')
    if ('?' in name_of_file): name_of_file = name_of_file.replace('?', ' ')
    if ('"' in name_of_file): name_of_file = name_of_file.replace('"', ' ')
    if (':' in name_of_file): name_of_file = name_of_file.replace(':', ' ')

    if 'filejoker.net' in download_url:
        name_of_file = '+' + name_of_file

    description = all_info.find('div', attrs={'class': 'f-desc full-text clearfix'}).get_text()

    try:
        _, Year = title.split('(20')
        cnt = 0
    except:
        try:
            _, Year = title.split('( 20')
            cnt = 0
        except:
            try:
                _, Year = title.split('( 19')
                cnt = 1
            except:
                try:
                    _, Year = title.split('(19')
                    cnt = 1
                except:
                    try:
                        _, Year = title.split('( 2O')
                        cnt = 0
                    except:
                        try:
                            _, Year = title.split('(2O')
                            cnt = 0
                        except:
                            if len(title.split('(20')) > 2:
                                Year = title.split('(')
                                Year, _ = Year[1].split(')')
                                cnt = 20
                            elif len(title.split('(19')) > 2:
                                Year = Movie.split('(')
                                Year, _ = Year[1].split(')')
                                cnt = 21
                            elif len(title.split('(2O')) > 2:
                                Year = Movie.split('(')
                                Year, _ = Year[1].split(')')
                                cnt = 20


    Year = Year.split(')')
    Year = Year[0]
    if cnt == 1: Year = '19' + Year
    elif cnt == 0: Year = '20' + Year
    OF = {
        'Title': title,
        'Main Image': main_img,
        'Movie': Movie,
        'Year': Year,
        'Starring': starring,
        'Categories': genres,
        'Video': video,
        'Duration': duration,
        'Size': size,
        'Download Link': download_url,
        'Images': images,
        'Description': description
    }

    OF = str(OF)
    OF = OF.replace("'Title'", "\n'Title'").replace("'Year'", "\n'Year'").replace("'Main Image'", "\n'Main Image'")
    OF = OF.replace("'Movie'", "\n'Movie'").replace("'Starring'", "\n'Starring'").replace("'Video'", "\n'Video'")
    OF = OF.replace("'Categories'", "\n'Categories'").replace("'Duration'", "\n'Duration'").replace("'Size'", "\n'Size'")
    OF = OF.replace("'Download Link'", "\n'Download Link'").replace("'Images'", "\n'Images'")
    OF = OF.replace("'Description'", "\n'Description'").replace("}", "\n}")


    with open(name_of_file, 'w', encoding='utf-8') as file:
        print(OF, file=file)

    with open(name_of_file, 'r', encoding='utf-8') as file:
        doc = file.read()
    if '{' in doc: print('"'+title+'"'+' downloaded!')
    else: print('Failed: '+title)

def get_news_list(num_of_page):
    url = 'http://nudecelebvideo.net/page/{}/'.format(num_of_page)
    web_page = BeautifulSoup(r.get(url).text, 'html5lib')

    info = web_page.find('div', attrs={'id': 'dle-content'})
    info = info.find_all('div', attrs={'class': 'thumb'})
    videos = []
    for elem in info:
        videos.append(elem.find('a').get('href'))
    return videos

def get_pages(from_page, to_page):
    from_page, to_page = int(from_page), int(to_page)
    if to_page <= 0 or from_page <=0: return 'numbers of pages must be positive'
    if to_page < from_page: return '"from_page" must be less than "to_page"'
    diff = to_page - from_page
    pages = []
    for i in range(diff + 1):
        pages.append(from_page + i)
    for num_page in pages:
        cnt = 0
        for url in get_news_list(num_page):
            get_news_from_page(url)
            cnt += 1
            print(str(cnt) + '/20')
        print('\n\n' + str(num_page) + ' Page fully downloaded!\n\n')
    return 'All is Done'

if __name__ == '__main__':
    try: os.mkdir('txt')
    except: pass
    os.chdir(os.getcwd() + '/txt')
    print(get_pages(input('from page: '), input('to_page: ')))
    # get_news_from_page('http://nudecelebvideo.net/hd-video/6048-anna-paquin-true-blood-s06e05-06-2013-hd-1080p.html')