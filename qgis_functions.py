"""
Scripts for interfacing with QGIS
"""
from osgeo import ogr
from qgis.core import *
from qgis.PyQt.QtGui import QColor
from matplotlib import cm

def run_qgis():
    # Create a reference to the QgsApplication.  Setting the
    # second argument to False disables the GUI.
    qgs = QgsApplication([], False)

    # Load providers
    qgs.initQgis()
    return(qgs)
    
def new_project(crs=3857):
    project = QgsProject.instance()
    project = set_project_crs(project,number=crs)
    return(project)

def open_project(path):
    project = QgsProject.instance()
    project.read(path)
    return(project)

def save_project(project,path):
    project.write(path)
    return

def exit_qgis(qgs):
    qgs.exit()
    return

def add_gpkg(path,project,crs=4326):
    layers = [x.GetName() for x in ogr.Open(path)]
    for layer in layers:
        full_name = path + "|layername=" + layer
        vlayer = QgsVectorLayer(full_name,layer,'ogr')
        vlayer = set_layer_crs(vlayer,number=crs)
        if not vlayer.isValid():
            print(layer+' failed.')
        else:
            project.addMapLayer(vlayer)
    return

def add_shp(path,project,crs=4326,name='layer'):
    layer = QgsVectorLayer(path,name,'ogr')
    layer = set_layer_crs(layer,number=crs)
    if not vlayer.isValid():
        print(name+' failed.')
    else:
        project.addMapLayer(layer)
    return(layer)

def add_xyz(source,project):
    if source=='Google Hybrid':
        url = (
            'type=xyz&url=https://mt1.google.com/vt/lyrs%3Dy%26x%3D%7Bx%7D%26y%3D%7By%7D%26z%3D%7Bz%7D&zmax=18&zmin=0'
            )
    else:
        print('Layer Not Found')
    layer = QgsRasterLayer(url,source,'wms')
    
    if layer.isValid():
        project.addMapLayer(layer)
    else:
        print('Adding Layer Failed')
        
def set_layer_crs(layer,number=4326):
    crs = layer.crs()
    crs.createFromId(number)
    layer.setCrs(crs)
    return(layer)

def set_project_crs(project,number=3857):
    crs = QgsCoordinateReferenceSystem(number)
    project.setCrs(crs)
    return(project)

def get_layers(project,criteria='all'):
    layers = project.mapLayers().values()
    if criteria=='all':
        return(layers)
    elif criteria=='vector':
        vlayers = []
        for layer in layers:
            if layer.type()==QgsMapLayerType.VectorLayer:
                vlayers.append(layer)
        return(vlayers)
    else:
        clayers = []
        for layer in layers:
            if criteria in layer.name():
                clayers.append(layer)
        return(clayers)

def change_shape_color(layer,shape,color,size):
    renderer = layer.renderer()
    symbol = QgsMarkerSymbol.createSimple(
        {'name':shape,'color':color,'size':size}
        )
    renderer.setSymbol(symbol)
    return

def categorized_symbology(layer,field,values,shapes,colors,sizes):
    
    categories = []
    if len(values) == len(shapes) == len(colors) == len(sizes):
        for x in range(len(values)):
            symbol = QgsMarkerSymbol.createSimple(
                {'name':shapes[x],'color':colors[x],'size':sizes[x]}
                )
            category = QgsRendererCategory(values[x], symbol, str(values[x]))
            categories.append(category)
        renderer = QgsCategorizedSymbolRenderer(field,categories)
        layer.setRenderer(renderer)
    else:
        print('Lengths of values, shapes, and colors do not match')
    return

def qgis_colormap(cmap,number):
    colormap = cm.get_cmap(cmap,number)
    colors = []
    for i in range(colormap.N):
        rgba = colormap(i)
        rgba_255 = [x*255 for x in rgba]
        color = QColor(rgba_255[0],rgba_255[1],rgba_255[2],rgba_255[3])
        colors.append(color)
    return(colors)

        
        

    
    