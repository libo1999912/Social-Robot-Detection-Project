import csv
import json

# 读取包含100个JSON数据的文件
json_file = "xhs-es中原发评论数据.json"

with open(json_file, 'r', encoding='utf-8-sig') as file:
    users_data = json.load(file)

# 获取所有字段名
all_fields = set()
for user_data in users_data:
    all_fields.update(user_data["_source"].keys())

# 导出为CSV表格
csv_file = "xhs-es中原发评论数据.csv"

with open(csv_file, mode='w', newline='', encoding='utf-8-sig') as file:
    writer = csv.writer(file)

    # 写入列头
    writer.writerow(all_fields)

    # 写入数据行
    for user_data in users_data:
        row = [user_data["_source"].get(field) for field in all_fields]
        writer.writerow(row)

print(f"CSV文件已导出为: {csv_file}")





# import csv
# import json
#
# # 读取包含10w个用户数据的JSON文件
# json_file = "0611-100个机器人用户数据.json"
#
# # 指定要导出的字段列表
# fields_to_export = ["author_id","author_name", "reg_type", "nfans", "nfol"]
#
# # 读取JSON数据
# with open(json_file, 'r', encoding='utf-8') as file:
#     users_data = json.load(file)
#
# # 取前200个用户数据
# users_data = users_data[:200]
#
# # 导出为CSV表格
# csv_file = "0611-100个机器人用户数据.csv"
#
# with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
#     writer = csv.writer(file)
#
#     # 写入列头
#     writer.writerow(fields_to_export)
#
#     # 写入数据行
#     for user_data in users_data:
#         row = [user_data["_source"].get(field) for field in fields_to_export]
#         writer.writerow(row)
#
# print(f"CSV文件已导出为: {csv_file}")
