import os

import cv2
import numpy as np
import pygame as pg
import pygame.locals
from PIL import Image
from pygame import freetype

from font.Font import Font
from syntxt.SynTxt import TxtImg

pg.init()

DATA_DIR = 'data'
FONT_DIR = 'font'
IMG_DIR = 'img'
TXT_DIR = 'txt'
LABEL_DIR = 'label'
TXT_IMG_DIR = 'txtimg'
TXT_LABEL_DIR = 'txtlable'

def main(imgpath,labelpath):
    txt_dir = os.path.join(DATA_DIR,TXT_DIR)
    font_dir = os.path.join(DATA_DIR,FONT_DIR)
    txtimg = TxtImg(txt_dir)

    if os.path.exists(imgpath) == False:
        print("\033[1;31;30m%s doesn't exist!\033m" % (imgpath))
        return
    if os.path.exists(labelpath) == False:
        print("\033[1;31;30m%s doesn't exist!\033m" % (labelpath))
        return
    
    for imgfile in os.listdir(imgpath):
        imgfilepath = os.path.join(imgpath,imgfile)
        if os.path.isfile(imgfilepath) == False:
            continue
        srcimg = cv2.imread(imgfilepath)
        pos = imgfile.find('.')
        imgname = imgfile[0:pos]
        labelfile = 'gt_' + imgname + '.txt'
        labelfilepath = os.path.join(labelpath,labelfile)
        if os.path.isfile(labelfilepath) == False:
            continue
        with open(labelfilepath,'r',encoding='utf-8', errors='ignore') as txtfile:
            txtlabledir = os.path.join(DATA_DIR,TXT_LABEL_DIR)
            if os.path.exists(txtlabledir) == False:
                os.mkdir(txtlabledir)
            txtlabelpath = os.path.join(txtlabledir,labelfile)
            txtlabelfile = open(txtlabelpath,'w',encoding='utf-8')
            for line in txtfile:
                linearr = line.strip().split(' ')
                linearr = np.array(linearr[0:4],np.int32)
                w = linearr[2] - linearr[0]
                h = linearr[3] - linearr[1]
                pos = np.array([linearr[0],linearr[1],w,h])
                font = Font(font_dir)
                font.size = float(h)
                font.init_font()
                ch_count = 0
                isVertical = False
                if int(w/h) > 0 :
                    ch_count = int(w/h)
                else:
                    ch_count = int(h/w)
                    isVertical = True
                srcimg,txt = txtimg.genSynImg(srcimg,pos,font,ch_count,isVertical)
                txtarr = ' '.join(str(i) for i in linearr)
                txtlabel = txtarr + ' "' + txt + '"'
                #print('{}:{}\r\n'.format(imgname,txt))
                txtlabelfile.write(txtlabel+'\n')
        newimgdir = os.path.join(DATA_DIR,TXT_IMG_DIR)
        if os.path.exists(newimgdir) == False:
            os.makedirs(newimgdir)
        newimgpath = os.path.join(newimgdir,imgfile)
        cv2.imwrite(newimgpath,srcimg)

if __name__ == "__main__":
    imgpath = os.path.join(DATA_DIR,IMG_DIR)
    labelpath = os.path.join(DATA_DIR,LABEL_DIR)
    main(imgpath,labelpath)