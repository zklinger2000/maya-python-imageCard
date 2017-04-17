__author__ = 'zklinger'
import maya.cmds as cmds


class ZDepthShader(object):
    def __init__(self, imageName, dirName, layerNum, nearDistance, farDistance):
        self._imageName = imageName
        self._dirName = dirName
        self._layerNum = layerNum
        self._shaderGroup = cmds.sets(empty=True, renderable=True,
                                      noSurfaceShader=True,
                                      name='zDepthShaderSG_' +
                                           str(self._layerNum))
        self._surfaceShader = cmds.shadingNode('surfaceShader',
                                               n='zSurfaceShader_' +
                                               str(self._layerNum),
                                               asShader=True)
        self._layeredShader = cmds.shadingNode('layeredShader',
                                               n='zLayeredShader_' +
                                                 str(self._layerNum),
                                               asShader=True)
        self._imgFile = cmds.shadingNode('file', n='zFile_' +
                                                   str(self._layerNum),
                                         asTexture=True)
        self._place2D = cmds.shadingNode('place2dTexture', n='zPlace2D',
                                         asUtility=True)
        self._reverse = cmds.shadingNode('reverse',
                                         n='zReverse_' + str(self._layerNum),
                                         asUtility=True)
        self._sampler = cmds.shadingNode('samplerInfo',
                                         n='zSamplerInfo' +
                                           str(self._layerNum),
                                         asUtility=True)
        self._distance = cmds.shadingNode('distanceBetween',
                                          n='zDistanceBetween' +
                                            str(self._layerNum),
                                          asUtility=True)
        self._range = cmds.shadingNode('setRange',
                                       n='zSetRange' + str(self._layerNum),
                                       asUtility=True)
        self._ramp = cmds.shadingNode('ramp',
                                      n='zRamp' + str(self._layerNum),
                                      asUtility=True)
        # Layered shader
        cmds.setAttr(self._layeredShader + '.compositingFlag', 1)
        cmds.connectAttr(self._layeredShader + '.outColor',
                         self._shaderGroup + '.surfaceShader',
                         force=True)
        # Surface shader
        cmds.connectAttr(self._surfaceShader + '.outColor',
                         self._layeredShader + '.inputs[0].color',
                         force=True)
        # Image File node
        cmds.setAttr(self._imgFile + '.fileTextureName',
                     self._dirName + self._imageName,
                     type='string')
        cmds.setAttr(self._imgFile + '.filterType', 0)
        # Placement node
        cmds.connectAttr(self._place2D + '.outUV', self._imgFile + '.uv')
        # Sampler node
        cmds.connectAttr(self._sampler + '.pointCamera', self._distance + '.point1',
                         force=True)
        # Distance node
        cmds.connectAttr(self._distance + '.distance', self._range + '.value.valueX')
        # Ramp node
        cmds.setAttr(self._ramp + '.colorEntryList[0].position', 0)
        cmds.setAttr(self._ramp + '.colorEntryList[0].color', 1, 1, 1)
        cmds.setAttr(self._ramp + '.colorEntryList[1].position', 1)
        cmds.setAttr(self._ramp + '.colorEntryList[1].color', 0, 0, 0)
        # Range node
        cmds.connectAttr(self._range + '.outValue.outValueX',
                         self._ramp + '.uvCoord.vCoord',
                         force=True)
        cmds.setAttr(self._range + '.maxX', 1)
        # Connect Min/Max values for Range to locators
        cmds.connectAttr(nearDistance + '.distance', self._range + '.oldMinX',
                         force=True)
        cmds.connectAttr(farDistance + '.distance', self._range + '.oldMaxX',
                         force=True)
        # connecting the Reverse node
        cmds.connectAttr(self._imgFile + '.outAlpha',
                         self._reverse + '.inputX')
        cmds.connectAttr(self._reverse + '.outputX',
                         self._layeredShader + '.inputs[0].transparencyR')
        cmds.connectAttr(self._reverse + '.outputX',
                         self._layeredShader + '.inputs[0].transparencyG')
        cmds.connectAttr(self._reverse + '.outputX',
                         self._layeredShader + '.inputs[0].transparencyB')
        # Ramp node
        cmds.connectAttr(self._ramp + '.outColor',
                         self._surfaceShader + '.outColor',
                         force=True)

    def getSG(self):
        return self._shaderGroup

    def getShader(self):
        return self._layeredShader

    def __repr__(self):
        return '[Shader: %s, %s, %s]' % (str(self._layerNum),
                                         self._layeredShader,
                                         self._shaderGroup)
