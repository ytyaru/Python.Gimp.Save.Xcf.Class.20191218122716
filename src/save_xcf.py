#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gimpfu import *
import os,sys

class Image(object):
    def __init__(self):
        self.image = None
        self.layer = None
    def __create_image(self, width=512, height=512, _type=RGB):
        self.image = gimp.Image(width, height, _type) # type=RGB,GRAY,INDEXED
    def __create_layer(self, name="layer01", width=512, height=512, _type=RGBA_IMAGE, opacity=100, mode=NORMAL_MODE):
        self.layer = gimp.Layer(self.image, name, width, height, _type, 100, mode)
        self.layer.fill(TRANSPARENT_FILL)
    def __add_layer(self):
        self.image.add_layer(self.layer, 0)
    def create(self, width=512, height=512):
        self.__create_image(width=width, height=height)
        self.__create_layer(width=width, height=height)
        self.__add_layer()

class Drawer(object):
    def __init__(self, layer):
        self.layer = layer
    def draw(self):
        self.__draw_rectangle()       
        self.__to_argb()
    def __draw_rectangle(self, r=1.0, g=0.0, b=0.0, x=128, y=128, w=256, h=256):
        import cairo
        self.surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, self.layer.width, self.layer.height)
        ctx = cairo.Context(self.surface)
        ctx.set_source_rgb(r, g, b)
        ctx.rectangle(x, y, w, h)
        ctx.fill()
    def __get_rgba_str(self, src):
        import struct
        rgba_buf = ""
        l = len(src)
        for i in range(l / 4):
            i0 = i * 4
            i1 = i0 + 4
            bgra = struct.unpack('@L', src[i0 : i1])[0]
            a = (bgra >> 24) & 0x0ff
            r = (bgra >> 16) & 0x0ff
            g = (bgra >> 8) & 0x0ff
            b = bgra & 0x0ff
            rgba = struct.pack('4B', r, g, b, a)
            rgba_buf += rgba
        return rgba_buf
    def __to_argb(self):
        src = self.surface.get_data()
        dst = self.__get_rgba_str(src)
        w = self.layer.width
        h = self.layer.height
        rgn = self.layer.get_pixel_rgn(0, 0, w, h, True, True)
        rgn[0:w, 0:h] = str(dst)
        self.layer.flush()
        self.layer.merge_shadow()
        self.layer.update(0, 0, w, h)

class Xcf(object):
    def __init__(self): pass
    def save(self, image, path=""):
        save_path = self.__path()
        pdb.gimp_xcf_save(0,image,image.layers[0],save_path,save_path)
        gimp.message("Python " + sys.version)
        gimp.message("ファイル保存しました。: " + save_path)
    def __path(self, path=""):
        dir_path = path
        if "" == dir_path: dir_path = "/tmp/work/"
        try:
            os.makedirs(dir_path)
        except: pass
            #import traceback
            #traceback.print_exc()
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        save_path = os.path.join(dir_path, timestamp + ".xcf")
        return save_path 


i = Image()
i.create()
d = Drawer(i.layer)
d.draw()
x = Xcf()
x.save(i.image)
pdb.gimp_quit(1)

