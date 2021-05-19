import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.spatial import Voronoi, voronoi_plot_2d
from ReadSvgPath import ReadSvgPath

"""
Map_names: Svg files you want to add the voronoi from (Lot of differents svg maps are available from Wikipedia)
Location_names = Csv files you want to create the voronoi diagram from (You could extract this from the svg directly or from lat long)
point_formats = Format of the location file.    If 0 location are extracted directly from csv (correct coordinate just need traslation) 
                                                If 1 location are extracted from lat lon and need some scaling. parameters should be modified to have correct scaling
svgsizes = Scaling of the svg file to have correct axis limits

Above_L = Boolean if you want to add a layer on top of the map (usually to cut the voronoi lines going to infinity)
Above_Layers = Svg file of the layer you want to add on top. This layer can be created by removing all inside data from your svg map and adding a white rectangle on the exterior. (use inkscape)
"""
##################
# TO BE MODIFIED #
##################

Map_names = ["France_region","France_region2016","Suisse_canton"] #SVG
Location_names = ["France_Location","France_Location2016","Suisse_Location"] #CSV
point_formats = [1,1,0]
svgsizes = [[0, 587.5, 0, 550],[0, 587.5, 0, 550],[0, 1052, 0, 744]]

Above_L = True
Above_Layers = ["France","France","Suisse"] #SVG

######################
# NOT TO BE MODIFIED #
######################

for mapsvg,location,layer,point_format,svgsize in zip(Map_names,Location_names,Above_Layers,point_formats,svgsizes):
    fig = plt.figure()
    ax = fig.add_subplot(111, aspect='equal')
    
    ax = ReadSvgPath(mapsvg + ".svg",ax,0)
    
    df = pd.read_csv("./" + location + ".csv")
    
    if point_format == 0:
        points=np.array(df)
        points[:,0] = points[:,0] + 340
        points[:,1] = points[:,1] + 160
    else:
        points=[]
        for i in range(0, df.shape[0]):
            point = df['point'][i].split(',')
            points.append([float(point[1][:]),-float(point[0][1:])])
            
        points=np.array(points)
        
        points[:,0] = points[:,0] - points[:,0].min() + 3
        points[:,0] = points[:,0] / points[:,0].max() * 477
        
        points[:,1] = points[:,1] - points[:,1].min() +0.6
        points[:,1] = points[:,1] / points[:,1].max() * 438
        
    vor = Voronoi(points)
    voronoi_plot_2d(vor,ax, show_vertices=False, point_size=2, line_alpha = 0.9,line_width=0.5)
    
    if Above_L:     
        ax = ReadSvgPath(layer + ".svg",ax,2)
    
    ax.axis(svgsize)
    ax.invert_yaxis()
    plt.axis('off')
    if Above_L:
        st = ""
    else:
        st = "_notcut"
    plt.savefig("Voronoi_" + mapsvg + st +".png", dpi=400, bbox_inches='tight')
    plt.show()