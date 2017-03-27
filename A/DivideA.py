#coding:utf-8
import math
import time

'''找到的A股数据是逆序的， 处理成正序的'''
class Divider:
    #分割成几年的间隔
    __yearGap = 2
    #文件中日期字段是第几个数据格
    __date = 0
    #文件中收盘价是地几个数据格
    __price = 3

    def _write(self, beg, end, data):
        file = open(str(beg)+"_"+str(end)+".csv", "w")
        length = len(data)

        for i in range(0, length):
            item = data[length-i-1]
            #日期
            date = str(item[0].tm_year)+"-"+str(item[0].tm_mon)+"-"+str(item[0].tm_mday)
            #收盘价
            price = str(item[1])
            file.write(date + "," + price + "\n")


    def divide(self):

        file = open("000001.csv")
        #去掉数据头
        file.readline()
        #读取数据
        line = file.readline()
        #保存一个周期的数据
        data = []
        #头年份
        begYear = -1
        while(0 != len(line)):
            line = line.split(',')
            date = time.strptime(line[self.__date], "%Y-%m-%d")
            price = eval(line[self.__price])

            #如果是第一年，更新年份
            if -1 == begYear:
                begYear = date.tm_year
            #第一次到两年后， 将之前两年的写入文件
            elif date.tm_year == begYear - 2:
                self._write(begYear, begYear+self.__yearGap-1, data)
                begYear = date.tm_year
                data = []

            #将这个数据存入data
            data.append([date, price])
            #读下一行
            line = file.readline()

        #处理剩余的数据
        self._write(begYear, begYear+self.__yearGap-1,data)


if __name__ == "__main__":

    testObj = Divider()

    testObj.divide()
