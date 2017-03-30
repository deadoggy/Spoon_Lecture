#coding: utf-8

import sklearn.cluster as cl
from sklearn.neighbors import NearestNeighbors
from sklearn.metrics import silhouette_score
import numpy as np
import time
import matplotlib.pylab as plt


class clusterer:

    __beg = 1897
    __end = 2011
    __gap = 1
    __dataVec = []
    __dateVec = []
    __dimension = 244
    __k = 5

    def readFile(self):


        for index in range(self.__beg, self.__end+self.__gap, self.__gap):
            fileName = "A_and_DowJones/" + str(index) + "_" +str(index+self.__gap-1)+".csv"
            file = open(fileName)
            vec = []
            for index2 in range(0, self.__dimension):
                list = file.readline().split(",")
                if len(list) == 2:
                    valStr = list[1]
                vec.append(eval(valStr)*100)
            self.__dataVec.append(vec)

        file = open(u"201501to201612/three_1")
        vec = []
        for index in range(0, self.__dimension):
            valStr = file.readline().split(",")[1]
            vec.append(eval(valStr))
        self.__dataVec.append(vec)

        file = open(u"201501to201612/three_2")
        vec = []
        for index in range(0, self.__dimension):
            valStr = file.readline().split(",")[1]
            vec.append(eval(valStr))
        self.__dataVec.append(vec)


    def divideViolence(self):
        file = open("A_and_DowJones/DowJonesAfter1950.csv")
        preprice = eval(file.readline().split(",")[1])
        line = file.readline()
        all_data = []
        while line is not None and len(line)!= 0:
            try:
                self.__dateVec.append(time.strptime(line.split(",")[0], "%Y%m%d"))
            except Exception as e:
                self.__dateVec.append(time.strptime(line.split(",")[0], "%m/%d/%Y"))
            curprice = eval(line.split(",")[1])
            rate = (curprice - preprice) / preprice
            preprice = curprice
            all_data.append(rate)
            line = file.readline()
        gap = 244
        beg = 0
        length = len(all_data)
        while beg + gap <= length:
            self.__dataVec.append(all_data[beg: beg+gap])
            beg += 1

        fileList = [u"201501to201612/three_1", u"201501to201612/three_2"]

        for i in range(len(fileList)):
            file = open(fileList[i])
            vec = []
            for index in range(0, self.__dimension):
                valStr = file.readline().split(",")[1]
                vec.append(eval(valStr))
            self.__dataVec.append(vec)

    def KNN(self):

        X = np.array(self.__dataVec)
        knner = NearestNeighbors(n_neighbors=self.__k).fit(X)

        dis1, clu1 = knner.kneighbors(X[-1, :]) // 2016
        dis2, clu2 = knner.kneighbors(X[-2, :]) // 2015

        res = open("knnRes", "w")

        clu1_date1 = []
        for item in clu1[0]:
            clu1_date1.append([self.__dateVec[item].tm_year,self.__dateVec[item].tm_mon, self.__dateVec[item].tm_mday])
        clu2_date2 = []
        for item in clu2[0]:
            clu2_date2.append([self.__dateVec[item].tm_year,self.__dateVec[item].tm_mon, self.__dateVec[item].tm_mday])

        #将结果写到文件里
        res.write(str(clu1_date1) + "\n")
        res.write(str(clu2_date2) + "\n")
        res.close()
        #把股价画图




    def eul_kmean(self): #耗费的实际那很大， 效果并不太好
        print "k_means.....,"
        data_Arr = np.array(self.__dataVec)
        max_silhouette = -1
        label = []
        for n_cluster in range(4, 100):
            clusterer = cl.KMeans(n_clusters=n_cluster)
            cluster_label = clusterer.fit_predict(data_Arr)
            sil = silhouette_score(data_Arr, cluster_label)
            if sil > max_silhouette:
                max_silhouette = sil
                label = cluster_label

        last_1 = label[len(label)-1]
        last_2 = label[len(label)-2]
        res_1 = []
        res_2 = []

        for index in range(len(label)):
            if 0 == cmp(last_1, label[index]):
                res_1.append(self.__dateVec[index])

            if 0 == cmp(last_2, label[index]):
                res_2.append(self.__dateVec[index])

        resfile1 = open("res1",'w')

        for item in res_1:
            resfile1.write(str(item) + "\n")

        resfile2 = open("res2",'w')

        for item in res_2:
            resfile2.write(str(item) + "\n")
        resfile1.close()
        resfile2.close()

    def _str2time(self, dateStr):
        try:
            date = time.strptime(dateStr, "%Y%m%d")
        except Exception as e:
            try:
                date = time.strptime(dateStr, "%m/%d/%Y")
            except Exception as e2:
                date = time.strptime(dateStr, "%Y-%m-%d")
        return date

    def draw(self, year, mon, day, datelen):
        file = open("A_and_DowJones/DowJonesAfter1950.csv")
        line = file.readline()
        time = self._str2time(line.split(",")[0])
        val  = eval(line.split(",")[1])

        X = np.linspace(0, datelen, datelen)

        Y = []

        endDate = []

        while len(line) > 0:
            if time.tm_year == year and time.tm_mon == mon and time.tm_mday == day:
                for index in range(datelen):
                    Y.append(val)
                    if index == datelen-1:
                        endDate = time
                    line = file.readline()
                    time = self._str2time(line.split(",")[0])
                    val = eval(line.split(",")[1])
                break
            line = file.readline()
            time = self._str2time(line.split(",")[0])
            val = eval(line.split(",")[1])
        plt.plot(X, Y)
        name = str(year) + "_" + str(mon) + "_" + str(day) + "_to_" +\
            str(endDate.tm_year) + "_" + str(endDate.tm_mon) + "_" + str(endDate.tm_mday) +"_"+ str(datelen)
        plt.savefig("Img/" + name + ".png")
        plt.close()

    def drawThr(self):
        X = np.linspace(0, 244, 244)


        fileList = ["2015_three", "2016_three"]
        for fileName in fileList:
            Y = []
            file = open("201501to201612/" + fileName+".csv")
            line = file.readline()
            while 0 != len(line):
                Y.append(eval(line.split(",")[1]))
                line = file.readline()
            plt.plot(X, Y)
            plt.savefig("Img/" + fileName + ".png")
            plt.close()


if __name__ == "__main__":
    obj = clusterer()
    # obj.divideViolence()
    # obj.KNN()
    # obj.draw(1987, 8, 26, 244)
    # obj.draw(2008, 7, 28, 300)
    # obj.draw(1987, 4, 23, 420)
    # obj.draw(2008, 2, 11, 244)
    obj.drawThr()