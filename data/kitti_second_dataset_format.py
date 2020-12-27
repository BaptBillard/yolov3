# -*- coding: utf-8 -*-
from pathlib import Path, PosixPath
import os
import cv2

def labelsFormat(indice, labels_pathes, labels_path):
    
    kitti_labels = {"Car": 0, "Van": 1, "Truck": 2, "Pedestrian": 3, "Person_sitting": 4, "Cyclist": 5, "Tram": 6,  "Misc": 7, "DontCare": 7}
    img_size = (1242, 375)  # width, height: à vérifier

    output_labels_folder = labels_path

    f_old = open(labels_pathes[indice], "r")
    f_new = open(output_labels_folder + labels_pathes[indice][-10:], "w")  # on veut juste le nom du fichier, pas tout le chemin
    for line in f_old:
        data_old = line.split()  # sépare le str en liste, chaque element est separé par un espace
            
        x_center = ((float(data_old[4]) + float(data_old[6])) / 2) / img_size[0]  # moyenne des cotes de la BB, divisé par la taille de l'image pour avoir un résultat entre 0 et 1
        y_center = ((float(data_old[5]) + float(data_old[7])) / 2) / img_size[0]  # idem
        width = (abs(float(data_old[4]) - float(data_old[6])) / img_size[0])  # idem: largeur de la BB divisée par largeur totale
        height = (abs(float(data_old[5]) - float(data_old[7])) / img_size[1])  # idem
            
        data_new = str(kitti_labels[data_old[0]]) + ' ' \
                   + str(x_center) + ' ' \
                   + str(y_center) + ' ' \
                   + str(width) + ' ' \
                   + str(height) + '\n'  # pas sûr de la fin de ligne
            
        f_new.write(data_new)
        
    f_new.close()
    f_old.close()

if __name__ == '__main__':

    img_size = (1242, 375)  # width, height: à vérifier

    images_folder = 'training/images/'
    output_train_folder = "second_kitti/images/train/"
    output_val_folder = "second_kitti/images/val/"
    labels_folder = 'training/labels/'
    output_labels_train_folder = 'second_kitti/labels/train/'
    output_labels_val_folder = 'second_kitti/labels/val/'
    images_pathes_dp = [str(PosixPath(path)) for path in Path(images_folder).rglob("*_Dp.png")]
    images_pathes_of = [str(PosixPath(path)) for path in Path(images_folder).rglob("*_Of.png")]
    images_pathes_vl = [str(PosixPath(path)) for path in Path(images_folder).rglob("*_Vl.png")]
    labels_pathes = [str(PosixPath(path)) for path in Path(labels_folder).rglob("*.txt")]
    labels_pathes.sort()

    # put 1/5 in val (no shuffle here because of the 3 lists, not sure it changes anything anyway)
    labels_indices_val = []
    print(len(images_pathes_dp))
    for i in range(0,int(len(images_pathes_dp)/5)):
        tmp_merged_path_val = images_pathes_dp.pop()  # just in order to save the name
        tmp_img_dp = cv2.imread(tmp_merged_path_val, 0)
        tmp_img_of = cv2.imread(images_pathes_of.pop(), 0)
        tmp_img_vl = cv2.imread(images_pathes_vl.pop(), 0)
        
        # channel order can be changed if needed
        tmp_merged_image = cv2.merge((tmp_img_dp, tmp_img_of, tmp_img_vl))

        # save the newly created image
        tmp_merged_path_val = tmp_merged_path_val[:-7] + ".png"
        tmp_merged_path_val = tmp_merged_path_val.rsplit('/', 2)
        tmp_merged_path_val = output_val_folder + tmp_merged_path_val[2]

        cv2.imwrite(tmp_merged_path_val, tmp_merged_image)

        labels_indices_val.append(int(tmp_merged_path_val[-10:-4]))

    #save labels in the right place
    for i in range(0, len(labels_pathes)):
        if i in labels_indices_val:
            labelsFormat(i, labels_pathes, output_labels_val_folder)
        else :
            labelsFormat(i, labels_pathes, output_labels_train_folder)


    # put the 4/5 remaining in the train
    print(len(images_pathes_dp))
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
