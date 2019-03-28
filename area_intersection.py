# Licence: CC-BY
# Description: This script estimates the intersecting area between two layers
# it adds a column (in the input layer) and fill it with the intersection area
# with objects fron the second layer (in the facilities layer)
# Note: This script is expected to run within the QGIS v3 console
#
# Authors:  Diego Pajarito 

from qgis.core import *
import qgis.utils
from qgis.core import QgsVectorLayer
import processing

# Setting up the input values
# Type here the input layer name as seen in the project. This layer will receive
# the values with the intersecting area
input_layer_name = 'censusblocks'
# Field in which the area will be stored
field_name = 'area_res'
# Type here the intersection layer which will serve for calculating the 
# intersection area
intersection_layer_name = 'prim_residential'

# 
input_layer = QgsProject.instance().mapLayersByName(input_layer_name)[0]
inter_layer = QgsProject.instance().mapLayersByName(intersection_layer_name)[0]
input_fields = input_layer.fields().names()

if field_name in input_fields:
    print('Field already exists. No changes in the layer structure')
else:
    # If there is no field, the layer gets modified
    input_layer.startEditing()
    input_layer.dataProvider().addAttributes([QgsField(field_name, QVariant.Double)])
    input_layer.updateFields()
    input_fields = input_layer.fields().names()
    input_layer.commitChanges()
    print('Field does not exist. We proceeded to add it to the layer')
field_idx = input_layer.dataProvider().fieldNameIndex(field_name)
print('Field idx (to store): ' + str(field_idx))

i = 0  # a simple counter

for feature in input_layer.getFeatures():
    i = i + 1
    # select the features in intersection layer for area
    area = 0
    cands = inter_layer.getFeatures(QgsFeatureRequest().setFilterRect(feature.geometry().boundingBox()))
    for area_feature in cands:
        # Here we add all the pieces of area intersecting to build a single value
        if feature.geometry().intersects(area_feature.geometry()):
            intersection = area_feature.geometry().intersection(feature.geometry())
            area = area + intersection.area()
    # Update values only when there is area intersecting
    input_layer.startEditing()
    feature_id = feature.id()
    input_layer.changeAttributeValues(feature_id, {field_idx:area})
    input_layer.commitChanges()

print('Processed %i objects' % i)
    
if not input_layer.isValid():
    raise Exception('Input layer is not valid')
