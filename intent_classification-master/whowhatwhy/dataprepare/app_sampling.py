# -*- coding: utf-8 -*-
#
# Usage:
# python -m classifier.dataset.app_sampling

import json
import random
import urllib
import os
from socket import error as SocketError
import errno

def bin_apps_by_rating_count():
    bins = [[0, 10], [10, 100], [100, 1000], [1000, 10000], [10000, 50000], [50000, 100000], [100000, 200000], [200000, 1000000], [1000000, 500000000]]
    bins_list = [[] for i in range(len(bins))]
    with open("data/googleplay/crawl_metas_nodownloadcount.txt") as f:
        lines = f.readlines()
        for line in lines:
            entry = json.loads(line)
            rating_count = 0 if entry["rating_count"] == None else float(entry["rating_count"])
            for idx, single_bin in enumerate(bins):
                if rating_count > single_bin[0] and rating_count < single_bin[1]:
                    bins_list[idx].append(entry)
    return bins_list



def sample_apps_from_bin(bins_list, numperbin = 10):
    sampled_bins_list = []
    for bins_apps in bins_list:
        numperbin = min(numperbin, len(bins_apps))
        sampled_bin = [bins_apps[i] for i in sorted(random.sample(xrange(len(bins_apps)), numperbin))]
        sampled_bins_list.append(sampled_bin)
    return sampled_bins_list


def download_apps(sampled_bins_list, download_dir):
    sampledapps = [entry["package"] for x in sampled_bins_list for entry in x]
    s3app_paths = []
    # static analysis
    with open("data/applist/all_apps.txt") as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            fields = line.split("/")
            app_name = fields[-1]
            packagename = app_name.replace(".apk", "")
            if packagename in sampledapps:
                s3app_paths.append(line)

    template = "http://chimpsapks.s3-website-us-west-2.amazonaws.com/{}"

    testfile = urllib.URLopener()
    for s3app_path in s3app_paths:
        downloadpath = template.format(s3app_path)
        print ("downloading: ", downloadpath)
        filename = downloadpath.split("/")[-1]
        if os.path.exists("{}{}".format(download_dir, filename)):
            print ("skip downloading")
            continue
        try:
            testfile.retrieve(downloadpath, "{}{}".format(download_dir, filename))
        except SocketError as e:
            if e.errno != errno.ECONNRESET:
                raise
            pass



if __name__ == '__main__':
    # download_dir = "/media/haojian/Data/appdownload/"
    download_dir = "/media/haojian/TOSHIBA EXT/apkdownload/feb24/"
    logfile_path = "{}sampled_bins_list.json".format(download_dir)

    if not os.path.exists(download_dir):
        os.mkdir(download_dir)

    if os.path.exists(logfile_path):
        print("load existing log file")
        with open(logfile_path, "r") as f:
            sampled_bins_list = json.load(f)
    else:
        bins_list = bin_apps_by_rating_count()
        sampled_bins_list = sample_apps_from_bin(bins_list, 1000)
        with open(logfile_path, "w") as f:
            json.dump(sampled_bins_list, f)
    download_apps(sampled_bins_list, download_dir)

