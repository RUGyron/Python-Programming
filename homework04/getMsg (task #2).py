import webbrowser
import argparse
import requests
import json
import time
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
from datetime import datetime
from copy import deepcopy
from get_response import get_response


def getMsg(user_idMsg):
    domain = "https://api.vk.com/method"
    my_token = "6277a1bfa5c4b7e06368583e97b436ffe762dcbc78eaa252a5cd3ccb04a43eaf6b2d4236d62f910259787"
    rev = 1
    API_key = 'E1Jq5ZJhZI13KGonkkRa'

    query_params = {
        'domain': domain,
        'my_token': my_token,
        'user_idMsg': user_idMsg
    }        

    query = "{domain}/messages.getHistory?access_token={my_token}&user_id={user_idMsg}&v=5.53".format(**query_params)
    response = get_response(requests.get(query))

    plotly.tools.set_credentials_file(username='RUGyron', api_key=API_key)

    amount = response.json()['response']['count']
    count = amount
    cnt = count
    n = count // 200
    Msg = []
    count = 200

    if n == 0:
        n += 1
        count = cnt
    for elem in range(n):
        offset = 200*elem

        query_params = {
            'domain': domain,
            'my_token': my_token,
            'user_idMsg': user_idMsg,
            'fieldsMsg': 'date, body',
            'offset': offset,
            'count': count,
            'rev': rev
        }        

        query = "{domain}/messages.getHistory?access_token={my_token}&user_id={user_idMsg}&fields={" \
                "fieldsMsg}&v=5.53&count={count}&offset={offset}&rev={rev}".format(**query_params)
        response = get_response(requests.get(query))
        messages = response.json()['response']['items']
        numb = str((offset/amount)*100)
        print(numb[:numb.index('.')+2], '%')
        for i in range(count):
            try:
                time.sleep(0.001)
                Msg.append(datetime.fromtimestamp(messages[i]['date']).strftime("%Y-%m-%d"))
            except:
                continue

        if elem == n-1:
            print('100.0 %')

    X = ['0']
    for i in Msg:
        if X[-1] != i:
            X.append(i)
    X = X[1:]
    cur = Msg[0]
    cnt = 0

    Y = []
    for i in Msg:
        if cur == i:
            cnt += 1
        elif cur != i:
            Y.append(cnt)
            cur = i
            cnt = 1
    Y.append(cnt)
    data = [go.Scatter(x=X, y=Y)]
    py.iplot(data)


if __name__ == '__main__':
    getMsg(148255980)
