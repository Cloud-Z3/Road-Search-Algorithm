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

a=5
b=294
mode = 2 # 此处选择模式
# 0 早上8点，这时人流主要分布在宿舍区、品学楼、立人楼及之间的路上
# 1 中午13点，这时人流主要分布在宿舍区
# 2 晚上9点，这时人流主要分布在科研楼、体育场
# 3 人流均匀分布
t4 = time()
show(data,knot_id_cor,allPath,a,b,mode)
'''
distMat = open_distMat('distMat.txt')
streamMat = open_distMat('streamMat' + str(mode) + '.txt')
points = open_distMat('points' + str(mode) + '.txt')
l = len(knot_id_cor)
distMat_new = [[0 for i in range(l)] for i in range(l)]
weigth = -0.5
for x in range(l):
    for y in range(l):
        if distMat[x][y] != len(data) * len(data[0]):
            distMat_new[x][y] = distMat[x][y] + weigth * streamMat[x][y]
        else:
            distMat_new[x][y] = len(data) * len(data[0])
roadd = dijkstra2(distMat_new, a)
pathShow(data, knot_id_cor, roadd, allPath, a, b)
for i in points:
    x = int(i[0])
    y = int(i[1])
    colorChange(data, x, y, 0, 255, 0, 0)
# colorChange(data, 980, 1990, 30, 0, 255, 255)
image = Image.fromarray(data)  # 将之前的矩阵转换为图片
image.show()  # 调用本地软件显示图片，win10是叫照片的工具'''


print(t4 -t1)
