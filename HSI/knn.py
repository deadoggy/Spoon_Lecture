#coding:utf-8

from sklearn.neighbors import NearestNeighbors
import numpy as np
import matplotlib.pylab as plt

hsi_rate = open("HSI_rate")

date_list = []
rate_list = []
price_list = []
line = hsi_rate.readline()

temp_vec = []

while len(line) > 0:
    date_item = line.split(" ")[0]
    date_list.insert(0, date_item)
    price_item = line.split(" ")[2]
    price_list.insert(0, eval(price_item.replace(",","")))

    rate_item = eval(line.split(" ")[1])
    temp_vec.insert(0, rate_item)

    if len(temp_vec) == 244:
        rate_list.insert(0, temp_vec[:])
        temp_vec.pop()

    line = hsi_rate.readline()

file = open(u"../201501to201612/three_1")
vec = []
for index in range(0, 244):
    valStr = file.readline().split(",")[1]
    vec.append(eval(valStr)/100)
rate_list.append(vec)

file = open(u"../201501to201612/three_2")
vec = []
for index2 in range(0, 244):
    valStr = file.readline().split(",")[1]
    vec.append(eval(valStr)/100)
rate_list.append(vec)

rate_list = np.array(rate_list)

knner = NearestNeighbors(n_neighbors=5).fit(rate_list)

dis1, clu1 = knner.kneighbors(rate_list[-1, :]) #2016
dis2, clu2 = knner.kneighbors(rate_list[-2, :]) #2015

date_res = clu1.tolist()[0][1:] + clu2.tolist()[0][1:]
date_res.sort()

beg = date_res[0]

end = date_res[-1] + 244

Y = price_list[beg: end]

plt.plot(np.linspace(0, end-beg, end-beg), Y)

plt.show()

# plt.savefig(date_list[beg] + "_to_" + date_list[end] + ".png")

plt.close()




