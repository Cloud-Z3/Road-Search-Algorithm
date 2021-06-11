from MyLib import*
t1=time()

distMat=open_distMat()
l=len(distMat)
data = readData('rawmapn.tif')
data = np.array(data)
print(1)

knot_cor_id=open_KCI()
print(2)

knotRoad=open_knotRoad(knot_cor_id)
allPath=open_path(knot_cor_id)
print(3)

knot_id_cor=id2cor(knot_cor_id)
l=len(knot_id_cor)
distMat_new=[[len(data)*len(data[0]) for i in range(l)] for i in range(l)]

for i in allPath.keys():
    cor=str2cor(i)
    x=cor[0]
    y=cor[1]
    distMat_new[x][y]=distance(allPath[i])

road=floyd(distMat_new)   #Floyd算法
#road=dijkstra(distMat_new,0)
'''所有键的显示
roadkeys=list(road.keys())
roadkeys=[str2cor(i) for i in roadkeys]
roadkeys.sort()
for key in roadkeys:
    print(key)'''
a=0
b=323
#pathShow(data, knot_id_cor, road, allPath, a, b)
'''#节点显示
for i in knot_cor_id.keys():
    cor=str2cor(i)
    x=cor[0]
    y=cor[1]
    colorChange(data, x, y, 5, 255, 0, 20)
image = Image.fromarray(data)  # 将之前的矩阵转换为图片
image.show()  # 调用本地软件显示图片，win10是叫照片的工具
'''

#路径显示
for i in allPath.keys():
    a2b=str2cor(i)
    a=a2b[0]
    b=a2b[1]
    abpath = allPath[i]
    for i in range(len(abpath)):
        p = abpath[i]
        x=p[0]
        y=p[1]
        if i==0 or i==len(abpath)-1:
            colorChange(data, x, y, 2, 255, 0, 0)
            continue
        colorChange(data, x, y, 1.5, 0, 255, 255)
image = Image.fromarray(data)  # 将之前的矩阵转换为图片
image.show()  # 调用本地软件显示图片，win10是叫照片的工具


#pathShow(data,knot_id_cor,road,allPath,a,b)
#pathShow(data,knot_id_cor,road,allPath,b,a)

''' #生成的Floyd矩阵可以放在第三阶段的文件夹里了
f = open('E:\\Jerry\\My University\\大学\\课程\\第四学期\\创业实训\\算法\\最终\\第三阶段——用户控制\\floyd.txt', 'w', encoding="utf-8")
for i in range(l):
    for j in range(i+1,l):
        roadi2j=road[cor2str(i,j)]
        length = len(roadi2j)
        string = str(roadi2j[0])
        for k in range(0, length - 1):
            string += ' '
            string += str(roadi2j[k + 1])
        string += '\n'
        f.write(string)
f.close()
t2=time()
#print(distMat)
#print(knot_cor_id)
#print(knotRoad)
print(t2-t1)
print(len(allPath))'''


