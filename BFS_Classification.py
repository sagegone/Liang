import torch
import numpy as np
import laspy
import sys
import traceback
import os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D 

las = laspy.read('stratmap20-50cm_3397552b3.las')
#print(len(las.points))

visited = []
queue = [] 
finlist = [[]]

xoffset = las.header.offsets[0]
xscale = las.header.scales[0]
xmax = las.header.max[0]
xmin = las.header.min[0]

yoffset = las.header.offsets[1]
yscale = las.header.scales[1]
ymax = las.header.max[1]
ymin = las.header.min[1]

zoffset = las.header.offsets[2]
zscale = las.header.scales[2]
zmax = las.header.max[2]
zmin = las.header.min[2]

# visisted = np.zeros((xmax,ymax,zmax))

count = 0

# separate into high vegetation & low vegetation
    # probably use a string array for naming? 
"""
highfile = laspy.create(point_format=las.header.point_format, file_version=las.header.version)
highfile.points = las.points[las.classification == 5]
highfile.write('highveg.las')

midfile = laspy.create(point_format=las.header.point_format, file_version=las.header.version)
midfile.points = las.points[las.classification == 4]
midfile.write('midveg.las')
"""

# create tree.las file (naming convention later) by combining high + low veg 
# code from https://gis.stackexchange.com/questions/410809/append-las-files-using-laspy 
""" try:

    out_las = '/Users/sagekim/projects/helloworld/Personal/Liang/treefile.las'
    inDir = '/Users/sagekim/projects/helloworld/Personal/Liang/las'    

    def append_to_las(in_laz, out_las):
        with laspy.open(out_las, mode='a') as outlas: # a = append only! 
            with laspy.open(in_las) as inlas:
                for points in inlas.chunk_iterator(2_000_000):
                    outlas.append_points(points)

    for (dirpath, dirnames, filenames) in os.walk(inDir):
        for inFile in filenames:
            if inFile.endswith('.las'):
                in_las = os.path.join(dirpath, inFile)
                append_to_las(in_las, out_las)
            
except:
    tb = sys.exc_info()[2]
    tbinfo = traceback.format_tb(tb)[0]
    print('Error in append las')
    print ("PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError     Info:\n" + str(sys.exc_info()[1]))    

""" 
    
tree = laspy.read('treefile.las') 
print(len(tree.points))

for n in tree: 

    # 500 trees? break! 
    if (count > 100): break

    # medium + high vegetation 
    if n.classification == 4 or n.classification == 5: 
        
        # counts every time there's a new cluster of green 
        count += 1 
        #print(count)

        # list of This Bunch Of Green Stuff 
        templist = []

        # throw 'starting value' into the queue/visited/&c 
        visited.append(n)
        queue.append(n)
        templist.append(n)

        while queue: 

            # basic bfs 
            m = queue.pop(0)

            # hard-code potential offsets 
            coordmanip = [ [-1, -1, +1], [0, -1, +1], [+1, -1, +1], 
                        [-1, 0, +1], [0, 0, +1], [+1, 0, +1], 
                        [-1, +1, +1], [0, +1, +1], [+1, +1, +1], 
                        [-1, -1, 0], [0, -1, 0], [+1, -1, 0],
                        [-1, 0, 0], [+1, 0, 0], 
                        [-1, +1, 0], [0, +1, 0], [+1, +1, 0], 
                        [-1, -1, -1], [0, -1, -1], [+1, -1, -1],
                        [-1, 0, -1], [0, 0, -1], [+1, 0, -1], 
                        [-1, +1, -1], [0, +1, -1], [+1, +1, -1] ]
            
            # calc offset manually  
            for manip in coordmanip:

                # check to see if new coords are in range 
                X_invalid = (xmin > ((n.X*xscale) + xoffset + manip[0])) | (xmax < ((n.X*xscale) + xoffset + manip[0]))
                Y_invalid = (ymin > ((n.Y*yscale) + yoffset + manip[1])) | (ymax < ((n.Y*yscale) + yoffset +  + manip[1]))
                Z_invalid = (zmin > ((n.Z*zscale) + zoffset + manip[2])) | (zmax < ((n.Z*zscale) + zoffset + manip[2]))
                
                if not np.any(X_invalid | Y_invalid | Z_invalid): 
                    #print("Run!")
                    neighbor = [((n.X*xscale) + xoffset + manip[0]), ((n.Y*yscale) + yoffset + manip[1]), ((n.Z*zscale) + zoffset + manip[2])]
                    if neighbor not in visited:
                            visited.append(neighbor)
                            queue.append(neighbor)
                            templist.append(neighbor)
                            #print(neighbor)
                            #print(templist)
        finlist.append(templist)
        #print(finlist[count])
        #print(templist)

print("Rendering stage.")

for coords in finlist:

    print(coords)

    max_x = max(coords[:,0])
    print(max_x)
    """max_y = coords.max[1]
    max_z = coords.max[2]

    min_x = coords.header.min[0]
    min_y = coords.header.min[1]
    min_z = coords.header.min[2]"""

    """if (coord[0] > max_x): 
            max_x = coord[0]
        if (coord[0] < min_x): 
            min_x = coord[0]
        if (coord[1] > max_y): 
            max_y = coord[1]
        if (coord[1] < min_y): 
            min_y = coord[1]
        if (coord[2] > max_z): 
            max_z = coord[2]
        if (coord[2] < min_z): 
            min_z = coord[2]"""

    # print(max_x, min_x, max_y, min_y, max_z, min_z)
        
# turn it into a numpy array for 3d slicing(?) purposes 
#nplist = np.array(finlist)
#test = finlist[0]

#print(finlist[0])

#print(x_data)
#print(y_data)
#print(z_data)

#fig = plt.figure(figsize=(5, 5))
#ax = fig.add_subplot(111, projection="3d")

#ax.scatter(x_data, y_data, z_data)
#ax.set_axis_off()
#plt.show()
