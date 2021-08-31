# -*- coding: utf-8 -*-
""" 
Created on 8/2/2021 8:18 AM
@author  : Kuro Kien
@File name    : pinkcoord_landmark_plot.py 
"""

import numpy as np
import os
import cv2 as cv
from xml.dom import minidom
from skimage.transform import rotate

inputDir = "new_2"
outputDir = "new_2"

# inputDir = r"C:\Users\DELL\Downloads\tony_project\new_2"
# outputDir = r"C:\Users\DELL\Downloads\tony_project\new_2"

node_name_outlines = ["top", "right_forehead_9", "right_forehead_10", "left_forehead_9", "left_forehead_10"]
node_name_mouth = ["above_lip_lw_1", "above_lip_lw_4", "above_lip_lw_5", "below_lip_up_5",
                   "below_lip_up_1", "left_forehead_10"]
node_name_iris_list = ["iris", "iris_size"]

folders = ['coords_path','primary_image_path']
def read_new_landmark(root):
    """This functions return the angle between a horizontal line and a line that joins the eyes"""
    coor = []
    for node in root.childNodes:
        if type(node) == minidom.Element:
            # print(node.tagName)
            for nod in node.childNodes:
                if type(nod) == minidom.Element:
                    # print(nod.tagName)
                    for finally_node in nod.childNodes:
                        if type(finally_node) == minidom.Element:
                            # print(finally_node.tagName)
                            if not ((nod.tagName == 'outlines' and finally_node.tagName in node_name_outlines) \
                                    or (nod.tagName == 'mouth' and finally_node.tagName in node_name_mouth) \
                                    or (finally_node.tagName in node_name_iris_list)):
                                x, y = float(finally_node.attributes['x'].value), float(finally_node.attributes['y'].value)
                                coor.append([int(x), int(y)])
    return coor


def draw_landmark(inputDir, outputDir, folders):
    sec_folders = os.listdir(os.path.join(inputDir, folders[0]))
    for sec_folder in sec_folders:
        path_coord = os.path.join(inputDir, folders[0], sec_folder)
        path_image = os.path.join(inputDir, folders[1], sec_folder)
        path_images = os.listdir(path_image)
        path_coords = os.listdir(path_coord)

        for im, coo in np.array([path_images, path_coords]).T:
            if os.path.isdir(os.path.join(outputDir, "landmark_plot", sec_folder)) == False:
                os.makedirs(os.path.join(outputDir, "landmark_plot", sec_folder))
            img = cv.imread(path_image + "/" + im)
            corrFile = path_coord + "/" + coo
            # print(corrFile)
            dom = minidom.parse(corrFile)
            root = dom.documentElement
            coordinates = read_new_landmark(root)
            # print(coordinates)
            for coor in coordinates:
                cv.circle(img, tuple(coor), 1, (0, 190, 255), -1)
            cv.imwrite(outputDir + "/landmark_plot/" + sec_folder + "/" + im, img)
            # cv.imshow("input", img)
            # cv.waitKey(0)

draw_landmark(inputDir, outputDir, folders)

