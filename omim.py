import requests
import json
from urllib.parse import quote
import math
import time
import xlwt

keyword = 'prefix:#'
totalResult = 4354
page = math.ceil(4354/20)

wb = xlwt.Workbook('omim.xls')
sheet1 = wb.add_sheet('normal')
sheet1.write(0, 0, 'mimnumber')
sheet1.write(0, 1, 'preferredTitle')
sheet1.write(0, 2, 'inheritance')
sheet1.write(0, 3, 'molecularBasis')
sheet1.write(0, 4, 'clinicalSynopsis')
line1_num = 1

sheet2 = wb.add_sheet('oldformat')
sheet2.write(0, 0, 'mimNumber')
sheet2.write(0, 1, 'preferredTitle')
sheet2.write(0, 2, 'oldFormat')
line2_num = 1

CurrentDate = time.strftime("%Y%m%d")
print(CurrentDate)
def find_all_leftIndex(str, leftBracket):
    return [i for i, s in enumerate(str) if s == leftBracket]


def find_all_rightIndex(str, rightBracket):
    return [i for i, s in enumerate(str) if s == rightBracket]

for p in range(page):
    #limit默认为10，接口中最多只能设置20，大于20均按照20展示结果
    url = 'https://api.omim.org/api/clinicalSynopsis/search?search='+ quote(keyword) + '&start=' +quote(str(p*20))+ '&limit=20&include=clinicalSynopsis&format=json'
    #print(url)
    cookies = {'ApiKey': 'xxxxxxxxxxxxxxx'}
    response = requests.get(url, cookies=cookies)
    data = json.loads(response.text)
    clinicalSynopsisList = data['omim']['searchResponse']['clinicalSynopsisList']
    #print(clinicalSynopsisList)
    for i in clinicalSynopsisList:
        cs = i['clinicalSynopsis']
        line = []
        if 'oldFormat' not in cs.keys():
            mimNumber = cs['mimNumber']  # mimNumber
            cs.pop('mimNumber')
            line.append(mimNumber)
            preferredTitle = cs['preferredTitle']  # preferredTitle
            cs.pop('preferredTitle')
            line.append(preferredTitle)
            if ('inheritance' in cs.keys()):
                inheritance = cs['inheritance']  # inheritance
                cs.pop('inheritance')
                #print(inheritance)
            else:
                inheritance = ''
            line.append(inheritance)
            if ('molecularBasis' in cs.keys()):
                molecularBasis = cs['molecularBasis']  # molecularBasis
                cs.pop('molecularBasis')

            line.append(molecularBasis)
            tmp = ''
            if 'molecularBasis' in cs.keys():
                cs.pop('molecularBasis')
            if 'prefix' in cs.keys():
                cs.pop('prefix')
            cs.pop('matches')
            [(k, cs[k]) for k in sorted(cs.keys())] # 对dict按照key排序
            for (k, v) in cs.items():
                tmp = tmp + str(k) + ':' + str(v).strip('\t') + '\n'
                # print("cs [%s]=" % k, v)
            # print()
            line.append(tmp)
            for t in range(len(line)):
                sheet1.write(line1_num, t, line[t])
            print('normal写入第' + str(line1_num) + '行')
            line1_num += 1

        else:
            mimNumber = cs['mimNumber']  # mimNumber
            line.append(mimNumber)
            preferredTitle = cs['preferredTitle']  # preferredTitle
            line.append(preferredTitle)
            tmp = ''
            [(k, cs['oldFormat'][k]) for k in sorted(cs['oldFormat'].keys())]  # 对dict按照key排序
            for (k, v) in cs['oldFormat'].items():
                tmp = tmp + str(k) + ':' + str(v).strip('\t') + '\n'
            line.append(tmp)
            for t in range(len(line)):
                sheet2.write(line2_num, t, line[t])
            print('oldformat写入第' + str(line2_num) + '行')
            line2_num += 1

    wb.save('omim_original_'+ CurrentDate + '.xls')