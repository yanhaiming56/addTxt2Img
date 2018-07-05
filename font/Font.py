import os

import numpy as np
import pygame as pg
from pygame import freetype


class Font:
    def __init__(self, font_dir):
        self.size = 20
        self.rotation = -90
        self.color = (255, 255, 255)
        self.fontfiles = self.__load_fonts(font_dir)

    def init_font(self):
        font_num = len(self.fontfiles)
        font_code = np.random.randint(0, font_num)
        self.font = freetype.Font(self.fontfiles[font_code], self.size)

    def __load_fonts(self, font_dir):
        fonts = []
        if os.path.exists(font_dir) == False:
            print("\033[1;31;40m%s doesn't exist!\033[0m" % (font_dir))
        for fontfile in os.listdir(font_dir):
            fontpath = os.path.join(font_dir, fontfile)
            if os.path.isfile(fontpath):
                fonts.append(fontpath)
        return fonts
