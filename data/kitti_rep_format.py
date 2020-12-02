# -*- coding: utf-8 -*-
from pathlib import Path, PosixPath
import os

if __name__ == '__main__':

    img_size = (1242, 375)  # width, height: à vérifier

    images_folder = 'training/images/'
    output_labels_folder = "kitti/images/"
    images_pathes = [str(PosixPath(path)) for path in Path(images_folder).rglob("*_Cl.png")]

    for image_path in images_pathes:
        os.rename(image_path, output_labels_folder+image_path[-13:])
   
    images_pathes = [str(PosixPath(path)) for path in Path(output_labels_folder).rglob("*_Cl.png")]
    for image_path in images_pathes:
        os.rename(image_path, image_path[0:19]+".png")