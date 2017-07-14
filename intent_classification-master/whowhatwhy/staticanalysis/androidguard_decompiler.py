import logging
import json
import os
import time

from androguard.misc import save_session, load_session, AnalyzeDex, AnalyzeAPK
from androguard.session import Session
from androguard.core.analysis.analysis import *
from androguard.core.bytecodes.dvm import DalvikVMFormat
from androguard.core.bytecodes.apk import APK



# ##### Increase the stack depth
# import resource
import sys
#
# print resource.getrlimit(resource.RLIMIT_STACK)
print(sys.getrecursionlimit())
#
# # Will segfault without this line.
# # resource.setrlimit(resource.RLIMIT_STACK, [0x10000000, resource.RLIM_INFINITY])
sys.setrecursionlimit(0x10000)
#
# print resource.getrlimit(resource.RLIMIT_STACK)
print(sys.getrecursionlimit())
# ##### End


def writeStringsToFile(folderpath, appName, d):
    stringsfile = folderpath + '/' + appName + '_strings.txt'
    strings = d.get_strings()
    string_buff = ' '.join(strings)
    with open(stringsfile, 'w') as target:
        target.write(string_buff)


def writeClassesToFile(class_arr, folderpath, ds):
    for c in class_arr:
        if not c:
            continue
        cname = c.replace('/', '.')
        classpath = folderpath + '/' + cname[:-1] + '.txt'
        with open(classpath, 'w') as target:
            code_str = ds.get_class(c).get_source()
            target.write(code_str)


def writeDexToFile(ds, packagename, outputpath):
    if type(ds) is list:
        for d in ds:
            class_arr = d.get_classes_names()
            writeClassesToFile(class_arr, outputpath, d)
            writeStringsToFile(outputpath, packagename, d)
    else:
        class_arr = ds.get_classes_names()
        writeClassesToFile(class_arr, outputpath, ds)
        writeStringsToFile(outputpath, packagename, ds)


class androidguard_decompiler(object):
    """
    analysis result of androguard
    """

    def __init__(self, app_path):
        """
        :param app_path: local file path of app, should not be None
        analyse app specified by app_path
        """
        self.app_path = app_path
        try:
            self.a = APK(self.app_path)
        except:
            raise
        self.ds = None
        self.dx = None


    def get_detailed_analysis(self):
        self.a, self.ds, self.dx = AnalyzeAPK(self.app_path)
        print("decompiler done.")

    #
    # def get_fast_analysis(self):
    #     self.ds = DalvikVMFormat( self.a.get_dex() )

    def save_session(self, outputpath):
        save_session([self.a, self.ds, self.dx], "{}/session.json".format(outputpath))


    def process_and_savesession_multiplefolder(self, outputdirs):
        print("filename: ", os.path.basename(self.app_path))
        filename = os.path.basename(self.app_path)
        filename = filename.replace(".apk", "")
        for outputdir in outputdirs:
            outputpath = "{}{}".format(outputdir, filename)
            if os.path.exists(outputpath):
                print("skip based on filename: {}.".format(filename))
                return
        self.process_and_savesession(outputdirs[-1])


    def process_and_savesession(self, outputdir):
        packagename = self.a.get_package()
        outputpath = "{}{}".format(outputdir, packagename)
        if os.path.exists(outputpath):
            print("skip based on package name: {}.".format(packagename))
            return
        os.mkdir(outputpath)
        try:
            if self.ds == None:
                self.get_detailed_analysis()
            self.save_session(outputpath)
            # writeDexToFile(self.ds, packagename, outputpath)
        except Exception as e:
            print (e)
            os.rmdir(outputpath)



    def output_sorce(self, outputdir):
        packagename = self.a.get_package()
        outputpath = "{}{}".format(outputdir, packagename)
        if os.path.exists(outputpath):
            print("skip {}.".format(packagename))
            return
        os.mkdir(outputpath)
        try:
            if self.ds == None:
                self.get_detailed_analysis()
            writeDexToFile(self.ds, packagename, outputpath)
        except Exception as e:
            print(e)
            os.rmdir(outputpath)



if __name__ == '__main__':
    filepath = "data/apks/archery.apk"
    save_dir = "output/"
    decompiler = androidguard_decompiler(filepath)
    decompiler.process_and_savesession(save_dir)

