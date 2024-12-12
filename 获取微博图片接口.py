import os
import requests
from pathlib import Path


def save_image_to_local(image_url, save_path):
    try:
        response = requests.get(image_url)
        if response.status_code == 200:
            # 处理成功的响应
            image_data = response.content

            # 确定保存的文件夹路径
            save_folder = os.path.join(str(Path.home()), save_path)

            # 确保保存的文件夹存在
            os.makedirs(save_folder, exist_ok=True)

            # 提取图片文件名
            filename = image_url.split('/')[-1]

            # 保存图片到本地文件
            filepath = os.path.join(save_folder, filename)
            with open(filepath, 'wb') as f:
                f.write(image_data)

            print("图片已保存至：{}".format(filepath))
        else:
            # 处理错误的响应
            print("请求失败，状态码：{}".format(response.status_code))
    except requests.exceptions.RequestException as e:
        # 处理请求异常
        print("请求发生异常：{}".format(str(e)))


# 调用示例
image_url = "http://10.160.90.38:3509/author_img_url_f"  # 根据实际情况提供图片的URL
save_path = "Desktop/folder"  # 保存图片的本地文件夹路径

save_image_to_local(image_url, save_path)
