#coding:utf-8

import math
import time
import numpy
import sys

reload(sys)

sys.setdefaultencoding('utf8')


class ProcessData:

    __gap = 2

    def processCustomData(self):
        #数据格式：
        #时间	社会消费品零售总额_当期值(亿元)	社会消费品零售总额_累计值(亿元)
        file = open(u'居民消费总额.csv')
        record = []
        ret = []

        line = file.readline()
        while 0 != len(line):
            item = line.split(u',')
            leng = len(item[0])
            item[0] = item[0][6: len(item[0])-2]

            if 0 == eval(item[0]) % self.__gap:
                if 0 == len(ret)%6:
                    preval = 0
                else:
                    preval = record[len(record)-1]
                ret.append(eval(item[2]) - preval)
                record.append(eval(item[2]))
            line = file.readline()
        index = len(ret)-1
        while index > 0:
            ret[index] = math.log(ret[index]/ret[index-1])
            index -= 1
        #去掉第一个数据
        ret.pop(0)

        return ret

    def prodessStockData(self):
        #数据格式：
        #日期	股票代码	名称	收盘价
        file = open(u'三板成指.csv')
        ret = []
        record = []

        #读入数据
        line = file.readline().decode('gbk').encode('UTF-8')
        while 0!=len(line):
            line = line.split(',')
            record.append([time.strptime(line[0], "%Y-%m-%d"), eval(line[1])])
            line = file.readline().decode('gbk')


        #以gap个月为单位的收益率
        monthEndFlag = []
        preFlag = []
        gap = self.__gap  # 以几个月为单位，以后只要修改这里就可以了
        for dataItem in record:

            if 1 == gap:
                gapCondition = True
            else:
                gapCondition = 0 != dataItem[0].tm_mon%gap


            if preFlag!= [] and gapCondition and dataItem[0].tm_mon != preFlag[0].tm_mon:
                if 0 != len(monthEndFlag):
                    ret.append(math.log(preFlag[1]/monthEndFlag[1]))
                monthEndFlag = preFlag
            preFlag = dataItem
        #最后一个月的数据要加上
        var = record[len(record)-1][1]
        ret.append(math.log(record[len(record)-1][1]/monthEndFlag[1]))
        return ret

    def processInterestRate(self):
        file = open(u'一年期存款利率.csv')
        temp = []
        ret = []

        line = file.readline()
        while 0 != len(line):
            rate = eval(line) / 100
            temp.append(rate)
            line = file.readline()

        for i in range(1, len(temp)):
            ret.append(math.log(temp[i]/temp[i-1]))
        return ret




        #以下为年度数据，需要除以月度
        # line = file.readline()
        # while 0 != len(line):
        #     rate = eval(line)/1200
        #     for index in range(0,6):
        #         ret.append(rate)
        #     line = file.readline()
        # ret.pop(0)
        # return ret

    def calc(self):
        stock = self.prodessStockData()
        custom = self.processCustomData()
        save = self.processInterestRate()

        #股票
        stock_ave = numpy.average(stock)
        stock_sigma = math.sqrt(numpy.var(stock))
        stock_cov = numpy.cov(custom, stock)
        stock_per = numpy.corrcoef(custom,stock)

        #消费增长率
        custom_ave = numpy.average(custom)
        custom_sigma = math.sqrt(numpy.var(custom))
        custom_cov = numpy.cov(custom)
        custom_per = 1.0

        #无风险利率
        save_ave = numpy.average(save)
        save_sigma = math.sqrt(numpy.var(save))
        save_cov = numpy.cov(custom,save)
        save_per = numpy.corrcoef(custom,save)

        #记录条数
        length = len(save)

        #aer
        aer = []
        for index in range(0, length):
            aer.append(stock[index] - save[index])

        #aer计算
        aer_ave = numpy.average(aer)
        aer_sigma = math.sqrt(numpy.var(aer))
        aer_cov = numpy.cov(custom, aer)
        aer_per = numpy.corrcoef(custom,aer)


        #算sigma_m：
        sigmaM = (aer_ave + numpy.var(aer)/2)/aer_sigma
        gema =  (aer_ave + numpy.var(aer)/2)/aer_cov[0][1]

        #输出结果

        fileOutput = open('result.txt','w')
        fileOutput.write("股票：\n" + "\t均值: " + str(stock_ave) + "\n\t标准差：" + str(stock_sigma) + "\n\t协方差：" + str(stock_cov[0][1]) + "\n\t相关系数："+str(stock_per[0][1]) + u"\n")
        fileOutput.write("居民消费增长率：\n" + "\t均值: " + str(custom_ave) + "\n\t标准差：" + str(custom_sigma) + "\n\t协方差：" + str(custom_cov) + "\n\t相关系数："+str(custom_per) + u"\n")
        fileOutput.write("储蓄利率：\n" + u"\t均值: " + str(save_ave) + "\n\t标准差：" + str(save_sigma) + "\n\t协方差：" + str(save_cov[0][1]) + "\n\t相关系数："+str(save_per[0][1]) + "\n")
        fileOutput.write("aer：\n" + "\t均值: " + str(aer_ave) + "\n\t标准差：" + str(aer_sigma) + "\n\t协方差：" + str(aer_cov[0][1]) + "\n\t相关系数："+str(aer_per[0][1]) + "\n")

        fileOutput.write("\nsigmaM: " + str(sigmaM) + "\n")

        fileOutput.write("\ngema: " + str(gema) + "\n")



if __name__ == "__main__":
    testObj = ProcessData()
    testObj.calc()


