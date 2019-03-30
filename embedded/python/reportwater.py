#!/bin/python3
import json
import requests
import os
import logging
import sys
import time
import readwater
import gps


def register_meter():
    if not os.path.exists("data"):
        os.mkdir("data")
    elif not os.path.isdir("data"):
        os.remove("data")
        os.mkdir("data")
    data = json.dumps(gps.get_coordinates())

    response = requests.post("http://lahacks.appspot.com/api/register", data=data)
    uuid = ""
    if response.status_code == 200:
        result = response.json()
        print(result)
        if result["success"]:
            logging.info("Successfully registered with central server")
            uuid = result["uuid"]
        else:
            logging.warning("Unable to register meter: "+result["error"])
            return None
    else:
        logging.error("Unable to get good response from server, status code {}".format(response.status_code))
        return None
    
    dict = {"uuid":uuid}
    with open("data/einfo.json", "w") as f:
        json.dump(dict, f)
    return uuid


def post_update():
    # Setup logging
    logging.basicConfig(format='[%(levelname)s] %(asctime)s : %(message)s', filename="embedded.log", level=logging.INFO)

    if not os.path.exists("data/einfo.json"):
        uuid = register_meter()
        if uuid is None:
            return
    else:
        with open("data/einfo.json") as f:
            data = json.load(f)
            uuid = data["uuid"]
    water = readwater.get_water_reading()
    update_data = {"uuid":uuid, "water":water}
    requests.post("http://lahacks.appspot.com/api/updatewater", data=update_data)    
    

def main():
    interval = int(sys.argv[1])
    while True:
        post_update()
        time.sleep(interval)

if __name__ == "__main__":
    main()