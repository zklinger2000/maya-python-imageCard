__author__ = 'zklinger'
import maya.cmds as cmds


class positionShader(object):
    def __init__(self, imageName, dirName, layer):
        self._imageName = imageName
        self._dirName = dirName
        self._layerNum = str(layer)
        self._surfaceShader = cmds.shadingNode('surfaceShader',
                                               n='positionSurfaceShader_' +
                                               self._layerNum,
                                               asShader=True)
        self._layeredShader = cmds.shadingNode('layeredShader',
                                               n='positionLayeredShader_' +
                                                 self._layerNum,
                                               asShader=True)
#setAttr "zLayeredShader_001.compositingFlag" 1
        cmds.setAttr(self._layeredShader + '.compositingFlag', 1)
        self._shaderGroup = cmds.sets(empty=True, renderable=True,
                                      noSurfaceShader=True,
                                      name='positionShaderSG_' +
                                           self._layerNum)
        #cmds.connectAttr(self._layeredShader + '.message',
        #                 self._shaderGroup + ".miMaterialShader",
        #                 force=True)
        #cmds.connectAttr(self._layeredShader + '.message',
        #                 self._shaderGroup + ".miPhotonShader",
        #                 force=True)
        #cmds.connectAttr(self._layeredShader + '.message',
        #                 self._shaderGroup + ".miShadowShader",
        #                 force=True)
        self._imgFile = cmds.shadingNode('file', n='positionFile_' +
                                                   self._layerNum,
                                         asTexture=True)
        # creating the samplerInfo node
        self._sampler = cmds.shadingNode('samplerInfo',
                                         n='positionSamplerInfo' +
                                           self._layerNum,
                                         asUtility=True)
        self._place2D = cmds.shadingNode('place2dTexture', n='positionPlace2D',
                                         asUtility=True)

#setAttr "ramp1.colorEntryList[0].color" -type double3 1 1 1 ;
#setAttr "ramp1.colorEntryList[2].color" -type double3 0 0 0 ;
        cmds.connectAttr(self._sampler + '.pointWorldX', self._surfaceShader + '.outColorR',
                         force=True)
        cmds.connectAttr(self._sampler + '.pointWorldY', self._surfaceShader + '.outColorG',
                         force=True)
        cmds.connectAttr(self._sampler + '.pointWorldZ', self._surfaceShader + '.outColorB',
                         force=True)
        # connecting stuff I don't know about
        #cmds.connectAttr(self._layeredShader + '.message',
        #                 self._shaderGroup + ".miMaterialShader",
        #                 force=True)
        #cmds.connectAttr(self._layeredShader + '.message',
        #                 self._shaderGroup + ".miPhotonShader",
        #                 force=True)
        #cmds.connectAttr(self._layeredShader + '.message',
        #                 self._shaderGroup + ".miShadowShader",
        #                 force=True)



        # connecting the File node
        cmds.setAttr(self._imgFile + '.fileTextureName',
                     self._dirName + self._imageName,
                     type='string')
        cmds.setAttr(self._imgFile + '.filterType', 0)
        #cmds.connectAttr(self._imgFile + '.outAlpha',
        #                 self._shader + '.cutout_opacity',
        #                 force=True)
        # connecting the Placement node
        cmds.connectAttr(self._place2D + '.outUV', self._imgFile + '.uv')

# connecting reverse_001.output.outputX to layeredShader1.inputs.transparency.transparencyR. //
        cmds.connectAttr(self._imgFile + '.outTransparency',
                         self._layeredShader + '.inputs[0].transparency')

        #cmds.connectAttr(self._imgFile + '.outColor',
        #                 self._shader + '.diffuse',
        #                 force=True)

# connecting setRange2.outValue.outValueX to surfaceShader2.outColor.outColorG. //
#connectAttr -f setRange2.outValueX surfaceShader2.outColorG;
#        cmds.connectAttr(self._ramp + '.outValueX',
#                         self._surfaceShader + '.outColorG',
#                         force=True)
# connecting setRange2.outValue.outValueX to surfaceShader2.outColor.outColorB. //
#connectAttr -f setRange2.outValueX surfaceShader2.outColorB;
#        cmds.connectAttr(self._ramp + '.outValueX',
#                         self._surfaceShader + '.outColorB',
#                         force=True)
# connecting zSurfaceShader_001.outColor to zLayeredShader_001.inputs.color. //
#connectAttr -force zSurfaceShader_001.outColor zLayeredShader_001.inputs[0].color;


        cmds.connectAttr(self._surfaceShader + '.outColor',
                         self._layeredShader + '.inputs[0].color',
                         force=True)

# connecting zLayeredShader_002.outColor to zDepthShaderSG_002.surfaceShader. //
#connectAttr -f zLayeredShader_002.outColor zDepthShaderSG_002.surfaceShader;
        cmds.connectAttr(self._layeredShader + '.outColor',
                         self._shaderGroup + '.surfaceShader',
                         force=True)

    def getSG(self):
        return self._shaderGroup

    def getShader(self):
        return self._layeredShader

    def __repr__(self):
        return '[Shader: %s, %s, %s]' % (self._layerNum,
                                         self._layeredShader,
                                         self._shaderGroup)
