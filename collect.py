import argparse
from datetime import datetime
import filecmp
import os
from PIL import Image, ImageFilter
from time import sleep
import requests

argparser = argparse.ArgumentParser(description="Endlessly collects images from NSW RMS traffic cameras.")
argparser.add_argument('-c', action="store", dest="camera", help="Traffic camera name")
argparser.add_argument('-p', action="store", dest="path", help="Path to save images", default="./download")
argparser.add_argument('--filter', action="store_true", dest="filtering", help="Enable image filtering", default=False)
args = argparser.parse_args()

url = "http://www.rms.nsw.gov.au/trafficreports/cameras/camera_images/{0}.jpg".format(args.camera, )
imageCount = 1
checkCount = 1
dupeCount = 0
oldLastMod = ""
oldFileName = ""

# Create download directory
if not os.path.exists(args.path):
    os.mkdir(args.path)

# Create filtered directory
if args.filtering and not os.path.exists(args.path + "/filtered"):
    os.mkdir(args.path + "/filtered")
    os.mkdir(args.path + "/filtered/detail")
    os.mkdir(args.path + "/filtered/sharpen")


def log(message):
    print("[{0}] {1}".format(str(datetime.now())[:-7], message))


while True:
    print("\n---------Checks: {0}---------Images: {1}---------Duplicates: {2}---------".format(checkCount, imageCount, dupeCount))
    log("Checking for image {0}...".format(imageCount))

    nowTime = datetime.now()

    currentFileName = "{0}-{1}.jpg".format(args.camera, datetime.timestamp(nowTime))
    currentFilePath = args.path + "/" + currentFileName

    try:
        r = requests.head(url)

        # Make sure server responded with HTTP 200
        if not r.status_code == 200:
            log("HTTP error while checking image {0} ({1})".format(imageCount, r.status_code))
        else:
            # Check if new image is available
            lastMod = r.headers['Last-modified']
            if lastMod == oldLastMod:
                log("No new image found")
            else:
                log("Downloading new image...")
                r = requests.get(url)
                open(currentFilePath, "wb").write(r.content)

                if filecmp.cmp(currentFilePath, args.path + "/" + oldFileName):
                    log("Deleting duplicate image")
                    os.remove(currentFilePath)
                    dupeCount += 1
                else:
                    log("Saved {0}".format(currentFileName))

                    # Filtering
                    if args.filtering:
                        img = Image.open(currentFilePath)

                        filteredFileName = "{0}-sharpen-{1}.jpg".format(args.camera, datetime.timestamp(nowTime))
                        filteredFilePath = args.path + "/filtered/sharpen/" + filteredFileName
                        filteredImg = img.filter(ImageFilter.SHARPEN)
                        filteredImg.save(filteredFilePath)

                        filteredFileName = "{0}-detail-{1}.jpg".format(args.camera, datetime.timestamp(nowTime))
                        filteredFilePath = args.path + "/filtered/detail/" + filteredFileName
                        filteredImg = img.filter(ImageFilter.DETAIL)
                        filteredImg.save(filteredFilePath)

                        log("Image filters applied")

                    imageCount += 1
                    oldFileName = currentFileName

    except requests.ConnectionError as e:
        log("Error downloading image {0} ({1})".format(imageCount, e.strerror))
        pass

    sleep(30)
    checkCount += 1
    oldLastMod = lastMod
