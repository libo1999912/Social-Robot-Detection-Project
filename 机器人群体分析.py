import csv
from collections import defaultdict
from datetime import datetime
import jieba
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from gensim.models import Word2Vec

def compute_text_similarity(text1, text2):
    tokens1 = jieba.lcut(text1)
    tokens2 = jieba.lcut(text2)
    model = Word2Vec([tokens1, tokens2], min_count=1)
    vec1 = np.mean([model.wv[token] for token in tokens1 if token in model.wv], axis=0)
    vec2 = np.mean([model.wv[token] for token in tokens2 if token in model.wv], axis=0)
    similarity = cosine_similarity(vec1.reshape(1, -1), vec2.reshape(1, -1))[0][0]
    return similarity

def process_data(filename):
    user_messages = defaultdict(list)
    with open(filename, 'r', encoding='gb18030') as file:
        reader = csv.reader(file)
        next(reader)  # 跳过标题行
        for row in reader:
            user_id = row[0]
            message = row[2]
            timestamp = datetime.strptime(row[3], '%H:%M:%S')
            user_messages[user_id].append((message, timestamp))

    similar_messages = defaultdict(list)
    for user_id, messages in user_messages.items():
        for i in range(len(messages)):
            for j in range(i + 1, len(messages)):
                message1, timestamp1 = messages[i]
                message2, timestamp2 = messages[j]
                time_diff = (timestamp2 - timestamp1).total_seconds()
                if abs(time_diff) <= 60:  # 时间间隔在1分钟以内
                    similarity = compute_text_similarity(message1, message2)
                    if similarity < 1.0:  # 排除完全相同的消息
                        similar_messages[(user_id, user_id)].append((message1, message2, similarity))

    return similar_messages

def save_results(similar_messages, output_file):
    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['User 1', 'User 2', 'Message 1', 'Message 2', 'Similarity'])
        for (user1, user2), messages in similar_messages.items():
            for message1, message2, similarity in messages:
                writer.writerow([user1, user2, message1, message2, similarity])

if __name__ == '__main__':
    data_file = '评论时间间隔.csv'
    output_file = 'similar_messages.csv'

    # 处理数据
    similar_messages = process_data(data_file)

    # 保存结果
    save_results(similar_messages, output_file)
