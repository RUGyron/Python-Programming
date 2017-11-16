import argparse
import webbrowser
import requests
from pprint import pprint as pp
from collections import Counter
from get_response import get_response


domain = "https://api.vk.com/method"
access_token = '3245beaa3245beaa3245beaa96321aacd8332453245beaa6ba82386c1441514b0e63b51'
user_id = '60355185'

def getFriends(user_id=60355185):
    query_params = {
        'domain' : domain,
        'access_token': access_token,
        'user_id': user_id,
        'fields': 'bdate'
    }

    query = "https://api.vk.com/method/friends.get?fields={fields}&access_token={access_token}&v=5.53&user_id={user_id}".format(**query_params)
    response = get_response(requests.get(query))

    friends = response.json()['response']['items']
    bdate_list = []
    for i in friends:
        cnt = 0
        try:
            if i['bdate']:
                i['bdate'] = i['bdate'][len(i['bdate'])-4:]
                for j in i['bdate']:
                    if j == '.':
                        cnt = 1
                if cnt == 0 and len(i['bdate']) == 4:
                    bdate_list.append([int(i['bdate'])])
        except:
            continue
    maxi = -1
    for i in bdate_list:
        if bdate_list.count(i) > maxi:
            maxi = bdate_list.count(i)
            maxi_i = i
    if maxi == -1:
        return False
    user_age = 'Predicted age: ' + str(2017 - maxi_i[0])
    iD = 'ID = ' + str(user_id) + ', ' + user_age
    return iD

if __name__ == '__main__':
    print(getFriends(118668698))
