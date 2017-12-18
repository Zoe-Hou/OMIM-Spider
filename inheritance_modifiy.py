import xlrd
from xlutils.copy import copy
import time

CurrentDate = time.strftime("%Y%m%d")
workbook = xlrd.open_workbook('omim_molecularBasis_'+ CurrentDate +'.xls')
sheet = workbook.sheet_by_name('normal')
wb = copy(workbook)
sheet_ = wb.get_sheet(0)



def find_all_leftIndex(str, leftBracket):
    return [i for i, s in enumerate(str) if s == leftBracket]


def find_all_rightIndex(str, rightBracket):
    return [i for i, s in enumerate(str) if s == rightBracket]

for si in range(1, sheet.nrows):
    str = sheet.cell(si, 2).value
    leftBraceList = find_all_leftIndex(str, '{')
    rightBraceList = find_all_leftIndex(str, '}')
    inheritanceName = ''
    i = 0
    for s in str:
        i = i + 1
        if len(leftBraceList)<1:
            inheritanceName = ''
        elif i < leftBraceList[0]:
            inheritanceName = inheritanceName + s
    #print(inheritanceName)


    def find_pos(string, search):
        pos = []
        start = 0
        while True:
            index = string.find(search, start)
            if index == -1:
                break
            pos.append(index)
            start = index + 1
        return pos


    snomedctID = []
    umlsID = []
    hpoID = []
    for bindex in range(len(leftBraceList)):
        braceContent = str[leftBraceList[bindex] + 1: rightBraceList[bindex]]
        # print(braceContent)
        pos_snomedctID = find_pos(braceContent, 'SNOMEDCT')
        pos_UMLS = find_pos(braceContent, 'UMLS')
        pos_HPO = find_pos(braceContent, 'HPO')
        for p in pos_snomedctID:
            snomedctID.append(braceContent[p + 9:p + 18])

        for p in pos_UMLS:
            result = []
            result.append(braceContent[p + 5:p + 13])
            k = p + 13
            while True:
                if braceContent[k:k + 2] == ',C':
                    result.append(braceContent[k + 1:k + 9])
                    k += 9
                else:
                    break
            for t in result:
                if t not in umlsID:
                    umlsID.append(t)
        for p in pos_HPO:
            result = []
            result.append(braceContent[p + 4:p + 14])
            k = p + 14
            while True:
                if braceContent[k:k + 3] == ',HP':
                    result.append(braceContent[k + 1:k + 11])
                    k += 9
                else:
                    break
            for t in result:
                if t not in hpoID:
                    hpoID.append(t)
    line = inheritanceName+';'
    for k in snomedctID:
        line += k +','
    line += ';'
    for k in umlsID:
        line += k + ','
    line += ';'
    for k in hpoID:
        line += k + ','
    #sheet.put_cell(i, 2, 1, line, 0)
    print(line)
    sheet_.write(si, 2, line)
wb.save('omim_inheritance_'+ CurrentDate +'.xls')
