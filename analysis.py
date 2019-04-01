dic = {}

fr = open('data.txt', 'r')
f1 = fr.readlines()
for i in f1:
    a = i.split()
    dic[a[0]] = a[1:]

fr.close()
mem = [float(i[0:-1]) for i in dic['mem'][1:-1]]
cpu = [float(i[0:-1]) for i in dic['cpu'][1:-1]]
store = [float(i[0:-1]) for i in dic['store'][1:-1]]
net = [float(i[0:-1]) for i in dic['net'][1:-1]]
print('mem: ', mem)
print('cpu: ', cpu)
print('store: ', store)
print('net: ', net)
