import os

import numpy as np
import pygame as pg
import pygame.locals
from pygame import freetype
from PIL import Image
from font.Font import Font
import cv2


class TxtImg:
    def __init__(self, txt_dir):
        self.txtfiles = self.__load_txt(txt_dir)

    def __load_txt(self, txt_dir):
        txts = []
        if os.path.exists(txt_dir) == False:
            print("\033[1;31;40m%s doesn't exist!\033[0m" % (txt_dir))
            return txts
        for txtfile in os.listdir(txt_dir):
            txtpath = os.path.join(txt_dir, txtfile)
            if os.path.isfile(txtpath):
                txts.append(txtpath)
        return txts

    def __getTxt(self, ch_count):
        if len(self.txtfiles) == 0:
            return ''
        txtfile_code = np.random.randint(0, len(self.txtfiles))
        with open(self.txtfiles[txtfile_code], 'r', encoding='utf-8', errors='ignore') as txtfile:
            txtlines = txtfile.readlines()
            txtline = ''
            while txtline == '':
                txtline_code = np.random.randint(0, len(txtlines))
                txtline = txtlines[txtline_code].strip()
            maxChCount = 0
            txt_code = 0
            if len(txtline) > ch_count:
                txt_code = np.random.randint(0, len(txtline) - ch_count + 1)
            text = txtline[txt_code:txt_code+ch_count]
        return text

    def __genTxtImg(self, font, ch_count, isVertical):
        surfarr,txt,bbox = [], '', []
        txt = self.__getTxt(ch_count)
        if txt == '':
            return surfarr,txt,bbox
        rect = font.font.get_rect(txt, rotation=font.rotation)
        surf = pg.Surface((rect.height, rect.width), pg.locals.SRCALPHA, 32)
        rect = surf.get_rect()
        bbox = font.font.render_to(surf, rect, txt)
        surfarr = pg.surfarray.pixels_alpha(surf)
        if isVertical == False:
            img = Image.fromarray(surfarr)
            img = img.rotate(font.rotation, expand=True).transpose(Image.FLIP_LEFT_RIGHT)
            surfarr = np.array(img)
        return surfarr, txt, bbox

    def genSynImg(self, srcimg, pos, font, ch_count, isVertical = False):
        txtimg, txt, bbox = self.__genTxtImg(font, ch_count, isVertical)
        if txt == '':
            print("\033[1;31;40m synthetic text image failed!\033[0m")
        txtimg = cv2.cvtColor(txtimg, cv2.COLOR_GRAY2BGR)
        txtimg = cv2.resize(txtimg,(pos[2],pos[3]))
        txtmask = np.zeros(txtimg.shape, txtimg.dtype)
        h, w = txtimg.shape[0:2]
        color = np.random.randint(0,255,3)
        for row in range(h):
            for col in range(w):
                if (txtimg[row,col] == np.array([255,255,255])).all():
                    txtimg[row,col] = color
        poly = np.array([[0, 0], [w, 0], [w, h], [0, h]])
        cv2.fillPoly(txtmask, [poly], (255, 255, 255))
        center = (int(pos[0]+pos[2]/2), int(pos[1]+pos[3]/2))
        synimg = cv2.seamlessClone(
            txtimg, srcimg, txtmask, center, cv2.MIXED_CLONE)
        return synimg, txt
