__author__ = 'zklinger'
import maya.cmds as cmds


class XPassShader(object):
    def __init__(self, imageName, dirName):
        self._imageName = imageName
        self._dirName = dirName
        self._layerNum = imageName[11:14]
        self._shader = cmds.shadingNode('mia_material_x_passes',
                                        n='x_passes_' +  self._layerNum,
                                        asShader=True)
        self._shaderGroup = cmds.sets(empty=True, renderable=True,
                                      noSurfaceShader=True,
                                      name=self._shader + "SG")
        #self._image = cmds.image(image=dirName + imageName)
        #print cmds.listAttr(self._image,s=True)
        self._imgFile = cmds.shadingNode('file', n='file_' + self._layerNum,
                                         asTexture=True)
        #print cmds.getAttr(self._imgFile + ".outSizeX")
        self._place2D = cmds.shadingNode('place2dTexture', asUtility=True)
        # creating a reverse node to use in Transparency
        self._reverse = cmds.shadingNode('reverse',
                                         n='reverse_' + self._layerNum,
                                         asUtility=True)

        # connecting everything
        cmds.connectAttr(self._shader + '.message',
                         self._shaderGroup + ".miMaterialShader",
                         force=True)
        cmds.connectAttr(self._shader + '.message',
                         self._shaderGroup + ".miPhotonShader",
                         force=True)
        cmds.connectAttr(self._shader + '.message',
                         self._shaderGroup + ".miShadowShader",
                         force=True)
        cmds.setAttr(self._imgFile + '.fileTextureName',
                     self._dirName + self._imageName,
                     type='string')
        cmds.setAttr(self._imgFile + '.filterType', 0)
        cmds.connectAttr(self._imgFile + '.outColor',
                         self._shader + '.diffuse',
                         force=True)
        cmds.connectAttr(self._imgFile + '.outAlpha',
                         self._shader + '.cutout_opacity',
                         force=True)
        cmds.connectAttr(self._imgFile + '.outAlpha', self._reverse + '.inputX')
        cmds.connectAttr(self._reverse + '.outputX', self._shader + '.transparency')
        cmds.connectAttr(self._place2D + '.outUV', self._imgFile + '.uv')

    def getSG(self):
        return self._shaderGroup

    def __repr__(self):
        return '[Shader: %s, %s, %s]' % (self._layerNum,
                                         self._shader,
                                         self._shaderGroup)

"""
if __name__ == '__main__':                      # When run for testing only
    # self-test code
    #dirName = r'C:\Users\zklinger\Google Drive\Docs\PROJECTS\SB\IMG\SB_010'
    imageName = 'sb010_card_001_001.tif'
    layerNum = imageName[11:14]
    shader = XPassShader(imageName)
    print shader
    #card01.createCard()

    # Set the textured display mode.
    currentPanel = cmds.getPanel(withLabel='Persp View')
    if currentPanel != '':
        cmds.modelEditor(currentPanel, edit=True, da='smoothShaded', displayTextures=True, dl='default',
                         rnm='vp2Renderer')
        cmds.modelEditor()
"""
