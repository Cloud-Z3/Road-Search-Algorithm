import cv2
from skimage import morphology
import numpy as np

img = cv2.imread('rawmapn.png', 0)   # 读取图片
_,binary = cv2.threshold(img, 250, 255, cv2.THRESH_BINARY)  # 二值化处理
cv2.imwrite("binary.png", binary)   # 保存二值化图片
binary[binary==255] = 1
skeleton0 = morphology.skeletonize(binary)   # 骨架提取
num = 0
x,y=skeleton0.shape
skeleton=np.zeros([x,y,3],np.int)

for i in range(len(skeleton0)):
    for j in range(len(skeleton0[i])):
        ele=skeleton0[i][j]
        for k in range(3):
            skeleton[i][j][k]=ele*255
print(skeleton)
#skeleton = skeleton0.astype(np.uint8)*255
cv2.imwrite("skeleton.png", skeleton)        # 保存骨架提取后的图片
