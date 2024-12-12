from gensim.models import Word2Vec
import jieba
import json
import csv
from collections import Counter


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


if __name__ == '__main__':
    with open('0624-500个随机用户全日发文数据.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        similarities = compute_text_similarity(data)

        # 统计author_id的出现次数
        author_id_counter = Counter(user_data["_source"]["author_id"] for user_data in data)

        # 对相似度字典按照author_id出现次数进行降序排序
        sorted_similarities = dict(sorted(similarities.items(), key=lambda x: author_id_counter[x[0]], reverse=True))


        # 创建包含所有数据的JSON对象
        result = json.dumps(sorted_similarities, indent=4, ensure_ascii=False)

        # 创建CSV文件并写入结果
        with open('similar_word2vec.csv', 'w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['author_id', 'similarity'])  # 写入表头
            for user_id, similarity in sorted_similarities.items():
                writer.writerow([user_id, similarity])
