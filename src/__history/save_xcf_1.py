#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from gimpfu import *
img = gimp.Image(512, 512, RGB)
layer = gimp.Layer(img, "layer01", 512, 512, RGBA_IMAGE, 100, NORMAL_MODE)
layer.fill(TRANSPARENT_FILL)
img.add_layer(layer, 0) 
#gimp.Display(img)

import cairo
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 512, 512)
ctx = cairo.Context(surface)
ctx.set_source_rgb(1.0, 0.0, 0.0)
ctx.rectangle(128, 128, 256, 256)
ctx.fill()

import struct
def get_rgba_str(bgra_buf):
    rgba_buf = ""
    l = len(bgra_buf)
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

src = surface.get_data()
dst = get_rgba_str(src)
rgn = layer.get_pixel_rgn(0, 0, 512, 512, True, True)
rgn[0:512, 0:512] = str(dst)
layer.flush()
layer.merge_shadow()
layer.update(0, 0, 512, 512)

import os,sys
dir_path = "/tmp/work/"
try:
    os.makedirs(dir_path)
except: pass
#    import traceback
#    traceback.print_exc()
from datetime import datetime
timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
save_path = os.path.join(dir_path, timestamp + ".xcf")
pdb.gimp_xcf_save(0,img,layer,save_path,save_path)
gimp.message("Python " + sys.version)
gimp.message("ファイル保存しました。: " + save_path)

#pdb.gimp_displays_flush()
pdb.gimp_quit(1)

