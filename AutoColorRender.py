import cv2
import numpy as np
from skimage import color
import matplotlib.image as mpimg
import colorsys


img1 = mpimg.imread('1.jpg')   #输入底色图的文件名
img2 = mpimg.imread('2.jpg')   #输入黑白素描图的文件名

sp1 = img1.shape                            #此乃shape
high1 = sp1[0] ; wide1 = sp1[1]
sp2 = img2.shape
high2 = sp2[0] ; wide2 = sp2[1]

if(high1 == high2 and wide1 == wide2):
    print("size check ok", sp1)

    img1_hsv = color.rgb2hsv(img1)          #此乃hsv
    arr_img1_hsv = np.array(img1_hsv)
    h1, s1, v1 = np.dsplit(arr_img1_hsv, 3)
    s1 = (s1 * 100) #.astype(np.uint8)
    v1 = (v1 * 100) #.astype(np.uint8)
    #print(s1, v1)


    def rgb2gray(rgb):                      #此乃神圣完美灰度
        return np.dot(rgb[..., :3], [0.2989, 0.5870, 0.1140])
    g1 = ((rgb2gray(img1) * 100) // 255)#.astype(np.uint8)
    g2 = ((rgb2gray(img2) * 100) // 255)#.astype(np.uint8)
    #print(g1,g2)


    v1=np.reshape(v1,(high1,wide1))
    e = g2 - g1
    v3 = v1 + e
    #print(e, v2)
    h1 = np.reshape(h1, (high1, wide1))
    #h1 = ((h1*100).astype(np.uint8))/100
    v3 = v3 / 100




    def hsv2rgb(h, s, v):
        return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h,s,v))

    s3 = np.zeros(shape=(high1, wide1))

    i = 0;j = 0;k = 0

    while j < wide1:
        i = 0
        while i < high1:
            k = 0
            h1v = h1[i, j]
            v3v = v3[i, j]
            g2v = g2[i, j]
            while k < 1:
                rgb3 = hsv2rgb(h1v, k, v3v)
                g3 = ((0.2989 * rgb3[0] + 0.587 * rgb3[1] + 0.114 * rgb3[2]) * 100) // 255
                if g3 == g2v:
                    s3[i, j] = k
                    break
                k += 0.01
                if g3 >= g2[i,j]:
                    s3[i, j] = 1
            i += 1
        j += 1

    #print(s3)
    img3_hsv = np.dstack([h1,s3,v3])
    img3 = (color.hsv2rgb(img3_hsv))#*255)/1)#.astype(np.uint8)

    r1, g1, b1 = np.dsplit(img3, 3)
    img3mk2 = np.dstack([b1, g1, r1])
    cv2.imwrite('3.jpg', (img3mk2*255).clip(0, 255).astype(np.uint8))   #设置输出图片的文件名






else:
    print("not same size pic")