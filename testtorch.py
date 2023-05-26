import torch
import numpy as np
import laspy
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D 

las = laspy.read('stratmap20-50cm_3397552b3.las')
print(las) 

visited = []
queue = [] 
finlist = []

xoffset = las.header.offsets[0]
xscale = las.header.scales[0]

yoffset = las.header.offsets[1]
yscale = las.header.scales[1]

zoffset = las.header.offsets[2]
zscale = las.header.scales[2]


count = 0

for n in las: 

    # 500 trees? break! 
    if (count > 500): break

    # medium + high vegetation 
    if n.classification == 4 or n.classification == 5: 
        
        # counts every time there's a new cluster of green 
        count += 1 
        print(count)

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
                X_invalid = (las.header.mins[0] > ((n.X*xscale) + xoffset + manip[0])) | (las.header.maxs[0] < ((n.X*xscale) + xoffset + manip[0]))
                Y_invalid = (las.header.mins[1] > ((n.Y*yscale) + yoffset + manip[1])) | (las.header.maxs[1] < ((n.Y*yscale) + yoffset +  + manip[1]))
                Z_invalid = (las.header.mins[2] > ((n.Z*zscale) + zoffset + manip[2])) | (las.header.maxs[2] < ((n.Z*zscale) + zoffset + manip[2]))

                if not np.any(X_invalid | Y_invalid | Z_invalid): 
                    print("Run!")
                    neighbor = [((n.X*xscale) + xoffset + manip[0]), ((n.Y*yscale) + yoffset + manip[1]), ((n.Z*zscale) + zoffset + manip[2])]
                    lasneigh = neighbor in las
                    print(lasneigh)
                    if neighbor not in visited:
                        if lasneigh.classification == 4 or lasneigh.classification == 5:  
                            visited.append(neighbor)
                            queue.append(neighbor)
                            templist.append(neighbor)
                            print(neighbor)
                            print(templist)

        finlist.append(templist)

print("Rendering stage.")

#for i in finlist: 
    #for n in i: 
        #print(n)

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
