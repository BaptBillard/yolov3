# -*- coding: utf-8 -*-
from pathlib import Path, PosixPath
import os
import cv2

if __name__ == '__main__':

    img_size = (1242, 375)  # width, height: à vérifier

    images_folder = 'training/images/'
    output_train_folder = "second_kitti/images/train/"
    output_val_folder = "second_kitti/images/val/"
    images_pathes_dp = [str(PosixPath(path)) for path in Path(images_folder).rglob("*_Dp.png")]
    images_pathes_of = [str(PosixPath(path)) for path in Path(images_folder).rglob("*_Of.png")]
    images_pathes_vl = [str(PosixPath(path)) for path in Path(images_folder).rglob("*_Vl.png")]

    # put 1/5 in val (no shuffle here because of the 3 lists, not sure it changes anything anyway)
    for i in range(0,int(len(images_pathes_dp)/5)):
        tmp_merged_path = images_pathes_dp.pop()  # just in order to save the name
        tmp_img_dp = cv2.imread(tmp_merged_path, 0)
        tmp_img_of = cv2.imread(images_pathes_of.pop(), 0)
        tmp_img_vl = cv2.imread(images_pathes_vl.pop(), 0)
        
        # channel order can be changed if needed
        tmp_merged_image = cv2.merge((tmp_img_dp, tmp_img_of, tmp_img_vl))

        # save the newly created image
        tmp_merged_path = tmp_merged_path[:-7] + ".png"
        tmp_merged_path = tmp_merged_path.rsplit('/', 2)
        tmp_merged_path = output_val_folder + tmp_merged_path[2]

        cv2.imwrite(tmp_merged_path, tmp_merged_image)


    # put the 4/5 remaining in the train
    for image_path in images_pathes_dp:
        tmp_merged_path = images_pathes_dp.pop()  # just in order to save the name
        tmp_img_dp = cv2.imread(tmp_merged_path, 0)
        tmp_img_of = cv2.imread(images_pathes_of.pop(), 0)
        tmp_img_vl = cv2.imread(images_pathes_vl.pop(), 0)
        
        # channel order can be changed if needed
        tmp_merged_image = cv2.merge((tmp_img_dp, tmp_img_of, tmp_img_vl))

        # save the newly created image
        tmp_merged_path = tmp_merged_path[:-7] + ".png"
        tmp_merged_path = tmp_merged_path.rsplit('/', 2)
        tmp_merged_path = output_train_folder + tmp_merged_path[2]

        cv2.imwrite(tmp_merged_path, tmp_merged_image)