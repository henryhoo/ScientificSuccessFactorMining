#!/usr/bin/env python3
#encoding=utf8


import sqlite3
import math


DATA_SOURCE = './result.sqlite3'

result = sqlite3.connect(DATA_SOURCE)

try:
    cursor = result.cursor()
    cursor.execute('create table frequence(filename text,phrase text,'
        'N integer,M integer,frequence double,'
        'frequence_all double,rate double,'
        'TF double, IDF double,TF_IDF double)')
    result.commit()
    cursor.close()
except:
    pass

cursor = result.cursor()
cursor.execute('select count(phrase) from result')
rows = cursor.fetchall()
cursor.close()

total_phrase = rows[0][0]  # 总词频

cursor = result.cursor()
cursor.execute('select count(filename) from result group by filename')
rows = cursor.fetchall()
cursor.close()

N = rows[0][0]

cursor=result.cursor()
cursor.execute('select phrase,count(phrase) from result group by phrase')
rows = cursor.fetchall()
total_phrases = {}
for row in rows:
    total_phrases[row[0]]=row[1] # 在所有文件中的，单词词频
cursor.close()


cursor = result.cursor()
cursor.execute('select filename,count(phrase) from result group by filename')
rows = cursor.fetchall()
cursor.close()

filenames = rows

cursor = result.cursor()
for filename, phrase_count in filenames:
    cursor.execute('select phrase, count(phrase) from result where filename = ? group by phrase',(filename,))
    phrases = []
    rows = cursor.fetchall()
    for row in rows:
        phrases.append((row[0],row[1]))

    for phrase in phrases:
        frequence = phrase[1]/phrase_count
        frequence_all = total_phrases[phrase[0]]/total_phrase
        rate = math.log(frequence/frequence_all)

        TF = frequence

        cursor.execute('select filename from result where '
                       'phrase=? group by filename', (phrase[0], ))
        rows = cursor.fetchall()
        PN = len(rows)
        IDF = math.log(PN/N)

        TF_IDF = TF * IDF

        cursor.execute('insert into frequence values(?,?,?,?,?,?,?,?,?,?)',
            (filename,phrase[0],phrase[1],total_phrases[phrase[0]],
                frequence, frequence_all, rate, TF, IDF, TF_IDF))


result.commit()
cursor.close()
