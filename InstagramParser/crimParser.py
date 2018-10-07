from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from bs4 import BeautifulSoup
import requests as r
import time, os
from pprint import pprint as pp

def main():
    if 'data.db' in os.listdir():
        os.remove('data.db')
    cnt = 0
    # Init Database
    Base = declarative_base()
    engine = create_engine('sqlite:///data.db')
    session = sessionmaker(bind=engine)

    class Data(Base):
        __tablename__ = "data"
        ID = Column(Integer, primary_key=True)
        SurName = Column(String)
        Name = Column(String)
        DadName = Column(String)
        Birthday = Column(String)
        Organ = Column(String)
        Phone = Column(String)
        Image_URL = Column(String)

    Base.metadata.create_all(bind=engine)

    if 'data.db' in os.listdir():
        s = session()
        rows = s.query(Data).all()
        id_list = [row.ID for row in rows]
        for elem in id_list:
            if elem > cnt:
                cnt = elem

    counter = [39, 107, 71, 41]
    for count in range(len(counter)):
        for page in range(1, counter[count]+1):
            if count == 0:
                urlAli = 'http://qamqor.gov.kz/portal/page/portal/POPageGroup/Services/Alimony?' \
                      '_piref36_230050_36_230049_230049.__ora_navigState=p_page_cnt=%d&p_page_num=%d&' \
                      '_piref36_230050_36_230049_230049.__ora_navigValues='%(counter[count], page)
                web_page = BeautifulSoup(r.get(urlAli).text, 'html5lib')
            else:
                url = 'http://qamqor.gov.kz/portal/page/portal?_type=portlet&_decoration=false&_providerid=542798125&' \
                      '_portletid=10&_referencepath=122637_PORTLET10_542798125&_pref=36_223092_36_223091_223091&' \
                      '_backurl=http%3A%2F%2Fqamqor.gov.kz%2Fportal%2Fpage%2Fportal%2FPOPageGroup%2FServices%2FSuRet%3F' \
                      '_piref36_223092_36_223091_223091.__ora_navigState%3Dsearch%253Dgallery%2526obl%253D19%2526sureg%253D' \
                      '-1%2526ret_type%253D1%2526eventSubmit_doSearch%253D%2525D0%25259F%2525D0%2525BE%2525D0%2525BA%2525D0' \
                      '%2525B0%2525D0%2525B7%2525D0%2525B0%2525D1%252582%2525D1%25258C%26_piref36_223092_36_223091_223091.' \
                      '__ora_navigValues%3D&_mode=6&_title=SU&__ora_wsrp_state=wsrp%3Anormal&_renderdecoration=false&_atar' \
                      'get=36_223092_36_223091_223091&__ora_type=block'
                data = {
                    'search': 'gallery',
                    'obl': '19',
                    'sureg': '-1',
                    'ret_type': count,
                    'eventSubmit_doSearch': 'gallery',
                    'page_cnt': counter[count],
                    'page_num': page
                }

                web_page = BeautifulSoup(r.post(url, data).text, 'html5lib')

            table = web_page.find('div', attrs={'id': 'service'}).find('div', attrs={'class': 'gallery'}).find_all('li')
            for pearson in table:
                cnt += 1
                info = pearson.find_all('input')
                new_info = [each.get('value') for each in info]
                new_info.append(pearson.find('img').get('src'))
                s = session()
                db_table = Data(
                    ID=cnt,
                    SurName=new_info[0],
                    Name=new_info[1],
                    DadName=new_info[2],
                    Birthday=new_info[3],
                    Organ=new_info[4],
                    Phone=new_info[5],
                    Image_URL=new_info[6]
                )
                s.add(db_table)
                s.commit()
            print(str(page) + ' страниц загружено')




if __name__ == '__main__':
    main()