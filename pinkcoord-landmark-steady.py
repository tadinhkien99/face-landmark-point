# -*- coding: utf-8 -*-
"""
Created on 8/3/2021 6:35 PM
@author  : Kuro Kien
@File name    : pink_old.py
"""

# -*- coding: utf-8 -*-
import math

"""
Created on Sun Aug 1 9:52:10 2021

@author: kuro
"""
from scipy.linalg import solve
import numpy as np
import os
import cv2 as cv
from xml.dom import minidom


inputDir = r"C:\Users\DELL\Downloads\AI_FL\tony_project\FrontalFace-adv-2"
outputDir = r"C:\Users\DELL\Downloads\AI_FL\tony_project\new_2"

#inputDir = r"E:\BigData\IMG_REPO\face_landmarks\PinkCoords\PremiUserImage_20190101_20210430-parsed"
#outputDir = r"E:\BigData\IMG_REPO\face_landmarks\PinkCoords\PremiUserImage_20190101_20210430-steady"

"""Create list tag to ignore"""
node_name_outlines = ["top", "right_forehead_9", "right_forehead_10", "left_forehead_9", "left_forehead_10"]
node_name_mouth = ["above_lip_lw_1", "above_lip_lw_4", "above_lip_lw_5", "below_lip_up_5",
                   "below_lip_up_1", "left_forehead_10"]
node_name_iris_list = ["iris", "iris_size"]


def Find_rect(p1, p2):
    """Find the line between two points"""
    p1 = np.array(p1)
    p2 = np.array(p2)
    b = p2 - p1
    b = b[0] / b[1]
    c = p1[0] - p1[1] * b
    return b, c


def Find_angle(p1, p2, p3=[2.00000009, 1], p4=[2.0000001, 2]):
    """Find the angle between two lines"""
    b1, c1 = Find_rect(p1, p2)
    b2, c2 = Find_rect(p3, p4)
    v1 = np.array([-1, b1])
    v2 = np.array([-1, b2])
    angle = v2 @ v1 / (np.linalg.norm(v1) * np.linalg.norm(v2))
    return np.arccos(angle) / np.pi * 180


def Rotate_image(root):
    """This functions return all the angle between a horizontal line and all control rotate"""
    x_left = []
    y_left = []
    x_right = []
    y_right = []
    all_angle = []
    all_control = []
    y_right_array = []
    x_right_array = []
    for node in root.childNodes:
        if type(node) == minidom.Element:
            # print(node.tagName)
            for nod in node.childNodes:
                if type(nod) == minidom.Element and nod.tagName == "eyeL":
                    # print(nod.tagName)
                    # print(nod.attributes)
                    for elements in nod.childNodes:
                        if type(elements) == minidom.Element and not elements.tagName in node_name_iris_list:
                            if elements.tagName=='left':
                                y_left.append(float(elements.attributes["y"].value))
                                x_left.append(float(elements.attributes["x"].value))
                if type(nod) == minidom.Element and nod.tagName == "eyeR":
                    # print(nod.tagName)
                    # nod.attributes
                    for elements in nod.childNodes:
                        if type(elements) == minidom.Element and not elements.tagName in node_name_iris_list:
                            if elements.tagName=='right':
                                y_right.append(float(elements.attributes["y"].value))
                                x_right.append(float(elements.attributes["x"].value))

    for i in range(len(x_left)):
        control = False
        if y_left[i] > y_right[i]:
            control = True
        angle = Find_angle([y_right[i], x_right[i]], [y_left[i], x_left[i]])
        all_angle.append(angle)
        all_control.append(control)
        y_right_array.append(y_right[i])
        x_right_array.append(x_right[i])
    return all_angle, all_control


def rotatePoints(angle, point, x_center, y_center):
    """Rotate point according angle"""
    x_center = int(x_center)
    y_center = int(y_center)
    point = [y_center - point[0], x_center - point[1]]
    angle = np.radians(angle)
    cos_1 = np.cos(angle)
    sin_1 = np.sin(angle)
    return np.round(y_center - (point[0] * cos_1 - point[1] * sin_1)), np.round(
        x_center - (point[0] * sin_1 + point[1] * cos_1))

def find_nose_bottom_point(root):
    """Find nose bottom point to be angle point"""
    x_center = []
    y_center = []
    for node in root.childNodes:
        if type(node) == minidom.Element:
            # print(node.tagName)
            for nod in node.childNodes:
                if type(nod) == minidom.Element:
                    # print(nod.tagName)
                    for finally_node in nod.childNodes:
                        if type(finally_node) == minidom.Element:
                            # print(finally_node.tagName)
                            if nod.tagName == 'nose' and finally_node.tagName == 'bottom':
                                x_c = finally_node.attributes['x'].value
                                y_c = finally_node.attributes['y'].value
                                x_center.append(x_c)
                                y_center.append(y_c)
    return x_center, y_center

def New_coord(root, angle, x_center, y_center, x_cropped_point, y_cropped_point):
    """ Update the xml files"""
    for node in root.childNodes:
        if type(node) == minidom.Element:
            # print(node.tagName)
            for nod in node.childNodes:
                if type(nod) == minidom.Element:
                    # print(nod.tagName)
                    for finally_node in nod.childNodes:
                        if type(finally_node) == minidom.Element:
                            # print(finally_node.tagName)
                            #if point in list ignore, just write old point to write point
                            if ((nod.tagName == 'outlines' and finally_node.tagName in node_name_outlines) \
                                    or (nod.tagName == 'mouth' and finally_node.tagName in node_name_mouth)\
                                    or (finally_node.tagName in node_name_iris_list)):
                                finally_node.attributes['x'].value, finally_node.attributes['y'].value = (str(-1), str(-1))
                            #if bottom nose, just subtract cropped begin point, don't rotate
                            elif nod.tagName == 'nose' and finally_node.tagName == 'bottom':
                                x, y = float(finally_node.attributes['x'].value), \
                                       float(finally_node.attributes['y'].value)
                                finally_node.attributes['x'].value, finally_node.attributes['y'].value = str(
                                    int(x-x_cropped_point)), str(int(y-y_cropped_point))
                            #another point will angle old point then subtract to update new point
                            else:
                                x, y = float(finally_node.attributes['x'].value), \
                                       float(finally_node.attributes['y'].value)
                                y, x = rotatePoints(angle, [y, x], x_center, y_center)
                                # if nod.tagName not in parent_and_nodeName_list.keys() and finally_node.tagName not in parent_and_nodeName_list.values()
                                finally_node.attributes['x'].value, finally_node.attributes['y'].value = str(
                                    int(x-x_cropped_point)), str(int(y-y_cropped_point))
    return root

def get_rotated_point_brow_chin(root, angle, x_center, y_center):
    """get brow left point, brow right point and chin bottom point to calculate crop size"""
    outlines_bottom=[]
    browL_left=[]
    browR_right=[]
    outlines_left = []
    outlines_right = []
    for node in root.childNodes:
        if type(node) == minidom.Element:
            # print(node.tagName)
            for nod in node.childNodes:
                if type(nod) == minidom.Element:
                    # print(nod.tagName)
                    for finally_node in nod.childNodes:
                        if type(finally_node) == minidom.Element:
                            # print(finally_node.tagName)
                            x, y = float(finally_node.attributes['x'].value), float(
                                finally_node.attributes['y'].value)
                            if (nod.tagName == 'outlines' and finally_node.tagName == 'bottom'):
                                y_bottom, x_bottom = rotatePoints(angle, [y, x], x_center, y_center)
                                outlines_bottom.append([x_bottom, y_bottom])
                            elif (nod.tagName == 'browL' and finally_node.tagName == 'left'):
                                y_left, x_left = rotatePoints(angle, [y, x], x_center, y_center)
                                browL_left.append([x_left, y_left])
                            elif (nod.tagName == 'browR' and finally_node.tagName == 'right'):
                                y_right, x_right = rotatePoints(angle, [y, x], x_center, y_center)
                                browR_right.append([x_right, y_right])
                            elif (nod.tagName == 'outlines' and finally_node.tagName == 'left_8'):
                                y_out_line_left, x_out_line_left = rotatePoints(angle, [y, x], x_center, y_center)
                                outlines_left.append([x_out_line_left,y_out_line_left])
                            elif (nod.tagName == 'outlines' and finally_node.tagName == 'right_8'):
                                y_out_line_right, x_out_line_right = rotatePoints(angle, [y, x], x_center, y_center)
                                outlines_right.append([x_out_line_right,y_out_line_right])

    return outlines_bottom, browL_left, browR_right, outlines_left, outlines_right

def calculate_distance(p1, p2):
    """calculate distance between left brow point and right brow point"""
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])

def crop_rotated_image(image, distance, y_bottom_point,left_point, x_center_cropped_point):
    """get first point of crop size and width height fo this size"""
    # x = left_point[0]-(distance)
    y = left_point[1]-(distance)
    height = width = y_bottom_point-y+(distance/2)
    x = int(x_center_cropped_point) - height/2
    #check crop size is in image size
    if x>0 and y > 0 and (x+width) < image.shape[1] and (y+height) < image.shape[0]:
        image_cropped = image[int(y):int(y+height),int(x):int(x+width)]
        return image_cropped, x, y
    else:
        x=y=0
        return image, x,y


numbered_folders = os.listdir(os.path.join(inputDir, "primary_image_path"))
header = ["<?xml version=\"1.0\" encoding=\"utf-8\"?>"]
for numbered_folder in numbered_folders:
    numbered_folder_image = os.path.join(inputDir, "primary_image_path", numbered_folder)
    numbered_folder_xml = os.path.join(inputDir, "coords_path", numbered_folder)
    path_images = os.listdir(numbered_folder_image)

    for path_image in path_images:
    #for im, coo in np.array([path_images, path_coords]).T:
        if os.path.isdir(os.path.join(outputDir, "primary_image_path", numbered_folder)) == False:
            os.makedirs(os.path.join(outputDir, "primary_image_path", numbered_folder))
        if os.path.isdir(os.path.join(outputDir, "coords_path", numbered_folder)) == False:
            os.makedirs(os.path.join(outputDir, "coords_path", numbered_folder))
        print(os.path.join(numbered_folder_image, path_image))
        img = cv.imread(os.path.join(numbered_folder_image, path_image))
        arr_img = []
        xml_filename = str(path_image[:-4] + ".xml")
        path_xml = os.path.join(numbered_folder_xml, xml_filename)  # XML File Path
        if os.path.exists(path_xml) == False:
            print("Skipping: xml not found")
            txt_object = open(os.path.join(inputDir, 'error_log.txt'), 'a')
            txt_object.write('xml not found: ')
            txt_object.write(os.path.join(numbered_folder_image, path_image))
            txt_object.write("\n")
            txt_object.close()
            continue
        dom = minidom.parse(path_xml)
        root = dom.documentElement
        # image is rotated so that the corners of the eyes are in horizontal line.
        angle, control = Rotate_image(root)
        # print(angle)
        # center-point of rotation needed is tip of the nose.
        x_center, y_center = find_nose_bottom_point(root)
        for sub_img in range(len(angle)):
            arr_img.append(img.copy())
        for idx_face in range(len(angle)):
            dom = minidom.parse(path_xml)
            root = dom.documentElement
            count_face = []
            final_xml = []
            if control[idx_face]:
                angle[idx_face] *= -1
            center = tuple([float(x_center[idx_face]), float(y_center[idx_face])])
            #get matric rotate
            M = cv.getRotationMatrix2D(center, angle[idx_face], scale=1)
            #rotate image base on matrix rotate at nose bottom point
            img_rotated = cv.warpAffine(arr_img[idx_face], M, (arr_img[idx_face].shape[1], arr_img[idx_face].shape[0]), flags=cv.INTER_CUBIC)
            outlines_bottom, browL, browR, outlines_left, outlines_right  = get_rotated_point_brow_chin(root, angle[idx_face], x_center[idx_face], y_center[idx_face])
            distance = calculate_distance([browL[idx_face][0],browL[idx_face][1]],[browR[idx_face][0],browR[idx_face][1]])
            img_cropped, x_cropped_point, y_cropped_point = crop_rotated_image(image=img_rotated, distance=distance,
                                             y_bottom_point=outlines_bottom[idx_face][1], left_point=browL[idx_face],
                                                                               x_center_cropped_point=(outlines_right[idx_face][0]-outlines_left[idx_face][0])/2+outlines_left[idx_face][0])
            # cv.imshow("result", img_cropped)
            # img_cropped = cv.pyrUp(img_cropped,(9,9))
            if (img_cropped.shape[0]!= img_rotated.shape[0]) and (img_cropped.shape[0]<400 and img_cropped.shape[1]<400):
                print("Skipping: Cropped face {:d} size is less than 400x400".format(idx_face))
                continue
            elif (img_cropped.shape[0]== img_rotated.shape[0]):
                print("Skipping: Cropped face {:d} size is out of size original image".format(idx_face))
                continue
            cv.imwrite(outputDir + "/primary_image_path/"+numbered_folder+"/"+ path_image[:-4] + "_" +str(idx_face) + ".png", img_cropped, [cv.IMWRITE_PNG_COMPRESSION, 9])
            new_root = New_coord(root, angle[idx_face], x_center[idx_face], y_center[idx_face], x_cropped_point, y_cropped_point)
            new_root = new_root.toxml()
            all_root = new_root.split('\n')
            for j in range(len(all_root)):
                if "facelandmarks" in all_root[j]:
                    count_face.append(j)
            #write xml format
            final_xml = header + all_root[0:1] + all_root[
                                                 count_face[2 * idx_face]:count_face[2 * idx_face + 1]] + all_root[-2:]
            s_xml = ""
            f = open(outputDir + "/coords_path/"+numbered_folder+"/"+ xml_filename[:-4] + "_" +str(idx_face) + ".xml", 'w', encoding="utf-8")
            for s in final_xml:
                f.write(s + '\n')

