#coding:utf-8
import math
import time

'''找到的A股数据是逆序的， 处理成正序的'''
class Divider:
    #分割成几年的间隔
    __yearGap = 1
    #文件中日期字段是第几个数据格
    __date = 0
    #A股文件中涨跌幅是第几个数据格
    __price = 9

    def _write(self, beg, end, data, sort):
        file = open(str(beg)+"_"+str(end)+".csv", "w")
        length = len(data)

        for i in range(0, length):
            if not sort:# 倒序
                item = data[length-i-1]
            else:
                item = data[i]
            #日期
            date = str(item[0].tm_year)+"-"+str(item[0].tm_mon)+"-"+str(item[0].tm_mday)
            #收盘价
            price = str(item[1])
            file.write(date + "," + price + "\n")


    def divideA(self):

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
                self._write( begYear-self.__yearGap+1, begYear, data, False)
                begYear = date.tm_year
                data = []

            #将这个数据存入data
            data.append([date, price])
            #读下一行
            line = file.readline()

        #处理剩余的数据
        self._write(begYear-self.__yearGap+1, begYear,data, False)

    def divideDow(self):
        file = open("DowJones.csv")
        #去掉文件头
        file.readline()
        #前一年最后的数据，用于计算第一天的涨跌幅
        pre = file.readline().split(",")
        prePrice =eval(pre[1])

        # 读取数据
        line = file.readline()
        # 保存一个周期的数据
        data = []
        # 头年份
        begYear = -1
        while (0 != len(line)):
            line = line.split(',')
            #处理不同的日期格式
            dateStr = line[0]
            if dateStr.__contains__("/"):
                date =  time.strptime(dateStr, "%m/%d/%Y")
            elif dateStr.__contains__("-"):
                try:
                    date = time.strptime(dateStr, "%Y-%m-%d")
                except Exception as e:
                    date  = time.strptime(dateStr, "%m-%d-%Y")
            else:
                date = time.strptime(dateStr, "%Y%m%d")

            price = eval(line[1])

            # 如果是第一年，更新年份
            if -1 == begYear:
                begYear = date.tm_year
            # 第一次到两年后， 将之前两年的写入文件
            elif date.tm_year - self.__yearGap == begYear:
                self._write(begYear , begYear + self.__yearGap - 1 , data, True)
                begYear = date.tm_year
                data = []

            # 将这个数据存入data
            data.append([date, (price - prePrice)/prePrice])
            # 更新前一个价格
            prePrice = price
            # 读下一行
            line = file.readline()

        # 处理剩余的数据
        self._write(begYear , begYear + self.__yearGap - 1 , data, True)

    def divideViolence(self):
        file = open("DowJonesAfter1950.csv")
        line = file.readline()
        all_data = []
        ret = []
        while line is not None and len(line)!= 0:
            all_data.append(eval(line.split(",")[1]))
            line = file.readline()
        gap = 244
        beg = 0
        length = len(all_data)
        while beg + gap <= length:
            ret.append(all_data[beg: beg+gap])
            beg += 1

        return ret




if __name__ == "__main__":

    testObj = Divider()
    testObj.divideDow()


