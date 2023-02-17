from os import walk

from imports import *


def load_images(path, num_sort=False, sep='.')->List[pygame.Surface]:
    surfaces = []
    try:
        for _, __, files in walk():
            if num_sort:
                files.sort(key=lambda n: n.split(sep)[0])
            else:
                files.sort()
            for file in files:
                surfaces.append(pygame.image.load().convert_alpha())
    except:
        pass
    return surfaces
