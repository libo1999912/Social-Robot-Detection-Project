import csv

# 读取文件1的账号信息和列数据
file1_data = {}
with open("0628-0704-200个随机用户全日发文数据.csv", 'r', encoding="utf-8-sig") as f:
    reader = csv.reader(f)
    headers = next(reader)  # 获取CSV文件头部
    for row in reader:
        account = row[0]  # 假设账号信息在CSV文件的第一列
        file1_data[account] = row[1:]  # 将账号后面的列数据存储在字典中

# 读取文件2的账号信息
file2_accounts = set()
with open("200个随机真人用户.csv", 'r', encoding="latin1") as f:  # 将文件2的文件名替换为实际的文件名
    reader = csv.reader(f)
    next(reader)  # 跳过CSV文件头部
    for row in reader:
        account = row[0]  # 假设账号信息在CSV文件的第一列
        file2_accounts.add(account)

# 构建文件3的数据
file3_data = []
for account in file2_accounts:
    if account in file1_data:
        # 文件1中存在的账号，复制对应的列信息
        file3_data.append([account] + file1_data[account])
    else:
        # 文件1中不存在的账号，将后续列信息补充为0
        file3_data.append([account] + [0] * (len(headers) - 1))

# 将数据写入文件3
with open("近7天-200个随机用户测试数据.csv", 'w', encoding="utf-8-sig", newline='') as f:  # 文件3的文件名可以根据需要进行替换
    writer = csv.writer(f)
    writer.writerow(headers)  # 写入CSV文件头部
    writer.writerows(file3_data)  # 写入数据行
