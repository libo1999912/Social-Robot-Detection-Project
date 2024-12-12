import pandas as pd
import json


def csv_to_json():
    # 读取csv文件
    df = pd.read_csv('6月24号100个机器人的用户评论分析.csv')

    # 创建一个空的字典
    data = {}

    # 遍历每一行数据
    for index, row in df.iterrows():
        user_id = row['用户ID']
        comment = row['评论内容']

        if not pd.isnull(comment):
            # 如果用户ID不存在于字典中，则创建一个新的键值对
            if user_id not in data:
                data[user_id] = []

            # 将评论内容添加到用户ID对应的列表中
            data[user_id].append(comment)

    # 创建包含所有数据的JSON对象
    json_data = json.dumps(data, indent=4,ensure_ascii=False)
    # 将JSON数据写入文件
    with open('6月24号100个机器人的用户评论分析.json', 'w',encoding='utf-8') as file:
        file.write(json_data)

if __name__ == '__main__':
    csv_to_json()