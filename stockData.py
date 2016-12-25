#coding:utf-8
import time
import numpy
import math
import sys

reload(sys)

sys.setdefaultencoding('utf8')

class stockDataProcessor:
    __fileName = "000001.csv"

    def processStockProfitability(self):
        stockData = open(self.__fileName)
        res = []
        ret = []
        while True:
            line = stockData.readline().decode('gbk')
            if line != None:
                dataList = line.split(',')
                if dataList[0] == '':
                    break;
                item = [time.strptime(dataList[0],"%Y/%m/%d"), eval(dataList[3])]
                res.append(item)
            else:
                break
        #找出每月的收益
        monthBegFlag = []
        preFlag = []
        for item in res:
            if preFlag==[]:
               monthBegFlag = item
               preFlag = item
               continue
            elif item[0].tm_mon != preFlag[0].tm_mon:
                pro = math.log(preFlag[1]/monthBegFlag[1])
                ret.append( pro)
                preFlag = item
                monthBegFlag = item
            else:
                preFlag = item
        #最后一个数据
        ret.append(math.log(res[len(res)-1][1]/monthBegFlag[1]))
        return ret

    def processSaveRate(self):
        file = open('moneyProRate.csv')
        ret = []
        while True:
            line = file.readline()
            if line == '':
                break
            if line != None:
                rate = eval(line)
                for index in range(0,12):
                    ret.append(math.log(1+rate/1200))
            else:
                break
        return ret


    def processCustomData(self):
        file = open('xiaofei.csv')
        ret = []

        while True:
            line = file.readline()
            if line == '':
                break
            data = eval(line.split(',')[1])
            ret.append(math.log(1+data/100))
        return ret

    def calc(self):
        stock = self.processStockProfitability()
        custom = self.processCustomData()
        save = self.processSaveRate()

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

        #aer
        aer = []
        for index in range(0,84):
            aer.append(stock[index] - save[index])

        #aer计算
        aer_ave = numpy.average(aer)
        aer_sigma = math.sqrt(numpy.var(aer))
        aer_cov = numpy.cov(custom,aer)
        aer_per = numpy.corrcoef(custom,aer)


        #算sigma_m：
        sigmaM = (aer_ave + numpy.var(aer)/2)/aer_sigma
        gema =  (aer_ave + numpy.var(aer)/2)/aer_cov[0][1]

        #输出结果

        fileOutput = open('result.txt', 'w')
        fileOutput.write("股票：\n" + "\t均值: " + str(stock_ave) + "\n\t标准差：" + str(stock_sigma) + "\n\t协方差：" + str(stock_cov[0][1]) + "\n\t相关系数："+str(stock_per[0][1]) + u"\n")
        fileOutput.write("居民消费增长率：\n" + "\t均值: " + str(custom_ave) + "\n\t标准差：" + str(custom_sigma) + "\n\t协方差：" + str(custom_cov) + "\n\t相关系数："+str(custom_per) + u"\n")
        fileOutput.write("储蓄利率：\n" + u"\t均值: " + str(save_ave) + "\n\t标准差：" + str(save_sigma) + "\n\t协方差：" + str(save_cov[0][1]) + "\n\t相关系数："+str(save_per[0][1]) + "\n")
        fileOutput.write("aer：\n" + "\t均值: " + str(aer_ave) + "\n\t标准差：" + str(aer_sigma) + "\n\t协方差：" + str(aer_cov[0][1]) + "\n\t相关系数："+str(aer_per[0][1]) + "\n")

        fileOutput.write("\nsigmaM: " + str(sigmaM) + "\n")

        fileOutput.write("\ngema: " + str(gema) + "\n")




if __name__ == '__main__':
    obj = stockDataProcessor()
    obj.calc()