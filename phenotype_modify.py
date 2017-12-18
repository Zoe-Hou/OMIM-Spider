import xlrd
from xlutils.copy import copy
import time

CurrentDate = time.strftime("%Y%m%d")
workbook = xlrd.open_workbook('omim_inheritance_'+ CurrentDate+ '.xls')
sheet = workbook.sheet_by_name('normal')
wb = copy(workbook)
sheet_ = wb.get_sheet(0)



def find_all_leftIndex(str, leftBracket):
    return [i for i, s in enumerate(str) if s == leftBracket]


def find_all_rightIndex(str, rightBracket):
    return [i for i, s in enumerate(str) if s == rightBracket]

for si in range(1, sheet.nrows):
    str = sheet.cell(si, 4).value
    list = str.split('\n')
    line = ''
    for str in list:
        leftBraceList = find_all_leftIndex(str, '{')
        rightBraceList = find_all_leftIndex(str, '}')
        inheritanceName = ''
        i = 0
        for s in str:
            i = i + 1
            if len(leftBraceList) < 1:
                inheritanceName = ''
            elif i < leftBraceList[0]:
                inheritanceName = inheritanceName + s
        # print(inheritanceName)

        def find_pos(string, search):
            pos = []
            start = 0
            while True:
                index = string.find(search, start)
                # if search string not found, find() returns -1
                # search is complete, break out of the while loop
                if index == -1:
                    break
                pos.append(index)
                # move to next possible start position
                start = index + 1
            return pos


        snomedctID = []
        umlsID = []
        hpoID = []
        ICD10CMID = []
        ICD9CMID = []
        for bindex in range(len(leftBraceList)):
            braceContent = str[leftBraceList[bindex] + 1: rightBraceList[bindex]]
            # print(braceContent)
            pos_snomedctID = find_pos(braceContent, 'SNOMEDCT')
            pos_UMLS = find_pos(braceContent, 'UMLS')
            pos_HPO = find_pos(braceContent, 'HPO')
            pos_ICD10CM = find_pos(braceContent, 'ICD10CM')
            pos_ICD9CM = find_pos(braceContent, 'ICD9CM')
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
            for p in pos_ICD10CM:
                result = []
                result.append(braceContent[p:])
                for t in result:
                    if t not in ICD10CMID:
                        ICD10CMID.append(t)
            for p in pos_ICD9CM:
                result = []
                result.append(braceContent[p:])
                for t in result:
                    if t not in ICD9CMID:
                        ICD9CMID.append(t)
        line += inheritanceName + ';' + 'snomedct:'
        for k in snomedctID:
            line += k + ','
        line += ';'
        for k in umlsID:
            line += k + ','
        line += ';'
        for k in ICD10CMID:
            line += k + ','
        line += ';'
        for k in ICD9CMID:
            line += k + ','
        line += ';'
        for k in hpoID:
            line += k + ','
            # sheet.put_cell(i, 2, 1, line, 0)
        line += '\n'
    print(line)
    sheet_.write(si, 4, line)
wb.save('omim_phenotype_'+ CurrentDate+ '.xls')
