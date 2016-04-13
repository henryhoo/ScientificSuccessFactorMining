#!/usr/bin/env python3
# encoding=utf8


from gi.repository import Poppler
import re
import sys
import os
import sqlite3

SQLITE3_FILE = './data_result.sqlite3'

try:
    os.unlink(SQLITE3_FILE)
except:
    pass

conn = sqlite3.connect(SQLITE3_FILE)
cursor = conn.cursor()
try:
    cursor.execute(
        'create table data(year text, filename text, commet text, address text, content text, comment_todo text, content_todo text)')
    conn.commit()
except:
    pass
cursor.close()


date_regexp = '(January|February|March|April|May|June|July|August|September|October|November|December)\s[0-9]{1,2}(,|\.)\s*[0-9]{4,4}\s'

SUCCESS = 1
SUCCESS_COMMENT = 2
SUCCESS_CONTENT = 3
FAIL = 4


def get_pdf_content(filepath):
    global SUCCESS_COMMENT, SUCCESS, FAIL, SUCCESS_CONTENT
    path = 'file://' + filepath
    doc = Poppler.Document.new_from_file(path)
    page = doc.get_page(0)

    text = page.get_text()
    text = text.replace('\n', ' ')

    text = re.sub('\s+[1-9][0-9]?\.\s+[A-Z]', '\n', text)
    text = text.splitlines()[0]

    text = re.sub('indicates\s+that\s+this\s+paper\s+was\s+cited', '\n', text)
    text = re.sub(
        'indicates\s+that\s+this\s+paper\s+has\s+been\s+cited', '\n', text)

    # print('------------------------------------')
    # print(page.get_text())
    ret = SUCCESS
    text = re.sub('\[[^\[\]]+\]', '\n', text)
    lines = text.splitlines()
    if len(lines) == 2:
        text = lines[0]
        text = re.sub('(,?\s+[0-9]{4,4}|\s+p)\.\s', '\n', text)
        tmp = ['', text.splitlines()[-1], lines[1]]
        lines = tmp
        ret = SUCCESS_COMMENT
    elif len(lines) < 3:
        return FAIL, None, None, None
    comment = lines[1]
    text = re.sub(date_regexp, '\n', lines[2])
    lines = text.split('\n', 1)
    if len(lines) < 2:
        if ret != SUCCESS:
            return FAIL, None, None, None
        return SUCCESS_CONTENT, comment, lines[0], lines[0]
    address = lines[0]
    content = lines[1]
    return ret, comment, address, content

# prev, address, content = get_pdf_content(sys.argv[1])
# print(prev)
# print('------------------------------------')
# print(address)
# print('------------------------------------')
# print(content)
# sys.exit()

if len(sys.argv) <= 1:
    print('%s pdf_dir' % sys.argv[0])
    sys.exit(0)


success = 0
success_comment = 0
success_content = 0
fail = 0

cursor = conn.cursor()
for parent, dirnames, filenames in os.walk(sys.argv[1]):
    base = os.path.basename(parent)
    try:
        if not (int(base) >= 1977 and int(base) <= 1993):
            continue
    except Exception as e:
        continue

    s = 0
    f = 0
    s_comment = 0
    s_content = 0
    for filename in filenames:
        if not filename.endswith('.pdf'):
            continue
        path = parent + '/' + filename
        try:
            ret, comment, address, content = get_pdf_content(path)
            if len(content) < 500:
                ret = FAIL
        except Exception as e:
            print(e)
            ret = FAIL
        filename = filename[:-4]
        year = base
        if ret == FAIL:
            f += 1
            cursor.execute('insert into data values(?,?,?,?,?,?,?)',
                           (year, filename, '', '', '', '', ''))
        else:
            comment_todo = ''
            content_todo = ''
            if ret == SUCCESS_COMMENT:
                s_comment += 1
                comment_todo = comment
            elif ret == SUCCESS_CONTENT:
                s_content += 1
                content_todo = content
                address = ''
                content = ''
            else:
                s += 1
            cursor.execute('insert into data values(?,?,?,?,?,?,?)',
                           (year, filename, comment, address, content,
                            comment_todo, content_todo))

    print(base)
    print('success: ' + str(s))
    print('fail: ' + str(f))
    print('success_comment: ' + str(s_comment))
    print('success_content: ' + str(s_content))
    print('-----------------------------------------')
    success += s
    fail += f
    success_content += s_content
    success_comment += s_comment


print('-----------------------------------------')
conn.commit()
cursor.close()
print('result:' )
print('success: ' + str(success))
print('fail: ' + str(fail))
print('success_comment: ' + str(success_comment))
print('success_content: ' + str(success_content))
