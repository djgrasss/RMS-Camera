import argparse
import os

argparser = argparse.ArgumentParser(description="Create MP4 from folder of JPGs")
argparser.add_argument('-i', action="store", dest="input", help="Path to folder containing images")
argparser.add_argument('-p', action="store", dest="prefix", help="Image prefix")
argparser.add_argument('-o', action="store", dest="output", help="Path to save MP4", default="./anim.mp4")
argparser.add_argument('-f', action="store", dest="fps", help="MP4 FPS", default="8")
args = argparser.parse_args()

print("Creating MP4 \"{0}\" from \"{1}\"".format(args.output, args.input))

# Remove existing MP4 file
if os.path.exists(args.output):
    os.remove(args.output)

# Run FFMPEG command
os.system("ffmpeg -pattern_type glob -y -r {0} -i \"{1}/{2}-*.jpg\" {3}".format(args.fps, args.input, args.prefix, args.output))
