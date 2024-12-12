import json
import csv
import datetime
from collections import Counter

# 读取第一个JSON文件
with open("0624-500个随机用户全日发文数据.json", 'r', encoding="utf-8") as f:
    data = json.load(f)


# 统计用户ID出现次数
user_id_counts = Counter(item["_source"]["author_id"] for item in data)

# 获取出现频次前100的用户ID
top_100_user_ids = [user_id for user_id, count in user_id_counts.most_common(100)]

# 构建用户ID、用户名、出现次数、评论类型、时间和评论内容的列表
results = []
for item in data:
    user_id = item["_source"]["author_id"]
    if user_id in top_100_user_ids:
        username = item["_source"]["author_name"]
        msg_type = item["_source"]["msg_type"]  # 将 "msg_type" 替换为实际的评论类型字段名
        comment_time = datetime.datetime.fromtimestamp(item["_source"]["pt"] / 1000)  # 将时间戳转换为时间
        comment_text = item["_source"]["cont"]  # 将 "cont" 替换为实际的评论内容字段名
        user_count = user_id_counts[user_id]
        father_msg_type = item["_source"]["father_msg_type"]  # 将 "father_msg_type" 替换为实际的父节点类型字段名
        lvideo = item["_source"]["lvideo"]

        results.append([user_id, username, user_count, msg_type, comment_time, comment_text,father_msg_type,lvideo])

# 按出现次数降序和用户ID升序排序
results = sorted(results, key=lambda x: (x[2], x[0]), reverse=True)

# 写入结果到CSV文件
with open("0624-500个随机用户全日发文数据.csv", 'w', encoding="utf-8-sig", newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["用户ID", "用户名", "出现次数", "评论类型（11代表评论，12代表发文标题）", "发文及评论时间", "评论内容", "父节点类型（11代表评论，12代表发文标题，13代表直播）","原视频"])  # 写入CSV文件头部
    writer.writerows(results)  # 写入数据行

