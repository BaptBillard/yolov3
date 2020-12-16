# -*- coding: utf-8 -*-
from pathlib import Path, PosixPath
import os
import random

def labelsFormat(indice, labels_pathes, labels_path):
    
    kitti_labels = {"Car": 0, "Van": 1, "Truck": 2, "Pedestrian": 3, "Person_sitting": 4, "Cyclist": 5, "Tram": 6,  "Misc": 7, "DontCare": 7}
    img_size = (1242, 375)  # width, height: à vérifier

    labels_folder = 'training/labels/'
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

    kitti_labels = {"Car": 0, "Van": 1, "Truck": 2, "Pedestrian": 3, "Person_sitting": 4, "Cyclist": 5, "Tram": 6,  "Misc": 7, "DontCare": 7}
    img_size = (1242, 375)  # width, height: à vérifier

    images_folder = 'training/images/'
    output_train_folder = "kitti/images/train/"
    output_val_folder = "kitti/images/val/"
    labels_folder = 'training/labels/'
    output_labels_train_folder = 'kitti/labels/train/'
    output_labels_val_folder = 'kitti/labels/val/'
    images_pathes = [str(PosixPath(path)) for path in Path(images_folder).rglob("*_Cl.png")]
    labels_pathes = [str(PosixPath(path)) for path in Path(labels_folder).rglob("*.txt")]

    # put 1/5 in val
    random.shuffle(images_pathes)
    images_pathes_val = []
    labels_indices_val = []
    labels_indices_train = []
    for i in range(0,int(len(images_pathes)/5)):
        images_pathes_val.append(images_pathes.pop())
        tmp_path = output_val_folder + images_pathes_val[i][-13:]
        print(int(images_pathes_val[i][-13:-7]))
        labels_indices_val.append(int(images_pathes_val[i][-13:-7]))
        tmp_path = tmp_path.rsplit("_", 1)[0] + ".png"
        
        os.rename(images_pathes_val[i], tmp_path)

    for i in labels_indices_val_labels:
        labelsFormat(i, labels_pathes, output_labels_val_folder)


    # put the 4/5 remaining in train
    for image_path in images_pathes:
        tmp_path = output_train_folder + image_path[-13:]
        tmp_path = tmp_path.rsplit("_", 1)[0] + ".png"
        os.rename(image_path, tmp_path)

    for i in range(len(labels_pathes)):
        if i not in labels_indices_val:
            labels_indices_train.append(i)

    for i in labels_indices_train:
        labelsFormat(i,output_labels_train_folder)

