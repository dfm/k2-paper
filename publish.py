#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function
import os
import re
import shutil
from datetime import date
from itertools import imap
from subprocess import check_call

datestamp = date.today().strftime("%m%d")
TMPDIR = "fore" + datestamp
outfn = TMPDIR+".tar"
tex = open("ms.tex", "r").read()

try:
    os.makedirs(TMPDIR)
except os.error:
    pass


def rename(fn):
    a, b = os.path.split(fn)
    return os.path.split(a)[1] + "-" + b, fn


def find_figures(tex):
    return re.findall("includegraphics(?:.*?){(.*)}", tex)


for a, b in imap(rename, find_figures(tex)):
    shutil.copyfile(b, os.path.join(TMPDIR, a))
    tex = tex.replace(b, a)

shutil.copyfile("tab-cand.tex", os.path.join(TMPDIR, "tab-cand.tex"))
shutil.copyfile("ms.bbl", os.path.join(TMPDIR, "ms.bbl"))
open(os.path.join(TMPDIR, "ms.tex"), "w").write(tex)
check_call(" ".join(["cd", TMPDIR+";",
                     "tar", "-cf", os.path.join("..", outfn), "*"]),
           shell=True)
shutil.rmtree(TMPDIR)

print("Wrote file: '{0}'".format(outfn))
