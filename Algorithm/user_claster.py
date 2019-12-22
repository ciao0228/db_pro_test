# -*- coding:utf-8 -*-

"""
    Author: Thinkgamer
    Desc:
        代码2-1  实例1：搭建你的第一个推荐系统-电影推荐系统
        从中随机选择1000个与用户进行计算
"""
import os
import json
import random
import math


class FirstRec:
    """
        初始化函数
            filePath: 原始文件路径
            seed：产生随机数的种子
            k：选取的近邻用户个数
            nitems：为每个用户推荐的电影数
    """

    def __init__(self, file_path, seed, k, n_items):
        self.file_path = file_path
        self.users_1000 = self.__select_1000_users()
        self.seed = seed
        self.k = k
        self.n_items = n_items
        self.train, self.test = self._load_and_split_data()  # 调用load~方法生成类对象的训练集

    # 获取所有用户并随机选取1000个
    def __select_1000_users(self):
        print("随机选取1000个用户！")
        if os.path.exists("data/train.json") and os.path.exists("data/test.json"):
            return list()
        else:
            users = set()
            # 获取所有用户
            for file in os.listdir(self.file_path):
                one_path = "{}/{}".format(self.file_path, file)
                print("{}".format(one_path))
                with open(one_path, "r") as fp:
                    for line in fp.readlines():
                        if line.strip().endswith(":"):
                            continue
                        userID, _, _ = line.split(",")
                        users.add(userID)
            # 随机选取1000个
            users_1000 = random.sample(list(users), 1000)
            print(users_1000)
            return users_1000

    # 加载数据，并拆分为训练集和测试集
    def _load_and_split_data(self):
        train = dict()
        test = dict()
        if os.path.exists("data/train.json") and os.path.exists("data/test.json"):
            print("从文件中加载训练集和测试集")
            train = json.load(open("data/train.json"))
            test = json.load(open("data/test.json"))
            print("从文件中加载数据完成")
        else:
            # 设置产生随机数的种子，保证每次实验产生的随机结果一致
            random.seed(self.seed)
            for file in os.listdir(self.file_path):
                one_path = "{}/{}".format(self.file_path, file)
                print("{}".format(one_path))
                with open(one_path, "r") as fp:
                    movieID = fp.readline().split(":")[0]
                    for line in fp.readlines():
                        if line.endswith(":"):
                            continue
                        userID, rate, _ = line.split(",")
                        # 判断用户是否在所选择的1000个用户中
                        if userID in self.users_1000:
                            if random.randint(1, 50) == 1:
                                test.setdefault(userID, {})[movieID] = int(rate)
                            else:
                                train.setdefault(userID, {})[movieID] = int(rate)
            print("加载数据到 data/train.json 和 data/test.json")
            json.dump(train, open("data/train.json", "w"))
            json.dump(test, open("data/test.json", "w"))
            print("加载数据完成")
        return train, test

    """
        计算皮尔逊相关系数
            rating1：用户1的评分记录，形式如{"movieid1":rate1,"movieid2":rate2,...}
            rating2：用户1的评分记录，形式如{"movieid1":rate1,"movieid2":rate2,...}
    """

    def pearson(self, rating1, rating2):
        sum_xy = 0
        sum_x = 0
        sum_y = 0
        sum_x2 = 0
        sum_y2 = 0
        num = 0
        for key in rating1.keys():
            if key in rating2.keys():
                num += 1
                x = rating1[key]
                y = rating2[key]
                sum_xy += x * y
                sum_x += x
                sum_y += y
                sum_x2 += math.pow(x, 2)
                sum_y2 += math.pow(y, 2)
        if num == 0:
            return 0
        # 皮尔逊相关系数分母
        denominator = math.sqrt(sum_x2 - math.pow(sum_x, 2) / num) * math.sqrt(sum_y2 - math.pow(sum_y, 2) / num)
        if denominator == 0:
            return 0
        else:
            return (sum_xy - (sum_x * sum_y) / num) / denominator

    """
        用户userID进行电影推荐
            userID：用户ID
    """

    def recommend(self, userID):
        neighborUser = dict()
        # print("输出keys",end=' ')
        # print(self.train.keys())
        for user in self.train.keys():
            if userID != user:
                distance = self.pearson(self.train[userID], self.train[user])
                neighborUser[user] = distance
        # 字典排序后，neighbour表示与改用户相邻的用户和评分合集
        # <class 'dict'>: {'2269844': 0.16773505367546937, '1581186': 0.8703882797784892, '975874': -1.000000000000002, '50123': 0.23059447499374497, '1426472': 0.045226282149815784, '254222': 0.21380958539120345, '2446682': 0.2132242743497144, '775436': -0.11182650591230758, '1605728': 0.2284210216281974, '779140': 0, '2638940': -0.16222142113076254, '1782553': 0.07876618310282212, '1621920': 0.1613598518569988, '2599687': -0.05590169943749515, '133707': 0.0077310601173788485, '1416817': 0.3340576761085447, '17149': 0.0, '14728': 0.08202656579359295, '1251028': 0.2555096891200297, '2170383': -0.3825460278380029, '1797713': 0, '2428151': 0.2204498374712975, '124291': -1.0, '534993': 0.14189513095212064, '1832599': -0.2380632768576815, '2547767': 0, '245841': -0.03149020634665051, '758904': 0.0615410834629596, '1581165': 0.2520701088716134, '679218': 0, '145258': 0.03986205025895435, '683973': 0.0, '14994': 0.047595070252160435, '2629660': 0.300817784873178, '271797': 0.27928635247053507, '1071272': 0.0, '1731121': 0.11145968058655921, '1398124': 0.9999999999999998, '943196': 0.1973684210526338, '844909': 0, '2097548': 0.3582639379126273, '1308697': 0.48686449556014766, '162279': -0.5000000000000053, '1533530': 0.19063063483017648, '7963': -0.252457797976289, '717033': 0.542609516234293, '1102270': 0.23896829396961855, '117386': -0.16149550497722265, '1945912': 0.08342120563201576, '1193468': 0.3412935961132531, '1945265': 0.12143696022085827, '2438449': 0.06451474500711994, '1947128': 0, '912171': 0.05405405405405649, '1919296': 0.2138443426239272, '1263062': 0.30509393351946573, '1227114': 0.15380715444026818, '1937587': 0.21529345949739215, '958359': 0.21821789023599536, '1969156': -0.07779417425101043, '153109': 0.009035226544160526, '2451835': 0.0, '516722': 0.26452373116849665, '328779': 0.06679742070747578, '659907': -0.36835473434187727, '1738198': 0.20079068862440771, '2493011': -0.26862135879771804, '228919': 0.08557692796658052, '1687738': 0.4016096644512494, '1589331': 0.5892556509887896, '2356793': 0.0327186642542067, '331946': 0.3712434168032515, '1562633': 0.12242050134200802, '1602984': 0.12412570250359391, '1715533': 0.12010923989517504, '509864': 0.020689873853700847, '157357': 0.03598612642396088, '1431311': -0.08039050359989477, '2604501': 0.1888158056167551, '109316': -0.7385489458759952, '246681': 0.11781260898015569, '1099179': 0.13333333333333333, '933104': 0.0746242340958701, '298900': 0.030173090236809905, '1044269': 0.0336457635180741, '812068': -0.5466081666101248, '1709381': 0.7653749516204755, '1733123': 0.03761716940259551, '1792510': -0.1685499656158094, '79575': -0.04003203845127059, '1067920': 0.31265111347200636, '484464': -0.4170288281141495, '1194937': 0.30508510792387805, '2024848': 0.3875136798331671, '1555444': 0.11531640100360963, '491722': 0.34641016151377707, '874699': -0.21040146079235725, '1903123': 0.2725126197120499, '1150025': 0.7842289302333945, '240837': -0.021699728499248658...

        newNU = sorted(neighborUser.items(), key=lambda k: k[1], reverse=True)
        # .items（）函数返回dict中所有（键，值）的列表

        movies = dict()
        for (sim_user, sim) in newNU[0:self.k]:  # 对每个元组判断，
            for movieID in self.train[sim_user].keys(): #对训练集sim_user的每个字电影序号判断
                movies.setdefault(movieID, 0)#setdefulat函数，对字典序汇总若没有改movieid，则加入
                movies[movieID] += sim * self.train[sim_user][movieID]
        newMovies = sorted(movies.items(), key=lambda k: k[1], reverse=True)
        return newMovies

    """
        推荐系统效果评估函数
            num: 随机抽取 num 个用户计算准确率
    """

    def evaluate(self, num=30):
        print("开始计算准确率")
        precisions = list()
        random.seed(10)
        for userID in random.sample(self.test.keys(), num):
            hit = 0
            result = self.recommend(userID)[:self.n_items]
            for (item, rate) in result:
                if item in self.test[userID]:
                    hit += 1
            precisions.append(hit / self.n_items)
        return sum(precisions) / precisions.__len__()


# main函数，程序的入口
if __name__ == "__main__":
    file_path = "../data/netflix/training_set"
    seed = 30
    k = 15
    n_items = 20
    f_rec = FirstRec(file_path, seed, k, n_items)  # 构造函数
    # 计算用户 195100 和 1547579的皮尔逊相关系数
    r = f_rec.pearson(f_rec.train["195100"], f_rec.train["1547579"])
    print(f_rec.train['195100'])
    # 用户训练集中取出用户对电影评分，类似于{'77': 3, '1148': 5, '1220': 5, '1307': 4, '1798': 4, '2372': 5, '3106': 1, '3326': 4, '3433': 2, '3610': 4, '3624': 5, '3684': 5, '3936': 2, '44
    print("195100 和 1547579的皮尔逊相关系数为：{}".format(r))  # 用format格式定义参数
    # 为用户195100进行电影推荐
    result = f_rec.recommend("195100")
    print("为用户ID为：195100的用户推荐的电影为：{}".format(result))
    print("算法的推荐准确率为: {}".format(f_rec.evaluate()))
