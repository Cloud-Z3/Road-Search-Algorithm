from PIL import Image
import numpy as np
from time import time
import matplotlib.pyplot as plt
import sys
from math import*

sys.setrecursionlimit(8000)

def readData(filename):                   #读取图片信息
    image_dir = filename
    x = Image.open(image_dir)  # 打开图片方式1
    #x = mpimg.imread(image_dir)  #打开图片方式2
    #x = Image.open(image_dir)    #打开图片方式2
    data = np.array(x)  # 转换为矩阵
    data.flags.writeable = True
    return data

def cor2str(i,j):
    return str(i)+','+str(j)

def str2cor(string):
    a=string.split(',')
    return (int(a[0]),int(a[1]))

def isBlack(alist):
    if alist[0]+alist[1]+alist[2]==0:
        return True
    else:
        return False

def isWhite(alist):
    if alist[0]==255 and alist[1]==255 and alist[2]==255:
        return True
    else:
        return False

def isKnot(cor_pixel,cor):
    x=cor[0]
    y=cor[1]
    sum=0
    if isWhite(cor_pixel[cor2str(x-1,y-1)]):
        sum+=1
    if isWhite(cor_pixel[cor2str(x-1,y)]):
        sum+=1
    if isWhite(cor_pixel[cor2str(x-1,y+1)]):
        sum+=1
    if isWhite(cor_pixel[cor2str(x,y-1)]):
        sum+=1
    if isWhite(cor_pixel[cor2str(x,y+1)]):
        sum+=1
    if isWhite(cor_pixel[cor2str(x+1,y-1)]):
        sum+=1
    if isWhite(cor_pixel[cor2str(x+1,y)]):
        sum+=1
    if isWhite(cor_pixel[cor2str(x+1,y+1)]):
        sum+=1
    if sum>=3 or sum==1: #阈值
        return True
    else:
        return False

def whitePointGet(data,cor_pixel):
    white_cor = []  # 白像素坐标
    length = len(data)
    wide = len(data[0])
    print(1)
    for i in range(length):
        for j in range(wide):
            cor_pixel[cor2str(i, j)] = data[i][j]  # 键值对生成
            if isWhite(data[i][j]):
                white_cor.append([i, j])  # 白像素提取
    print(2)
    return white_cor

def knotGet(data,white_cor,cor_pixel):
    knot = []  # 节点
    length = len(data)
    wide = len(data[0])
    for i in white_cor:
        if i[0] == 0 or i[0] == length - 1 or i[1] == 0 or i[1] == wide - 1:
            continue
        else:
            if isKnot(cor_pixel, i):
                knot.append(i)
    print(3)
    knotnew=filter(knot)
    while knotnew!=knot:
        knot=knotnew
        knotnew=filter(knot)
    return knotnew

def filter(knot):
    knotnew = []  # 筛选后节点
    visit = []
    for i in range(len(knot)):
        if (i in visit):
            continue
        nearpoints = []
        for j in range(i + 1, len(knot)):
            if (dist(knot[i], knot[j]) <= 2):
                nearpoints.append(knot[j])
                visit.append(j)
        l = len(nearpoints)
        if l == 0:
            knotnew.append(knot[i])
        else:
            xsum = knot[i][0] + sum([i[0] for i in nearpoints])
            ysum = knot[i][1] + sum([i[1] for i in nearpoints])
            knotnew.append([round(xsum / (l + 1)), round(ysum / (l + 1))])
    return knotnew

def LM(data):
    length=len(data)
    wide=len(data[0])
    return [[0 for i in range(wide)] for i in range(length)]

def search(scor,cor,LableMatrix,distMat,cor_color):
    length=len(LableMatrix)
    wide=len(LableMatrix[0])
    #print(cor)
    x=cor[0]
    y=cor[1]
    if LableMatrix[x][y] == 1 or dist(scor,cor)>500:  #限定搜索范围
        return 0
    keys=cor_color.keys()
    LableMatrix[x][y]=1
    road=[]
    if cor_color[cor2str(x,y)]==1:
        print('Got it!')
        return [[cor]]
    else:
        flag=0
        #pre condition judge
        if x!=0 and (cor2str(x-1,y) in keys) and LableMatrix[x-1][y]==0 and cor_color[cor2str(x-1,y)]==1:
            LableMatrix[x - 1][y] = 1
            return [[cor,[x-1,y]]]
        if x!=0 and (cor2str(x,y-1) in keys) and LableMatrix[x][y-1]==0 and cor_color[cor2str(x,y-1)]==1:
            LableMatrix[x][y-1] = 1
            return [[cor,[x,y-1]]]
        if x!=0 and (cor2str(x+1,y) in keys) and LableMatrix[x+1][y]==0 and cor_color[cor2str(x+1,y)]==1:
            LableMatrix[x + 1][y] = 1
            return [[cor,[x+1,y]]]
        if x!=0 and (cor2str(x,y+1) in keys) and LableMatrix[x][y+1]==0 and cor_color[cor2str(x,y+1)]==1:
            LableMatrix[x][y+1] = 1
            return [[cor,[x,y+1]]]
        if x!=0 and (cor2str(x-1,y-1) in keys) and LableMatrix[x-1][y-1]==0 and cor_color[cor2str(x-1,y-1)]==1:
            LableMatrix[x - 1][y-1] = 1
            return [[cor,[x-1,y-1]]]
        if x!=0 and (cor2str(x-1,y+1) in keys) and LableMatrix[x-1][y+1]==0 and cor_color[cor2str(x-1,y+1)]==1:
            LableMatrix[x - 1][y+1] = 1
            return [[cor,[x-1,y+1]]]
        if x!=0 and (cor2str(x+1,y-1) in keys) and LableMatrix[x+1][y-1]==0 and cor_color[cor2str(x+1,y-1)]==1:
            LableMatrix[x+1][y-1] = 1
            return [[cor,[x+1,y-1]]]
        if x!=0 and (cor2str(x+1,y+1) in keys) and LableMatrix[x+1][y+1]==0 and cor_color[cor2str(x+1,y+1)]==1:
            LableMatrix[x+1][y+1] = 1
            return [[cor,[x+1,y+1]]]
        if x!=0 and (cor2str(x-1,y) in keys) and LableMatrix[x-1][y]==0:
            #LableMatrix[x-1][y] = 1
            flag=1
            p=search(scor,[x-1,y], LableMatrix, distMat, cor_color)
            if p!=0:
                for i in range(len(p)):
                    roadt=[cor]
                    for j in p[i]:
                        roadt.append(j)
                    road.append(roadt)
        if y!=0 and (cor2str(x,y-1) in keys) and LableMatrix[x][y-1]==0:
            #LableMatrix[x][y-1] = 1
            flag = 1
            p=search(scor,[x,y-1], LableMatrix, distMat, cor_color)
            if p!=0:
                for i in range(len(p)):
                    roadt=[cor]
                    for j in p[i]:
                        roadt.append(j)
                    road.append(roadt)

        if x!=length-1 and (cor2str(x+1,y) in keys) and LableMatrix[x+1][y]==0:
            #LableMatrix[x+1][y] = 1
            flag = 1
            p=search(scor,[x+1,y], LableMatrix, distMat, cor_color)
            if p!=0:
                for i in range(len(p)):
                    roadt=[cor]
                    for j in p[i]:
                        roadt.append(j)
                    road.append(roadt)
        if y!=wide-1 and (cor2str(x,y+1) in keys) and LableMatrix[x][y+1]==0:
            #cor_color[cor2str(x,y+1)]==0
            #LableMatrix[x][y+1] = 1
            flag = 1
            p=search(scor,[x,y+1], LableMatrix, distMat, cor_color)
            if p!=0:
                for i in range(len(p)):
                    roadt=[cor]
                    for j in p[i]:
                        roadt.append(j)
                    road.append(roadt)
        if x!=0 and y!=0 and (cor2str(x-1,y-1) in keys) and LableMatrix[x-1][y-1]==0:
            #LableMatrix[x-1][y - 1] = 1
            flag = 1
            p=search(scor,[x-1,y-1], LableMatrix, distMat, cor_color)
            if p != 0:
                for i in range(len(p)):
                    roadt = [cor]
                    for j in p[i]:
                        roadt.append(j)
                    road.append(roadt)
        if x!=length-1 and y!=0 and (cor2str(x+1,y-1) in keys) and LableMatrix[x+1][y-1]==0:
            #LableMatrix[x+1][y - 1] = 1
            flag = 1
            p=search(scor,[x+1,y-1], LableMatrix, distMat, cor_color)
            if p != 0:
                for i in range(len(p)):
                    roadt = [cor]
                    for j in p[i]:
                        roadt.append(j)
                    road.append(roadt)
        if x!=0 and y!=wide-1 and (cor2str(x-1,y+1) in keys) and LableMatrix[x-1][y+1]==0:
            #LableMatrix[x-1][y + 1] = 1
            flag = 1
            p=search(scor,[x-1,y+1], LableMatrix, distMat, cor_color)
            if p != 0:
                for i in range(len(p)):
                    roadt = [cor]
                    for j in p[i]:
                        roadt.append(j)
                    road.append(roadt)
        if x!=length-1 and y!=wide-1 and (cor2str(x+1,y+1) in keys) and LableMatrix[x+1][y+1]==0:
            #LableMatrix[x+1][y + 1] = 1
            flag = 1
            p=search(scor,[x+1,y+1], LableMatrix, distMat, cor_color)
            if p != 0:
                for i in range(len(p)):
                    roadt = [cor]
                    for j in p[i]:
                        roadt.append(j)
                    road.append(roadt)
        if flag==0:
            return 0
        else:
            return road

def distance(aList):
    l=len(aList)
    dis=0
    for i in range(l-1):
        dis+=dist(aList[i],aList[i+1])
    return dis

def distanceAdd(data,knotnew,knot_cor_id,distMat,knotRoad,cor_color_ori):
    l=len(knotnew)
    allEdge = []
    for i in range(l):
        print(i)
        LableMatrix = LM(data)
        start=knotnew[i]
        cor_color=cor_color_ori.copy()
        cor_color[cor2str(start[0], start[1])] = 2
        road = search(start, start, LableMatrix, distMat, cor_color)
        for j in road:
            allEdge.append(j)
            s=j[0]
            e=j[-1]
            a=knot_cor_id[cor2str(s[0],s[1])]
            b=knot_cor_id[cor2str(e[0],e[1])]
            dis=distance(j)
            if(dis<distMat[a][b]):
                distMat[a][b] = dis
                distMat[b][a] = dis
                knotRoad[cor2str(a, b)] = j
                jr=j.copy()
                jr.reverse()
                knotRoad[cor2str(b, a)] = jr
            '''
            for k in j:
                print(k)
            x = j[-1][0]
            y = j[-1][1]
            dddata[x][y][0] = 0
            dddata[x][y][1] = 0
            dddata[x][y][2] = 255
        print(type(road))
            '''
    return allEdge

def writedata(file1,file2,file3,file4,distMat,knotRoad,knot_cor_id,allEdge):
    #距离矩阵写入文件
    f = open(file1,'w', encoding="utf-8")
    k=0
    for i in distMat:
        l = len(i)
        string = str(i[0])
        for j in range(0, l - 1):
            string += ' '
            string += str(i[j + 1])
        string += '\n'
        print(k)
        f.write(string)
        k+=1
    f.close()

    #路径写入文件
    f = open(file2, 'w', encoding="utf-8")
    for i in knotRoad.values():
        l = len(i)
        string = str(i[0][0])+','+str(i[0][1])
        for j in range(0, l - 1):
            string += ' '
            string += str(i[j + 1][0])+','+str(i[j + 1][1])
        string += '\n'
        f.write(string)
    f.close()

    #节点坐标——序号 写入文件
    f = open(file3, 'w', encoding="utf-8")
    for i in knot_cor_id.keys():
        string = i
        string += ','+str(knot_cor_id[i])+'\n'
        f.write(string)
    f.close()

    #边 写入文件
    f = open(file4, 'w', encoding="utf-8")
    for i in allEdge:
        l = len(i)
        string = str(i[0][0])+','+str(i[0][1])
        for j in range(0, l - 1):
            string += ' '
            string += str(i[j + 1][0])+','+str(i[j + 1][1])
        string += '\n'
        f.write(string)
    f.close()