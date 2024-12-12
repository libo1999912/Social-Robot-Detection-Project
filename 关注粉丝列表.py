import sys
import time
import traceback
import requests
import json
import pyodbc
import pandas as pd
from tqdm import tqdm

user_ids = []
file = "author_id.txt"
with open(file, 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for line in lines:
        #index,id,name = line.strip().split(',')
        id = line.strip().split(',')[0]
        user_ids.append(id)

#定义了一个名为get_user_related的函数，用于获取用户的关注列表和粉丝列表。
def get_user_related(author_id, page, limit):
    """
    target: 1 获取关注列表，2 获取粉丝列表，3是同时获取关注和粉丝列表
    """
    url = 'http://10.160.94.19:30050/getinfo'        #修改端口号为30050
    payload = {
        'cmd_id': 'ICT_GK_ONLINE_20230210101010_11111',
        'cmd_type': 'query',
        'cmd_content': {
            'cmd_action': 'getuserrllist',
            'cmd_params': [{
                'userid': author_id,
                'limit': f'{limit}',
                'offset': f'{(page-1)*limit}',
                'target': ["3"],
                'asp': 'kuaishou.com'                   #修改asp为kuaishou.com
            }]
        }
    }
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'token': 'eyJhbGciOiJIUzUxMiIsInppcCI6IkdaSVAifQ.H4sIAAAAAAAAAKtWKi5NUrJS8nQOiXf3jvf38_H0c1XSUUqtKFCyMjQzNzc1NzO1tKwFAPYo92soAAAA.b45vJooae0-ZWwUH0hUL9R8zrwyepkmwwj7WMWXb6MyfIP4BGDOAtSk1LXZI4MdMkSuYNjsjkYVmx0ia-UsEUA'
    }
    response = requests.post(url=url, headers=headers, json=payload, timeout=50)
    res = json.loads(response.text)
    print(res)
    gz_ids = res['rst_content'][0]['relatealist']
    fs_ids = res['rst_content'][0]['fansalist']
    gz_ids = [str(id) for id in gz_ids] if gz_ids else []
    fs_ids = [str(id) for id in fs_ids] if fs_ids else []
    return gz_ids, fs_ids


for userid in tqdm(user_ids):
    try:
        gz_ids, fs_ids = get_user_related(userid, 1, 100)
        print("关注: ", gz_ids)
        print("粉丝: ", fs_ids)
    except:
        traceback.print_exc()
