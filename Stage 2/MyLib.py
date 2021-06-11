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