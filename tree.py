#!/usr/bin/env python3
# trees


import nltk
from nltk.draw.util import CanvasFrame
from nltk.draw.tree import TreeWidget
import sys

grammar = """
NOUN:{<NN>} # 名词
{<NNS>}     #复数名词
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

if len(sys.argv) < 2:
    sys.exit(0)

for s in sys.argv[1:]:
    print('*****************************')
    print(s)
    tags = nltk.pos_tag(nltk.word_tokenize(s))
    tree = nltk.chunk.ne_chunk(tags)
    print(str(tree))
    cf = CanvasFrame()
    tc = TreeWidget(cf.canvas(), tree)
    cf.add_widget(tc, 10, 10)
    cf.print_to_file(s+'.1.ps')
    cf.destroy()
    tree = cp.parse(tags)

    print(str(tree))
    cf = CanvasFrame()
    tc = TreeWidget(cf.canvas(), tree)
    cf.add_widget(tc, 10, 10)
    cf.print_to_file(s+'.2.ps')
