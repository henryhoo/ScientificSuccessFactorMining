#!/usr/bin/env python3
#encoding=utf8


import sqlite3
import openpyxl
import sys


if len(sys.argv)<=2:
    print('%s sqlite3 table [more tables]' % sys.argv[0])
    sys.exit(0)

conn = sqlite3.connect(sys.argv[1])

for table in sys.argv[2:]:
    cursor=conn.cursor()
    cursor.execute('select * from '+ table)
    rows = cursor.fetchall()
    cursor.close()

    wb = openpyxl.Workbook()
    ws = wb.active
    for row in rows:
        ws.append(list(row))
    wb.save(table+'.xlsx')
    print(table+'.xlsx is saved')
