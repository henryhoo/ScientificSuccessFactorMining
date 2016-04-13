#!/usr/bin/env python3
# encoding=utf8


from openpyxl import Workbook
import sqlite3
import sys


if len(sys.argv)<=1:
    print('%s output_dir' % sys.argv[0])
    sys.exit()

PATH = sys.argv[1]

if not PATH.endswith('/'):
    PATH += '/'

SQLITE3_FILE = './data_result.sqlite3'

conn = sqlite3.connect(SQLITE3_FILE)

cursor = conn.cursor()
cursor.execute('select * from data')
rows = cursor.fetchall()
cursor.close()


books = {}

for row in rows:
    year = row[0]
    if year in books:
        wb = books[year][0]
    else:
        wb = Workbook()
        books[year] = (wb, wb.active)
    ws = wb.active
    ws.append(row)

for key, value in books.items():
    wb = value[0]
    wb.save(PATH + key + '.xlsx')
