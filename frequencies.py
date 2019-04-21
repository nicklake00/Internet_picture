import pymorphy2
import re
import operator

morph = pymorphy2.MorphAnalyzer()
v = []

d = {}
last_d = {}
my_file = open("all_of_news.txt", "r")
data = my_file.readlines() # read ALL the lines!
#print(data[0])
my_file.close()


for j in range(len(data)):
    str1 = data[j].split()
    for i in str1: #data[0]:
        p = morph.parse(i)[0]
        l = p.tag.POS
        p = p.normal_form
        result = re.sub(r',' , '', p)
        result = re.sub(r'»', '', result)
        result = re.sub(r'«', '', result)
        #result = re.sub(r'.', '', result)

        #if ((l == 'NOUN') or (l == None)):
        if ((l == 'VERB') or (l == None) or (l == 'INFN') or (l == 'PRTS') or (l == 'PRTF') or (l == 'GRND')):
        #if (l == 'ADJF' or l == 'ADJS' or l == 'ADVB' or l == None):
	        if d.get(result) == None:
	            d[result] = 1
	        else:
	            d[result] += 1

        #print(result, ' ', l)
    print(j, '\n')

for w in sorted(d, key=d.get, reverse=True):
    #print(w, ' ', d[w])
    if (d[w] >= 10):
    	last_d[w] = d[w]

new_file = open("frequences_all_verbs.txt", "a")
for w in sorted(last_d, key=d.get, reverse=True):
	print(w, ' ', d[w])
	new_file.write(w)
	new_file.write(' ')
	new_file.write(str(d[w]))
	new_file.write('\n')

