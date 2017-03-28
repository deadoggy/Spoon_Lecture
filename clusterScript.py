#coding: utf-8

import sklearn.cluster as cl
from sklearn.metrics import silhouette_score
import numpy as np


class clusterer:

    __beg = 1897
    __end = 2011
    __gap = 1
    __dataVec = []
    __dimension = 244

    def readFile(self):

        for index in range(self.__beg, self.__end+self.__gap, self.__gap):
            fileName = "A/" + str(index) + "_" +str(index+self.__gap-1)+".csv"
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
        file = open("A/DowJonesAfter1950.csv")
        line = file.readline()
        all_data = []
        while line is not None and len(line)!= 0:
            all_data.append(eval(line.split(",")[1]))
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

    def eul_kmean(self):
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
        for item in label:
            if 0 == cmp(last_1, item):
                res_1.append(item)

            if 0 == cmp(last_2, item):
                res_2.append(item)

        resfile1 = open("res1","w")
        resfile1.writelines(res_1)
        resfile2 = open("res2","w")
        resfile2.writelines(res_2)





if __name__ == "__main__":
    obj = clusterer()
    obj.divideViolence()
    label = obj.eul_kmean()
    pass
