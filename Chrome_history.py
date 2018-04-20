import os,sqlite3,urlparse,pyecharts

data_path = os.path.expanduser('~')+'/.config/google-chrome/Default'
#data_path =os.path.expanduser('~')+'/.mozilla/firefox/aequw2ah.default'
print os.listdir(data_path)
history_db = os.path.join(data_path,'History')
print history_db
conn = sqlite3.connect(history_db)
cursor = conn.cursor()
state = "select urls.url,urls.visit_count from urls,visits where urls.id=visits.url;"
#state ="select * from sqlite_master;"
#state = "select * from urls;"
cursor.execute(state)
result = cursor.fetchall()

def get_domain(url):
    try:
        url_change = urlparse.urlparse(url)
        if url_change[1]:
            domain =url_change[0]+'://'+url_change[1]
        else:
            domain = 'Local file'
        return domain
    except IndexError:
        print "parse URL fail,Please double check URL format"

dict ={}
for item in result:
    dict[item[0]]=item[1]
print len(dict)
dic_new={}
for key,value in dict.items():
    dic_new[get_domain(key)]=value
    if get_domain(key) in dic_new.keys():
        dic_new[get_domain(key)] += value
    else:
        dic_new[get_domain(key)] = value

attr=[]
value =[]
for k,v in sorted(dic_new.items(),key=lambda  item:item[1],reverse=True):
    attr.append(k)
    value.append(v)

bar = pyecharts.Bar(width=1000)
bar.add('',attr,value,mark_line=["average"], mark_point=["min", "max"], is_more_utils=True,xaxis_rotate=60)
bar.show_config()
bar.render()
