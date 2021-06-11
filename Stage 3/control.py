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
t2=time()
import tkinter as tk
import tkinter.messagebox

root = tk.Tk()
root.title('用户选择界面')
w = root.winfo_screenwidth()
h = root.winfo_screenheight()
root.geometry("%dx%d" % (w, h))

# 创建上下两个框架
frame1 = tk.Frame(root)
frame2 = tk.Frame(root)

# 创建两个文字类
var = tk.StringVar()
var.set("请在右侧地图上单击\n来选择你的起点")  # 设置文字
print("以下是起点：")

# 创建一个标签类, [frame]所属框架, [justify]:对齐方式
textLabel = tk.Label(frame1, textvariable=var, justify='center', font=("宋体", 40))
textLabel.pack(side='left')  # side：方位

# 创建一个Canvas来容纳地图
cv = tk.Canvas(root, bg='white', height=1000, width=1013)
filename = tk.PhotoImage(file="rawmapn1.png")
cv.create_image(506.5, 500, anchor='center', image=filename)  # anchor:锚点位置
cv.pack(side='right')

# 获取鼠标点击位置
x = 0
y = 0

def callback1(event):
    print(event.x, event.y)
    global x, y
    x = event.x
    y = event.y
    tk.messagebox.askokcancel(title='提示', message='地点已选定')  # 弹出对话框


cv.bind("<Button-1>", callback1)  # 1：表示左键 2：中间键的滚轮点击 3：右键

# 按钮触发的函数
count = 0
listx = []  # 最后结果
listy = []

def callback2():
    global count, listx, listy
    listx.append(x)
    listy.append(y)
    var.set("请在右侧地图上单击\n来选择你的终点")
    count += 1
    if (count == 2):
        root.destroy()
        return
    print("以下是终点：")

# 创建一个按钮, command：触发方法
theButton = tk.Button(frame2, text="确定", font=("宋体", 40), command=callback2)
theButton.pack()

# 调整框架的位置
frame1.pack(side='top', ipadx=10, ipady=200)
frame2.pack(side='bottom', ipadx=10, ipady=75)

root.wm_state('zoomed')  # 默认全屏
tk.mainloop()
t3=time()
print('起点：')
print(int(listy[0]*1990/1000),int(listx[0]*2015/1013))
print('终点：')
print(int(listy[1]*1990/1000),int(listx[1]*2015/1013))
pa=nearPointFind(int(listy[0]*1990/1000),int(listx[0]*2015/1013),knot_cor_id)
pb=nearPointFind(int(listy[1]*1990/1000),int(listx[1]*2015/1013),knot_cor_id)

a=knot_cor_id[cor2str(pa[0],pa[1])]
print(a)
b=knot_cor_id[cor2str(pb[0],pb[1])]
print(b)
mode = 2  # 此处选择模式
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


print(t4 - t3+t2-t1)
