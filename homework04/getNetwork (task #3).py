from igraph import Graph, plot, layout
import numpy as np
import requests
import time
from get_response import get_response


def getFriends(user_id):
    domain = "https://api.vk.com/method"
    access_token = '3245beaa3245beaa3245beaa96321aacd8332453245beaa6ba82386c1441514b0e63b51'
    query_params = {
        'domain': domain,
        'access_token': access_token,
        'user_id': user_id,
        'fields': 'bdate'
    }
    query = "https://api.vk.com/method/friends.get?fields={fields}&access_token={access_token}&v=5.53&user_id={user_id}".format(**query_params)
    response = get_response(requests.get(query))

    try:
        friends = response.json()['response']['items']
    except:
        return False

    bdate_list = []
    for i in friends:
        try:
            time.sleep(0.0008)
            bdate_list.append((i['id'], i['last_name']))
        except:
            continue
    return bdate_list


def getNetwork(user_id=118668698):
    vertices = [c[0] for c in getFriends(user_id)]
    verticesN = [c[1] for c in getFriends(user_id)]
    N = len(vertices)
    edges = []
    for elem in range(N):
        print(elem, '/', len(vertices), verticesN[elem])
        if getFriends(vertices[elem]) is False:
            continue
        uFriends = [c[0] for c in getFriends(vertices[elem])]
        uFriendsN = [c[1] for c in getFriends(vertices[elem])]
        for i in range(N):
            if vertices[i] in uFriends:
                edges.append((elem, i))

    g = Graph(vertex_attrs={"label": verticesN},
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
    plot(g, **visual_style)


if __name__ == '__main__':
    getNetwork(210922771)
