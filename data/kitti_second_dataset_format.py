# -*- coding: utf-8 -*-
from pathlib import Path, PosixPath
import os
import cv2

if __name__ == '__main__':

    img_size = (1242, 375)  # width, height: à vérifier

    images_folder = 'training/images/'
    output_labels_folder = "kitti/images/"
    images_pathes_dp = [str(PosixPath(path)) for path in Path(images_folder).rglob("*_Dp.png")]
    images_pathes_of = [str(PosixPath(path)) for path in Path(images_folder).rglob("*_Of.png")]
    images_pathes_vl = [str(PosixPath(path)) for path in Path(images_folder).rglob("*_Vl.png")]

    # create merged images
    for i in range(len(images_pathes_dp)):
        tmp_merged_path = image_pathes_dp[i]
        tmp_merged_path = tmp_merged_path[:-7] + ".png"

        tmp_img_dp = cv2.imread(images_pathes_dp[i], 0)
        tmp_img_of = cv2.imread(images_pathes_of[i], 0)
        tmp_img_vl = cv2.imread(images_pathes_vl[i], 0)
        
        # channel order can be changed if needed
        tmp_merged_image = cv2.merge((tmp_img_dp, tmp_img_of, tmp_img_vl))

        # save the newly created image
        cv2.imwrite(tmp_merged_path, tmp_merged_image)
