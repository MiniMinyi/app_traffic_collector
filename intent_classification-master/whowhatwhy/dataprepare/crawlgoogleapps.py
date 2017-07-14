from boto.s3.connection import S3Connection
# from urllib.error import URLError, HTTPError
# from urllib.request import urlopen
# import httplib
from bs4 import BeautifulSoup
from urllib.request import urlopen
from collections import defaultdict
import json
from multiprocessing.dummy import Pool as ThreadPool


AWS_ACCESS_KEY = 'AKIAIVW3YVQ63GTBVSBA'
AWS_ACCESS_SECRET_KEY = 'v7hQUOXxMPhC0ihPJe62aTMiQZuax6LkhghfaXDq'


def download_file_list():
    conn = S3Connection(AWS_ACCESS_KEY, AWS_ACCESS_SECRET_KEY)
    bucket = conn.get_bucket('chimpsapks')
    for key in bucket.list():
        print(key.name.encode('utf-8'))


def get_package_names():
    res = []
    with open("all_apps.txt") as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            fields = line.split("/")
            app_name = fields[-1]
            # print app_name.replace(".apk", "")
            res.append( app_name.replace(".apk", "") )
    return res



def parse_googleplay_page(googleplay_url, params = None):
    try:
        soup = BeautifulSoup(urlopen(googleplay_url).read(), "html.parser")
    except Exception as e:
        return None, None, None, None

    div_contents = soup.find_all('div', class_="show-more-content text-body")
    desc = ""
    for div_content in div_contents:
        desc += div_content.get_text(separator="\t")
    try:
        rating_count = soup.find(itemprop="ratingCount").get("content")
        div_rating = soup.find_all('div', class_="score")
        rating = div_rating[0].get_text()
        category = soup.find(itemprop="genre").get_text()
    except Exception as e:
        print (e)
        category = ""
        rating_count = 0
        rating = 0
    # print soup.find(itemprop="genre")
    # print rating_count, rating, category
    # print download_count[0].get_text()
    return rating_count, rating, category, desc


def crawl_app_stats(app_packages):
    print(len(app_packages))
    done_list = []
    with open("crawl_metas.txt", "r") as f:
        lines = f.readlines()
        for line in lines:
            jsonobj = json.loads(line)
            done_list.append(jsonobj["package"])
    print(done_list)
    with open("crawl_metas.txt", "a") as f:
        for app_package in app_packages:
            print(app_package)
            if app_package in done_list:
                print("Skip", app_package)
                continue
            testurl = "https://play.google.com/store/apps/details?id={}".format(app_package)
            res = parse_googleplay_page(testurl)
            metainfos = {}
            rating_count, rating, category, desc = res
            metainfos["package"] = app_package
            metainfos["rating_count"] = rating_count
            metainfos["rating"] = rating
            metainfos["category"] = category
            metainfos["desc"] = desc
            f.write(json.dumps(metainfos) + "\n")
            f.flush()


def crawl_app_by_package(app_package):
    print(app_package)
    testurl = "https://play.google.com/store/apps/details?id={}".format(app_package)
    res = parse_googleplay_page(testurl)
    metainfos = {}
    rating_count, rating, category, desc = res
    metainfos["package"] = app_package
    metainfos["rating_count"] = rating_count
    metainfos["rating"] = rating
    metainfos["category"] = category
    metainfos["desc"] = desc
    # metainfos[]
    return metainfos


def crawl_app_stats_multithread(app_packages):
    # Make the Pool of workers
    pool = ThreadPool(4)
    # Open the urls in their own threads
    # and return the results
    results = pool.map(crawl_app_by_package, app_packages)
    #close the pool and wait for the work to finish
    pool.close()
    pool.join()


if __name__ == '__main__':
    # download_file_list()
    app_names = get_package_names()
    print(len(app_names))
    crawl_app_stats(app_names) # seems google has a bot check. the multithread version is not faster.

    # crawl_app_stats(app_names)
    # crawl_app_stats(app_names[:100])
    # no performance difference on the same machine.
    # crawl_app_stats_multithread(app_names[:100])


    # testurl = "https://play.google.com/store/apps/details?id=flipboard.boxer.app"
    # print (parse_googleplay_page(testurl))
    # testurl1 = "https://play.google.com/store/apps/details?id=com.sec.android.Kies"
    # print (parse_googleplay_page(testurl1))

