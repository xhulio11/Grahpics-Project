import numpy as np

def interpolate_color(x1, x2, x, C1, C2):
    # Taking the RGB values for each corner
    r1,r2 = C1[0],C2[0]
    g1,g2 = C1[1],C2[1]
    b1,b2 = C1[2],C2[2]
    if x1<x<x2:
        l = x2 - x1
        ra = x - x1
        # Implementing the interpolation
        # vp = l-x/l * va + x/l * vb

        r = ((l-ra)/l) * r1 + (ra/l) * r2
        g = ((l-ra)/l) * g1 + (ra/l) * g2
        b = ((l-ra)/l) * b1 + (ra/l) * b2
        return [r,g,b]
    # if x is out of the range for interoplation then take
    # the color of the borders
    elif x <= x1:
        return C1
    else:
        return C2

def shade_triangle(img, verts2d, vcolors):
    
    x1,y1 = verts2d[0][0],verts2d[0][1]
    x2,y2 = verts2d[1][0],verts2d[1][1]
    x3,y3 = verts2d[2][0],verts2d[2][1]

    y = [y1,y2,y3]
    triangle_points = [[int(x1),int(y1)],[int(x2),int(y2)],[int(x3),int(y3)]]
    
    # Sorting based on y cordinate
    index = np.argsort(y)
    triangle_points = sorted(triangle_points,key=lambda x:x[1])
    C1 = vcolors[index[0]]
    C2 = vcolors[index[1]]
    C3 = vcolors[index[2]]
    
    triangle_filler(img,triangle_points,C1,C2,C3)


def triangle_filler(img, points,C1,C2,C3):
    # Taking the corners of the triangle (y cordinates are sorted)
    # So y3 => y2 => y1
    x1,y1 = points[0][0],points[0][1]
    x2,y2 = points[1][0],points[1][1]
    x3,y3 = points[2][0],points[2][1]
    
    # There are 7 different cases
    # One spot
    if x1 == x2 == x3 and y1 == y2 == y3:
        R = (C1[0] + C2[0] + C3[0])/3
        G = (C1[1] + C2[1] + C3[1])/3
        B = (C1[2] + C2[2] + C3[2])/3
        img[x1][y1] = [R,G,B]
  
    # One vertical line
    elif x1 == x2 == x3 and y1 != y2:
        fun1(img,x1,y1,y3,C1,C3)

    # Horizontal line
    elif y1 == y2 == y3 and x1 != x2 :
        x = [x1,x2,x3]
        x_min = np.min(x)
        x_max = np.max(x)
        for x in range(x_min,x_max + 1):
            img[y1][x] = interpolate_color(x1,x3,x,C1,C3)
    
    # Triangle with up edge horizontal
    elif y2 == y3 and y1 != y2 and x3 != x2 :
        fun3(img,x1,x2,x3,y1,y2,y3,C1,C2,C3)

    # Triangle with down edge horizontal
    elif y1 == y2 and y3 != y1 and x1 != x2:
        fun4(img,x1,x2,x3,y1,y2,y3,C1,C2,C3)
       
    # Normal Triangle or Line with slope
    elif y1 != y2 and y2 != y3 :
        m12 = (x2-x1)/(y2 - y1)
        m23 = (x2-x3)/(y2 - y3)
        m13 = (x1-x3)/(y1 - y3)
        # Line with slope
        if m12 == m13:
            fun2(img,x1,x2,x3,y1,y2,y3,C1,C3)
        # Normal Trianlge
        else:
            fun5(img,x1,x2,x3,y1,y2,y3,C1,C2,C3)



"""
FOR THE VERTICAL LINE
"""
def fun1(img,x1,y1,y3,C1,C3):
    img[y1][x1] = C1
    img[y1][x1] = C3
    for y in range(y1+1, y3):
        img[y][x1] == interpolate_color(y1, y3, y, C1, C3)

""" 
FOR THE BENDED LINE
"""
def fun2(img,x1,x2,x3,y1,y2,y3,C1,C3):
    m = (x1 - x2)/(y1 - y2)
    x = x1
    img[y1][x1] = C1
    img[y3][x3] = C3
    for y in range(y1 +1, y3 ):
        img[y][int(np.rint(x))] = interpolate_color(y1,y3,y,C1,C3)
        x = x + m        

"""
TRIANGLE WITH UP EDGE HORIZONTAL
"""
def fun3(img,x1,x2,x3,y1,y2,y3,C1,C2,C3):
    m12 = (x1 - x2)/(y1 - y2)
    m13 = (x1 - x3)/(y1 - y3)
    
    # filling the first color
    img[y1][x1] = C1
    img[y2][x2] = C2
    img[y3][x3] = C3
    x_left = x_right = x1
        
    if x2 < x3:   
        for y in range(y1+1,y3):
            x_left = x_left + m12
            x_right = x_right + m13
            left_color = interpolate_color(y1,y2,y,C1,C2)
            right_color = interpolate_color(y1,y3,y,C1,C3)
            for x in range(int(x_left),int(np.rint(x_right))):
                img[y][x] = interpolate_color(x_left,x_right,x,left_color,right_color)

    elif x3 < x2:

        for y in range(y1+1,y3):
            x_left = x_left + m13
            x_right = x_right + m12
            left_color = interpolate_color(y1,y3,y,C1,C3)
            right_color = interpolate_color(y1,y2,y,C1,C2)
            for x in range(int(x_left),int(np.rint(x_right))):
                img[y][x] = interpolate_color(x_left,x_right,x,left_color,right_color)

"""
TRIANGLE WITH DOWN EDGE HORIZONTAL
"""
def fun4(img,x1,x2,x3,y1,y2,y3,C1,C2,C3):
    m23 = (x2 - x3)/(y2 - y3)
    m13 = (x1 - x3)/(y1 - y3)


    if x1 < x2:
        x_left = x1
        x_right = x2 
        
        for x in range(x_left, int(np.rint(x_right)) ):
            img[y1][x] = interpolate_color(x_left,x_right,x,C1,C2)

        for y in range(y1+1,y3+1):
            x_left = x_left + m13
            x_right = x_right + m23
            left_color = interpolate_color(y1,y3,y,C1,C3)
            right_color = interpolate_color(y2,y3,y,C2,C3)
            for x in range(int(x_left),int(np.rint(x_right))):
                img[y][x] = interpolate_color(x_left,x_right,x,left_color,right_color)

    elif x1 > x2:
        x_left = x2
        x_right = x1

        for x in range(x_left, x_right):
            img[y1][x] = interpolate_color(x_left,x_right,x,C2,C1)

        for y in range(y1+1,y3+1):
            x_left = x_left + m23
            x_right = x_right + m13
            left_color = interpolate_color(y2,y3,y,C2,C3)
            right_color = interpolate_color(y1,y3,y,C1,C3)
            for x in range(int(x_left),int(np.rint(x_right))):
                img[y][x] = interpolate_color(x_left,x_right,x,left_color,right_color)

"""
RANDOM NORMAL TRIANGLE
"""
def fun5(img,x1,x2,x3,y1,y2,y3,C1,C2,C3):
    # Finding the slopes
    m12 = (x2-x1)/(y2 - y1)
    m23 = (x2-x3)/(y2 - y3)
    m13 = (x1-x3)/(y1 - y3)

    # Initializing the colors of the corners
    img[y1][x1] = C1

    temp_x1 = x1
    temp_x2 = x1

    """
    1. Finding the 2 active points
    2. Taking the indexes of the sorted two points (We need this to choose the right colors for interpolation)
    3. Finding the color_1 and color_2 which are the interpolation between y cordinates
    4. Interpolating for every x in a for loop
    """
    for y in range(y1+1, y2+1):
        temp_x1 = temp_x1 + m12
        temp_x2 = temp_x2 + m13

        index = np.argsort([temp_x1,temp_x2])
        s = sorted([temp_x1,temp_x2])
        color_1 = interpolate_color(y1,y2,y,C1,C2) 
        color_2 = interpolate_color(y1,y3,y,C1,C3)
        colors = [color_1,color_2]

        for x in range(int(s[0]), int(np.rint(s[1]))):
            img[y][x] = interpolate_color(s[0],s[1],x,colors[index[0]],colors[index[1]])
    
    for y in range(y2+1, y3+1):
        temp_x1 = temp_x1 + m23
        temp_x2 = temp_x2 + m13
        index = np.argsort([temp_x1,temp_x2])
        s = sorted([temp_x1,temp_x2]) # these are the indexes of the sorted active x cordinates

        color_1 = interpolate_color(y1,y3,y,C2,C3)
        color_2 = interpolate_color(y2,y3,y,C1,C3) 
        colors = [color_1,color_2]
        
        for x in range(int(s[0]), int(np.rint(s[1]))):
            img[y][x] = interpolate_color(s[0],s[1],x,colors[index[0]],colors[index[1]])
   







