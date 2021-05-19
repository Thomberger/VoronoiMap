import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import re
from svgpath2mpl import parse_path

def getAttr(string):
    opacity_id = string.find('opacity:')
    opacity_id_2 = string.find(';',opacity_id)
    if opacity_id >=0 :
        opacity = float(string[opacity_id+8:opacity_id_2])
    else:
        opacity=1
        
    color_id = string.find('stroke:')
    color_id_2 = string.find(';',color_id)
    if color_id >=0 :
        color = string[color_id+7:color_id_2]
    else:
        color = 'black'
        
    fill_id = string.find('fill:')
    fill_id_2 = string.find(';',fill_id)
    if fill_id >=0 :
        fill = string[fill_id+5:fill_id_2]
    else:
        fill = 'none'
    
    fill_opacity_id = string.find('fill-opacity:')
    fill_opacity_id_2 =  string.find(';',fill_opacity_id)
    if fill_opacity_id >= 0 :
        fill_opacity = float(string[fill_opacity_id+13:fill_opacity_id_2])
    else:
        fill_opacity = 1
           
    stroke_width_id = string.find('stroke-width:')
    stroke_width_id_2 = string.find(';',stroke_width_id)
    if stroke_width_id >= 0 :
        stroke_width = float(string[stroke_width_id+13:stroke_width_id_2])/3
    else:
        stroke_width=1
        
    return opacity,color,fill,fill_opacity,stroke_width





def ReadSvgPath(filepath,ax,zorder):
    from svgpathtools import svg2paths
    paths, attributes = svg2paths(filepath, convert_circles_to_paths=False,convert_rectangles_to_paths=False)
    for j,path in enumerate(paths):
        attribs = attributes[j]['style']
        opacity,color,fill,fill_opacity,stroke_width = getAttr(attribs)
        
        MPLPath = parse_path(attributes[j]['d'])
        patch = patches.PathPatch(MPLPath, facecolor=fill, edgecolor=color, linewidth=stroke_width, alpha=fill_opacity, zorder=zorder)
        ax.add_patch(patch)
    

        
    return ax
    
