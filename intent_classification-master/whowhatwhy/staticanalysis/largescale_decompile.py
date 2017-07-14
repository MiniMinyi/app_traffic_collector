# -*- coding: utf-8 -*-
#
# Usage:
# python2.7 preferred
# python -m classifier.staticanalysis.batchdecompile


from os import listdir
from os.path import isfile, join
from staticanalysis.androidguard_decompiler import androidguard_decompiler

import sys
import logging
import logging.config
import json
import os
from multiprocessing.dummy import Pool as ThreadPool

from androguard.misc import save_session, load_session
from androguard.session import Session
from androguard.core.analysis.analysis import *
from glob import glob
from itertools import chain


def singledecompile(apk_file):
    print(apk_file)
    try:
        decompiler = androidguard_decompiler(apk_file)
        # decompiler.process_and_savesession(save_dir)
        decompiler.process_and_savesession_multiplefolder(save_dirs)
    except Exception as e:
        print (e)
    # print save_dir
    return save_dir


# function to be mapped over
def decompileParallel(apk_files, threads=5):
    pool = ThreadPool(threads)
    results = pool.map(singledecompile, apk_files)
    pool.close()
    pool.join()
    return results


if __name__ == '__main__':
    apks_dir = "/media/chimps/TOSHIBA EXT/apkdownload/apr14/"
    save_dir = "/media/chimps/data_4tb1/decompiled/apr14/"
    save_dirs = [save_dir]
    results = [y for x in os.walk(apks_dir) for y in glob(os.path.join(x[0], '*.apk'))]
    print(len(results))
    decompileParallel(results, threads=2)
    # result = (chain.from_iterable(glob(os.path.join(x[0], '*.apk')) for x in os.walk(apks_dir)))
    # counter = 0
    # for apkpath in result:
    #     print apkpath
    #     counter += 1
    # print counter


    # for apkpath in result:
    #     print apkpath
    # apk_file_list = [ join(apks_dir, f) for f in listdir(apks_dir) if isfile(join(apks_dir, f)) and f.endswith(".apk") ]
    # for apk_file in apk_file_list:
    #     print apk_file
        # try:
        #     decompiler = androidguard_decompiler(apk_file)
        #     decompiler.process_and_savesession(save_dir)
        # except Exception as e:
        #     print e