__author__ = 'zklinger'
import maya.cmds as cmds


class ImageCard(object):
    def __init__(self, imageName, layer, w=19.2, h=10.8):
        self._imageName = imageName
        self._layerNum = str(layer)
        self._imageFile = cmds.image(image='self._imageName')
        self._width = w
        self._height = h
        # creating the polygon card
        self._card = cmds.polyPlane(n='imageCard_' + self.getLayerNum(),
                                    w=self._width, h=self._height,
                                    ax=[1, 0, 0], sx=1, sy=1)
        
        self._shaderGroup = cmds.sets(self._card[0], edit=True,
                                      forceElement='initialShadingGroup')
        # moving into place !? This should be done here?
        cmds.move(0, 0, 0, self._card, absolute=True)
        cmds.rotate(0, -90, 0, self._card, relative=True)

    def getLayerNum(self):
        return self._layerNum

    def setSG(self, shaderGroup):
        self._shaderGroup = cmds.sets(self._card[0], edit=True,
                                      forceElement=shaderGroup)

    def getSG(self):
        return self._shaderGroup

    def getPolyNode(self):
        return self._card[0]

    def move(self, x=0, y=0, z=0):
        cmds.move(x, y, z, self._card, relative=True)

    def __repr__(self):
        return '[ImageCard: %s, %s, %s, %s]' % (self._imageName,
                                                self._layerNum,
                                                self._width,
                                                self._height)
