## 短视频平台社交机器人检测系统
本项目基于随机森林（Random Forest）和潜在狄利克雷分配（LDA）模型，结合用户行为与文本特征，实现对短视频平台（如快手）中社交机器人的高效检测。通过分析四个关键特征（日发帖量、发帖时间间隔异常、内容相似度、异常活跃时间）及LDA主题相似性，显著提升了检测的召回率与F1分数。

## 📌 项目背景
社交机器人通过自动化程序在短视频平台大量发布虚假信息或无关评论，破坏用户体验。传统方法在短视频场景下面临挑战，因机器人行为模式与微博等平台存在显著差异（如评论内容与视频主题无关）。本项目提出融合随机森林与LDA的检测框架，结合行为特征与文本主题分析，实现更精准的识别。
## 论文核心贡献：
    提出四维行为特征（日发帖量、时间间隔、内容相似度、活跃时间）
    
    引入LDA模型量化评论与视频主题的偏离度
    
    实验表明，联合模型使召回率提升5%，F1分数提升4%

## 🛠️功能模块
1. 随机森林模型 (随机森林模型.py)
  输入：训练集（训练集2.csv）与测试集（测试集2.csv）

  特征：

    日发帖量：用户单日发帖/评论总数（阈值：>15次）
    
    发帖时间间隔异常：连续5次间隔<5秒
    
    内容相似度：基于Word2Vec的余弦相似度
    ![image](https://github.com/user-attachments/assets/97fe7967-f4e0-4c00-bf58-f05e39d3e68b)

    异常活跃时间：凌晨0-2点及晚10-12点发帖占比>40%

  输出：预测结果（预测结果-4个特征近7天数据.csv）

2. LDA主题建模 (LDA.py)
  功能：计算用户评论与视频原内容的主题相似性

  核心逻辑：

    对视频标题和用户评论分别进行LDA主题建模
    
    若两者主题分布差异显著，判定用户为机器人

3. 数据统计模块
    活跃时间分析 (统计活跃时间.py)：计算用户凌晨及晚间发帖占比
    
    日发帖量统计 (日发帖量统计.py)：统计用户ID的发帖频率
    
    评论时间间隔分析 (评论时间间隔分析.py)：检测连续短间隔评论行为

4. 数据获取 (es数据查询.py)
从Elasticsearch集群中爬取快手平台的用户行为数据


## 📊实验结果
![image](https://github.com/user-attachments/assets/5b3183b1-35a2-44a7-a07b-d6446daeaeca)


## 🚀 快速使用
## 环境依赖

pip install pandas scikit-learn gensim jieba elasticsearch chardet

## 运行步骤
  1.数据准备

        将训练集与测试集分别命名为 训练集2.csv 和 测试集2.csv

        确保数据包含以下字段：
                用户账号, 日发帖量, 发帖时间间隔异常, 内容相似度, 凌晨活跃占比

  2.训练与预测
        python 随机森林模型.py
  3.LDA主题分析
        python LDA.py
  3.结果输出

        预测结果保存至 预测结果-4个特征近7天数据.csv
        
        各统计模块生成对应CSV文件（如 时间间隔短的用户.csv）

📜 论文引用
本项目成果已发表论文《Social Robot Detection on Short Video Platform Based on Random Forest and LDA Model》。
![image](https://github.com/user-attachments/assets/3e910ea1-8ef1-4f44-9cad-66aa56d98340)

