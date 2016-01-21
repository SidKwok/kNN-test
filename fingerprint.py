# coding=utf-8
# __author__ = 'Sid'
from numpy import *


def getdataset(filename):
    f = open(filename, 'r')
    arrayOLines = f.readlines()
    # 坐标集
    locset = []
    # ap 名字集
    apnameset = []
    # 所有的 ap集
    apset = []

    for line in arrayOLines:
        line = line.strip()
        listFromLine = line.split(' ')
        location = listFromLine[0].split('|')
        locset.append(location)
        # 每一个的训练的ap集
        aplist = []
        for ap in listFromLine[1:]:
            apname, apvalue = ap.split('|')[0], int(ap.split('|')[1])
            if apname not in apnameset:
                apnameset.append(apname)
            aplist.append((apname, apvalue))
        apset.append(dict(aplist))
    return apset, locset


def kNN(trainapset, trainlocset, testapset, testlocset, k):

    resultlist = []
    for j in range(len(testapset)):
        answer = {}
        for i in range(len(trainapset)):
            locvalue = 0
            # 记录训练集中存在的个数
            count = 0
            # 遍历测试集的地址项
            for apmac in testapset[j]:
                # 若训练集中存在，则计算距离
                if apmac in trainapset[i].keys():
                    locvalue += (trainapset[i][apmac] -
                                 testapset[j][apmac]) ** 2
                    # locvalue += (trainapset[i][apmac] - testapset[j][apmac])
                    # print locvalue
                    count += 1
                # answer.append(locvalue)
            answer[str(i)] = sqrt(locvalue) / count
        sortanswer = sorted(answer.items(), key=lambda x: x[1])
        resultlist.append(sortanswer)

    predictlist = []
    for result in resultlist:
        weightcount = 0.0
        predictx = 0.0
        predicty = 0.0
        for i in range(k):
            x = float(trainlocset[int(result[i][0])][0])
            y = float(trainlocset[int(result[i][0])][1])
            predictx += x * result[i][1]
            predicty += y * result[i][1]
            weightcount += result[i][1]
        predictx = predictx / weightcount
        predicty = predicty / weightcount
        predictlist.append([predictx, predicty])

    print predictlist
    meanerror = 0.0
    for i in range(len(predictlist)):
        xx = (predictlist[i][0] - float(testlocset[i][0])) ** 2
        yy = (predictlist[i][1] - float(testlocset[i][1])) ** 2
        meanerror += sqrt(xx + yy)

    meanerror = meanerror * (1.0 / len(predictlist))
    print meanerror


trainapset, trainlocset = getdataset('fingerprint.txt')
testapset, testlocset = getdataset('test.txt')
p = '00:1a:1e:fd:62:e3'
# print trainapset
# print trainlocset
kNN(trainapset, trainlocset, testapset, testlocset, 4)
kNN(trainapset, trainlocset, testapset, testlocset, 5)
kNN(trainapset, trainlocset, testapset, testlocset, 6)
kNN(trainapset, trainlocset, testapset, testlocset, 7)
kNN(trainapset, trainlocset, testapset, testlocset, 8)
kNN(trainapset, trainlocset, testapset, testlocset, 9)