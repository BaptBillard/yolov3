# -*- coding: utf-8 -*-
from pathlib import Path, PosixPath

if __name__ == '__main__':

    kitti_labels = {"Car": 0, "Van": 1, "Truck": 2, "Pedestrian": 3, "Person_sitting": 4, "Cyclist": 5, "Tram": 6,  "Misc": 7, "DontCare": 7}
    img_size = (1242, 375)  # width, height: à vérifier

    labels_folder = 'training/labels/'
    output_labels_folder = "kitti/labels/"
    labels_pathes = [str(PosixPath(path)) for path in Path(labels_folder).rglob("*.txt")]

    for label_path in labels_pathes:
        f_old = open(label_path, "r")
        f_new = open(output_labels_folder + label_path[-10:], "w")  # on veut juste le nom du fichier, pas tout le chemin
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


