__author__ = 'zklinger'

import maya.cmds as cmds
import sys
sys.path.append('C:/Users/zklinger/Documents/maya/scripts/maya-python-imageCard/scripts')
import gravModTools as gMT
from PIL import Image
import json


#createRenderLayer -name "layer1" -number 1 -noRecurse `ls -selection`;
zDepthRenderLayer = cmds.createRenderLayer(empty=True,
                                           name='zDepthRenderLayer',
                                           number=1, noRecurse=True)

AORenderLayer = cmds.createRenderLayer(empty=True,
                                           name='AORenderLayer',
                                           number=2, noRecurse=True)

positionRenderLayer = cmds.createRenderLayer(empty=True,
                                           name='positionRenderLayer',
                                           number=3, noRecurse=True)

imageFolder = 'C:/Users/zklinger/Code/generator/plugins/generator-imageCard/test/'
imageFileList = cmds.getFileList(folder=imageFolder, filespec='*.png')

with open('C:/Users/zklinger/Code/generator/plugins/generator-imageCard/test/docInfo.json', 'r') as f:
    data = json.load(f)

numLayers = len(data['layers'])

cardList = []

for x in range(0, numLayers):
    name = data['layers'][x]['name']
    width = data['layers'][x]['bounds']['right'] - data['layers'][x]['bounds']['left']
    height = data['layers'][x]['bounds']['bottom'] - data['layers'][x]['bounds']['top']
    moveX = data['layers'][x]['bounds']['left'] + (width * 0.5)
    moveY = data['bounds']['bottom'] - data['layers'][x]['bounds']['bottom'] + (height * 0.5)
    imagePath = imageFolder + name + '.png'
    # Set Image Object
    im = Image.open(imagePath)

    zDepthShader = gMT.ZDepthShader.ZDepthShader(name + '.png',
                                                 imageFolder, x, 34, 55)

    AOShader = gMT.AOShader.AOShader(name + '.png', imageFolder, x)

    positionShader = gMT.positionShader.positionShader(name + '.png', imageFolder, x)

    # Create Card
    card = gMT.ImageCard.ImageCard(name + '.png', x, w=width, h=height)

    shader = gMT.XPassShader.XPassShader(name + '.png', imageFolder)
    cmds.editRenderLayerGlobals(currentRenderLayer='defaultRenderLayer')

    card.setSG(shader.getSG())
    card.move(moveX, moveY, 0)
    # Add to cardList
    cardList.append(card)

    print (cardList[x].getSG())
    print (cardList[x].getPolyNode())
    #editRenderLayerMembers -noRecurse zDepthRenderLayer imageCard_000;
    cmds.editRenderLayerMembers(zDepthRenderLayer,
                                cardList[x].getPolyNode(),
                                noRecurse=True)
    cmds.editRenderLayerGlobals(currentRenderLayer=zDepthRenderLayer)
    card.setSG(zDepthShader.getSG())

    #editRenderLayerMembers -noRecurse AORenderLayer imageCard_000;
    cmds.editRenderLayerMembers(AORenderLayer,
                                cardList[x].getPolyNode(),
                                noRecurse=True)
    cmds.editRenderLayerGlobals(currentRenderLayer=AORenderLayer)
    card.setSG(AOShader.getSG())

    #editRenderLayerMembers -noRecurse positionRenderLayer imageCard_000;
    cmds.editRenderLayerMembers(positionRenderLayer,
                                cardList[x].getPolyNode(),
                                noRecurse=True)
    cmds.editRenderLayerGlobals(currentRenderLayer=positionRenderLayer)
    card.setSG(positionShader.getSG())

# Set the textured display mode.
currentPanel = cmds.getPanel(withLabel='Persp View')
if currentPanel != '':
    cmds.modelEditor(currentPanel, edit=True, da='smoothShaded',
                     displayTextures=True, dl='default',
                     rnm='vp2Renderer')
    cmds.modelEditor()



'''
imageFolder = 'C:\Users\zklinger\Documents\maya\scripts\maya-python-imageCard\example\layers\\'
imageFileList = cmds.getFileList(folder=imageFolder, filespec='*.png')

cardList = list()

#createRenderLayer -name "layer1" -number 1 -noRecurse `ls -selection`;
zDepthRenderLayer = cmds.createRenderLayer(empty=True,
                                           name='zDepthRenderLayer',
                                           number=1, noRecurse=True)

#createRenderLayer -name "layer1" -number 1 -noRecurse `ls -selection`;
AORenderLayer = cmds.createRenderLayer(empty=True,
                                           name='AORenderLayer',
                                           number=2, noRecurse=True)

#createRenderLayer -name "layer1" -number 1 -noRecurse `ls -selection`;
positionRenderLayer = cmds.createRenderLayer(empty=True,
                                           name='positionRenderLayer',
                                           number=2, noRecurse=True)

for i in range(len(imageFileList)):
    im = Image.open(imageFolder + imageFileList[i])
    # imageName = imageFileList[i].split("_"))
    card = gMT.ImageCard.ImageCard(imageFileList[i], w=im.size[0], h=im.size[1])
    shader = gMT.XPassShader.XPassShader(imageFileList[i], imageFolder)
    cmds.editRenderLayerGlobals(currentRenderLayer='defaultRenderLayer')

    card.setSG(shader.getSG())

    card.move(0, 0, i * -2)

    zDepthShader = gMT.ZDepthShader.ZDepthShader(imageFileList[i],
                                                 imageFolder, 34, 55)

    AOShader = gMT.AOShader.AOShader(imageFileList[i], imageFolder)

    positionShader = gMT.positionShader.positionShader(imageFileList[i], imageFolder)

    #print zDepthShader
    cardList.append(card)
    print (cardList[i].getSG())
    #editRenderLayerMembers -noRecurse zDepthRenderLayer imageCard_000;
    cmds.editRenderLayerMembers(zDepthRenderLayer,
                                cardList[i].getPolyNode(),
                                noRecurse=True)
    cmds.editRenderLayerGlobals(currentRenderLayer=zDepthRenderLayer)
    card.setSG(zDepthShader.getSG())

    #editRenderLayerMembers -noRecurse AORenderLayer imageCard_000;
    cmds.editRenderLayerMembers(AORenderLayer,
                                cardList[i].getPolyNode(),
                                noRecurse=True)
    cmds.editRenderLayerGlobals(currentRenderLayer=AORenderLayer)
    card.setSG(AOShader.getSG())

    #editRenderLayerMembers -noRecurse positionRenderLayer imageCard_000;
    cmds.editRenderLayerMembers(positionRenderLayer,
                                cardList[i].getPolyNode(),
                                noRecurse=True)
    cmds.editRenderLayerGlobals(currentRenderLayer=positionRenderLayer)
    card.setSG(positionShader.getSG())


# Set the textured display mode.
currentPanel = cmds.getPanel(withLabel='Persp View')
if currentPanel != '':
    cmds.modelEditor(currentPanel, edit=True, da='smoothShaded',
                     displayTextures=True, dl='default',
                     rnm='vp2Renderer')
    cmds.modelEditor()
