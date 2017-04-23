#coding:utf-8

import re

hsi_origin = open('HSI.txt').read()

date_list = re.findall("class=\"first left bold noWrap\">(.*?)</td>", hsi_origin)

rate_list = re.findall("<td class=\"bold (green|red)Font\">(.*?)</td>", hsi_origin)

price_list = re.findall("<td class=\"(green|red)Font\">(.*?)</td>", hsi_origin)

out_file = open("HSI_rate","w")

for index in range(len(date_list)):
    format_date = date_list[index].replace("年", "-").replace("月","-").replace("日","")
    format_rate = eval(rate_list[index][1].replace("%", "")) / 100
    out_file.write(format_date + " " + str(format_rate) + " " + str(price_list[index][1]) + "\n")

out_file.close()



pass

