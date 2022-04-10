from re import I
import numpy as np


def shade_triangle(img, verts2d, vcolors):
    
    x1,y1 = verts2d[0][0],verts2d[0][1]
    x2,y2 = verts2d[1][0],verts2d[1][1]
    x3,y3 = verts2d[2][0],verts2d[2][1]

    C1 = vcolors[0]
    C2 = vcolors[1]
    C3 = vcolors[2]

    # Average color of the three corners
    R = (C1[0] + C2[0] + C3[0])/3
    G = (C1[1] + C2[1] + C3[1])/3
    B = (C1[2] + C2[2] + C3[2])/3
    color_center = [R,G,B]    

    triangle_points = [[int(x1),int(y1)],[int(x2),int(y2)],[int(x3),int(y3)]]
    
    # Sorting based on y cordinate
    triangle_points = sorted(triangle_points,key=lambda x:x[1])
    
    return triangle_filler(img,triangle_points,color_center)



def triangle_filler(img, points, color_center):
    # Taking the corners of the triangle (y cordinates are sorted)
    # So y3 => y2 => y1
    x1,y1 = points[0][0],points[0][1]
    x2,y2 = points[1][0],points[1][1]
    x3,y3 = points[2][0],points[2][1]
    
    # There are 7 different cases
    # One spot
    if x1 == x2 == x3 and y1 == y2 == y3:
        img[x1][y1] = color_center
    # One vertical line
    elif x1 == x2 == x3 and y1 != y2:
        fun1(img,x1,y1,y3,color_center)
    # Horizontal line
    elif y1 == y2 == y3 :
        x = [x1,x2,x3]
        x_min = np.min(x)
        x_max = np.max(x)
        for x in range(x_min,x_max + 1):
            img[y1][x] = color_center
    # Triangle with up edge horizontal
    elif y2 == y3 and y1 != y2 and x3 != x2 :
        fun3(img,x1,x2,x3,y1,y2,y3,color_center)
    # Triangle with down edge horizontal
    elif y1 == y2 and y3 != y1 and x1 != x2:
        fun4(img,x1,x2,x3,y1,y2,y3,color_center)
    # Normal Triangle or Line with slope
    elif y1 != y2 and y2 != y3 :
        m12 = (x2-x1)/(y2 - y1)
        m13 = (x1-x3)/(y1 - y3)
        # Line with slope
        if m12 == m13:
            fun2(img,x1,x2,y1,y2,y3,color_center)
        else:
            # Normal Trianlge
            fun5(img,x1,x2,x3,y1,y2,y3,color_center)
    # Two points line
    elif y1 == y2 and y2 != y3:
        fun2(img,x1,x3,y1,y3,y3,color_center)
    # Two points line
    elif y1 != y2 and y2 == y3:
        fun2(img,x1,x2,y1,y2,y2,color_center)


"""
FOR THE VERTICAL LINE
"""
def fun1(img,x1,y1,y3,color_center):
    for y in range(y1, y3+1):
        img[y][x1] == color_center

""" 
FOR THE BENDED LINE
"""
def fun2(img,x1,x2,y1,y2,y3,color_center):
    m = (x1 - x2)/(y1 - y2)
    x = x1
    for y in range(y1, y3 + 1):
        img[y][int(np.rint(x))] = color_center
        x = x + m        

"""
TRIANGLE WITH UP EDGE HORIZONTAL
"""
def fun3(img,x1,x2,x3,y1,y2,y3,color_center):
    m12 = (x1 - x2)/(y1 - y2)
    m13 = (x1 - x3)/(y1 - y3)
    
    # filling the first color
    img[y1][x1] = color_center
    x_left = x_right = x1
        
    if x2 < x3:   
        for y in range(y1+1,y3+1):
            x_left = x_left + m12
            x_right = x_right + m13

            for x in range(int(x_left),int(np.rint(x_right))+1):
                img[y][x] = color_center

    elif x3 < x2:

        for y in range(y1+1,y3+1):
            x_left = x_left + m13
            x_right = x_right + m12

            for x in range(int(x_left),int(np.rint(x_right))+1):
                img[y][x] = color_center

"""
TRIANGLE WITH DOWN EDGE HORIZONTAL
"""
def fun4(img,x1,x2,x3,y1,y2,y3,color_center):
    m23 = (x2 - x3)/(y2 - y3)
    m13 = (x1 - x3)/(y1 - y3)

    if x1 < x2:
        x_left = x1
        x_right = x2 
        
        for x in range(x_left, int(np.rint(x_right)) + 1):
            img[y1][x] = color_center

        for y in range(y1+1,y3+1):
            x_left = x_left + m13
            x_right = x_right + m23

            for x in range(int(x_left),int(np.rint(x_right))+1):
                img[y][x] = color_center

    elif x1 > x2:
        x_left = x2
        x_right = x1
        for x in range(x_left, x_right + 1):
            img[y1][x] = color_center

        for y in range(y1+1,y3+1):
            x_left = x_left + m23
            x_right = x_right + m13

            for x in range(int(x_left),int(np.rint(x_right))+1):
                img[y][x] = color_center

"""
RANDOM NORMAL TRIANGLE
"""

def fun5(img,x1,x2,x3,y1,y2,y3,color_Center):
    m12 = (x2-x1)/(y2 - y1)
    m23 = (x2-x3)/(y2 - y3)
    m13 = (x1-x3)/(y1 - y3)

    img[y1][x1] = color_Center
    temp_x1 = x1
    temp_x2 = x1
    for y in range(y1+1, y2+1):
        temp_x1 = temp_x1 + m12
        temp_x2 = temp_x2 + m13
        x = sorted([temp_x1,temp_x2])

        for x in range(int(x[0]), int(np.rint(x[1]))):
            img[y][x] = color_Center
    
    for y in range(y2+1, y3+1):
        temp_x1 = temp_x1 + m23
        temp_x2 = temp_x2 + m13
        x = sorted([temp_x1,temp_x2])

        for x in range(int(x[0]), int(np.rint(x[1]))):
            img[y][x] = color_Center
        





