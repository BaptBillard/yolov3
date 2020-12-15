# -*- coding: utf-8 -*-
from pathlib import Path, PosixPath
import os
import random

if __name__ == '__main__':

    img_size = (1242, 375)  # width, height: à vérifier

    images_folder = 'training/images/'
    output_train_folder = "kitti/images/train/"
    output_val_folder = "kitti/images/val/"
    images_pathes = [str(PosixPath(path)) for path in Path(images_folder).rglob("*_Cl.png")]

    # put 1/5 in val
    random.shuffle(images_pathes)
    images_pathes_val = []
    for i in range(0,int(len(images_pathes)/5)):
        images_pathes_val.append(images_pathes.pop())
        tmp_path = output_val_folder + images_pathes_val[i][-13:]
        tmp_path = tmp_path.rsplit("_", 1)[0] + ".png"
        os.rename(images_pathes_val[i], tmp_path)


    # put the 4/5 remaining in train
    for image_path in images_pathes:
        tmp_path = output_train_folder + image_path[-13:]
        tmp_path = tmp_path.rsplit("_", 1)[0] + ".png"
        os.rename(image_path, tmp_path)

