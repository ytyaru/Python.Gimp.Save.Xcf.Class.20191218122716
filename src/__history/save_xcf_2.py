#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gimpfu import *

class XcfSaver(object):
    def __init__(self):
        self.img = None
        self.layer = None
        self.surface = None
    def __create_image(self):
        self.img = gimp.Image(512, 512, RGB)
        self.layer = gimp.Layer(self.img, "layer01", 512, 512, RGBA_IMAGE, 100, NORMAL_MODE)
        self.layer.fill(TRANSPARENT_FILL)
        self.img.add_layer(self.layer, 0) 
        #gimp.Display(img)
    def __draw_rectangle(self):
        import cairo
        self.surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 512, 512)
        ctx = cairo.Context(self.surface)
        ctx.set_source_rgb(1.0, 0.0, 0.0)
        ctx.rectangle(128, 128, 256, 256)
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
        rgn = self.layer.get_pixel_rgn(0, 0, 512, 512, True, True)
        rgn[0:512, 0:512] = str(dst)
        self.layer.flush()
        self.layer.merge_shadow()
        self.layer.update(0, 0, 512, 512)
    def __save_xcf(self):
        import os,sys
        dir_path = "/tmp/work/"
        try:
            os.makedirs(dir_path)
        except: pass
            #import traceback
            #traceback.print_exc()
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        save_path = os.path.join(dir_path, timestamp + ".xcf")
        pdb.gimp_xcf_save(0,self.img,self.layer,save_path,save_path)
        gimp.message("Python " + sys.version)
        gimp.message("ファイル保存しました。: " + save_path)
    def __quic_gimp(self):
        #pdb.gimp_displays_flush()
        pdb.gimp_quit(1)
    def run(self):
        self.__create_image()
        self.__draw_rectangle()
        self.__to_argb()
        self.__save_xcf()
        self.__quic_gimp()


c = XcfSaver()
c.run()
