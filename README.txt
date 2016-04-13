
ex2sql.py   指定一个包含所有excel文件的目录，将excel文件转化为sqlite3格式。
            在当前目录下生成data.sqlite3。

            data.sqlite3只有一个表，就是
                data(year text,filename text, author text,article text,
                     journal text, page text, publish text, comment text,
                     address text, content text,reference text)

main.py     对data表进行处理，提取出所有符合条件的单词和词组，得到result.sqlite3。

            result.sqlite3只有一个表，就是
                result(filename text, phrase text, label text)

frequence.py 对result表进行统计，在result.sqlite3中直接创建新表frequence。

            frequence(filename text,phrase text,
                      N integer,M integer,frequence double,
                      frequence_all double,rate double,'
                      TF double, IDF double,TF_IDF double)


-----------------------------------------------------------

final.py 是将上述三个步骤整合起来的程序，指定一个包含所有excel文件的目录。
         生成final.sqlite3，其中包含上述的几个表。


country.py 指定final.sqlite3和国家文件excel，将在fianl.sqlite3中添加国家表country和城市表city。

topic.py 指定final.sqlite3和主题词文件excel。生成topic.sqlite3，其中包含了所有topic相关的表。
        basic
        topic
        year
        year_detail      
        continent
        continent_detail
        state_year
        state_year_detail
        region
        region_detail
        type_basic
        type
        type_detail

xltopic.py 指定topic.sqlite3，生成一个主题词的excel文件


----------------------------------------------------------------------
这些是额外的程序

pdf.py  就是解析pdf不同片段数据，这其实是真正的第一步。然后结合这个结果手动完成了所有的pdf数据。

country.py  将pdf中的地址和excel格式的城市、国家匹配起来，有些没有匹配到的手动处理的。


pdf_country.py 这个其实就是将excel格式的国家和pdf对象的转化为sqlite3格式。输入是手动匹配完的结果。

tree.py     生成语法分析，可视化的树状图。几个ps文件就是输出。

lite2my.py 将sqlite3数据录入到mysql数据库

openpyxl 是一个第三方库，用来解析excel文件的，只能解析xlsx，不能解析xls
