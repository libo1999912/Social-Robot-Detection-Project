# import pandas as pd
# import chardet
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.metrics import accuracy_score
# from sklearn.model_selection import train_test_split
#
# # 读取数据集文件为一个DataFrame对象
# with open("训练集1.csv", "rb") as f:
#     result = chardet.detect(f.read())
# encoding = result["encoding"]
# df = pd.read_csv("训练集1.csv", encoding=encoding)
#
# # 将特征值和目标变量分别存储到X和y中
# X = df.iloc[:, :-1].values
# y = df.iloc[:, -1].values
#
# # 将数据集划分为训练集和测试集
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
#
# # 创建一个随机森林分类器并进行训练
# rf = RandomForestClassifier(n_estimators=100, random_state=42)
# rf.fit(X_train, y_train)
#
# # 在测试集上进行预测，并计算准确率
# y_pred = rf.predict(X_test)
# accuracy = accuracy_score(y_test, y_pred)
# print("测试集准确率：", accuracy)
#
# # 读取新用户数据集，并指定用户账号列的数据类型为字符串
# new_data = pd.read_csv("测试集1.csv", encoding=encoding, dtype={'用户账号': str})
#
# # 去除用户账号列中的 .0
# new_data['author_id'] = new_data['author_id'].astype(int).astype(str)
#
# X_new = new_data.iloc[:, :-1].values
#
# # 使用训练好的模型对新用户数据进行预测
# predictions = rf.predict(X_new)
#
# # 打印预测结果
# for i, prediction in enumerate(predictions):
#     if prediction == 0:
#         print("用户", new_data.iloc[i]['author_id'], "：机器人")
#     else:
#         print("用户", new_data.iloc[i]['author_id'], "：真人")
#
# # 创建结果表格
# result_df = pd.DataFrame({'用户账号': new_data['author_id'], '预测结果': predictions})
#
# # 输出结果表格为CSV文件
# result_df.to_csv('预测结果.csv', index=False)
#
# # 打印结果表格
# print(result_df)






# import pandas as pd
# import cchardet as chardet
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.metrics import accuracy_score
# from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import LabelEncoder
#
# # 使用chardet检测文件编码
# with open("训练集.csv", "rb") as f:
#     result = chardet.detect(f.read())
# encoding = result["encoding"]
#
# # 读取数据集文件为一个DataFrame对象
# df = pd.read_csv("训练集.csv", encoding=encoding, engine='python')
#
# # # 对author_id和author_name列进行转换
# label_encoder = LabelEncoder()
# df['author_id'] = label_encoder.fit_transform(df['author_id'])
# df['author_name'] = label_encoder.fit_transform(df['author_name'])
#
# # 将特征值和目标变量分别存储到X和y中
# X = df.iloc[:, :-1].values
# y = df.iloc[:, -1].values
#
# # 将数据集划分为训练集和测试集
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
#
# # 创建一个随机森林分类器并进行训练
# rf = RandomForestClassifier(n_estimators=100, random_state=42)
# rf.fit(X_train, y_train)
#
# # 在测试集上进行预测，并计算准确率
# y_pred = rf.predict(X_test)
# accuracy = accuracy_score(y_test, y_pred)
# print("测试集准确率：", accuracy)
#
# # # 读取新用户数据集，并对author_id和author_name列进行转换
# new_data = pd.read_csv("测试集.csv", encoding=encoding, engine='python')
# new_data['author_id'] = label_encoder.transform(new_data['author_id'])
# new_data['author_name'] = label_encoder.transform(new_data['author_name'])
#
# X_new = new_data.iloc[:, :-1].values
#
# # 使用训练好的模型对新用户数据进行预测
# predictions = rf.predict(X_new)
#
# # 打印预测结果
# for i, prediction in enumerate(predictions):
#     if prediction == 0:
#         print("用户", new_data.iloc[i]['author_id'], "：机器人")
#     else:
#         print("用户", new_data.iloc[i]['author_id'], "：真人")
#
# # 创建结果表格
# result_df = pd.DataFrame({'用户账号': new_data['author_id'], '预测结果': predictions})
#
# # 输出结果表格为CSV文件
# result_df.to_csv('预测结果.csv', index=False)
#
# # 打印结果表格
# print(result_df)




# 现版随机森林
import pandas as pd
import chardet
from sklearn.ensemble import RandomForestClassifier

# 读取训练集文件为一个DataFrame对象
with open("训练集2.csv", "rb") as f:
    result = chardet.detect(f.read())
encoding = result["encoding"]
df_train = pd.read_csv("训练集2.csv", encoding=encoding)

# 将特征值和目标变量分别存储到X_train和y_train中
X_train = df_train[['日发帖量', '发帖时间间隔异常（连续小于5秒的次数）', '发文及评论内容相似度','凌晨0点到2点和晚上10点到12点占总量比']].values
y_train = df_train['是否为机器人(1是真人，0是机器人）'].values

# 创建一个随机森林分类器并进行训练
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)

# 读取测试集文件为一个DataFrame对象
df_test = pd.read_csv("测试集2.csv", encoding=encoding)

# 去除用户账号列中的 .0
df_test['author_id'] = df_test['author_id'].astype(int).astype(str)

# 提取测试集的特征值
X_test = df_test[['日发帖量', '发帖时间间隔异常（连续小于5秒的次数）', '发文及评论内容相似度','凌晨0点到2点和晚上10点到12点占总量比']].values

# 使用训练好的模型对测试集进行预测
predictions = rf.predict(X_test)

# 打印预测结果
for i, prediction in enumerate(predictions):
    if prediction == 0:
        print("用户", df_test.iloc[i]['author_id'], "：机器人")
    else:
        print("用户", df_test.iloc[i]['author_id'], "：真人")

# 创建结果表格
result_df = pd.DataFrame({'用户账号': df_test['author_id'], '预测结果': predictions})

# 输出结果表格为CSV文件
result_df.to_csv('预测结果-4个特征近7天数据.csv', index=False)

# 打印结果表格
print(result_df)







# import pandas as pd
# from sklearn.ensemble import RandomForestClassifier
# import cchardet as chardet
# from sklearn.preprocessing import LabelEncoder
# import numpy as np
#
#
# # 读取训练集文件为一个DataFrame对象
# with open("训练集.csv", "rb") as f:
#     result = chardet.detect(f.read())
# encoding = result["encoding"]
# df_train = pd.read_csv("训练集.csv", encoding=encoding)
# #print("检测到的编码类型：", encoding)
#
# # 对author_id和author_name列进行转换
# label_encoder = LabelEncoder()
# df_train['author_id'] = label_encoder.fit_transform(df_train['author_id'])
# df_train['author_name'] = label_encoder.fit_transform(df_train['author_name'])
#
# # 将特征值和目标变量分别存储到X_train和y_train中
# X_train = df_train[['日发帖量', '发帖时间间隔异常（连续小于5秒的次数）', '发文及评论内容相似度']].values
# y_train = df_train['是否为机器人(1是真人，0是机器人）'].values
#
# # 创建一个随机森林分类器并进行训练
# rf = RandomForestClassifier(n_estimators=100, random_state=42)
# rf.fit(X_train, y_train)
#
# # 读取测试集文件为一个DataFrame对象
# df_test = pd.read_csv("测试集.csv", encoding='gb18030')
# # with open("测试集.csv", "rb") as f:
# #     result = chardet.detect(f.read())
# # encoding = result["encoding"]
# # df_test = pd.read_csv("测试集.csv", encoding=encoding)
#
#
# # 处理新用户数据集中的未见过的标签
# df_test['author_id'] = df_test['author_id'].apply(lambda x: x if x in label_encoder.classes_ else 'Unknown')
# df_test['author_name'] = df_test['author_name'].apply(lambda x: x if x in label_encoder.classes_ else 'Unknown')
# # 将"Unknown"添加到训练集的标签列表中
# label_encoder.classes_ = np.append(label_encoder.classes_, 'Unknown')
#
#
# df_test['author_id'] = label_encoder.transform(df_test['author_id'])
# df_test['author_name'] = label_encoder.transform(df_test['author_name'])
#
# # 提取测试集的特征值
# X_test = df_test[['日发帖量', '发帖时间间隔异常（连续小于5秒的次数）', '发文及评论内容相似度']].values
#
# # 使用训练好的模型对测试集进行预测
# predictions = rf.predict(X_test)
#
# # 打印预测结果
# for i, prediction in enumerate(predictions):
#     if prediction == 0:
#         print("用户", df_test.iloc[i]['author_id'], "：机器人")
#     else:
#         print("用户", df_test.iloc[i]['author_id'], "：真人")
#
# # 创建结果表格
# result_df = pd.DataFrame({'用户账号': df_test['author_id'], '预测结果': predictions})
#
# # 输出结果表格为CSV文件
# result_df.to_csv('预测结果.csv', index=False)
#
# # 打印结果表格
# print(result_df)


















