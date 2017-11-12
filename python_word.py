import pymongo
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import jieba

conn = pymongo.MongoClient('localhost', 27017)
db = conn.pythonweb_db
work_detail = db.work_detail


def write_file():
    result = work_detail.find({})
    with open('description.txt', 'w') as fp:
        for i in result:
            data = i['description']
            fp.write(data.encode('utf-8'))
    print 'well done!'

write_file()


text_file = open('description.txt').read()
word_list_after_jieba = jieba.cut(text_file, cut_all=True)

wl_space_split = ' '.join(word_list_after_jieba)
print wl_space_split
my_wordcloud = WordCloud(font_path='simsun.ttc', width=1920, height=1080).generate(wl_space_split)
plt.imshow(my_wordcloud)
plt.axis('off')
plt.show()

