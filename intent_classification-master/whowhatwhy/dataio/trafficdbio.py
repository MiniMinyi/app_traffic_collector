import requests
import os
import sys


import pymysql

url = "privacyproxy.io"
port = 3306

conn = pymysql.connect(host=url, port=port, user='haojian', passwd='cmuchimps', db='netflow')

cur = conn.cursor()
cur.execute("SELECT * FROM netflow_data")

print(cur.description)
print()

for row in cur:
    print(row)

cur.close()
conn.close()