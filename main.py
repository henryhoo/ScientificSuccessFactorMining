#!/usr/bin/env python3
# encoding=utf8


import sqlite3
import nltk
import os
from nltk.stem import WordNetLemmatizer

wnl = nltk.stem.WordNetLemmatizer()


def isplural(word):
    lemma = wnl.lemmatize(word, 'n')
    plural = True if word is not lemma else False
    return plural, lemma


def all_ascii(text):
    for c in text:
        if not (c.isalpha() or c == ' ' or c == '-'):
            return False
    return True


def has_upper(text):
    for c in text:
        if c.isupper():
            return True
    return False


def strize(e):
    if type(e) != nltk.tree.Tree:
        if e[1] == 'NN' and has_upper(e[0]):
            return None
        return e[0]
    ch = []
    for i in e.leaves():
        t = strize(i)
        if t is None:
            return None
        ch.append(t)
    return ' '.join(ch)


grammar = """
NOUN:{<NN>} # 名词
{<NNS>}     # 复数名词
NOUN_NOUN:{<NOUN><NOUN>} # 名词+名词
ADJ:{<JJ>} # 形容词
ADJ_NOUN:{<ADJ><ADJ><NOUN>}
{<ADJ><NOUN><NOUN>}
{<ADJ><NOUN>} # 形容词+名词
NOUN_PREP_NOUN:{<ADJ><NOUN><IN><ADJ><NOUN>}
{<NOUN><IN><ADJ><NOUN>}
{<ADJ><NOUN><IN><NOUN>}
{<NOUN><IN><NOUN>} # 名词+介词+名词
ADV_ADJ:{<RB><ADJ>} # 副词+形容词
ADJ_PREP_NOUN:{<ADJ><IN><NOUN>} # 形容词+介词+名词
"""

cp = nltk.RegexpParser(grammar)


def fortree(tree, cur, filename):
    label = tree.label()
    if label == 'NOUN' or label == 'NOUN_NOUN' or label == 'ADJ_NOUN'\
       or label == 'NOUN_PREP_NOUN' or label == 'ADV_ADJ'\
       or label == 'ADJ_PREP_NOUN' or label == 'ADJ':
        text = strize(tree)
        if text is None:
            return
        if all_ascii(text):
            if label == "NOUN_NOUN":
                pass
            elif label == "NOUN":
                if has_upper(text):
                    return
                plural, text = isplural(text)
            elif label == "ADJ_NOUN":
                pass
            elif label == "NOUN_PREP_NOUN":
                pass
            elif label == "ADV_ADJ":
                pass
            elif label == "ADJ_PREP_NOUN":
                pass
            elif label == "ADJ":
                pass
            text = text.lower()
            cur.execute(
                'insert into result values(?,?,?)',
                (filename, text, label))
            return
    if tree.height() > 2:
        first = 0
        for subtree in tree.subtrees():
            if first == 0:
                first = 1
            else:
                fortree(subtree, cur, filename)


conn = sqlite3.connect('data.sqlite3')
cur = conn.cursor()
cur.execute('select content,filename from data')
all = cur.fetchall()
cur.close()

try:
    os.unlink('./result.sqlite3')
except:
    pass
retconn = sqlite3.connect('./result.sqlite3')

c = retconn.cursor()
c.execute('create table result(filename text, phrase text, label text)')
retconn.commit()
c.close()


cur = retconn.cursor()
for row in all:
    text = row[0]
    filename = row[1]
    sentences = nltk.sent_tokenize(text)
    for sentence in sentences:
        sentence = nltk.pos_tag(nltk.word_tokenize(sentence))
        tree = cp.parse(sentence)
        fortree(tree, cur, filename)

retconn.commit()
cur.close()
