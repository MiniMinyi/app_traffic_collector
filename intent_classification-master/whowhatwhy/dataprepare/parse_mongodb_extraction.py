import json

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

for perm_cate, perm_list in permission_list.items():
    with open("{}.csv".format(perm_cate), "r") as f1, open("{}_cleaned.csv".format(perm_cate), "w") as f2:
        lines = f1.readlines()
        app_cache = {}
        for line in lines:
            fields = line.split("\t")
            print (fields[0])
            packagename = fields[0]
            googleplay_url = "https://play.google.com/store/apps/details?id={}&hl=en".format(packagename)
            pg_url = "http://privacygrade.org/apps/{}.html".format(packagename)
            if fields[0] in app_cache:
                app_cache[fields[0]] = app_cache[fields[0]] + 1
                continue
            else: 
                app_cache[fields[0]] = 1
            f2.write("{}\t{}\t{}\n".format(packagename, googleplay_url, pg_url))
            # print ("https://play.google.com/store/apps/details?id={}&hl=en".format(fields[0]))
    # break
