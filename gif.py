import argparse
import os
import imageio

argparser = argparse.ArgumentParser(description="Create GIF from folder of JPGs")
argparser.add_argument('-i', action="store", dest="input", help="Path to folder containing images")
argparser.add_argument('-o', action="store", dest="output", help="Path to save GIF", default="./anim.gif")
argparser.add_argument('-f', action="store", dest="fps", help="GIF FPS", default="8")
args = argparser.parse_args()

print("Creating GIF \"{0}\" from \"{1}\"".format(args.output, args.input))

# Remove existing GIF file
if os.path.exists(args.output):
    os.remove(args.output)

# List files in download directory
for root, dirs, files in os.walk(args.input, topdown=False):
    files = [fi for fi in files if fi.endswith(".jpg")]

# images = []
# for file in files:
    # images.append(imageio.imread(args.input + "/" + file))
# imageio.mimsave(args.output, images)

olFrames = False
# Only use first 500 frames if more than 500 found
if len(files) > 500:
    files = files[:500]
    olFrames = True

# Better streaming method for larger image sets
counter = 0
with imageio.get_writer(args.output, mode='I', fps=args.fps) as writer:
    for filename in files:
        image = imageio.imread(args.input + "/" + filename)
        writer.append_data(image)

        percentage = round((counter/len(files))*100)
        print("{0}%  ({1})".format(percentage, filename))
        counter += 1

if olFrames:
    print("\nWARNING: More than 500 frames found in \"{0}\" ({1} total).".format(args.input, len(files)))
    print("GIF only supports 500 frames maximum. Using first 500 images in \"{0}\"".format(args.input))

print("{0} frames processed\n".format(len(files)))
