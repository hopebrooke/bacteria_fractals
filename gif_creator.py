import imageio.v2 as imageio
from natsort import natsorted 
import os

FOLDER = 'DATA_20250423-172441'
images = []
images_path = f'figures/{FOLDER}/'

if not os.path.exists(f"gifs/"):
        os.makedirs(f"gifs/")

with imageio.get_writer(f'gifs/{FOLDER}.gif', mode='I') as writer:
    for image in natsorted(os.listdir(images_path)):
        img = imageio.imread(images_path+image)
        writer.append_data(img)