__author__ = 'zklinger'

import maya.cmds as cmds
import sys
sys.path.append(r'C:\Users\zklinger\Google Drive\Docs\PROJECTS\CODE\PYTHON\gravModTools')
import gravModTools as gMT
import image as image
from PIL import Image


# When you first import a file you must give it the full path
gMT.psource( r'C:\Users\zklinger\Google Drive\Docs\PROJECTS\CODE\PYTHON\gravModTools\gravModTools.py' )
imageFolder = 'C:\Users\zklinger\Google Drive\Docs\PROJECTS\SB\IMG\SB_011\\'
imageFileList = cmds.getFileList(folder=imageFolder, filespec='*.tif')
#print imageFileList[0][11:14]

cardList = list()



#createRenderLayer -name "layer1" -number 1 -noRecurse `ls -selection`;
zDepthRenderLayer = cmds.createRenderLayer(empty=True,
                                           name='zDepthRenderLayer',
                                           number=1, noRecurse=True)

for i in range(len(imageFileList)):
    im = Image.open(imageFolder + imageFileList[i])
    #print im.size[0], im.size[1]
    # imageName = imageFileList[i].split("_"))
    card = gMT.ImageCard.ImageCard(imageFileList[i], (im.size[0] / 100.0), (im.size[1] / 100.0))
    shader = gMT.XPassShader.XPassShader(imageFileList[i], imageFolder)
    cmds.editRenderLayerGlobals(currentRenderLayer='defaultRenderLayer')

    card.setSG(shader.getSG())

    card.move(0, 0, i * -2)

    zDepthShader = gMT.ZDepthShader.ZDepthShader(imageFileList[i],
                                                 imageFolder, 34, 55)
    #print zDepthShader
    cardList.append(card)
    print (cardList[i].getSG())
    #editRenderLayerMembers -noRecurse zDepthRenderLayer imageCard_000;
    cmds.editRenderLayerMembers(zDepthRenderLayer,
                                cardList[i].getPolyNode(),
                                noRecurse=True)
    cmds.editRenderLayerGlobals(currentRenderLayer=zDepthRenderLayer)
    card.setSG(zDepthShader.getSG())


#// camera1 //
#camera -centerOfInterest 5 -focalLength 35 -lensSqueezeRatio 1 -cameraScale 1
# -horizontalFilmAperture 1.41732 -horizontalFilmOffset 0
# -verticalFilmAperture 0.94488 -verticalFilmOffset 0 -filmFit Fill
# -overscan 1 -motionBlur 0 -shutterAngle 144 -nearClipPlane 0.1
# -farClipPlane 10000 -orthographic 0 -orthographicWidth 30
# -panZoomEnabled 0 -horizontalPan 0 -verticalPan 0 -zoom 1;
# objectMoveCommand; cameraMakeNode 1 "";


# Set the textured display mode.
currentPanel = cmds.getPanel(withLabel='Persp View')
if currentPanel != '':
    cmds.modelEditor(currentPanel, edit=True, da='smoothShaded',
                     displayTextures=True, dl='default',
                     rnm='vp2Renderer')
    cmds.modelEditor()



#########################
# AO Pass starts here
#########################

