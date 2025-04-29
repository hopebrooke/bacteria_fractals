import imageio.v2 as imageio
from natsort import natsorted
import os
import argparse

# cli
parser = argparse.ArgumentParser(description='Create a GIF from PNG frames in a folder.')
parser.add_argument('folder', help='Name of the folder inside figures/ to process')
args = parser.parse_args()

FOLDER = args.folder
images_path = f'figures/{FOLDER}/'

#create gifs/
os.makedirs("gifs/", exist_ok=True)

with imageio.get_writer(f'gifs/{FOLDER}.gif', mode='I') as writer:
    for image in natsorted(os.listdir(images_path)):
        if not image.endswith('.png') or not image.startswith('frame'):
            continue

        img = imageio.imread(images_path + image)
        writer.append_data(img)