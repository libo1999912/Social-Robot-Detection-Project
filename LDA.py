import gensim
from gensim import corpora

# 准备数据
original_videos = ["这个地方真的好漂亮", ]
robot_comments = ["对面怎么了", "对面你自己", "对面傻不傻", "对面是不是", "对面傻不傻","对面怎么了","对面是不是","对面傻不傻"]

# 文本预处理
texts = original_videos + robot_comments
tokenized_texts = [text.split() for text in texts]

# 构建词典和文档-词频矩阵
dictionary = corpora.Dictionary(tokenized_texts)
corpus = [dictionary.doc2bow(text) for text in tokenized_texts]

# 训练LDA模型
num_topics = 5  # 设置主题数量
lda_model = gensim.models.LdaModel(corpus=corpus, id2word=dictionary, num_topics=num_topics)

# 获取主题分布
for i, topic in lda_model.show_topics(num_topics=num_topics):
    print(f"Topic {i + 1}: {topic}")

# # 推断新文档的主题分布
# new_document = "姑娘漂亮"
# new_bow = dictionary.doc2bow(new_document.split())
# new_topic_distribution = lda_model.get_document_topics(new_bow)
# print(f"New Document Topic Distribution: {new_topic_distribution}")






# import gensim
# from gensim import corpora
# import numpy as np
# from sklearn.metrics.pairwise import cosine_similarity
#
# # 准备数据
# original_videos = ["我爱你姑娘"]
# robot_comments = ["哈哈哈", "厉害", "对不起", "哈哈哈", "666","666","666","姑娘漂亮"]
#
# # 合并文本数据
# texts = original_videos + robot_comments
#
# # 文本预处理
# tokenized_texts = [text.split() for text in texts]
#
# # 构建词典和文档-词频矩阵
# dictionary = corpora.Dictionary(tokenized_texts)
# corpus = [dictionary.doc2bow(text) for text in tokenized_texts]
#
# # 训练LDA模型
# num_topics = 3  # 设置主题数量
# lda_model = gensim.models.LdaModel(corpus=corpus, id2word=dictionary, num_topics=num_topics)
#
# # 获取原视频主题分布
# original_video_bow = dictionary.doc2bow(original_videos[0].split())
# original_video_topic_distribution = lda_model.get_document_topics(original_video_bow)
#
# # 计算机器人评论与原视频主题的相似性得分
# similarity_scores = []
# for comment in robot_comments:
#     comment_bow = dictionary.doc2bow(comment.split())
#     comment_topic_distribution = lda_model.get_document_topics(comment_bow)
#
#     # 将主题分布转换为向量表示
#     original_video_topic_vec = np.array([weight for _, weight in original_video_topic_distribution])
#     comment_topic_vec = np.array([weight for _, weight in comment_topic_distribution])
#
#     # 计算余弦相似度
#     similarity_score = cosine_similarity([original_video_topic_vec], [comment_topic_vec])[0][0]
#     similarity_scores.append(similarity_score)
#
# # 输出相似性得分
# for i, score in enumerate(similarity_scores):
#     print(f"Robot Comment {i + 1} Similarity to Original Video: {score}")


