# 第二阶段介绍

## 目的

在这一阶段生成一个Floyd矩阵，表示任意两个节点间的路径信息（虽然第三阶段已经不需要这个啦，不过还是放这里好了）

## 方法

算法很简单，用**Dijkstra**、**Floyd**分别找到单源、全源最短路径即可。

等等，那每条边的长度呢？

在上一阶段已经得到所有边的像素信息了，只需根据像素信息计算边的长度即可（相邻像素距离为1，斜对角线相邻像素距离为根号2）。长度即为图的边的权重，于是现在我们已经得到矩阵了，对每个点跑一下Dijkstra算法就OK。

## 代码

调用的函数库：MyLib.py

```python
from time import*
from math import*
from PIL import Image
import numpy as np
from copy import *
epsilon=0.0001
def readData(filename):                   #读取图片信息
    image_dir = filename
    x = Image.open(image_dir)  # 打开图片方式1
    #x = mpimg.imread(image_dir)  #打开图片方式2
    #x = Image.open(image_dir)    #打开图片方式2
    data = np.array(x)  # 转换为矩阵
    data.flags.writeable = True
    return data

def distance(aList):
    l=len(aList)
    dis=0
    for i in range(l-1):
        dis+=dist(aList[i],aList[i+1])
    return dis

def cor2str(i,j):
    return str(i)+','+str(j)

def str2cor(string):
    a=string.split(',')
    return (int(a[0]),int(a[1]))

def open_distMat():
    with open('distMat.txt', 'r', encoding='utf-8') as f:
        distMat=[]
        for line in f:
            distMati = line.strip().split(' ')
            distMat.append([float(i) for i in distMati])
    f.close()
    return distMat

def open_KCI():
    with open('knot_cor_id.txt', 'r', encoding='utf-8') as f:
        knot_cor_id = dict()
        for line in f:
            cor_id = line.strip().split(',')
            knot_cor_id[cor_id[0] + ',' + cor_id[1]] = int(cor_id[2])
    f.close()
    return knot_cor_id

def open_knotRoad(knot_cor_id):
    with open('knotRoad.txt', 'r', encoding='utf-8') as f:
        knotRoad = dict()
        for line in f:
            road = line.strip().split(' ')
            a = knot_cor_id[road[0]]
            b = knot_cor_id[road[-1]]
            knotRoad[cor2str(a, b)] = [[j for j in str2cor(i)] for i in road]
    f.close()
    return knotRoad

def open_path(knot_cor_id):
    with open('allEdge.txt', 'r', encoding='utf-8') as f:
        allPath = dict()
        for line in f:
            road = line.strip().split(' ')
            a = knot_cor_id[road[0]]
            b = knot_cor_id[road[-1]]
            allPath[cor2str(a, b)] = [[j for j in str2cor(i)] for i in road]
    f.close()
    return allPath


def id2cor(knot_cor_id):
    knot_id_cor=dict()
    for i in knot_cor_id.keys():
        knot_id_cor[knot_cor_id[i]]=[j for j in str2cor(i)]
    return knot_id_cor

def colorChange(data,x,y,R,r,g,b):
    R=round(R)
    length=len(data)
    wide=len(data[0])
    p_candi=[]
    for i in range(-R,R+1):
        for j in range(-R,R+1):
            if x+i>=0 and x+i<length and y+j>=0 and y+j<wide:
                if dist([x+i,y+j],[x,y])<=R:
                    p_candi.append([x+i,y+j])
    for i in p_candi:
        x=i[0]
        y=i[1]
        data[x][y][0] = r
        data[x][y][1] = g
        data[x][y][2] = b

def floyd(distmat):
    l=len(distmat)
    road=dict()
    for i in range(l):
        print(i)
        roadi=dijkstra(distmat,i)
        for key in roadi.keys():
            if i==key:
                continue
            road[cor2str(i,key)]=roadi[key]
    return road

def dijkstra(distmat,a):
    distMat=deepcopy(distmat)
    maxdis = max([max(b) for b in distMat])
    road=dict()
    l=len(distMat)
    visit=set()
    visit.add(a)
    unvisit=set()
    for i in range(l):
        if distMat[a][i]==0:
            road[i]=[i]
            continue
        if distMat[a][i]!=maxdis:
            road[i]=[a,i]
    for i in range(l):
        if i==a:
            continue
        unvisit.add(i)
    while len(unvisit)!=0:
        uv=list(unvisit)
        id=uv[0]
        minimum=distMat[a][id]
        for i in uv:
            if distMat[a][i]<minimum-epsilon:
                minimum=distMat[a][i]
                id=i
        visit.add(id)
        unvisit.remove(id)
        uv=list(unvisit)
        for i in uv:
            if distMat[a][id]+distMat[id][i]<distMat[a][i]-epsilon:
                distMat[a][i] = distMat[a][id] + distMat[id][i]
                distMat[i][a] = distMat[a][id] + distMat[id][i]
                roadid=road[id].copy()
                roadid.append(i)
                road[i]=roadid
    return road

def pathShow(data,knot_id_cor,road,knotRoad,a,b):
    abpath = road[cor2str(a, b)]
    for i in range(len(abpath) - 1):
        s = abpath[i]
        e = abpath[i + 1]
        se_road = knotRoad[cor2str(s, e)]
        for j in range(1, len(se_road) - 1):
            x = se_road[j][0]
            y = se_road[j][1]
            colorChange(data, x, y, 2.5, 0, 255, 255)

    for i in range(len(abpath) - 1):
        s = abpath[i]
        e = abpath[i + 1]
        cor_s = knot_id_cor[s]
        cor_e = knot_id_cor[e]
        xs = cor_s[0]
        ys = cor_s[1]
        xe = cor_e[0]
        ye = cor_e[1]
        colorChange(data, xs, ys, 1, 255, 0, 20)
        if i == len(abpath) - 2:
            colorChange(data, xe, ye, 1, 255, 0, 20)

    image = Image.fromarray(data)  # 将之前的矩阵转换为图片
    image.show()  # 调用本地软件显示图片，win10是叫照片的工具
```

主程序：GraphAlth.py

```python
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
```

