import json
import csv
from datetime import datetime, timedelta
from collections import Counter
from gensim.models import Word2Vec
import jieba

# 计算发文内容相似度的两个函数
def compute_text_similarity(data):
    similarities = {}
    for user_data in data:
        user_id = user_data["_source"]["author_id"]
        documents = user_data["_source"]["cont"]
        if len(documents) > 1:
            corpus = [jieba.lcut(document, cut_all=True) for document in documents]
            model = Word2Vec(corpus, min_count=1)
            total_similarity = 0.0
            pair_count = 0
            for i in range(len(documents)):
                for j in range(i + 1, len(documents)):
                    text1 = documents[i]
                    text2 = documents[j]
                    similarity = compute_sentence_similarity(model, text1, text2)
                    total_similarity += similarity
                    pair_count += 1

            if pair_count > 0:
                average_similarity = total_similarity / pair_count
            else:
                average_similarity = 0.0
            if user_id not in similarities:
                similarities[user_id] = average_similarity
    return similarities


def compute_sentence_similarity(model, text1, text2):
    tokens1 = jieba.lcut(text1)
    tokens2 = jieba.lcut(text2)
    similarity_sum = 0.0
    pair_count = 0
    for token1 in tokens1:
        for token2 in tokens2:
            if token1 in model.wv.index_to_key and token2 in model.wv.index_to_key:
                similarity = model.wv.similarity(token1, token2)
                similarity_sum += similarity
                pair_count += 1

    if pair_count > 0:
        average_similarity = similarity_sum / pair_count
        return average_similarity
    else:
        return 0.0


# 读取JSON文件
with open("0628-0704-50个机器人全日发文数据.json", 'r', encoding="utf-8") as f:
    data = json.load(f)


# 1.统计每个用户的日发帖量
user_post_counts = Counter(item["_source"]["author_id"] for item in data)

# 先按用户id和发文时间排个序
data = sorted(data, key=lambda x: (x["_source"]["author_id"], x["_source"]["pt"]))
# 2.统计时间间隔绝对值连续小于5秒的次数
user_interval_counts = Counter()
max_count = 0

for i in range(1, len(data)):
    curr_item = data[i]
    prev_item = data[i-1]
    curr_user_id = curr_item["_source"]["author_id"]
    prev_user_id = prev_item["_source"]["author_id"]
    curr_timestamp = curr_item["_source"]["pt"] // 1000
    prev_timestamp = prev_item["_source"]["pt"] // 1000
    curr_time = datetime.fromtimestamp(curr_timestamp)
    prev_time = datetime.fromtimestamp(prev_timestamp)
    time_diff = abs((curr_time - prev_time).total_seconds())  # 计算时间间隔的绝对值

    # 检查时间间隔是否连续小于5秒
    if curr_user_id == prev_user_id and time_diff < 5:
        max_count += 1
        user_interval_counts[curr_user_id] = max(user_interval_counts[curr_user_id], max_count)
    else:
        max_count = 0

# 3.计算发文内容相似度
similarities = compute_text_similarity(data)

# 构建结果字典，每个用户只输出一次
results = {}
for item in data:
    user_id = item["_source"]["author_id"]
    username = item["_source"]["author_name"]
    post_count = user_post_counts[user_id]
    interval_count = user_interval_counts[user_id]
    similarity = similarities.get(user_id, 0.0)

    if user_id not in results:
        results[user_id] = {
            "author_id": user_id,
            "author_name": username,
            "日发帖量": post_count,
            "时间间隔连续小于5秒的次数": interval_count,
            "发文内容相似度": similarity
        }

# 按照日发帖量降序排序结果列表
sorted_results = sorted(results.values(), key=lambda x: x["日发帖量"], reverse=True)

# 写入结果到CSV文件
with open("0628-0704-50个机器人全日发文数据.csv", 'w', encoding="utf-8-sig", newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["author_id", "author_name", "日发帖量", "时间间隔连续小于5秒的次数", "发文内容相似度"])  # 写入CSV文件头部
    for result in sorted_results:
        writer.writerow([
            result["author_id"],
            result["author_name"],
            result["日发帖量"],
            result["时间间隔连续小于5秒的次数"],
            result["发文内容相似度"]
        ])
