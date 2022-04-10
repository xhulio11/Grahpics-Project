import numpy as np
import matplotlib.pyplot as plt
import flat as flat

# Initialiazing the img and resultion
N = M = 512
img = np.ones((N,M,3))

def main():
    # Taking the data from the hw1.npy file
    data = np.load("hw1.npy",allow_pickle=True)
    verts2d = data.item()['verts2d']
    vcolors = data.item()['vcolors']
    faces = data.item()['faces']
    depth = data.item()['depth']
    render(img,faces,verts2d,vcolors,depth)
  
  
def render(img,faces,verts2d, vcolors,depth):
    depth = depth_finder(depth,faces)
    # Sorting the depths from the biggest to the smallest
    indices = np.flip(np.argsort(depth))

    for i in indices:
        tri = faces[i]
        verts = [verts2d[tri[0]],verts2d[tri[1]],verts2d[tri[2]]]
        color = [vcolors[tri[0]],vcolors[tri[1]],vcolors[tri[2]]]
        flat.shade_triangle(img,verts,color)
       
    imgplt = plt.imshow(img)
    # Saving the Image
    plt.savefig("flat.jpg")
    # Showing the image
    plt.show()

# Finding the depth of eaech triangle
def depth_finder(depth, faces):
    fdepth = np.zeros([faces.shape[0]], dtype=np.float32)
    
    for idx, face in enumerate(faces):
        depths = depth[face]
        fdepth[idx] = np.mean(depths)
    return fdepth


main()