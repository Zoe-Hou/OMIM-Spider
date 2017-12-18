import xlrd
from xlutils.copy import copy
import time

CurrentDate = time.strftime("%Y%m%d")
workbook = xlrd.open_workbook('omim_original_'+ CurrentDate+ '.xls')
sheet = workbook.sheet_by_name('normal')
wb = copy(workbook)
sheet_ = wb.get_sheet(0)

def find_all_leftIndex(str, leftBracket):
    return [i for i, s in enumerate(str) if s == leftBracket]

def find_all_rightIndex(str, rightBracket):
    return [i for i, s in enumerate(str) if s == rightBracket]

for mi in range(1, sheet.nrows):
    molecularBasis = sheet.cell(mi, 3).value
    leftBracketList = find_all_leftIndex(molecularBasis, '(')
    rightBracketList = find_all_rightIndex(molecularBasis, ')')
    count = len(leftBracketList)
    if count > len(rightBracketList):
        count = len(rightBracketList)
    geneList = ''
    for index in range(count):
        geneStr = molecularBasis[leftBracketList[index] + 1:rightBracketList[index]]
        if(',') in geneStr:
            print(geneStr)
            geneList = geneList + geneStr + '\n'
    sheet_.write(mi, 3, geneList)
wb.save('omim_molecularBasis_'+ CurrentDate +'.xls')