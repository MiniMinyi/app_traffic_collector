# -*- coding: utf-8 -*-

import pymongo

permission_list = {
    "CALENDAR": ["READ_CALENDAR", "WRITE_CALENDAR"],
    "CAMERA": ["CAMERA"],
    "CONTACTS": ["READ_CONTACTS", "WRITE_CONTACTS"],
    "LOCATION": ["CONTROL_LOCATION_UPDATES", "ACCESS_FINE_LOCATION", "ACCESS_COARSE_LOCATION", "ACCESS_MOCK_LOCATION", "INSTALL_LOCATION_PROVIDER"],
    "MICROPHONE": ["RECORD_AUDIO", "MODIFY_AUDIO_SETTINGS"],
    "SENSORS": ["BLUETOOTH"],  # need to update
    "SMS": ["RECEIVE_SMS", "SEND_SMS", "WRITE_SMS", "READ_SMS"],
    "STORAGE": ["WRITE_EXTERNAL_STORAGE", ""],
    "NETWORK": ["ACCESS_NETWORK_STATE", "CHANGE_NETWORK_STATE", "CHANGE_WIFI_MULTICAST_STATE", "CHANGE_WIFI_STATE", "ACCESS_WIFI_STATE"]
}

conn = pymongo.MongoClient('mongodb://auditor:iamauditor042@localhost:27017/')
db = conn.staticAnalysis
col = db.Test_permissionlist


for perm_cate, perm_list in permission_list.items():
    with open("{}.csv".format(perm_cate), "w") as f:
        for perm in perm_list:
            print (perm)
            counter = 0
            for doc in col.find({"permission" : perm}):
                try:
                    f.write("{}\t{}\t{}\t{}\n".format(doc['packagename'], perm, doc['src'], doc['is_external']))
                    print(doc['packagename'], perm, doc['src'], doc['is_external'])
                    counter += 1
                    if counter > 1000:
                        break
                except:
                    print("error")
                    continue
