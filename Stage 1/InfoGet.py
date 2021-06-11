
#!D:/workplace/python
# -*- coding: utf-8 -*-
# @File  : face_prepare.py
# @Author: WangYe
# @Date  : 2019/4/17
# @Software: PyCharm
from MyLib import*

if __name__=='__main__':
    t1=time()
    print(1)
    #1数据读入
    data = readData('skeleton.png')
    data = np.array(data)
    cor_pixel = dict()  # 坐标——像素
    t2=time()

    #2白色像素提取
    white_cor = whitePointGet(data,cor_pixel)
    t3=time()

    #3节点提取
    knotnew=knotGet(data,white_cor,cor_pixel)
    plt.scatter([i[0] for i in knotnew],[i[1] for i in knotnew])
    #plt.show()
    t4=time()

    #4节点标记
    for i in knotnew:         #节点标记为红色
        data[i[0]][i[1]][1] = 0
        data[i[0]][i[1]][2] = 0
    #image = Image.fromarray(data)  # 将之前的矩阵转换为图片

    dddata=data               #用于可视化以调试
    #image.show()            #调用本地软件显示图片，win10是叫照片的工具

    #5节点间长度计算
    knot_cor_id=dict()           #节点 坐标——序号
    l=len(knotnew)
    for i in range(l):
        knot_cor_id[cor2str(knotnew[i][0],knotnew[i][1])]=i

    cor_color=dict()             #坐标——颜色(白色：0，红色：1，开始搜寻点：2)
    for i in white_cor:#白色
        cor_color[cor2str(i[0],i[1])]=0
    for i in knotnew:#红色
        cor_color[cor2str(i[0],i[1])]=1

    print(4)
    distMat=[[len(data)*len(data[0]) for i in range(l)] for i in range(l)]
    for i in range(l):
        distMat[i][i]=0
    knotRoad=dict()
    allEdge=distanceAdd(data,knotnew,knot_cor_id,distMat,knotRoad,cor_color)
    print(len(distMat),len(distMat[0]))
    image = Image.fromarray(dddata)  # 将之前的矩阵转换为图片
    image.show()            #调用本地软件显示图片，win10是叫照片的工具

    file1='E:\\Jerry\\My University\\大学\\课程\\第四学期\\创业实训\\算法\\最终\\第二阶段——图论算法\\distMat.txt'
    file2='E:\\Jerry\\My University\\大学\\课程\\第四学期\\创业实训\\算法\\最终\\第二阶段——图论算法\\knotRoad.txt'
    file3='E:\\Jerry\\My University\\大学\\课程\\第四学期\\创业实训\\算法\\最终\\第二阶段——图论算法\\knot_cor_id.txt'
    file4 = 'E:\\Jerry\\My University\\大学\\课程\\第四学期\\创业实训\\算法\\最终\\第二阶段——图论算法\\allEdge.txt'
    writedata(file1, file2, file3,file4, distMat, knotRoad, knot_cor_id,allEdge)

    file5='E:\\Jerry\\My University\\大学\\课程\\第四学期\\创业实训\\算法\\最终\\第三阶段——用户控制\\distMat.txt'
    file6='E:\\Jerry\\My University\\大学\\课程\\第四学期\\创业实训\\算法\\最终\\第三阶段——用户控制\\knotRoad.txt'
    file7='E:\\Jerry\\My University\\大学\\课程\\第四学期\\创业实训\\算法\\最终\\第三阶段——用户控制\\knot_cor_id.txt'
    file8 = 'E:\\Jerry\\My University\\大学\\课程\\第四学期\\创业实训\\算法\\最终\\第三阶段——用户控制\\allEdge.txt'
    writedata(file5, file6, file7,file8, distMat, knotRoad, knot_cor_id,allEdge)
    t5 = time()

    '''
    for i in road:
        print(i)
        x=[j[0] for j in i]
        y=[j[1] for j in i]
        plt.scatter(x,y)
        plt.show()'''
    # 图形导出
    #cv2.imwrite('2.jpg',data)
    #data2 = readData('2.jpg')

    print(t2-t1,t3-t2,t4-t3,t5-t4)

