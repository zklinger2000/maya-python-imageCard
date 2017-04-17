__author__ = 'Zack Klinger'

import maya.cmds as cmds
import sys
sys.path.append('C:/Users/zklinger/Documents/maya/scripts/maya-python-imageCard/scripts')
from PIL import Image
import json
from imageCard import ImageCard
from xPassShader import XPassShader
from zDepthShader import ZDepthShader
from AOShader import AOShader
from positionShader import PositionShader


imageFolder = 'C:/Users/zklinger/Code/generator/plugins/generator-imageCard/test/'
# Get JSON data from file exported using generator-imageCard with original Photoshop file
with open('C:/Users/zklinger/Code/generator/plugins/generator-imageCard/test/docInfo.json', 'r') as f:
    data = json.load(f)

cardList = [] # List of all cards in scene

# Create Render layers in Layer Editor
zDepthRenderLayer = cmds.createRenderLayer(empty=True,
                                           name='zDepthRenderLayer',
                                           number=1, noRecurse=True)

AORenderLayer = cmds.createRenderLayer(empty=True,
                                       name='AORenderLayer',
                                       number=2, noRecurse=True)

positionRenderLayer = cmds.createRenderLayer(empty=True,
                                             name='positionRenderLayer',
                                             number=3, noRecurse=True)

# TODO: Create camera group with two locators
# Create a camera and get the shape name.
# camera -centerOfInterest 5 -focalLength 35 -lensSqueezeRatio 1 -cameraScale 1 -horizontalFilmAperture 1.41732 -horizontalFilmOffset 0 -verticalFilmAperture 0.94488 -verticalFilmOffset 0 -filmFit Fill -overscan 1 -motionBlur 0 -shutterAngle 144 -nearClipPlane 0.1 -farClipPlane 10000 -orthographic 0 -orthographicWidth 30 -panZoomEnabled 0 -horizontalPan 0 -verticalPan 0 -zoom 1; objectMoveCommand; cameraMakeNode 1 ""
cameraMain = cmds.camera()
cameraShape = cameraMain[1]
cmds.move(0, 0, 10, cameraShape, absolute=True)

nearLocator=cmds.spaceLocator(n="nearLocator")
nearLocatorShape=nearLocator[0]
cmds.move(0,0,5,nearLocatorShape)

farLocator=cmds.spaceLocator(n="farLocator")
farLocatorShape=farLocator[0]
cmds.move(0,0,-5,farLocatorShape)

nearDistance = cmds.shadingNode('distanceBetween',
                                  n='nearDistance',
                                  asUtility=True)
cmds.connectAttr(nearLocatorShape + '.translate', nearDistance + '.point1',
                 force=True)
cmds.connectAttr(cameraMain[0] + '.translate', nearDistance + '.point2',
                 force=True)

farDistance = cmds.shadingNode('distanceBetween',
                                  n='farDistance',
                                  asUtility=True)
cmds.connectAttr(farLocatorShape + '.translate', farDistance + '.point1',
                 force=True)
cmds.connectAttr(cameraMain[0] + '.translate', farDistance + '.point2',
                 force=True)                

# Create each imageCard with shaders for each render pass
for x in range(0, len(data['layers'])):
    name = data['layers'][x]['name']
    width = data['layers'][x]['bounds']['right'] - data['layers'][x]['bounds']['left']
    height = data['layers'][x]['bounds']['bottom'] - data['layers'][x]['bounds']['top']
    moveX = data['layers'][x]['bounds']['left'] + (width * 0.5)
    moveY = data['bounds']['bottom'] - data['layers'][x]['bounds']['bottom'] + (height * 0.5)

    # Create Card
    card = ImageCard(name + '.png', x, w=width, h=height)
    # Move card into position
    card.moveRelative(moveX, moveY, 0)
    # Set Image Object
    im = Image.open(imageFolder + name + '.png')
    # Set up the beauty pass shader and add to render layer
    # TODO: add layer number to each shader class and refactor str() logic
    xPassShader = XPassShader(name + '.png', imageFolder, x)
    cmds.editRenderLayerGlobals(currentRenderLayer='defaultRenderLayer')
    card.setSG(xPassShader.getSG())
    # Set up the zDepth pass shader and add to render layer
    # TODO: create some measurement locators to pass into ZDepthShader() that retain the linking so we can set them later before render
    zDepthShader = ZDepthShader(name + '.png', imageFolder, x, nearDistance, farDistance)
    cmds.editRenderLayerMembers(zDepthRenderLayer,
                                card.getPolyNode(),
                                noRecurse=True)
    cmds.editRenderLayerGlobals(currentRenderLayer=zDepthRenderLayer)
    card.setSG(zDepthShader.getSG())
    # Set up the ambient occlusion pass shader and add to render layer
    aoShader = AOShader(name + '.png', imageFolder, x)
    cmds.editRenderLayerMembers(AORenderLayer,
                                card.getPolyNode(),
                                noRecurse=True)
    cmds.editRenderLayerGlobals(currentRenderLayer=AORenderLayer)
    card.setSG(aoShader.getSG())
    # Set up the position pass shader and add to render layer
    positionShader = PositionShader(name + '.png', imageFolder, x)
    cmds.editRenderLayerMembers(positionRenderLayer,
                                card.getPolyNode(),
                                noRecurse=True)
    cmds.editRenderLayerGlobals(currentRenderLayer=positionRenderLayer)
    card.setSG(positionShader.getSG())
    # Add to cardList
    cardList.append(card)

# Set the textured display mode.
currentPanel = cmds.getPanel(withLabel='Persp View')
if currentPanel != '':
    cmds.modelEditor(currentPanel, edit=True, da='smoothShaded',
                     displayTextures=True, dl='default',
                     rnm='vp2Renderer')
