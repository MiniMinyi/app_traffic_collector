# -*- coding: utf-8 -*-
#
# Usage:
# python2.7 preferred
# python -m classifier.staticanalysis.batchdecompile


from os import listdir
from os.path import isfile, join
from classifier.staticanalysis.androidguard_decompiler import androidguard_decompiler

import sys
import logging
import logging.config
import json
import os

from androguard.misc import save_session, load_session
from androguard.session import Session
from androguard.core.analysis.analysis import *



if __name__ == '__main__':
    apks_dir = "/media/haojian/Data/appdownload/"
    save_dir = "/media/haojian/Data/decompiled/"
    apk_file_list = [ join(apks_dir, f) for f in listdir(apks_dir) if isfile(join(apks_dir, f)) and f.endswith(".apk") ]
    for apk_file in apk_file_list:
        print(apk_file)
        try:
            decompiler = androidguard_decompiler(apk_file)
            decompiler.process_and_savesession(save_dir)
        except Exception as e:
            print(e)