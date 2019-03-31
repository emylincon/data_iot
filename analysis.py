fr = open('data.txt', 'r')
f1 = fr.readlines()
for i in f1:
    a = i.split()
    i[0] = i[1]

fr.close()
