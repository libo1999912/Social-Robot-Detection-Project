import json
import csv
from datetime import datetime, timedelta
from collections import Counter

# 读取第一个JSON文件
with open("0624-500个随机用户全日发文数据.json", 'r', encoding="utf-8") as f:
    data = json.load(f)

# 构建结果列表
results = []
for item in data:
    user_id = item["_source"]["author_id"]
    username = item["_source"]["author_name"]
    comment = item["_source"]["cont"]
    timestamp = item["_source"]["pt"] // 1000  # 将时间戳精确到秒
    timestamp = datetime.fromtimestamp(timestamp)  # 将时间戳转换为时间
    results.append([user_id, username, comment, timestamp])

# 统计用户ID出现次数
user_id_counts = Counter(item[0] for item in results)

# 按照出现次数、用户ID和时间降序排序
results = sorted(results, key=lambda x: (user_id_counts[x[0]], x[0], x[3]), reverse=True)
#results = sorted(results, key=lambda x: (user_id_counts[x[0]], x[0], x[3]))


# 计算时间间隔并添加到结果列表
user_intervals = {}
user_interval_counts = Counter()
for i in range(1, len(results)):
    if results[i][0] == results[i-1][0]:  # 只计算相同用户之间的时间间隔
        time_diff = results[i][3] - results[i-1][3]
        time_diff_seconds = time_diff.total_seconds()  # 将时间间隔转换为秒数
        results[i].append(time_diff_seconds)

        # 保存每个用户的时间间隔
        user_id = results[i][0]
        user_intervals.setdefault(user_id, []).append(time_diff_seconds)
        user_interval_counts[user_id] += 1

# 写入结果到CSV文件
with open("评论时间间隔.csv", 'w', encoding="utf-8-sig", newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["用户ID", "用户名", "评论内容", "时间戳", "时间间隔（秒）"])  # 写入CSV文件头部
    writer.writerows(results)  # 写入数据行

# 判断时间间隔短的用户
def count_interval_less_than_5(intervals):
    count = 0
    for interval in intervals:
        if interval < 5:
            count += 1
            if count >= 5:
                return True
        else:
            count = 0
    return False

# 统计时间间隔短的用户
short_interval_users = [user_id for user_id, intervals in user_intervals.items() if count_interval_less_than_5(intervals)]

# 写入时间间隔短的用户到CSV文件
with open("时间间隔短的用户.csv", 'w', encoding="utf-8-sig", newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["用户ID", "连续小于5秒的次数"])  # 写入CSV文件头部
    for user_id in short_interval_users:
        intervals = user_intervals[user_id]
        count = 0
        max_count = 0
        for interval in intervals:
            if abs(interval) < 5:  # 取绝对值后与5进行比较
                count += 1
                if count > max_count:
                    max_count = count
            else:
                count = 0
        writer.writerow([user_id, max_count])  # 写入用户ID和连续小于5秒的次数





