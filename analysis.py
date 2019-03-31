dic = {}

fr = open('data.txt', 'r')
f1 = fr.readlines()
for i in f1:
    a = i.split()
    dic[a[0]] = a[1]

fr.close()
print(dic)
