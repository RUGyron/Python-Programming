import igraph
import plotly
import plotly.graph_objs as go
import plotly.plotly as py
import random
import requests
import time
from datetime import datetime


access_token = '3245beaa3245beaa3245beaa96321aacd8332453245beaa6ba82386c1441514b0e63b51'
domain = "https://api.vk.com/method"


def get(response, timeout=5, max_retries=5, backoff_factor=0.3):
    delay = 0
    for i in range(max_retries):
        try:
            query = response
            return query
        except:
            pass
        time.sleep(delay)
        dalay = min(delay * backoff_factor, timeout)
        delay += random.random()
    raise ConnectionError("Error of connection")


def age_predict(user_id=60355185):
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"
    query_params = {
        'domain': domain,
        'access_token': access_token,
        'user_id': user_id,
        'fields': 'bdate'
    }
    friends = get_friends(user_id)
    bdate_list = []
    user_query = "https://api.vk.com/method/users.get?user_ids={0}&v=5.69".format(user_id)
    user_response = '(' + get(requests.get(user_query)).json()['response'][0]['first_name'] +\
                    ' ' + get(requests.get(user_query)).json()['response'][0]['last_name'] + ')'
    for i in friends:
        cnt = 0
        try:
            if i[2]:
                i[2] = i[2][len(i[2])-4:]
                for j in i[2]:
                    if j == '.':
                        cnt = 1
                if cnt == 0 and len(i[2]) == 4:
                    bdate_list.append([int(i[2])])
        except:
            continue
    maxi = -1
    for i in bdate_list:
        if bdate_list.count(i) > maxi:
            maxi = bdate_list.count(i)
            maxi_i = i
    if maxi == -1:
        return False
    return 'ID = ' + str(user_id) + ' ' + user_response + ', ' + 'Predicted age: ' + str(2017 - maxi_i[0])


def messages_get_history(user_idMsg=60355185, offset=0, count=20):
    assert isinstance(user_idMsg, int), "user_id must be positive integer"
    assert user_idMsg > 0, "user_id must be positive integer"
    my_token = "8430c495169af2fe767fd04ffcc33880df7ad17cf6c3fc71d2508fe173bed1850aa1985ccbb144e66b84d"
    rev = 1
    API_key = 'E1Jq5ZJhZI13KGonkkRa'
    query_params = {
        'domain': domain,
        'my_token': my_token,
        'user_idMsg': user_idMsg
    }
    query = "{domain}/messages.getHistory?access_token={my_token}&user_id={user_idMsg}&v=5.53".format(**query_params)
    response = get(requests.get(query))
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
        offset = 200 * elem
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
        messages = get(requests.get(query)).json()['response']['items']
        for i in range(count):
            try:
                Msg.append((messages[i]['from_id'], messages[i]['from_id']))
            except:
                time.sleep(0.001)
                Msg.append((messages[i]['from_id'], messages[i]['from_id']))
    return messages


def count_dates_from_messages(user_idMsg=60355185):
    assert isinstance(user_idMsg, int), "user_id must be positive integer"
    assert user_idMsg > 0, "user_id must be positive integer"
    my_token = "8430c495169af2fe767fd04ffcc33880df7ad17cf6c3fc71d2508fe173bed1850aa1985ccbb144e66b84d"
    rev = 1
    API_key = 'E1Jq5ZJhZI13KGonkkRa'
    query_params = {
        'domain': domain,
        'my_token': my_token,
        'user_idMsg': user_idMsg
    }
    query = "{domain}/messages.getHistory?access_token={my_token}&user_id={user_idMsg}&v=5.53".format(**query_params)
    response = get(requests.get(query))
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
        response = get(requests.get(query))
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
    return X, Y


def plotly_messages_freq(user_idMsg=60355185):
    X, Y = count_dates_from_messages(user_idMsg)
    return [go.Scatter(x=X, y=Y)]

def get_friends(user_id):
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"
    query_params = {
        'domain': domain,
        'access_token': access_token,
        'user_id': user_id,
        'fields': 'bdate'
    }
    query = "https://api.vk.com/method/friends.get?fields={fields}&access_token={access_token}&v=5.53&user_id={user_id}".format(
        **query_params)
    response = get(requests.get(query))

    try:
        friends = response.json()['response']['items']
    except:
        return False
    bdate_list = []
    for i in friends:
        try:
            time.sleep(0.0008)
            bdate_list.append([i['id'], i['last_name'], i['bdate']])
        except:
            try:
                bdate_list.append([i['id'], i['last_name']])
            except:
                continue
    return bdate_list


def get_network(user_id=60355185):
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"
    vertices = [c[0] for c in get_friends(user_id)]
    verticesN = [c[1] for c in get_friends(user_id)]
    N = len(vertices)
    edges = []
    for elem in range(N):
        print(elem + 1, '/', len(vertices), verticesN[elem])
        if get_friends(vertices[elem]) is False:
            continue
        uFriends = [c[0] for c in get_friends(vertices[elem])]
        uFriendsN = [c[1] for c in get_friends(vertices[elem])]
        for i in range(N):
            if vertices[i] in uFriends:
                edges.append((elem, i))
    g = igraph.Graph(vertex_attrs={"label": verticesN},
                     edges=edges, directed=False)
    visual_style = {}
    visual_style["vertex_size"] = 15
    visual_style["vertex_color"] = 'green'
    visual_style["vertex_label"] = g.vs["label"]
    visual_style["bbox"] = (1000, 1000)
    visual_style["margin"] = 100
    visual_style["edge_color"] = "grey"
    visual_style["vertex_label_dist"] = 2
    visual_style["layout"] = g.layout_fruchterman_reingold(
        maxiter=1000,
        area=N ** 3,
        repulserad=N ** 3)

    g.simplify(multiple=True, loops=True)
    igraph.plot(g, **visual_style)
    return edges


if __name__ == '__main__':
    print(age_predict(56200185))
    print('----------')
    print(get_network(56200185))
    print('----------')
    print(plotly_messages_freq(56200185))
