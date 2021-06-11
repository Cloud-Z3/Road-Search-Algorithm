from MyLib import*
t1=time()
knot_cor_id=open_KCI()
knotRoad=open_knotRoad(knot_cor_id)
allPath=open_path(knot_cor_id)
knot_id_cor=id2cor(knot_cor_id)

data = readData('rawmapn.tif')
data = np.array(data)
length=len(data)
wide=len(data[0])

print(0)
mode=0
points=randPeopleStream(data,mode,length,wide)
l=len(knot_id_cor)
distMat=[[len(data)*len(data[0]) for i in range(l)] for i in range(l)]
streamMat=[[0 for i in range(l)] for i in range(l)]
for i in allPath.keys():
    cor=str2cor(i)
    x=cor[0]
    y=cor[1]
    stream=weigthAdd(allPath[i],points)
    print(stream)
    distMat[x][y]=distance(allPath[i])
    streamMat[x][y]=stream
writeData('distMat.txt',distMat)
writeData('streamMat0.txt',streamMat)
writeData('points0.txt',points)

print(1)
mode=1
points=randPeopleStream(data,mode,length,wide)
l=len(knot_id_cor)
streamMat=[[0 for i in range(l)] for i in range(l)]
for i in allPath.keys():
    cor=str2cor(i)
    x=cor[0]
    y=cor[1]
    stream=weigthAdd(allPath[i],points)
    print(stream)
    streamMat[x][y]=stream
writeData('streamMat1.txt',streamMat)
writeData('points1.txt',points)

print(2)
mode=2
points=randPeopleStream(data,mode,length,wide)
l=len(knot_id_cor)
streamMat=[[0 for i in range(l)] for i in range(l)]
for i in allPath.keys():
    cor=str2cor(i)
    x=cor[0]
    y=cor[1]
    stream=weigthAdd(allPath[i],points)
    print(stream)
    streamMat[x][y]=stream
writeData('streamMat2.txt',streamMat)
writeData('points2.txt',points)

print(3)
mode=3
points=randPeopleStream(data,mode,length,wide)
l=len(knot_id_cor)
streamMat=[[0 for i in range(l)] for i in range(l)]
for i in allPath.keys():
    cor=str2cor(i)
    x=cor[0]
    y=cor[1]
    stream=weigthAdd(allPath[i],points)
    print(stream)
    streamMat[x][y]=stream
writeData('streamMat3.txt',streamMat)
writeData('points3.txt',points)

t7=time()
print(t7-t1)

#colorChange(data, 980, 1990, 30, 0, 255, 255)
image = Image.fromarray(data)  # 将之前的矩阵转换为图片
image.show()  # 调用本地软件显示图片，win10是叫照片的工具
