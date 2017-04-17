__author__ = 'zklinger'

import maya.cmds as cmds


class XPassShader(object):
    def __init__(self, imageName, path, layerNum):
        self._imageName = imageName
        self._path = path
        self._layerNum = layerNum
        self._shader = cmds.shadingNode('mia_material_x_passes',
                                        n='x_passes_' +  str(self._layerNum),
                                        asShader=True)
        self._shaderGroup = cmds.sets(empty=True, renderable=True,
                                      noSurfaceShader=True,
                                      name=self._shader + "SG")
        self._imgFile = cmds.shadingNode('file', n='file_' + str(self._layerNum),
                                         asTexture=True)
        self._place2D = cmds.shadingNode('place2dTexture', asUtility=True)
        # creating a reverse node to use in Transparency
        self._reverse = cmds.shadingNode('reverse',
                                         n='reverse_' + str(self._layerNum),
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
                     self._path + self._imageName,
                     type='string')
        cmds.setAttr(self._imgFile + '.filterType', 0)
        cmds.connectAttr(self._imgFile + '.outColor',
                         self._shader + '.diffuse',
                         force=True)
        cmds.connectAttr(self._imgFile + '.outAlpha',
                         self._shader + '.cutout_opacity',
                         force=True)
        cmds.connectAttr(self._imgFile + '.outAlpha', self._reverse + '.inputX')
        cmds.connectAttr(self._place2D + '.outUV', self._imgFile + '.uv')
        cmds.connectAttr(self._reverse + '.outputX', self._shader + '.transparency')

    def getSG(self):
        return self._shaderGroup

    def __repr__(self):
        return '[Shader: %s, %s, %s]' % (str(self._layerNum),
                                         self._shader,
                                         self._shaderGroup)
