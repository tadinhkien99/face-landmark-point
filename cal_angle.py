# -*- coding: utf-8 -*-
""" 
Created on 8/3/2021 5:07 PM
@author  : Kuro Kien
@File name    : cal_angle.py 
"""

import math

def get_angle(line1, line2):
    # Get directional vectors
    d1 = (line1[1][0] - line1[0][0], line1[1][1] - line1[0][1])
    d2 = (line2[1][0] - line2[0][0], line2[1][1] - line2[0][1])
    # Compute dot product
    p = d1[0] * d2[0] + d1[1] * d2[1]
    # Compute norms
    n1 = math.sqrt(d1[0] * d1[0] + d1[1] * d1[1])
    n2 = math.sqrt(d2[0] * d2[0] + d2[1] * d2[1])
    # Compute angle
    ang = math.acos(p / (n1 * n2))
    # Convert to degrees if you want
    ang = math.degrees(ang)
    return ang

line1 = [(404, 681), (412, 620)]
line2 = [(15, 15), (20,  8)]

print(get_angle(line1, line2))