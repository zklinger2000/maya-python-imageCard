__author__ = 'zklinger'

import maya.cmds as cmds
import sys
sys.path.append(r'C:\Users\zklinger\Documents\maya\scripts\maya-python-imageCard\scripts')
import gravModTools as gMT
from PIL import Image


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
